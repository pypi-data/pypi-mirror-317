# Flask Redis Stream PubSub

基于 Redis Stream 实现的一套简单易用的发布订阅 (Pub/Sub) 解决方案，支持 **多进程 + 多线程** 消费者模式，以及基于 **cron 语法** 的定时任务调度。项目主要面向 Flask 应用场景，提供了灵活的 **Producer（生产者）** 与 **Consumer（消费者）** API，让消息队列的使用更轻松。

## 特点

- **多进程 + 多线程**  
  通过 Python 的 `multiprocessing` 和 `ThreadPoolExecutor` 结合，使高并发处理消息更加简单。

- **基于 Redis Stream**  
  使用 Redis 最新的 Stream 数据结构，支持消息持久化、消费分组、重试/死信队列等高级特性。

- **定时任务 (Cron)**  
  内置对 `croniter` 的支持，可将定时任务与消息队列共存，统一管理调度。

- **自动重试**  
  通过 `xpending + xclaim` 的方式自动重试，超过指定次数后直接 `ack`，避免消息无限重发。

- **易于集成**  
  只需在 Flask 项目中简单初始化，即可开始使用；也支持无 Flask 环境的简易模式。

## 安装

Python 版本要求：**3.8+**

通过 pip 安装：

```bash
pip install flask-redis-stream-pubsub
```

或者从源码安装：
```bash
git clone https://github.com/eininst/flask-redis-stream-pubsub.git
cd flask-redis-stream-pubsub
python setup.py install
```

## Producer
### 1. 创建 Producer（生产者）

```python
from flask_redis_stream_pubsub import Producer

# 直接传入 redis_url
producer = Producer(redis_url='redis://localhost:6379/0')

# 生产一条消息
producer.publish('demo_stream', {'hello': 'world'})
```

在 Flask 环境下，可以使用 init_app 初始化：
```python
from flask import Flask
from flask_redis_stream_pubsub import Producer

app = Flask(__name__)
app.config['PUBSUB_REDIS_URL'] = 'redis://localhost:6379/0'

producer = Producer()
producer.init_app(app)
```

### 2.批量发布 (ProducerSession)
```python
producer = Producer(redis_url='redis://localhost:6379/0')
session = producer.session

# 分多次 add
session.add('stream1', {'hello': 'foo'})
session.add('stream2', {'hello': 'bar'})
session.add('stream1', {'hello': 'baz'})

# 最终一起提交
res_ids = session.commit()
print("Message IDs:", res_ids)
```
在 Flask App Context 下，`producer.session` 会自动缓存到 `app_ctx.producer_session`，在请求范围内复用同一个 `session`。


## Consumer

### 1. 创建 Consumer（消费者）并订阅
```python
from flask import Flask
from flask_redis_stream_pubsub import Consumer

# 定义一个消费者
consumer = Consumer(
    consumer_name='demo_consumer',
    group='demo_group',
    processes=2,
    threads=2
)

# 使用 subscribe 装饰器订阅某个 stream
@consumer.subscribe('demo_stream')
def handle_demo_stream(msg):
    print(f"Got message: {msg.payload}")
    # 正常处理逻辑 ...
    # 如果出现异常，会进行重试；若超过最大 retry 次数，会自动 ack

# 也可在消费者中初始化 app
app = Flask(__name__)
app.config['PUBSUB_REDIS_URL'] = 'redis://localhost:6379/0'
consumer.init_app(app)

if __name__ == "__main__":
    consumer.run()  # 进入事件循环
```

### 2. 多个 Consumers 同时运行
```python
from flask_redis_stream_pubsub import runs

consumer1 = Consumer(consumer_name='c1', group='g1')
consumer2 = Consumer(consumer_name='c2', group='g2')

@consumer1.subscribe('stream1')
def handle_stream1(msg):
    print(f"[C1] stream1 => {msg.payload}")

@consumer2.subscribe('stream2')
def handle_stream2(msg):
    print(f"[C2] stream2 => {msg.payload}")

if __name__ == "__main__":
    runs(consumer1, consumer2)  # 同时启动两个消费者进程
```

## 定时任务 (Cron)
`Consumer` 自带 `cron` 参数，用于定义定时任务：
```python
from flask_redis_stream_pubsub import Consumer

cron_consumer = Consumer(consumer_name='cron_consumer', group='cron_group')

@cron_consumer.subscribe('cron_stream', cron='*/1 * * * *')
def every_minute_job(msg):
    print("This job runs every minute")

if __name__ == "__main__":
    cron_consumer.run()
```

## 配置说明
在 Flask 中，默认的配置前缀为 `PUBSUB_REDIS`：
```python
app.config['PUBSUB_REDIS_URL'] = 'redis://localhost:6379/0'
# 其他可选参数：
app.config['PUBSUB_REDIS_OPTION'] = {
    'group': 'my_group',
    'processes': 4,
    'threads': 2,
    'retry_count': 5,
    'timeout_second': 300,
    'block_second': 6,
    'read_count': 16,
    'noack': False,
    # ...
}
```
* group: 消费者组名
* processes: 创建多少个进程
* threads: 每个进程中开启多少个工作线程
* retry_count: 超过此次数后自动 ack
* timeout_second: 超时阈值 (毫秒级)
* block_second: XREADGROUP 的阻塞时间 (毫秒级)
* read_count: 每次读取消息的数量
* noack: 是否自动 ack

## 常见问题
### 为什么我的消费者没收到消息？
* 检查 Consumer 的 `group` 和 `consumer_name` 是否已与 Redis 中的 Stream group 对应创建。
* 确保没有手动 `xdel` 或因 `maxlen` 导致旧消息被裁剪。
### 如何处理超时与重复消费？
* 使用 `xpending + xclaim` 自动重试。
* 若 `times_delivered` 超过 `retry_count`，会自动 ack。
### 如何控制 Consumer 日志？
* 可以设置 `pubsub` 的 logger，例如：
```python
logging.getLogger("pubsub").setLevel(logging.DEBUG)
```

## More Example
> See [example](/example)

## 开发与贡献
欢迎参与本项目开发和提交 Issue/PR：

* Issue: 遇到问题或有新需求，可在 Issues 反馈
* PR: 修复 Bug 或实现新特性后，可发起 Pull Request 贡献给社区

## License

*MIT*