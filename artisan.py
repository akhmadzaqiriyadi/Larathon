import typer
import subprocess
from vendor.Illuminate.Console import generators, database

app = typer.Typer(help="✨ Laravel-like Artisan CLI for FastAPI")

# -------------------------------
# Make Commands
# -------------------------------
@app.command("make:controller")
def make_controller(name: str, resource: bool = typer.Option(False, "--resource")):
    generators.make_controller(name, resource)

@app.command("make:model")
def make_model(
    name: str,
    m: bool = typer.Option(False, "-m", help="Create migration"),
    r: bool = typer.Option(False, "-r", help="Create resource controller")
):
    """Create a new model (optionally with migration and resource controller)."""
    # biarkan generator handle print
    generators.make_model(name)

    if m:
        migration_name = f"create_{name.lower()}s_table"
        generators.make_migration(migration_name)

    if r:
        controller_name = f"{name}Controller"
        generators.make_controller(controller_name, resource=True)

@app.command("make:migration")
def make_migration(name: str):
    generators.make_migration(name)

@app.command("make:seeder")
def make_seeder(name: str):
    generators.make_seeder(name)

@app.command("make:factory")
def make_factory(name: str):
    generators.make_factory(name)

# -------------------------------
# Database Commands
# -------------------------------
@app.command("migrate")
def migrate():
    database.migrate()

@app.command("db:seed")
def db_seed():
    database.run_seeders()

@app.command("migrate:fresh")
def migrate_fresh(seed: bool = typer.Option(False, "--seed")):
    database.fresh_migrate(seed)

# -------------------------------
# Serve Command
# -------------------------------
@app.command("serve")
def serve(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Run FastAPI server (like php artisan serve)."""
    cmd = ["uvicorn", "bootstrap.app:app", f"--host={host}", f"--port={port}"]
    if reload:
        cmd.append("--reload")
    subprocess.run(cmd)


if __name__ == "__main__":
    app()
