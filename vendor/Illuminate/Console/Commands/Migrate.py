import os
import re
import sys
import importlib.util
from vendor.Illuminate.Support.Env import Env
from sqlalchemy import create_engine, text

BASE_DIR = sys.path[0]

def get_engine():
    db_name = Env.get("DB_DATABASE", "laravelfastapi")
    user = Env.get("DB_USERNAME", "root")
    password = Env.get("DB_PASSWORD", "root")
    host = Env.get("DB_HOST", "127.0.0.1")
    port = Env.get("DB_PORT", "3306")

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}")
    return engine

def create_database_if_not_exists():
    db_name = Env.get("DB_DATABASE", "laravelfastapi")
    user = Env.get("DB_USERNAME", "root")
    password = Env.get("DB_PASSWORD", "root")
    host = Env.get("DB_HOST", "127.0.0.1")
    port = Env.get("DB_PORT", "3306")

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/")
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        print(f"✅ Database `{db_name}` ready.")

def ensure_migrations_table(engine):
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration VARCHAR(255) NOT NULL,
            batch INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))

def normalize_migration(filename: str) -> str:
    match = re.match(r"^\d{4}_\d{2}_\d{2}_\d{6}_(.*)\.py$", filename)
    return match.group(1) if match else filename

def get_ran_migrations(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT migration FROM migrations"))
        return [row[0] for row in result]

def log_migration(engine, migration, batch):
    with engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO migrations (migration, batch) VALUES (:migration, :batch)"
        ), {"migration": migration, "batch": batch})

def migrate():
    engine = get_engine()
    create_database_if_not_exists()
    ensure_migrations_table(engine)

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

    # Cari batch terakhir
    with engine.connect() as conn:
        result = conn.execute(text("SELECT MAX(batch) FROM migrations")).fetchone()
        batch = (result[0] or 0) + 1

    for file, core in new_migrations:
        migration_name = file.replace(".py", "")
        file_path = os.path.join(migrations_path, file)

        spec = importlib.util.spec_from_file_location(migration_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "up"):
            print(f"🔼 Running migration: {migration_name}")
            module.up(engine)
            log_migration(engine, core, batch)
        else:
            print(f"⚠️ No up() method in {migration_name}")
