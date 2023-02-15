from typing import Any, Dict, Optional

from dotenv import load_dotenv, dotenv_values
from pydantic import BaseSettings, PostgresDsn, validator
load_dotenv()


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: str
    PG_DATABASE: str
    PG_USER: str
    PG_PASSWORD: str
    SQLALCHEMY_DATABASE_URI: str

    PG_TEST_HOST: str
    PG_TEST_USER: str
    PG_TEST_PASSWORD: str
    PG_TEST_DB: str
    PG_TEST_PORT: str
    SQLALCHEMY_TEST_DATABASE_URI: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("PG_USER"),
            password=values.get("PG_PASSWORD"),
            host=values.get("PG_HOST"),
            path=f"/{values.get('PG_DATABASE') or ''}",
            port=values.get("PG_PORT"),
        )

    @validator("SQLALCHEMY_TEST_DATABASE_URI", pre=True)
    def assemble_test_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("PG_TEST_USER"),
            password=values.get("PG_TEST_PASSWORD"),
            host=values.get("PG_TEST_HOST"),
            path=f"/{values.get('PG_TEST_DB') or ''}",
            port=values.get("PG_TEST_PORT"),
        )


class Config:
    value_from_env = dotenv_values(".env")


settings = Settings()
