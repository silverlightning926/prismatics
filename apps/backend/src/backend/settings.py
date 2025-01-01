from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HISTORIC_YEARS: list[int] = [
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
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
