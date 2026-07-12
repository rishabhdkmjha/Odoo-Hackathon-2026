"""
Custom exceptions for business-rule violations. Caught centrally in main.py
so every error - expected or not - returns the standard JSON envelope.
"""
from fastapi import HTTPException, status


class ConflictError(HTTPException):
    """409 - e.g. double allocation, booking overlap."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class NotFoundError(HTTPException):
    """404 - referenced entity doesn't exist."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestError(HTTPException):
    """400 - malformed or logically invalid request."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ForbiddenError(HTTPException):
    """403 - authenticated but not permitted."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
