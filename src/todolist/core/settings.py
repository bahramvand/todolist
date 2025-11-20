import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseSettings:
    host: str = os.getenv("DB_HOST", "localhost")
    port: str = os.getenv("DB_PORT", "5432")
    user: str = os.getenv("DB_USER", "todolist")
    password: str = os.getenv("DB_PASSWORD", "todolist")
    name: str = os.getenv("DB_NAME", "todolist")

    @property
    def url(self) -> str:
        # SQLAlchemy URL for PostgreSQL
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


db_settings = DatabaseSettings()
