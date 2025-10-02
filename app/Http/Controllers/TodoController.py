# app/Http/Controllers/TodoController.py
from app.Http.Controllers.Controller import Controller
from app.Models.Todo import Todo
from vendor.Illuminate.Console import database
from sqlalchemy.orm import sessionmaker

# Ambil engine dari vendor console (pakai env config)
engine = database.get_engine()
SessionLocal = sessionmaker(bind=engine)

class TodoController(Controller):
    def index(self, request):
        session = SessionLocal()
        todos = session.query(Todo).all()
        session.close()
        return self.view("todos.index", request, {"todos": todos})

    def create(self, request):
        return self.view("todos.create", request)

    async def store(self, request):
        data = await self.request(request)
        print("STORE DATA:", data)  # <-- debug
        session = SessionLocal()
        todo = Todo(name=data.get("name"))
        session.add(todo)
        session.commit()
        session.close()
        return self.redirect("/todos")

    def show(self, request, id):
        session = SessionLocal()
        todo = session.query(Todo).get(id)
        session.close()
        return self.view("todos.show", request, {"todo": todo})

    def edit(self, request, id):
        session = SessionLocal()
        todo = session.query(Todo).get(id)
        session.close()
        return self.view("todos.edit", request, {"todo": todo})

    async def update(self, request, id):
        data = await self.request(request)
        session = SessionLocal()
        todo = session.query(Todo).get(id)
        if todo:
            todo.name = data.get("name")
            session.commit()
        session.close()
        return self.redirect("/todos")

    def destroy(self, request, id):
        session = SessionLocal()
        todo = session.query(Todo).get(id)
        if todo:
            session.delete(todo)
            session.commit()
        session.close()
        return self.redirect("/todos")
