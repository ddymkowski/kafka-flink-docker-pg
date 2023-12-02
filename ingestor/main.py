import argparse

from src.common.settings import Settings
from src.downloader import BinanceDataDownloader
from src.orchestrator import BinanceIngestionOrchestrator
from src.publisher import KafkaPublisher

settings = Settings()

URL = settings.url
HOST_NAME = settings.host_name
HOST_PORT = settings.host_port
TOPIC = settings.topic
DLQ = settings.dlq


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--scrape-interval-seconds', type=int)
    args = parser.parse_args()
    scrape_interval_seconds = args.scrape_interval_seconds

    ingestor = BinanceDataDownloader(URL)
    pub = KafkaPublisher(HOST_NAME, HOST_PORT, TOPIC, DLQ)
    orchestrator = BinanceIngestionOrchestrator(ingestor, pub, scrape_interval_seconds)

    orchestrator.ingest()


if __name__ == "__main__":
    print('starting ingestion')
    main()
