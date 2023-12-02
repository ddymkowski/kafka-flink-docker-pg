import json
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel

from src.common.enums import Errors


class BinanceTicker(BaseModel):
    symbol: str
    priceChange: str
    priceChangePercent: str
    weightedAvgPrice: str
    prevClosePrice: str
    lastPrice: str
    lastQty: str
    bidPrice: str
    bidQty: str
    askPrice: str
    askQty: str
    openPrice: str
    highPrice: str
    lowPrice: str
    volume: str
    quoteVolume: str
    openTime: int
    closeTime: int
    firstId: int
    lastId: int
    count: int
    ingestionTimestamp: int


@dataclass(frozen=True)
class BinanceKafkaData:
    __slots__ = "data", "error", "traceback", "details"
    data: Optional[BinanceTicker]
    error: Optional[Errors]
    traceback: Optional[str]
    details: Optional[Any]

    @property
    def valid(self) -> bool:
        return self.error is None

    @property
    def json(self) -> bytes:
        json_data = {slot: getattr(self, slot) for slot in self.__slots__}
        if self.valid:
            json_data["data"] = json_data["data"].model_dump()

        return json.dumps(json_data).encode("utf-8")
