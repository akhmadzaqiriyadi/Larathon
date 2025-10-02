# vendor/Illuminate/View/View.py
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="resources/views")

class View:
    @staticmethod
    def make(template: str, context: dict = None):
        # default kosong
        context = context or {}
        if "request" not in context:
            raise ValueError('View.make() requires "request" in context')
        return templates.TemplateResponse(template.replace(".", "/") + ".html", context)
