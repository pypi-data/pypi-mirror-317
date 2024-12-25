from fastapi import HTTPException


class AuthError(Exception):
    pass


class TokenError(AuthError, HTTPException):
    """Raised when token is invalid"""

    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code


class ParamsError(AuthError):
    pass


class RequestError(AuthError):
    """Raised when request is invalid or it could not be processed"""
