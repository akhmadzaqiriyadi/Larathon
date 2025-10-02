from app.Http.Controllers.Controller import Controller

class WelcomeController(Controller):
    def index(self, request):
        # render resources/views/welcome.html
        return self.view("welcome", request)
