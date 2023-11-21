import time
from typing import Any, Generator

import pydantic
from requests import Session
from common.enums import Errors
from ingestor.src.schemas.binance import BinanceKafkaData, BinanceTicker


class BinanceDataDownloader:
    def __init__(self, url: str) -> None:
        self._url = url

    def _request_data(
            self, session: Session
    ) -> tuple[bool, list[dict[str, Any]]]:
        response = session.get(self._url)
        if response.status_code == 200:
            return True, response.json()

        return False, [response.__dict__]

    def get_batch(
            self, session: Session
    ) -> Generator[BinanceKafkaData, None, None]:
        success, api_response_data = self._request_data(session)
        if success:
            for datapoint in api_response_data:
                timestamp = time.time_ns()
                try:
                    yield BinanceKafkaData(
                        data=BinanceTicker(**datapoint, ingestionTimestamp=timestamp),
                        error=None,
                        traceback=None,
                        details=None,
                    )
                except pydantic.ValidationError as err:
                    yield BinanceKafkaData(
                        data=None,
                        error=Errors.DATA_VALIDATION,
                        traceback=str(err),
                        details=str(datapoint),
                    )
        else:
            yield BinanceKafkaData(
                data=None,
                error=Errors.SOURCE_SYSTEM_REQUEST,
                traceback=None,
                details=str(api_response_data[0]),
            )
