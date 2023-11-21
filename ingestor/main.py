from common.settings import Settings
from ingestor.src.downloader import BinanceDataDownloader
from ingestor.src.orchestrator import BinanceIngestionOrchestrator
from ingestor.src.publisher import KafkaPublisher

settings = Settings()

URL = settings.url
HOST_NAME = settings.host_name
HOST_PORT = settings.host_port
TOPIC = settings.topic
DLQ = settings.dlq


def main() -> None:
    ingestor = BinanceDataDownloader(URL)
    pub = KafkaPublisher(HOST_NAME, HOST_PORT, TOPIC, DLQ)
    orchestrator = BinanceIngestionOrchestrator(ingestor, pub, 3)

    orchestrator.ingest()


if __name__ == "__main__":
    main()
