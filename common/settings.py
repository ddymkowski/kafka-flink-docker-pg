from pydantic_settings import BaseSettings


class Settings(BaseSettings):   # type: ignore
    url: str
    topic: str
    dlq: str
    host_name: str
    host_port: int

    class Config:
        env_file = "../.env"
