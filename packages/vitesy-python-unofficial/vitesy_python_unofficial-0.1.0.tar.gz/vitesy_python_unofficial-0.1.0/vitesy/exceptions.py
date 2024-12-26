class VitesyError(Exception):
    """Base exception for Vitesy SDK"""
    pass

class AuthenticationError(VitesyError):
    """Raised when authentication fails"""
    pass

class APIError(VitesyError):
    """Raised when the API returns an error"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}") 