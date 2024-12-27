from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HISTORIC_YEARS: list[int] = [
        2016,
        2017,
        2018,
        2019,
        2020,
        2022,
        2023,
        2024,
    ]

    request_throttle_secs: float = 5.0


settings = Settings()
