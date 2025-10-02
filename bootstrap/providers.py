from app.Providers.AppServiceProvider import AppServiceProvider
from app.Providers.AuthServiceProvider import AuthServiceProvider
from app.Providers.RouteServiceProvider import RouteServiceProvider
from app.Providers.ViewServiceProvider import ViewServiceProvider

def register_providers(app):
    providers = [
        AppServiceProvider(),
        AuthServiceProvider(),
        RouteServiceProvider(),
        ViewServiceProvider(),
    ]

    for provider in providers:
        provider.register(app)
