import asyncio
import logging
import signal
import time
import traceback
import uuid
import os
import math
import redis

from croniter import croniter
from flask import Flask, current_app
from werkzeug.utils import import_string, find_modules
from redis import asyncio as aioredis
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import current_process, Pool
from typing import Callable, Dict, Union

from flask_redis_stream_pubsub import util

# -------------------- 常量与默认配置 --------------------
RESET = '\033[0m'

logger = logging.getLogger("pubsub")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logger.level)
formatter = logging.Formatter("[%(asctime)s] PUBSUB %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

# Scheduler 常量
SCHEDULER_PIPE_BUFFER_SIZE = 20
SCHEDULER_INTERVAL = 0.2
SCHEDULER_JOB_STREAM_MAX_LEN = 256
SCHEDULER_LOCK_EX = 5

# Consumer 常量
CONSUMER_RETRY_LOOP_INTERVAL = 5
CONSUMER_TASK_SPLIT_THRESHOLD = 16

# -------------------- 工具函数 --------------------
def _thread_execute(fc: Callable, msg: "Msg"):
    """
    线程执行函数，提交到 thread_pool 或直接调用。
    """
    if current_process().thread_pool is None:
        fc(msg)
    else:
        current_process().thread_pool.submit(fc, msg)


class Msg:
    """
    消费者从 Redis stream 拿到的消息结构
    """
    __slots__ = ['stream_name', 'id', 'group_name', 'payload', 'consumer_name', 'retry_count']

    def __init__(self, stream_name: str, msg_id: str, group_name: str, payload: Dict,
                 consumer_name: str, retry_count: int = 0):
        self.stream_name = stream_name
        self.id = msg_id
        self.group_name = group_name
        self.payload = payload
        self.consumer_name = consumer_name
        self.retry_count = retry_count

    def __str__(self):
        return (f"Msg({self.consumer_name}-{self.id}-"
                f"{self.stream_name}-{self.payload}-"
                f"{self.group_name}-{self.retry_count})")

    @property
    def source(self) -> str:
        return self.payload.get('__SOURCE', '')

    @property
    def publish_time(self) -> int:
        return int(self.payload.get('__PUBLISH_TIME', 0))


class Consumer:
    """
    核心消费者类，负责订阅/消费 Redis Stream 中的消息，支持多进程 + 多线程。
    """

    def __init__(
        self,
        consumer_name: str,
        group: str = '',
        processes: int = 1,
        threads: int = 1,
        retry_count: int = 64,
        timeout_second: int = 300,
        block_second: int = 5,
        read_count: int = 16,
        noack: bool = False,
        config_prefix: str = 'PUBSUB_REDIS',
        app_factory: Union[str, Callable] = None
    ):
        """
        :param consumer_name: 消费者名称
        :param group: Redis Stream Group 名称
        :param processes: 启动的进程数
        :param threads: 每个进程可用的线程数
        :param retry_count: 超过此次数后自动 ack
        :param timeout_second: 超时时间，单位秒
        :param block_second: xreadgroup 阻塞时间，单位秒
        :param read_count: 每次读取消息数量
        :param noack: 是否无需手动 ack
        :param config_prefix: 配置前缀
        :param app_factory: Flask app 工厂，或者其 import string
        """
        self.app_factory = app_factory
        self.group = group
        self.timeout_mill = timeout_second * 1000
        self.block_mill = block_second * 1000
        self.read_count = read_count
        self.retry_count = retry_count
        self.consumer_name = consumer_name
        self.noack = noack

        self.processes = processes
        self.threads = threads
        self.__running = True
        self.__call_map = {}  # 订阅函数映射
        self.config_prefix = config_prefix
        self.redis_url = ""

        self.rcli = None
        self.process_pool = None

    # -------------------- 配置相关 --------------------
    def init_obj(self, obj: Union[str, object]):
        """
        从一个对象或 import string 获取配置（类似 Flask config）。
        """
        if isinstance(obj, str):
            obj = import_string(obj)

        cfg = {
            key: getattr(obj, key)
            for key in dir(obj) if key.isupper()
        }
        self.redis_url = cfg.get(f"{self.config_prefix}_URL", "redis://localhost:6379/0")
        self.__init_config(cfg)

    def init_app(self, app: Flask):
        """
        从 Flask app 的 config 中读取配置。
        """
        self.redis_url = app.config.get(f"{self.config_prefix}_URL", "redis://localhost:6379/0")
        cfg = app.config.get(f'{self.config_prefix}_OPTION') or {}
        self.__init_config(cfg)

    def __init_config(self, cfg: Dict):
        """
        初始化消费者相关配置。
        """
        self.group = cfg.get('group', self.group)
        self.processes = cfg.get('processes', self.processes)
        self.threads = cfg.get('threads', self.threads)
        self.retry_count = cfg.get('retry_count', self.retry_count)
        self.timeout_mill = int(cfg.get('timeout_second', self.timeout_mill // 1000)) * 1000
        self.block_mill = int(cfg.get('block_second', self.block_mill // 1000)) * 1000
        self.read_count = cfg.get('read_count', self.read_count)
        self.noack = cfg.get('noack', self.noack)

        if 'app_factory' in cfg:
            self.app_factory = cfg['app_factory']

    # -------------------- 订阅相关 --------------------
    def import_module(self, module: str):
        """
        递归导入指定 module 下的所有 py 文件，以触发 @subscribe 装饰器。
        """
        for name in find_modules(module, recursive=True, include_packages=False):
            import_string(name)

    def subscribe(
        self, stream: str, timeout: float = None, retry_count: int = None, cron: str = None
    ):
        """
        装饰器，用于标注某个函数订阅指定 stream。
        :param stream: redis stream 的名称
        :param timeout: 覆盖全局的 timeout_second 配置
        :param retry_count: 覆盖全局的 retry_count
        :param cron: 如果传入 cron 表达式，则变为周期性调度
        """
        if retry_count is None:
            retry_count = self.retry_count

        if cron is not None and not croniter.is_valid(cron):
            raise RuntimeError(f'{stream} cron is invalid: {cron}')

        def decorator(func: Callable):
            if stream in self.__call_map:
                raise RuntimeError(f'{stream} already subscribed')

            module_obj = __import__(func.__module__, fromlist=[''])
            func_info = {
                'module': module_obj,
                'name': func.__name__,
                'timeout': timeout,
                'retry_count': retry_count,
            }

            if cron is None:
                # 普通流订阅
                func_info.update({'type': 'subscribe'})
            else:
                # cron 定时任务
                func_info.update({
                    'type': 'cron',
                    'cron': cron,
                    'iter': croniter(cron, second_at_beginning=True),
                    'stream': stream,
                })

            self.__call_map[stream] = func_info

            @wraps(func)
            def wrapper(*args, **kwargs):
                with current_process().app.app_context():
                    ack = False
                    try:
                        msg = args[0]  # 第一个参数是 Msg
                        func(*args, **kwargs)
                        ack = True
                    except Exception:
                        current_app.logger.error(f'\033[91m{traceback.format_exc()}{RESET}')
                        raise
                    finally:
                        if current_process().noack:
                            return
                        cli = current_process().rcli
                        # 消费过多次后，直接 ack，或者执行成功后 ack
                        if retry_count <= 0 or ack:
                            cli.xack(msg.stream_name, msg.group_name, msg.id)

            return wrapper

        return decorator

    # -------------------- 运行逻辑 --------------------
    def run(self, app_factory: Union[str, Callable] = None, **kwargs):
        """
        同步入口，优先尝试 uvloop。若没有则使用 asyncio.run。
        """
        try:
            from uvloop import run
            logger.info(f'PID({os.getpid()}) \033[1muvloop running...{RESET}')
        except ImportError:
            from asyncio import run
            logger.info(f'PID({os.getpid()}) \033[1meventloop running...{RESET}')
        run(self.run_async(app_factory, **kwargs))

    async def run_async(self, app_factory: Union[str, Callable] = None, **kwargs):
        """
        异步入口，创建进程池、初始化 Redis 连接并启动事件循环。
        """

        self.__apply_kwargs(kwargs)
        if app_factory is None:
            app_factory = self.app_factory

        # 创建进程池
        self.process_pool = Pool(
            processes=self.processes,
            initializer=self.__init_process,
            initargs=(app_factory, self.threads, self.noack)
        )
        self.rcli = aioredis.from_url(self.redis_url, decode_responses=True)

        # 初始化 call_map，尝试创建 xgroup
        call_map_simple, job_list = await self.__prepare_subscribe_map()

        # 检查是否存在订阅
        if not call_map_simple:
            raise RuntimeError('No valid subscribe found')

        # 根据 call_map 的大小拆分成多组，防止单个进程任务过多
        parts = math.ceil(len(call_map_simple) / CONSUMER_TASK_SPLIT_THRESHOLD)
        call_map_groups = util.split_dict(call_map_simple, parts)

        # 创建消费与重试的任务
        tasks = []
        for call_map_group in call_map_groups:
            tasks.append(self.__xread_loop(call_map_group))
            if not self.noack:
                tasks.append(self.__retry_loop(call_map_group))

        # 如果有 cron job，加入调度器任务
        if job_list:
            tasks.append(self.__scheduler_loop(job_list))

        logger.info(
            f"PID({os.getpid()}) \033[94m"
            f"Parameters: processes={self.processes}, threads={self.threads}, "
            f"consumer_name={self.consumer_name}, group_id={self.group}{RESET}"
        )
        logger.info(
            f"PID({os.getpid()}) \033[96m"
            f"Discovery of subscribers: {', '.join(call_map_simple.keys())}{RESET}"
        )

        # 注册信号，用于优雅退出
        def _shutdown_handler(signum, frame):
            self.__running = False
            logger.warning(
                f"PID({os.getpid()}) \033[93m"
                f"Received signum={signum}, shutting down...PID({os.getpid()}){RESET}"
            )

        signal.signal(signal.SIGINT, _shutdown_handler)
        signal.signal(signal.SIGTERM, _shutdown_handler)

        # 并发执行所有任务
        await asyncio.gather(*tasks)

        self.process_pool.terminate()
        self.process_pool.join()

        logger.info(
            f"PID({os.getpid()}) \033[92m"
            f"Consumer shutdown successfully, PID({os.getpid()}){RESET}"
        )

    def __apply_kwargs(self, kwargs: Dict):
        """
        将 run_async() 里传入的关键字参数应用到当前 consumer 实例上。
        """
        redis_url = kwargs.get('redis_url')
        group = kwargs.get('group')
        processes = kwargs.get("processes")
        threads = kwargs.get("threads")
        retry_count = kwargs.get("retry_count")
        timeout_second = kwargs.get("timeout_second")
        block_second = kwargs.get("block_second")
        read_count = kwargs.get("read_count")
        noack = kwargs.get("noack")
        config_prefix = kwargs.get("config_prefix")

        if redis_url:
            self.redis_url = redis_url
        if group:
            self.group = group
        if processes:
            self.processes = processes
        if threads:
            self.threads = threads
        if retry_count is not None:
            self.retry_count = retry_count
        if timeout_second is not None:
            self.timeout_mill = int(timeout_second) * 1000
        if block_second is not None:
            self.block_mill = int(block_second) * 1000
        if read_count is not None:
            self.read_count = read_count
        if config_prefix:
            self.config_prefix = config_prefix
        if noack is not None:
            self.noack = noack

    async def __prepare_subscribe_map(self):
        """
        对订阅信息（__call_map）进行预处理，包括 xgroup 创建和区分 cron 与普通订阅。
        """
        call_map_simple = {}
        job_list = []

        for stream_name, info in self.__call_map.items():
            # 准备核心调用函数
            fc = getattr(info['module'], info['name'])
            call_map_simple[stream_name] = {
                'fc': fc,
                'timeout': info.get('timeout'),
                'retry_count': info.get('retry_count')
            }
            # 创建 xgroup
            try:
                # 这里用 redis-py 的 response error

                await self.rcli.xgroup_create(
                    name=stream_name, groupname=self.group, id='0', mkstream=True
                )

            except redis.exceptions.ResponseError:
                pass

            # 如果是 cron
            if info['type'] == 'cron':
                job_list.append(info)

        return call_map_simple, job_list

    # -------------------- 消费与重试逻辑 --------------------
    async def __retry_loop(self, fix_call_map: Dict):
        """
        周期性地检查超时的 pending message 并进行重试。
        """
        while self.__running:
            async with self.rcli.pipeline() as pipe:
                stream_list = []
                for k, val in fix_call_map.items():
                    _timeout_mill = val['timeout'] * 1000 if val['timeout'] else self.timeout_mill
                    _retry_count = val['retry_count']
                    stream_list.append({
                        'name': k,
                        'retry_count': _retry_count,
                        'timeout_mill': _timeout_mill
                    })
                    await pipe.xpending_range(
                        k, self.group, "0", "+", count=self.read_count, idle=_timeout_mill
                    )

                res = await pipe.execute()

            call_count = 0
            # 针对每个 stream 分别处理
            for i, pendings in enumerate(res):
                stream_dict = stream_list[i]
                stream_name = stream_dict['name']
                retry_count_limit = stream_dict['retry_count']
                timeout_mill = stream_dict['timeout_mill']

                message_ids, message_del_ids, times_delivered_map = [], [], {}
                for pending_item in pendings:
                    if pending_item['times_delivered'] > retry_count_limit:
                        message_del_ids.append(pending_item['message_id'])
                    else:
                        mid = pending_item['message_id']
                        message_ids.append(mid)
                        times_delivered_map[mid] = pending_item['times_delivered']

                # 超过最大重试次数，直接 ack
                if message_del_ids:
                    await self.rcli.xack(stream_name, self.group, *message_del_ids)

                # 尝试 xclaim
                if message_ids and stream_name in fix_call_map:
                    fc = fix_call_map[stream_name]['fc']
                    xmsgs = await self.rcli.xclaim(
                        stream_name, self.group, self.consumer_name, timeout_mill, message_ids
                    )
                    for xmsg in xmsgs:
                        mid = xmsg[0]
                        payload = xmsg[1]
                        retry_count_now = times_delivered_map[mid]
                        _msg = Msg(stream_name, mid, self.group, payload,
                                   self.consumer_name, retry_count=retry_count_now)
                        self.process_pool.apply_async(_thread_execute, (fc, _msg,))
                        call_count += 1

            # 若这一轮没有处理到消息，则等待一会再继续
            if call_count == 0:
                await asyncio.sleep(CONSUMER_RETRY_LOOP_INTERVAL)
            else:
                await asyncio.sleep(0)

    async def __xread_loop(self, fix_call_map: Dict):
        """
        持续地通过 XREADGROUP 拉取消息并分发给进程池执行。
        """
        streams = {key: ">" for key in fix_call_map.keys()}
        while self.__running:
            rets = await self.rcli.xreadgroup(
                self.group,
                self.consumer_name,
                streams,
                count=self.read_count,
                block=self.block_mill,
                noack=self.noack
            )
            for ret in rets:
                stream_name = ret[0]
                if stream_name not in fix_call_map:
                    current_app.logger.error(f'{stream_name} not in call funcs')
                    continue

                for msg_id, payload in ret[1]:
                    _msg = Msg(stream_name, msg_id, self.group, payload, self.consumer_name)
                    fc = fix_call_map[stream_name]['fc']
                    self.process_pool.apply_async(_thread_execute, (fc, _msg,))

    # -------------------- 调度器 (cron) --------------------
    async def __scheduler_loop(self, jobs: list):
        """
        对 cron 类型的任务进行调度，将任务写入对应 stream。
        """
        cron_jobs = []
        start_time = time.time()

        for job in jobs:
            cron_jobs.append({
                'iter': job['iter'],
                'stream': job['stream'],
                'last_time': int(job['iter'].get_next(start_time=start_time))
            })

        while self.__running:
            current_time = time.time()
            zjobs = []
            for job in cron_jobs:
                _next_time = int(job['iter'].get_next(start_time=current_time))
                if job['last_time'] != _next_time:
                    zjobs.append({
                        'stream': job["stream"],
                        'next_time': _next_time
                    })
                    job['last_time'] = _next_time

            if zjobs:
                # 分批次写入 pipeline，防止 pipeline 太长
                chunked_jobs = util.chunk_array(zjobs, SCHEDULER_PIPE_BUFFER_SIZE)
                await asyncio.gather(*[self.__job_pipe_xadds(chunk) for chunk in chunked_jobs])

            await asyncio.sleep(SCHEDULER_INTERVAL)

    async def __job_pipe_xadds(self, jobs: list) -> int:
        """
        将 cron job 写入对应 stream，每次写入前先 set nx 做锁，防止重复。
        """
        async with self.rcli.pipeline() as pipe:
            for job in jobs:
                key = f'{job["stream"]}_{job["next_time"]}'
                uid = uuid.uuid4().hex.upper()
                await pipe.set(key, uid, ex=SCHEDULER_LOCK_EX, nx=True)

            set_res = await pipe.execute()

            xcount = 0
            # 对成功 set 的 key，再真正 xadd
            async with self.rcli.pipeline() as pipe2:
                for i, success in enumerate(set_res):
                    if success:
                        job = jobs[i]
                        payload = {
                            '__PUBLISH_TIME': int(time.time() * 1000),
                            '__SOURCE': 'cron'
                        }
                        await pipe2.xadd(job['stream'], payload, maxlen=SCHEDULER_JOB_STREAM_MAX_LEN)
                        xcount += 1
                if xcount > 0:
                    await pipe2.execute()

            return xcount

    # -------------------- 进程初始化 --------------------
    def __init_process(self, app_factory: Union[str, Callable], threads: int, noack: bool):
        """
        初始化子进程时会调用，用于设置独立的 Flask app、Redis 连接和线程池等。
        """
        # 初始化 Flask app
        if isinstance(app_factory, str):
            app = import_string(app_factory)
        elif callable(app_factory):
            app = app_factory()
        else:
            raise RuntimeError("Invalid Flask app_factory")

        if app is None:
            raise RuntimeError("Flask app not initialized")

        # 初始化 Redis client
        redis_url = app.config.get(f"{self.config_prefix}_URL", "redis://localhost:6379/0")
        rcli = redis.from_url(redis_url, decode_responses=True)

        current_process().rcli = rcli
        current_process().app = app
        current_process().noack = noack

        # 如果需要多线程
        thread_pool = None
        if threads > 1:
            thread_pool = ThreadPoolExecutor(
                max_workers=threads,
                thread_name_prefix='PUBSUB'
            )
            current_process().thread_pool = thread_pool

        def _shutdown(signum, frame):
            """
            进程收到终止信号时的清理逻辑，比如关闭线程池。
            """
            if thread_pool is not None:
                thread_pool.shutdown()

        signal.signal(signal.SIGTERM, _shutdown)


def runs(*consumers: Consumer, app_factory: Union[str, Callable] = None):
    """
    同时运行多个 consumer，分别以独立的进程来执行。
    """
    if not consumers:
        raise RuntimeError("No consumers provided")

    from multiprocessing import Process

    processes = []
    for c in consumers:
        p = Process(target=c.run, args=(app_factory,))
        processes.append(p)
        p.start()

    def _shutdown_all(signum, frame):
        for p in processes:
            p.terminate()

    signal.signal(signal.SIGINT, _shutdown_all)
    signal.signal(signal.SIGTERM, _shutdown_all)

    for p in processes:
        p.join()
