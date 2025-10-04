from vendor.Illuminate.Routing.Router import Router
from vendor.Illuminate.Support.Facades.Route import Route
from routes.api import router as api_router

class RouteServiceProvider:
    def register(self, app):
        # buat instance Router
        router_instance = Router()

        # swap ke facade
        Route.swap(router_instance)

        # load definisi routes
        import routes.web  # <--- biarkan dia isi Route facade

        # setelah semua route terdaftar, baru include ke FastAPI
        app.include_router(router_instance.router)

        # sertakan juga routes/api.py
        app.include_router(api_router, prefix="/api")
