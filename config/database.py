import os
from sqlalchemy import create_engine

def get_engine():
    conn = os.getenv("DB_CONNECTION", "sqlite")

    if conn == "sqlite":
        db = os.getenv("DB_DATABASE", "database.sqlite")
        return create_engine(f"sqlite:///{db}")

    elif conn == "mysql":
        user = os.getenv("DB_USERNAME", "root")
        pwd = os.getenv("DB_PASSWORD", "")
        host = os.getenv("DB_HOST", "127.0.0.1")
        port = os.getenv("DB_PORT", "3306")
        db = os.getenv("DB_DATABASE", "test")
        return create_engine(f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}")

    else:
        raise Exception(f"Unsupported DB_CONNECTION: {conn}")
