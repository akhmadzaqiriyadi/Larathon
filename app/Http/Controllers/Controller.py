from vendor.Illuminate.Support.Facades.View import View
from fastapi.responses import RedirectResponse

class Controller:
    def view(self, template: str, request, context: dict = None):
        context = context or {}
        context["request"] = request
        return View.make(template, context)

    def redirect(self, url: str, status_code: int = 303):
        """Laravel-style redirect helper"""
        return RedirectResponse(url=url, status_code=status_code)

    async def request(self, request):
        """Auto detect request JSON/Form dan ignore _method."""
        content_type = request.headers.get("content-type", "")
        print("📌 Content-Type:", content_type)   # 👈 debug
        print("📌 Request method:", request.method)

        if "application/json" in content_type:
            data = await request.json()
            print("📥 JSON DATA:", data)   # 👈 debug
            return data

        elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            raw = await request.body()
            print("📥 RAW BODY:", raw.decode())
            form = await request.form()
            print("📥 RAW FORM:", form)
            data = {k: v for k, v in form.items() if k != "_method"}
            print("📥 CLEANED FORM DATA:", data)
            return data

        print("⚠️ Unknown body, returning empty dict")
        return {}

