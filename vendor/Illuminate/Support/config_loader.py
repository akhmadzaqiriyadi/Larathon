import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

def load_config():
    return {
        "APP_NAME": os.getenv("APP_NAME", "FastAPI App"),
        "APP_ENV": os.getenv("APP_ENV", "local"),
        "APP_DEBUG": os.getenv("APP_DEBUG", "false").lower() == "true",
        "APP_PORT": os.getenv("APP_PORT", "8000"),

        "DB_CONNECTION": os.getenv("DB_CONNECTION", "sqlite"),
        "DB_HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "DB_PORT": os.getenv("DB_PORT", "3306"),
        "DB_DATABASE": os.getenv("DB_DATABASE", "database.sqlite"),
        "DB_USERNAME": os.getenv("DB_USERNAME", "root"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", ""),
    }
