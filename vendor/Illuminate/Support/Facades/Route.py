# vendor/Illuminate/Support/Facades/Route.py
from vendor.Illuminate.Support.Facades.Facade import Facade

class Route(Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "router"
