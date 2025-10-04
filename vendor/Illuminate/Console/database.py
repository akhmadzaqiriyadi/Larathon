# vendor/Illuminate/Console/database.py
import os
import re
import sys
import importlib.util
from urllib.parse import quote_plus
from vendor.Illuminate.Support.Env import Env
from sqlalchemy import create_engine, text

BASE_DIR = sys.path[0]

def get_engine():
    db_connection = Env.get("DB_CONNECTION", "mysql")
    db_name = Env.get("DB_DATABASE", "laravelfastapi")
    user = Env.get("DB_USERNAME", "root")
    password = Env.get("DB_PASSWORD", "root")
    host = Env.get("DB_HOST", "127.0.0.1")
    port = Env.get("DB_PORT", "3306")

    # Clean up host: remove @ prefix and socket path
    if host.startswith('@'):
        host = host[1:]
    if '/.s.PGSQL' in host:
        host = host.split('/.s.PGSQL')[0]

    # Encode password for special characters
    encoded_password = quote_plus(password) if password else ""

    if db_connection == "mysql":
        engine = create_engine(f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{db_name}")
    elif db_connection == "pgsql":
        engine = create_engine(f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{db_name}")
    else:
        raise Exception(f"Unsupported DB_CONNECTION: {db_connection}")

    return engine

def create_database_if_not_exists():
    db_connection = Env.get("DB_CONNECTION", "mysql")
    db_name = Env.get("DB_DATABASE", "laravelfastapi")
    user = Env.get("DB_USERNAME", "root")
    password = Env.get("DB_PASSWORD", "")
    host = Env.get("DB_HOST", "127.0.0.1")
    port = Env.get("DB_PORT", "3306")

    # Clean up host: remove @ prefix and socket path
    if host.startswith('@'):
        host = host[1:]
    if '/.s.PGSQL' in host:
        host = host.split('/.s.PGSQL')[0]

    # Encode password for special characters
    encoded_password = quote_plus(password) if password else ""

    if db_connection == "mysql":
        engine = create_engine(f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/")
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            print(f"✅ Database `{db_name}` ready.")
    elif db_connection == "pgsql":
        engine = create_engine(f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/postgres")
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if result.fetchone() is None:
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"✅ Database `{db_name}` created.")
            else:
                 print(f"✅ Database `{db_name}` ready.")

def ensure_migrations_table(engine):
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            migration VARCHAR(255) NOT NULL UNIQUE,
            batch INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        conn.commit()

def normalize_migration(filename: str) -> str:
    match = re.match(r"^\d{4}_\d{2}_\d{2}_\d{6}_(.*)\.py$", filename)
    return match.group(1) if match else filename

def get_ran_migrations(engine):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT migration FROM migrations")).fetchall()
            return [row[0] for row in result]
    except Exception:
        # Table doesn't exist yet, return empty list
        return []

def log_migration(engine, migration, batch):
     with engine.connect() as conn:
        stmt = text("INSERT INTO migrations (migration, batch) VALUES (:migration, :batch)")
        conn.execute(stmt, {"migration": migration, "batch": batch})
        conn.commit()

def migrate():
    try:
        create_database_if_not_exists()
        engine = get_engine()
        ensure_migrations_table(engine)
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return

    migrations_path = os.path.join(BASE_DIR, "database", "migrations")
    if not os.path.exists(migrations_path):
        print("❌ No migrations directory found.")
        return

    ran = get_ran_migrations(engine)
    files = sorted(os.listdir(migrations_path))

    new_migrations = []
    for f in files:
        if f.endswith(".py"):
            core = normalize_migration(f)
            if core not in ran:
                new_migrations.append((f, core))

    if not new_migrations:
        print("✨ Nothing to migrate.")
        return

    with engine.connect() as conn:
        result = conn.execute(text("SELECT MAX(batch) FROM migrations")).scalar_one_or_none()
        batch = (result or 0) + 1

    for file, core in new_migrations:
        migration_name = file.replace(".py", "")
        file_path = os.path.join(migrations_path, file)
        spec = importlib.util.spec_from_file_location(migration_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "Migration"):
            instance = module.Migration()
            if hasattr(instance, "up"):
                print(f"🔼 Running migration: {migration_name}")
                instance.up(engine)
                log_migration(engine, core, batch)
        elif hasattr(module, "up"):
            print(f"🔼 Running migration: {migration_name}")
            module.up(engine)
            log_migration(engine, core, batch)
        else:
            print(f"⚠️ No up() method or Migration class in {migration_name}")
