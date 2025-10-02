# routes/web.py
from vendor.Illuminate.Routing.Router import Route
from app.Http.Controllers.TodoController import TodoController
from app.Http.Controllers.WelcomeController import WelcomeController

# Definisi semua route di sini
Route.get("/", WelcomeController, "index")
Route.resource("todos", TodoController)
