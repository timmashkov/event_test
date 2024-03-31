from typing import TypeVar

from fastapi import FastAPI

from endpoints.company import comp_router
from endpoints.user import user_router

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    """Сервер апи"""

    app = FastAPI()
    app.include_router(router=user_router, tags=["Users"])
    app.include_router(router=comp_router, tags=["Companies"])

    def __init__(self, app: FastAPI):
        self.__app = app

    def get_app(self) -> FastAPIInstance:
        return self.__app
