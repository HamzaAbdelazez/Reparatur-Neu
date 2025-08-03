import logging
import logging.config
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


def configure_logging():
    """
    Set up logging configuration.
    Logs messages to the console with a specified format.
    """
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[ %(levelname)s ] %(asctime)s %(name)s %(message)s",
            }
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["default"]},
    })


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    DATABASE_URL: Optional[str] = None

    @model_validator(mode='after')
    def compute_database_url(self):
        """
        Combine Postgres settings into a single database URL.
        Raises an error if any required settings are missing.
        """
        if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_PORT, self.POSTGRES_DB]):
            object.__setattr__(
                self,
                'DATABASE_URL',
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}",
            )
        else:
            raise ValueError("Incomplete database configuration.")
        return self

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Loading settings from environment variables or .env
settings = Settings()
