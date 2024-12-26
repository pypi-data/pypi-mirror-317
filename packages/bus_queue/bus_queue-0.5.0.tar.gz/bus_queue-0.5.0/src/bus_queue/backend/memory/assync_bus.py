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
