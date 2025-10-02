import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

class ViewFactory:
    def __init__(self):
        # atur folder templates (resources/views)
        views_path = os.path.join(os.getcwd(), "resources", "views")
        self.env = Environment(
            loader=FileSystemLoader(views_path),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def make(self, template, context=None):
        context = context or {}
        # laravel style: todos/index → todos/index.html
        template_path = template + ".html"
        tpl = self.env.get_template(template_path)
        return tpl.render(**context)
