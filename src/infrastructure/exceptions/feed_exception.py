from infrastructure.exceptions.base import BaseAPIException

from fastapi import status


class FeedbackNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Employer not found"


class FeedbackAlreadyExist(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Employer already exist"
