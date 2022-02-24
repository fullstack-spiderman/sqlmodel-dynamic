from functools import lru_cache
import os
from pprint import pprint
from typing import Optional

from pydantic import (
    BaseModel,
    BaseSettings,
    PostgresDsn,
    Field,
)

from scrape import main_reader, read_vault_sync


class AppSettings(BaseSettings):
    environment: str = Field(..., env="environmentish")

    class Config:
        env_file = 'environment/.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


# @lru_cache()
def get_app_settings():
    print('Getting AppSettings.....')
    return AppSettings()


# @lru_cache()
def read_attrs(env=None):
    if not env:
        app_settings = AppSettings()
        env = app_settings.environment
        db_settings = None
    # app_settings.environment = 'prod'
    # print({'env_read_attrs': env})
    res = main_reader(env)
    # res = read_vault_sync(env)
    # print({"res": res})
    if res:
        host = res.get('host')
        user = res.get('user')
        passwd = res.get('pass')
        port = res.get('port')
        env = res.get('env')
        db = res.get('db')
        result = (
            "postgresql+asyncpg://"
            f"{user}:{passwd}"
            f"@{host}:{port}/{db}"
        )
        # db_settings = DBSettings()
        # db_settings.pg_dsn = result
        return result
    else:
        return {'message': None}


class DBSettings(BaseSettings):
    # name: str
    # ip_address: str
    # user: str | None = None
    # password: str | None = None
    _pg_dsn: PostgresDsn = None
    app_settings = AppSettings()
    env = f'Env: {app_settings.environment}'
    attrss = read_attrs(app_settings.environment)
    # attrss = read_attrs(app_settings.environment)
    # _pg_dsn: PostgresDsn = os.getenv('PostgresDsn')

    # @property
    # def pg_dsn(self):
    #     if self._pg_dsn is None:
    #         if self.env == 'local':
    #             self._pg_dsn = Field(..., env="APP_ENV")
    #         self._pg_dsn = read_attrs()
    #     return self._pg_dsn

    def get_pg_dsn(self):
        # return dir(DBSettings())
        if self._pg_dsn is None:
            # if self.env == 'local':
            #     self._pg_dsn = Field(..., env="PostgresDsn")
            self._pg_dsn = read_attrs()
        return self._pg_dsn

    # @pg_dsn.setter
    # def pg_dsn(self, uri):
    #     self._pg_dsn = uri

    # domains: Set[str] = set()

    # more_settings: SubModel = SubModel()
    class Config:
        env_file = 'environment/dev.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


class ServerSettings(BaseSettings):
    api_key: str
    version: float
    # db_settings: Optional[DBSettings]


class Settings(BaseSettings):
    pass


def get_settings():
    print('Getting Settings.....')
    return Settings()


# @lru_cache()
def get_db_settings():
    print('Getting DBSettings.....')
    return DBSettings()


if __name__ == '__main__':
    app_settings = AppSettings()
    attrs = read_attrs()

    # db = get_db_settings()
    pprint(
        {
            "environment": app_settings.environment,
            "uri": attrs,
        }
    )
