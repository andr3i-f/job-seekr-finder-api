# File with environment variables and general configuration logic.
# Env variables are combined in nested groups like "Security", "Database" etc.
# So environment variable (case-insensitive) for jwt_secret_key will be "security__jwt_secret_key"
#
# Pydantic priority ordering:
#
# 1. (Most important, will overwrite everything) - environment variables
# 2. `.env` file in root folder of project
# 3. Default values
#
# "sqlalchemy_database_uri" is computed field that will create valid database URL
#
# See https://pydantic-docs.helpmanual.io/usage/settings/
# Note, complex types like lists are read as json-encoded strings.


import logging
import logging.config
from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, AnyUrl, BaseModel, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url
from sqlalchemy.engine.url import URL

PROJECT_DIR = Path(__file__).parent.parent.parent


class Security(BaseModel):
    jwt_access_token_expire_secs: int = 24 * 3600  # 1d
    refresh_token_expire_secs: int = 28 * 24 * 3600  # 28d
    password_bcrypt_rounds: int = 12
    allowed_hosts: list[str] = [
        "localhost",
        "127.0.0.1",
        "*.herokuapp.com",
        "jobseekr.dev",
    ]
    backend_cors_origins: list[AnyHttpUrl] = []
    jwt_iss: str = ""


class Database(BaseModel):
    hostname: str = "postgres"
    username: str = "postgres"
    password: SecretStr = SecretStr("passwd-change-me")
    port: int = 5432
    db: str = "postgres"


class Adzuna(BaseModel):
    application_id: str = "adzuna"
    application_key: str = "adzuna"


class General(BaseModel):
    env: str = ""


class Settings(BaseSettings):
    security: Security = Field(default_factory=Security)
    database: Database = Field(default_factory=Database)
    adzuna: Adzuna = Field(default_factory=Adzuna)
    general: General = Field(default_factory=General)
    log_level: str = "INFO"

    database_url: AnyUrl | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> URL:
        if self.database_url:
            return make_url(str(self.database_url)).set(drivername="postgresql+asyncpg")

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.database.username,
            password=self.database.password.get_secret_value(),
            host=self.database.hostname,
            port=self.database.port,
            database=self.database.db,
        )

    @computed_field
    @property
    def scheduler_database_uri(self) -> str:
        # APScheduler needs a synchronous driver (psycopg2)
        if self.database_url:
            url = make_url(str(self.database_url)).set(drivername="postgresql")
            if self.general.env == "production":
                url = url.set(query={"sslmode": "require"})
            return url

        return URL.create(
            drivername="postgresql",
            username=self.database.username,
            password=self.database.password.get_secret_value(),
            host=self.database.hostname,
            port=self.database.port,
            database=self.database.db,
            query={"sslmode": "require"} if self.general.env == "production" else {},
        )

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def logging_config(log_level: str) -> None:
    conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{asctime} [{levelname}] {name}: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "": {
                "level": log_level,
                "handlers": ["stream"],
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(conf)


logging_config(log_level=get_settings().log_level)
logger = logging.getLogger("uvicorn.error")
