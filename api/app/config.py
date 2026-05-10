from pydantic.fields import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str
    database_port: int
    database_password: str
    database_user: str
    database_name: str

    db_pool_size: int = 60
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    model_config = SettingsConfigDict(env_file='.env')

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f'postgresql+psycopg://{self.database_user}:{self.database_password}'
            f'@{self.database_host}:{self.database_port}/{self.database_name}'
        )


settings = Settings()  # pyright: ignore[reportCallIssue]
