import os


DATABASE_URL: str = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./cs_platform.db",
)

SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)
ALLOWED_ORIGINS: list[str] = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")
