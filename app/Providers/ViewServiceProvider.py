from jinja2 import Environment, FileSystemLoader
from vendor.Illuminate.Support.Facades.Facade import Facade

class ViewServiceProvider:
    def register(self, app):
        env = Environment(
            loader=FileSystemLoader("resources/views"),
            autoescape=True
        )

        class ViewManager:
            def make(self, template, context=None):
                if context is None:
                    context = {}
                template = env.get_template(template + ".html")
                if "request" not in context:
                    raise ValueError("Missing 'request' in context. Required for 'url_for()' to work.")

                return template.render(**context)

        Facade._resolved["view"] = ViewManager()
