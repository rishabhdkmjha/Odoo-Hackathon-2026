"""
Standard response envelope used by every endpoint:
{ "success": bool, "message": str, "data": Any }
"""
from typing import Any, Optional


def success_response(message: str = "Success", data: Any = None) -> dict:
    return {"success": True, "message": message, "data": data}


def error_response(message: str = "Something went wrong", data: Any = None) -> dict:
    return {"success": False, "message": message, "data": data}
