import os

from dotenv import load_dotenv

load_dotenv()

ADMIN_EMAIL: str = os.environ["ADMIN_EMAIL"]
SECRET_KEY: str = os.environ["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
ALGORITHM = "HS256"
