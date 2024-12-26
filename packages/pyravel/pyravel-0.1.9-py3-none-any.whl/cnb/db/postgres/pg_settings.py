from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class PgSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str | int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DRIVER: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        extra="ignore",
    )

    def get_postgres_uri(self):
        return MultiHostUrl.build(
            scheme=self.POSTGRES_DRIVER,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )


pg_settings = PgSettings()
