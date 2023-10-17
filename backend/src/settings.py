import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Shali"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("SHALI_POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("SHALI_POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("SHALI_POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "SHALI_POSTGRES_PORTA", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("SHALI_POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()

if __name__ == "__main__":
    print(settings.DATABASE_URL)
