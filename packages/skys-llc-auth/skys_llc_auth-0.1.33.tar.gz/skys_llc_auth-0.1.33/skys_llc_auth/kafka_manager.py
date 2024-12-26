import asyncio
import json
from collections.abc import AsyncGenerator
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, ConsumerRecord

from skys_llc_auth.utils import Singleton


class KafkaManager(Singleton):
    def __init__(
        self,
        *,
        bootstrap_servers: str,
        topics_consume: list[str],
    ):
        self.loop = asyncio.get_event_loop()
        self.topics = topics_consume
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=self.serializer,
            loop=self.loop,
        )
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=bootstrap_servers,
            loop=self.loop,
            value_deserializer=self.deserializer,
        )

    async def send_one(self, topic: str, payload: dict, **kw: Any):
        await self.producer.send(topic=topic, value=payload, **kw)

    def serializer(self, value: Any) -> bytes:
        return json.dumps(value).encode()

    def deserializer(self, serialized: bytes) -> Any:
        return json.loads(serialized)

    async def consume(self) -> AsyncGenerator[ConsumerRecord, None]:
        async for msg in self.consumer:
            yield msg
            if self.consumer._closed:
                return

    async def close(self):
        await self.consumer.stop()
        await self.producer.stop()
