class SrunException(Exception):
    """Base exception for all srun-related errors"""
    pass

class AuthenticationError(SrunException):
    """Raised when authentication fails"""
    pass

class NetworkError(SrunException):
    """Raised when network operations fail"""
    pass 