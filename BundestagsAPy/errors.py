import json

class BundestagsAPyException(Exception):
    """Base exception for BundestagsAPy"""
    pass

class HTTPException(BundestagsAPyException):
    """Exception raised when an HTTP request fails"""

    def __init__(self, response):
        self.response = response

        self.api_errors = []
        self.api_codes = []
        self.api_messages = []

        try:
            response_json = response.json()
        except json.JSONDecodeError:
            super().__init__(f"{response.status_code} {response.reason}")
        else:
            errors = response_json.get("errors", [])
            if "error" in response_json:
                errors.append(response_json["error"])
            error_text = ""
            for error in errors:
                self.api_errors.append(error)
                if "code" in error:
                    self.api_codes.append(error["code"])
                if "message" in error:
                    self.api_messages.append(error["message"])
                if "code" in error and "message" in error:
                    error_text += f"\n{error['code']} - {error['message']}"
                elif "message" in error:
                    error_text += '\n' + error["message"]
            super().__init__(
                f"{response.status_code} {response.reason}{error_text}"
            )

class BadRequest(HTTPException):
    """Exception raised for a 400 HTTP status code"""
    pass


class Unauthorized(HTTPException):
    """Exception raised for a 401 HTTP status code"""
    pass


class Forbidden(HTTPException):
    """Exception raised for a 403 HTTP status code"""
    pass


class NotFound(HTTPException):
    """Exception raised for a 404 HTTP status code"""
    pass


class TooManyRequests(HTTPException):
    """Exception raised for a 429 HTTP status code"""
    pass