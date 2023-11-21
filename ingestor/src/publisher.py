from functools import partial
from typing import Any

from kafka import KafkaProducer


class KafkaPublisher:
    _PRODUCER_TIMEOUT = 30

    def __init__(self, kafka_host: str, kafka_port: int, topic: str, dlq: str) -> None:
        self._producer = KafkaProducer(bootstrap_servers=f"{kafka_host}:{kafka_port}")
        self._topic = topic
        self._dlq = dlq

        self.publish_to_topic = partial(self._publish, topic=self._topic)
        self.publish_to_dlq = partial(self._publish, topic=self._dlq)

    def _publish(self, topic: str, **kwargs: dict[str, Any]) -> None:
        self._producer.send(topic=topic, **kwargs)
        self._producer.flush(self._PRODUCER_TIMEOUT)
