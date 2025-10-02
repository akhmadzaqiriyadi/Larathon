import os
from dotenv import load_dotenv

# tentukan root project (di mana artisan.py berada)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# load file .env sekali
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

class Env:
    @staticmethod
    def get(key: str, default=None):
        return os.getenv(key, default)

# alias mirip Laravel
env = Env.get
