import time
import redis
from typing import Dict, Any, Optional, List

from flask import Flask, has_app_context
from flask.globals import app_ctx

from flask_redis_stream_pubsub import util

DEFAULT_STREAM_MAX_LEN = 1024
PRODUCER_SESSION_BUFFER_SIZE = 32


class Producer:
    """
    生产者类，用于向 Redis Stream 发布消息，支持单条直接发布或批量发布（session）。
    """
    __slots__ = ('maxlen', 'approximate', '_rcli')

    def __init__(self, redis_url: str = '', maxlen: int = DEFAULT_STREAM_MAX_LEN, approximate: bool = True) -> None:
        """
        :param redis_url: Redis 连接地址，如果不传则需在后续显式调用 init_redis 或 init_app
        :param maxlen: 默认 stream 最大长度
        """
        self.maxlen = maxlen
        self.approximate = approximate
        self._rcli = None

        if redis_url:
            self._rcli = redis.from_url(redis_url, decode_responses=True)

    def init_redis(self, redis_url: str = '') -> None:
        """
        初始化 Redis 客户端
        :param redis_url: Redis 连接地址
        """
        self._rcli = redis.from_url(redis_url, decode_responses=True)

    def init_app(self, app: Flask, config_prefix: str = 'PUBSUB_REDIS') -> None:
        """
        从 Flask app 的 config 中读取对应的 Redis URL 并初始化
        :param app: Flask 实例
        :param config_prefix: 配置前缀，如 PUBSUB_REDIS
        """
        redis_url = app.config.get(f"{config_prefix}_URL", "redis://localhost:6379/0")
        self._rcli = redis.from_url(redis_url, decode_responses=True)

    def publish(self, stream_name: str, payload: Dict[str, Any], maxlen: Optional[int] = None,
                approximate: Optional[bool] = None) -> str:
        """
        发布一条消息到指定 Redis Stream
        :param stream_name: Redis stream 名称
        :param payload: 消息内容，最终会注入 __PUBLISH_TIME 与 __SOURCE
        :param maxlen: 如果不传，则使用实例级别的 maxlen
        :return: 新发布的消息在 Redis 中的 ID
        """
        if not self._rcli:
            raise RuntimeError("Redis client not initialized")

        _maxlen = maxlen if maxlen is not None else self.maxlen
        _approximate = approximate if approximate is not None else self.approximate

        payload['__PUBLISH_TIME'] = int(time.time() * 1000)
        payload['__SOURCE'] = 'producer'
        return self._rcli.xadd(stream_name, payload, maxlen=_maxlen, approximate=_approximate)

    @property
    def session(self) -> "ProducerSession":
        """
        返回用于批量发布消息的 session 对象。
        如果在 Flask App Context 下，会将 session 存储到 app_ctx 对象中复用。
        """
        if has_app_context():
            if not hasattr(app_ctx, 'producer_session'):
                app_ctx.producer_session = ProducerSession(self._rcli,
                                                           maxlen=self.maxlen, approximate=self.approximate)
            return app_ctx.producer_session

        return ProducerSession(self._rcli, self.maxlen)


class ProducerSession:
    """
    Producer 的批量发布会话，支持一次提交多条消息，并分 chunk 执行。
    """
    __slots__ = ('_rcli', 'maxlen', 'approximate', 'msgs')

    def __init__(self, rcli: redis.Redis, maxlen: int = DEFAULT_STREAM_MAX_LEN, approximate: bool = True) -> None:
        """
        :param rcli: Redis 客户端
        :param maxlen: 默认为 1024，可在 add 或 publish 时动态覆盖
        """
        self._rcli = rcli
        self.maxlen = maxlen
        self.approximate = approximate
        self.msgs = []

    def add(self, stream_name: str, payload: Dict[str, Any], maxlen: Optional[int] = None,
            approximate: Optional[bool] = None) -> None:
        """
        将一条消息加入缓冲，等待后续批量提交
        :param stream_name: Redis stream 名称
        :param payload: 消息内容
        :param maxlen: 可覆盖默认的最大长度
        """
        _maxlen = maxlen or self.maxlen
        _approximate = approximate if approximate is not None else self.approximate
        self.msgs.append({
            'name': stream_name,
            'payload': payload,
            'maxlen': _maxlen,
            'approximate': _approximate,
        })

    def clear(self) -> None:
        """ 清空当前缓冲区中的所有消息 """
        self.msgs.clear()

    def commit(self) -> List[str]:
        """
        提交（发布）当前缓冲中的所有消息，返回列表，包含每条消息的发布 ID。
        commit() 是 publish() 的别名。
        """
        return self.publish()

    def publish(self) -> List[str]:
        """
        将当前缓冲中的所有消息发布到各自的 stream，支持分批执行，
        以防止 pipeline 一次性操作数量过多。
        :return: 返回每条消息在 Redis 中的 ID 列表
        """
        if not self._rcli:
            raise RuntimeError("Redis client not initialized")

        # 拷贝后清空，保证 publish 多次调用时的数据安全
        msgs_to_publish = self.msgs[:]
        self.clear()

        # 分 chunk 处理，防止缓冲过大时 pipeline 时间过长
        chunked_msgs = util.chunk_array(msgs_to_publish, PRODUCER_SESSION_BUFFER_SIZE)
        result_ids = []

        for msg_group in chunked_msgs:
            with self._rcli.pipeline() as pipe:
                current_time = int(time.time() * 1000)
                for msg in msg_group:
                    payload = msg['payload']
                    payload['__PUBLISH_TIME'] = current_time
                    payload['__SOURCE'] = 'producer'
                    pipe.xadd(msg['name'], payload, maxlen=msg['maxlen'], approximate=msg['approximate'])

                pipe_res = pipe.execute()
                if isinstance(pipe_res, list):
                    result_ids.extend(pipe_res)

        return result_ids
