import json
from abc import ABC, abstractmethod
from typing import Callable, Any


class Backend(ABC):
    @abstractmethod
    def publish(self, topic: str, message: str) -> None:
        pass

    @abstractmethod
    def broadcast(self, topic: str, message: str) -> None:
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[str], None]) -> None:
        pass

    @abstractmethod
    def wait(self):
        pass


class EventBus:
    def __init__(self, backend: Backend):
        self.backend = backend

    def publish(self, topic: str, message: Any) -> None:
        self.backend.publish(topic, json.dumps(message))

    def subscribe(self, topic: str, callback: Callable[[str, Any], None]) -> None:
        def json_callback(t: str, message: str):
            decoded_message = json.loads(message)
            callback(t, decoded_message)

        self.backend.subscribe(topic, json_callback)

    def broadcast(self, topic: str, message: Any) -> None:
        self.backend.broadcast(topic, json.dumps(message))

    def wait(self):
        self.backend.wait()
