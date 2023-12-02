import time

import requests

from src.downloader import BinanceDataDownloader
from src.publisher import KafkaPublisher
from src.schemas.binance import BinanceKafkaData


class BinanceIngestionOrchestrator:
    def __init__(
        self,
        ingestor: BinanceDataDownloader,
        publisher: KafkaPublisher,
        wait_between_requests: int,
    ) -> None:
        self._ingestor = ingestor
        self._publisher = publisher
        self._wait_between_requests = wait_between_requests

    def _publish_datapoint(self, datapoint: BinanceKafkaData) -> None:
        if datapoint.error is None:
            self._publisher.publish_to_topic(value=datapoint.json)
        else:
            self._publisher.publish_to_dlq(value=datapoint.json)

    def ingest(self) -> None:
        with requests.Session() as session:
            while True:
                for datapoint in self._ingestor.get_batch(session):
                    self._publish_datapoint(datapoint)
                print("sleeping")
                time.sleep(self._wait_between_requests)
