# vendor/Illuminate/Support/Facades/Response.py
from fastapi.responses import JSONResponse

class Response:
    @staticmethod
    def json(data: dict, status: int = 200):
        return JSONResponse(content=data, status_code=status)

# helper global
def response(data: dict, status: int = 200):
    return Response.json(data, status)
