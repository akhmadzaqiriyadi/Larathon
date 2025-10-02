import os
import re
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# ------------------------
# Helpers
# ------------------------
def file_exists(path):
    return os.path.exists(path)

def normalize_migration(filename: str) -> str:
    """Ambil nama inti migration tanpa timestamp"""
    match = re.match(r"^\d{4}_\d{2}_\d{2}_\d{6}_(.*)\.py$", filename)
    return match.group(1) if match else filename


# ------------------------
# Controller
# ------------------------
def make_controller(name, resource=False):
    controllers_path = os.path.join(BASE_DIR, "app", "Http", "Controllers")
    os.makedirs(controllers_path, exist_ok=True)
    filename = os.path.join(controllers_path, f"{name}.py")

    if file_exists(filename):
        print(f"⚠️ Controller `{name}` already exists, skipped.")
        return

    if resource:
        content = f'''from app.Http.Controllers.Controller import Controller

class {name}(Controller):
    def index(self, request):
        return self.view("{name.lower()}.index", request)

    def create(self, request):
        return self.view("{name.lower()}.create", request)

    async def store(self, request):
        return {{"message": "Store new {name}"}}

    def show(self, request, id):
        return self.view("{name.lower()}.show", request, {{"id": id}})

    def edit(self, request, id):
        return self.view("{name.lower()}.edit", request, {{"id": id}})

    async def update(self, request, id):
        return {{"message": f"Update {{id}} {name}"}}

    def destroy(self, request, id):
        return {{"message": f"Delete {{id}} {name}"}}
'''
    else:
        content = f'''from app.Http.Controllers.Controller import Controller

class {name}(Controller):
    def __init__(self):
        pass
'''

    with open(filename, "w") as f:
        f.write(content)
    print(f"✅ Controller created: {filename}")

# ------------------------
# Model
# ------------------------
def make_model(name, migration=False):
    models_path = os.path.join(BASE_DIR, "app", "Models")
    os.makedirs(models_path, exist_ok=True)
    filename = os.path.join(models_path, f"{name}.py")

    if file_exists(filename):
        print(f"⚠️ Model `{name}` already exists, skipped.")
    else:
        content = f'''class {name}:
    def __init__(self):
        pass
'''
        with open(filename, "w") as f:
            f.write(content)
        print(f"✅ Model created: {filename}")

    if migration:
        make_migration(f"create_{name.lower()}s_table")


# ------------------------
# Migration
# ------------------------
def make_migration(name: str):
    migrations_path = os.path.join(BASE_DIR, "database", "migrations")
    os.makedirs(migrations_path, exist_ok=True)

    # 🔎 Cek apakah migration dengan nama sama sudah ada
    pattern = rf"^\d{{4}}_\d{{2}}_\d{{2}}_\d{{6}}_{name}\.py$"
    existing = [f for f in os.listdir(migrations_path) if re.match(pattern, f)]
    if existing:
        print(f"⚠️ Migration `{name}` already exists, skipped.")
        return

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename = os.path.join(migrations_path, f"{timestamp}_{name}.py")

    if name.startswith("create_") and name.endswith("_table"):
        table = name.replace("create_", "").replace("_table", "")
        content = f'''"""
Migration: {name}
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, TIMESTAMP
from datetime import datetime

class Migration:
    def up(self, engine):
        meta = MetaData()
        Table(
            "{table}", meta,
            Column("id", Integer, primary_key=True),
            Column("name", String(255)),
            Column("created_at", TIMESTAMP, default=datetime.utcnow),
        )
        meta.create_all(engine)
        print("🔼 Creating table: {table}")

    def down(self, engine):
        meta = MetaData(bind=engine)
        table = Table("{table}", meta, autoload_with=engine)
        table.drop(engine)
        print("🔽 Dropping table: {table}")
'''
    else:
        content = f'''"""
Migration: {name}
"""

class Migration:
    def up(self, engine):
        print("🔼 Applying migration: {name}")

    def down(self, engine):
        print("🔽 Rolling back migration: {name}")
'''

    with open(filename, "w") as f:
        f.write(content)

    print(f"✅ Migration created: {filename}")


# ------------------------
# Seeder
# ------------------------
def make_seeder(name):
    seeders_path = os.path.join(BASE_DIR, "database", "seeders")
    os.makedirs(seeders_path, exist_ok=True)
    filename = os.path.join(seeders_path, f"{name}.py")

    if file_exists(filename):
        print(f"⚠️ Seeder `{name}` already exists, skipped.")
        return

    content = f'''class {name}:
    def run(self):
        print("🌱 Seeding {name}...")
'''
    with open(filename, "w") as f:
        f.write(content)
    print(f"✅ Seeder created: {filename}")


# ------------------------
# Factory
# ------------------------
def make_factory(name):
    factories_path = os.path.join(BASE_DIR, "database", "factories")
    os.makedirs(factories_path, exist_ok=True)
    filename = os.path.join(factories_path, f"{name}.py")

    if file_exists(filename):
        print(f"⚠️ Factory `{name}` already exists, skipped.")
        return

    content = f'''class {name}:
    def definition(self):
        return {{
            "name": "Example",
            "email": "example@test.com"
        }}
'''
    with open(filename, "w") as f:
        f.write(content)
    print(f"✅ Factory created: {filename}")
