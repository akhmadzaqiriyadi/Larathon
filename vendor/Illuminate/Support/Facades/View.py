# vendor/Illuminate/Support/Facades/View.py
from vendor.Illuminate.View.View import View as BaseView

class View:
    @staticmethod
    def make(template: str, context: dict = {}):
        return BaseView.make(template, context)

def view(template: str, context: dict = {}):
    return View.make(template, context)
