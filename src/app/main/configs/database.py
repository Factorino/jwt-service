from app.main.configs.base import config


@config
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    db_name: str = "app_db"
    driver: str = "postgresql+asyncpg"

    @property
    def dsn(self) -> str:
        return (
            f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        )
