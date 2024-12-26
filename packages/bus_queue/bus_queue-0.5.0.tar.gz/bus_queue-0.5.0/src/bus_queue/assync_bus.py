import json
from abc import ABC, abstractmethod
from typing import Callable, Any, Awaitable


class AsyncBackend(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: str) -> None:
        pass

    @abstractmethod
    async def broadcast(self, topic: str, message: str) -> None:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable[[Any], Awaitable[None]]):
        pass

    @abstractmethod
    async def wait(self):
        pass


class AsyncEventBus:
    def __init__(self, backend: AsyncBackend):
        self.backend = backend

    async def publish(self, topic: str, message: Any) -> None:
        await self.backend.publish(topic, json.dumps(message))

    async def subscribe(self, topic: str, callback: Callable[[str, Any], Awaitable[None]]):
        async def json_callback(t: str, message: str):
            decoded_message = json.loads(message)
            await callback(t, decoded_message)

        await self.backend.subscribe(topic, json_callback)

    async def broadcast(self, topic: str, message: Any) -> None:
        await self.backend.broadcast(topic, json.dumps(message))

    async def wait(self):
        await self.backend.wait()
