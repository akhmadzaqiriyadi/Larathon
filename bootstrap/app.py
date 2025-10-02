from fastapi import FastAPI
from bootstrap.providers import register_providers
from fastapi.staticfiles import StaticFiles

def create_app():
    app = FastAPI()

    register_providers(app)

    # MOUNT STATIC FILES
    app.mount("/static", StaticFiles(directory="public/static"), name="static")

    return app


app = create_app()
