import os

APP_NAME = os.getenv("APP_NAME", "LaravelFastAPI")
APP_ENV = os.getenv("APP_ENV", "local")
APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
APP_PORT = int(os.getenv("APP_PORT", "8000"))
