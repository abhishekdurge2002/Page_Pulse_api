from pydantic_settings import BaseSettings  


class Settings:
    REQUEST_TIMEOUT = 10
    CACHE_TTL = 300
    RATE_LIMIT = "10/minute"


settings = Settings()