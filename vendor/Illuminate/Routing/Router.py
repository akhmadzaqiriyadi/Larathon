import re
import inspect
from fastapi import APIRouter, Request

class Router:
    routes = []
    router = APIRouter()

    @classmethod
    def add(cls, method, path, controller=None, action=None):
        # regex untuk match route <id>
        pattern = "^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path) + "$"
        fastapi_path = path.replace("<", "{").replace(">", "}")

        cls.routes.append({
            "method": method.upper(),
            "path": path,
            "pattern": re.compile(pattern),
            "controller": controller,
            "action": action
        })

        async def endpoint(request: Request):
            path_params = request.path_params

            # --- Method Spoofing (Laravel style) ---
            if request.method == "POST":
                try:
                    form = await request.form()
                    if "_method" in form:
                        method_override = form["_method"].upper()

                        action_map = {
                            "PUT": "update",
                            "DELETE": "destroy"
                        }

                        if method_override in action_map:
                            # ✅ simpan form ke request supaya bisa dipakai nanti
                            request.state._form = form

                            # 🚀 tentukan handler langsung
                            instance = controller()
                            handler = getattr(instance, action_map[method_override])
                            if inspect.iscoroutinefunction(handler):
                                return await handler(request, **path_params)
                            return handler(request, **path_params)
                except Exception as e:
                    print("⚠️ Spoofing error:", e)

            # --- CASE 1: closure langsung
            if callable(controller) and action is None:
                sig = inspect.signature(controller)
                args = {}
                for name, param in sig.parameters.items():
                    if name in path_params:
                        args[name] = path_params[name]
                    elif name == "request":
                        args[name] = request

                if inspect.iscoroutinefunction(controller):
                    return await controller(**args)
                return controller(**args)

            # --- CASE 2: controller class
            instance = controller()
            handler = getattr(instance, action)
            sig = inspect.signature(handler)
            args = {}
            for name, param in sig.parameters.items():
                if name in path_params:
                    args[name] = path_params[name]
                elif name == "request":
                    args[name] = request

            if inspect.iscoroutinefunction(handler):
                return await handler(**args)
            return handler(**args)

        # register ke FastAPI
        cls.router.add_api_route(
            fastapi_path,
            endpoint,
            methods=[method.upper()]
        )

    # Shortcut methods
    @classmethod
    def get(cls, path, controller=None, action=None):
        cls.add("GET", path, controller, action)

    @classmethod
    def post(cls, path, controller=None, action=None):
        cls.add("POST", path, controller, action)

    @classmethod
    def put(cls, path, controller=None, action=None):
        cls.add("PUT", path, controller, action)

    @classmethod
    def delete(cls, path, controller=None, action=None):
        cls.add("DELETE", path, controller, action)

    # resource style
    @classmethod
    def resource(cls, name, controller):
        base = f"/{name}"
        cls.get(base, controller, "index")
        cls.get(f"{base}/create", controller, "create")
        cls.post(base, controller, "store")
        cls.get(f"{base}/<id>", controller, "show")
        cls.get(f"{base}/<id>/edit", controller, "edit")
        cls.put(f"{base}/<id>", controller, "update")
        cls.delete(f"{base}/<id>", controller, "destroy")

    @classmethod
    def list_routes(cls):
        return cls.routes

Route = Router
