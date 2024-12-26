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
