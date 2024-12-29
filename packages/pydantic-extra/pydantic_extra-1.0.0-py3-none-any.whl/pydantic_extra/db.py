from __future__ import annotations

__all__ = ['DB', 'SQLite', 'Mysql', 'AnyDB', 'T_DB']

from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr
from sqlalchemy import create_engine, event, URL, Engine
from sqlalchemy.orm import Session
from typing_extensions import Literal, TypeAlias, Union


class DB(BaseModel, ABC):
    type: str

    @cached_property
    @abstractmethod
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""

    @cached_property
    def engine(self) -> Engine:
        """Создаёт sqlalchemy.Engine"""
        return create_engine(self.connect_str)

    def session(self) -> Session:
        """Создаёт sqlalchemy.Session"""
        return Session(self.engine)

    def setup(self):
        """Подготавливает sqlalchemy для работы с данным диалектом"""


class SQLite(DB):
    type: Literal["sqlite"]
    path: Path

    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return URL.create("sqlite", database=str(self.path.absolute()))

    def setup(self):
        """Подготавливает sqlalchemy для работы с sqlite"""

        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()


class Mysql(DB):
    type: Literal["mysql", "mariadb"]
    host: str
    port: int = 3306
    login: str
    password: SecretStr
    encoding: str = "utf8mb4"
    database: str

    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return URL.create(f"mysql+pymysql", self.login, self.password.get_secret_value(), self.host, self.port,
                          self.database,
                          {"charset": self.encoding})


class AnyDB(DB):
    type: Literal["any"]
    str_: str = Field(alias="str")

    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return self.str_


T_DB: TypeAlias = Union[SQLite, Mysql, AnyDB]
