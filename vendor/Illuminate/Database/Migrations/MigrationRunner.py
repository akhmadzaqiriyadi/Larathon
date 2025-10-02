import os
import psycopg2
from vendor.Illuminate.Support.Env import env

class MigrationRunner:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=env("DB_DATABASE"),
            user=env("DB_USERNAME"),
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env("DB_PORT"),
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        # Pastikan tabel migrations ada
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                migration VARCHAR(255) NOT NULL UNIQUE,
                batch INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def run(self):
        migrations_path = os.path.join(os.getcwd(), "database/migrations")
        files = sorted([f for f in os.listdir(migrations_path) if f.endswith(".py")])

        # Ambil batch terakhir
        self.cursor.execute("SELECT COALESCE(MAX(batch), 0) FROM migrations")
        current_batch = self.cursor.fetchone()[0] + 1

        for file in files:
            migration_name = file.replace(".py", "")

            # cek apakah sudah dieksekusi
            self.cursor.execute("SELECT 1 FROM migrations WHERE migration = %s", (migration_name,))
            if self.cursor.fetchone():
                print(f"⚠️ Skipped: {migration_name} already migrated")
                continue

            print(f"🔼 Running migration: {migration_name}")
            module = __import__(f"database.migrations.{migration_name}", fromlist=["Migration"])
            migration = module.Migration()
            migration.up(self.cursor)

            self.cursor.execute(
                "INSERT INTO migrations (migration, batch) VALUES (%s, %s)",
                (migration_name, current_batch),
            )

        self.cursor.close()
        self.conn.close()
