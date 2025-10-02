from app.Http.Middleware.MethodOverrideMiddleware import MethodOverrideMiddleware

class AppServiceProvider:
    def register(self, app):
        print("🔧 AppServiceProvider registered")
        app.add_middleware(MethodOverrideMiddleware)

    def boot(self, app):
        print("🚀 AppServiceProvider booted")
