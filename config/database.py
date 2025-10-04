# config/database.py
import os
from urllib.parse import quote_plus
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

        # Clean up host: remove @ prefix if present
        if host.startswith('@'):
            host = host[1:]

        # Encode password to handle special characters
        encoded_pwd = quote_plus(pwd) if pwd else ""

        return create_engine(f"mysql+pymysql://{user}:{encoded_pwd}@{host}:{port}/{db}")

    elif conn == "pgsql":
        user = os.getenv("DB_USERNAME")
        pwd = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_DATABASE")

        # Clean up host: remove @ prefix and any socket path suffixes
        if host.startswith('@'):
            host = host[1:]

        # Remove socket path if present (e.g., /.s.PGSQL.6543)
        if '/.s.PGSQL' in host:
            host = host.split('/.s.PGSQL')[0]

        # Build connection string with proper encoding for password
        encoded_pwd = quote_plus(pwd) if pwd else ""

        return create_engine(f"postgresql+psycopg2://{user}:{encoded_pwd}@{host}:{port}/{db}")

    else:
        raise Exception(f"Unsupported DB_CONNECTION: {conn}")
