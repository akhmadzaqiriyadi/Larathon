import os, importlib.util
from config.database import get_engine

class Migrator:
    def __init__(self):
        self.engine = get_engine()
        self.migrations_path = os.path.join(os.getcwd(), "database", "migrations")

    def run(self):
        if not os.path.exists(self.migrations_path):
            print("❌ No migrations directory found.")
            return

        for file in sorted(os.listdir(self.migrations_path)):
            if file.endswith(".py") and file != "__init__.py":
                migration_name = file.replace(".py", "")
                file_path = os.path.join(self.migrations_path, file)

                spec = importlib.util.spec_from_file_location(migration_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "up"):
                    print(f"🔼 Running migration: {migration_name}")
                    module.up(self.engine)
                else:
                    print(f"⚠️ No up() method in {migration_name}")
