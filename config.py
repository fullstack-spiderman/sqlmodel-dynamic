from typing import Optional

from pydantic import BaseSettings, Field, BaseModel, PostgresDsn, parse_obj_as
from settings import read_attrs


class AppConfig(BaseModel):
    """Application configurations."""

    VAR_A: int = 33
    VAR_B: float = 22.0


class GlobalConfig(BaseSettings):
    """Global configurations."""

    APP_CONFIG: AppConfig = AppConfig()

    # define global variables with the Field class
    APP_ENV: Optional[str] = Field(None, env="environmentish")

    class Config:
        """Loads the dotenv file."""

        env_file = 'environment/.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


class DevConfig(GlobalConfig):
    """Development configurations."""
    # uri: PostgresDsn = "postgresql+asyncpg://postgres:postgres@devhost:5432/webdev"
    global_env = GlobalConfig()
    env = global_env.APP_ENV
    uri: PostgresDsn = parse_obj_as(
        PostgresDsn, read_attrs()) if env == 'dev' else None


class LocalDevConfig(GlobalConfig):
    """Development configurations."""
    uri: str = Field(..., env="PostgresDsn")

    class Config:
        """Loads the dotenv file."""

        env_file = 'environment/local.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


class ProdConfig(GlobalConfig):
    """Production configurations."""
    # uri: PostgresDsn = "postgresql+asyncpg://produser:prodpass@prodhost:5432/webprod"
    # uri: PostgresDsn = read_attrs()
    global_env = GlobalConfig()
    env = global_env.APP_ENV
    uri: PostgresDsn = parse_obj_as(
        PostgresDsn, read_attrs()) if env == 'prod' else None


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, app_env: Optional[str]):
        self.app_env = app_env

    def __call__(self):
        if self.app_env == "dev":
            return DevConfig()

        elif self.app_env == "prod":
            return ProdConfig()
        elif self.app_env == 'local':
            return LocalDevConfig()


# print(GlobalConfig().APP_ENV)

cnf = FactoryConfig(GlobalConfig().APP_ENV)()
print(cnf.__repr__())
