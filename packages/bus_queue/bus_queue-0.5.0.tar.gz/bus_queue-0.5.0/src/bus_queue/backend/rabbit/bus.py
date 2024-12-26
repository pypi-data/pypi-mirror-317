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
                    if method.delivery_tag <= self.max_retries:
                        logger.info(f"Retrying message ({method.delivery_tag}/{self.max_retries})")
                        self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    else:
                        logger.exception(ex)
                        logger.info(f"Max retries. max_retries: {self.max_retries})")
                        self.channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=topic, on_message_callback=on_message, auto_ack=False)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=False)

    def wait(self):
        if self.channel is None:
            self.connect()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()
