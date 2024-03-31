from typing import TypeVar

from fastapi import FastAPI

from endpoints.user import user_router

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    """Сервер апи"""

    app_profile = FastAPI()
    app_profile.include_router(router=user_router, tags=["Users"])

    def __init__(self, app: FastAPI):
        self.__app = app

    def get_app(self) -> FastAPIInstance:
        return self.__app
