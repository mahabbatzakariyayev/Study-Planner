import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./study_planner.db")
    backend_cors_origins: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        origins_raw = os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
        configured = [origin.strip() for origin in origins_raw.split(",") if origin.strip()]
        # Keep local dev resilient when Next.js picks another local port (e.g. 3001).
        defaults = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
        ]
        self.backend_cors_origins = list(dict.fromkeys([*configured, *defaults]))


settings = Settings()
