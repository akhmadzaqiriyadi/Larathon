from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class MethodOverrideMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            try:
                form = await request.form()
                # hanya override jika ada _method dan nilainya valid
                if "_method" in form:
                    method_override = form["_method"].upper()
                    if method_override in ("PUT", "DELETE", "PATCH"):
                        request.scope["method"] = method_override
            except Exception:
                pass
        return await call_next(request)
