from infrastructure.exceptions.base import BaseAPIException

from fastapi import status


class CourseNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User not found"


class CourseAlreadyExist(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "User already exist"
