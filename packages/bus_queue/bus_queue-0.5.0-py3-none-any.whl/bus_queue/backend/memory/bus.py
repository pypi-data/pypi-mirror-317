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