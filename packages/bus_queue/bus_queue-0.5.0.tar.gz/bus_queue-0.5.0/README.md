## Event Bus in Python with RabbitMQ: Exploring Synchronous and Asynchronous Solutions

Today we're going to build an event bus with Python. It's an event bus according to my personal needs. The idea is to create a scalable event bus, with RabbitMQ as the message broker but easy to replace with another message broker such as MQTT or Redis. In fact, I've started with a memomry-based message broker. I'm not going to use never this on-memory message broker, but it was a good start to understand the basics of the event bus.

That's the on memory version:

```python

from bus_queue.backend.memory.bus import MemoryEventBus as Bus
from bus_queue import EventBus

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

logger = logging.getLogger(__name__)


def callback(topic, msg):
    logger.info(f"Received: topic: {topic} msg: {msg}")


def main():
    backend = Bus()
    bus = EventBus(backend)

    bus.subscribe("test", callback)

    bus.publish("test", dict(hola="Gonzalo"))
    bus.wait()


if __name__ == "__main__":
    main()
```

This on-memory version uses this implementation:

```python
from time import sleep
from typing import Callable, Dict, List, Any

from bus_queue import Backend


class MemoryEventBus(Backend):
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[str, Any], None]]] = {}

    def publish(self, topic: str, message: str) -> None:
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(topic, message)

    def broadcast(self, topic: str, payload: Any):
        self.publish(topic, payload)

    def subscribe(self, topic: str, callback: Callable[[str, Any], None]) -> None:
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def wait(self):
        while True:
            sleep(1)
```

This implementation is a synchronous version. I also want to create an asynchronous version. 

```python
import asyncio
import logging

from bus_queue.backend.memory.assync_bus import AsyncMemoryEventBus as Bus
from bus_queue import AsyncEventBus

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

for l in ['asyncio', ]:
    logging.getLogger(l).setLevel(logging. WARNING)

logger = logging.getLogger(__name__)


async def callback(topic, msg):
    logger.info(f"Received: topic: {topic} msg: {msg}")


async def main():
    backend = Bus()
    bus = AsyncEventBus(backend)

    await bus.subscribe("test", callback)

    await bus.publish("test", dict(hola="Gonzalo"))
    await bus.wait()


if __name__ == "__main__":
    asyncio.run(main())

```

```python
import asyncio
from typing import Callable, Dict, List, Any, Awaitable

from bus_queue import AsyncBackend


class AsyncMemoryEventBus(AsyncBackend):
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[str, Any], Awaitable[None]]]] = {}

    async def publish(self, topic: str, message: str):
        if topic in self.subscribers:
            tasks = [
                asyncio.create_task(subscriber(topic, message))
                for subscriber in self.subscribers[topic]
            ]
            await asyncio.gather(*tasks)

    async def broadcast(self, topic: str, message: str):
        await self.publish(topic, message)

    async def subscribe(self, topic: str, handler: Callable[[str, Any], Awaitable[None]]):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def wait(self):
        await asyncio.Event().wait()
```

But this on-memory version is not useful for me. I want to use RabbitMQ as the message broker. I'm going to create also a synchronous and an asynchronous version also. In this version I´m going to create two kind of ways to publish messages. One way is a simple publish, and the other way is a broadcast. The broadcast is going to send the message to all the subscribers of the topic, and the publishing is going to send the message to only one subscriber, using a round-robin strategy.

The synchronous version:
The listener:

```python
import logging

from bus_queue import EventBus
from bus_queue.backend.rabbit.bus import RabbitEventBus as Bus

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

for l in ['pika', ]:
    logging.getLogger(l).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def callback(topic, msg):
    logger.info(f"Received: topic: {topic} msg: {msg}")


def main():
    backend = Bus("amqp://guest:guest@localhost:5672/")
    bus = EventBus(backend)

    bus.subscribe("test", callback)
    bus.wait()


if __name__ == "__main__":
    main()
```

And the publisher:

```python
import logging

from bus_queue.backend.rabbit.bus import RabbitEventBus as Bus
from bus_queue import EventBus

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

for l in ['pika',]:
    logging.getLogger(l).setLevel(logging. WARNING)

logger = logging.getLogger(__name__)


def main():
    backend = Bus("amqp://guest:guest@localhost:5672/")
    bus = EventBus(backend)

    bus.publish("test", dict(hola="Gonzalo"))
    bus.broadcast("test", "Hola, broadcast")


if __name__ == "__main__":
    main()
```

The implementation is like that:

```python
import logging
from typing import Callable, Dict, Any, List

import pika

from bus_queue import Backend

logger = logging.getLogger(__name__)


def get_broadcast_exchange_from_topic(topic: str):
    return f"broadcast_{topic}"


class RabbitEventBus(Backend):
    def __init__(self, rabbitmq_url: str, max_retries: int = 3):
        self.rabbitmq_url = rabbitmq_url
        self.subscribers: Dict[str, List[Callable[[str, Any], None]]] = {}
        self.connection = None
        self.channel = None
        self.max_retries = max_retries

    def connect(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        self.channel = self.connection.channel()

    def broadcast(self, topic: str, payload: Any):
        if self.channel is None:
            self.connect()
        exchange = get_broadcast_exchange_from_topic(topic)
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.channel.basic_publish(exchange=exchange, routing_key='', body=payload.encode())

    def publish(self, topic: str, payload: Any):
        if self.channel is None:
            self.connect()
        self.channel.basic_publish(exchange='', routing_key=topic, body=payload.encode())

    def subscribe(self, topic: str, handler: Callable[[str, Any], None]):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

        if self.channel is None:
            self.connect()

        self.channel.queue_declare(queue=topic, auto_delete=True)
        exchange = get_broadcast_exchange_from_topic(topic)
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=exchange, queue=queue_name)

        def on_message(ch, method, properties, body):
            for subscriber in self.subscribers[topic]:
                try:
                    subscriber(topic, body.decode())
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as ex:
                    logger.exception(ex)
                    if method.delivery_tag <= self.max_retries:
                        logger.info(f"Retrying message ({method.delivery_tag}/{self.max_retries})")
                        self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    else:
                        logger.info(f"Max retries. max_retries: {self.max_retries})")
                        self.channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=topic, on_message_callback=on_message, auto_ack=False)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=False)

    def wait(self):
        if self.channel is None:
            self.connect()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()
```

And the asynchronous version:

The listener:

```python
import asyncio
import logging

from bus_queue import AsyncEventBus
from bus_queue.backend.rabbit.assync_bus import AsyncRabbitEventBus as Bus

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

for l in ['asyncio', 'aio-pika']:
    logging.getLogger(l).setLevel(logging. WARNING)

logger = logging.getLogger(__name__)


async def callback(topic, msg):
    logger.info(f"Received: topic: {topic} msg: {msg}")


async def main():
    backend = Bus("amqp://guest:guest@localhost:5672/")
    bus = AsyncEventBus(backend)

    await bus.subscribe("test", callback)
    await bus.wait()


if __name__ == "__main__":
    asyncio.run(main())
```

The implementation is like that:

```python
import asyncio
import logging
from typing import Callable, Dict, List, Any, Awaitable

import aio_pika

from bus_queue import AsyncBackend

logger = logging.getLogger(__name__)


def get_broadcast_exchange_from_topic(topic: str):
    return f"broadcast_{topic}"


class AsyncRabbitEventBus(AsyncBackend):
    def __init__(self, rabbitmq_url: str, max_retries: int = 3):
        self.subscribers: Dict[str, List[Callable[[str, Any], Awaitable[None]]]] = {}
        self.rabbitmq_url = rabbitmq_url
        self.max_retries = max_retries

    async def broadcast(self, topic: str, payload: Any):
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        exchange_type = aio_pika.ExchangeType.FANOUT
        exchange = get_broadcast_exchange_from_topic(topic)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(exchange, exchange_type)
            await exchange.publish(
                aio_pika.Message(body=payload.encode()),
                routing_key=topic
            )

    async def publish(self, topic: str, payload: Any):
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=payload.encode()),
                routing_key=topic
            )

    async def subscribe(self, topic: str, handler: Callable[[str, Any], Awaitable[None]]):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
        exchange = get_broadcast_exchange_from_topic(topic)

        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        async with connection:
            channel = await connection.channel()

            direct_queue = await channel.declare_queue(topic, auto_delete=True)
            broadcast_exchange = await channel.declare_exchange(exchange, aio_pika.ExchangeType.FANOUT)
            broadcast_queue = await channel.declare_queue('', exclusive=True)
            await broadcast_queue.bind(broadcast_exchange)

            async def process_queue(queue_iter):
                async for message in queue_iter:
                    try:
                        await handler(topic, message.body.decode())
                        await message.ack()
                    except Exception as ex:
                        if message.delivery_tag <= self.max_retries:
                            logger.info(f"Retrying message ({message.delivery_tag}/{self.max_retries})")
                            await message.nack(requeue=True)
                        else:
                            logger.exception(ex)
                            logger.info(
                                f"Max retries. Discarding event (max_retries: {self.max_retries})")
                            await message.ack()

            async with direct_queue.iterator() as direct_queue_iter, broadcast_queue.iterator() as broadcast_queue_iter:
                await asyncio.gather(
                    process_queue(direct_queue_iter),
                    process_queue(broadcast_queue_iter)
                )

    async def wait(self):
        await asyncio.Event().wait()
```

And that's all. The library can be installed with poetry in both versions: async and sync. You can use pip or poetry to install the library. 
```bash

For the sync version:
```bash
poetry add bus_queue --extras "sync"
pip install bus_queue[sync]
```
and for the async version:
```bash
poetry add bus_queue --extras "async"
pip install bus_queue[async]
```

