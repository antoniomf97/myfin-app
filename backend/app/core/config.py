from typing import List


class Settings:
    PROJECT_NAME: str = "MyFin App"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Personal Finance Tracker API"
    API_PREFIX: str = "/api/v1"  # You can use this later for versioning

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:5174",  # Vite alternative port
    ]

    # Database
    DATABASE_URL: str = "sqlite:///./data/myfinapp.db"


settings = Settings()
