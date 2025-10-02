import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class MakeMigrationCommand:
    @staticmethod
    def handle(name: str):
        migrations_path = os.path.join(BASE_DIR, "database", "migrations")
        os.makedirs(migrations_path, exist_ok=True)

        timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        filename = os.path.join(migrations_path, f"{timestamp}_{name}.py")

        content = f'''"""
Migration: {name}
"""

def up():
    print("🔼 Creating table: {name.replace("create_", "").replace("_table", "")}")
    # TODO: implement table creation

def down():
    print("🔽 Dropping table: {name.replace("create_", "").replace("_table", "")}")
    # TODO: implement table drop
'''

        with open(filename, "w") as f:
            f.write(content)

        print(f"✅ Migration created: {filename}")
