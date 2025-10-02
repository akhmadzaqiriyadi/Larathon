# Illuminate/Database/Connection.py
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from config.database import get_database_url

def get_engine(echo=False):
    db_url = get_database_url()
    engine = create_engine(db_url, echo=echo)

    if not database_exists(engine.url):
        print(f"⚡ Database not found. Creating: {engine.url.database}")
        create_database(engine.url)

    return engine
