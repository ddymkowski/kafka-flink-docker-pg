import enum


class Errors(str, enum.Enum):
    DATA_VALIDATION = "DATA_VALIDATION"
    SOURCE_SYSTEM_REQUEST = "SOURCE_SYSTEM_REQUEST"
