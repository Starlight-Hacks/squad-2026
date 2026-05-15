from functools import lru_cache

from pydantic.fields import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "SAABI API"
    debug: bool = False
    database_host: str
    database_port: int
    database_password: str
    database_user: str
    database_name: str

    db_pool_size: int = 60
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    redis_url: str = 'redis://redis:6379/0'

    squad_secret_key: str
    squad_base_url: str

    twilio_account_sid: str
    twilio_auth_token: str
    twilio_verify_service_sid: str
    twilio_from_number: str
    twilio_whatsapp_number: str
    twilio_join_code: str
    twilio_demo_mode: bool

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    model_config = SettingsConfigDict(env_file='.env')

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f'postgresql+psycopg://{self.database_user}:{self.database_password}'
            f'@{self.database_host}:{self.database_port}/{self.database_name}'
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()