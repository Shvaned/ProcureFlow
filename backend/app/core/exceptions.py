from typing import Optional, Any


class ProcureFlowException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, status_code: int = 500, details: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundException(ProcureFlowException):
    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(message, status_code=404, details=details)


class ValidationException(ProcureFlowException):
    def __init__(self, message: str = "Validation failed", details: Optional[Any] = None):
        super().__init__(message, status_code=422, details=details)


class AuthorizationException(ProcureFlowException):
    def __init__(self, message: str = "Permission denied", details: Optional[Any] = None):
        super().__init__(message, status_code=403, details=details)


class AuthenticationException(ProcureFlowException):
    def __init__(self, message: str = "Authentication required", details: Optional[Any] = None):
        super().__init__(message, status_code=401, details=details)


class ConflictException(ProcureFlowException):
    def __init__(self, message: str = "Resource already exists", details: Optional[Any] = None):
        super().__init__(message, status_code=409, details=details)


class BusinessRuleException(ProcureFlowException):
    def __init__(self, message: str = "Business rule violation", details: Optional[Any] = None):
        super().__init__(message, status_code=422, details=details)


class DatabaseException(ProcureFlowException):
    def __init__(self, message: str = "Database error", details: Optional[Any] = None):
        super().__init__(message, status_code=500, details=details)


class ExternalServiceException(ProcureFlowException):
    def __init__(self, message: str = "External service error", details: Optional[Any] = None):
        super().__init__(message, status_code=502, details=details)


class AIException(ProcureFlowException):
    def __init__(self, message: str = "AI service error", details: Optional[Any] = None):
        super().__init__(message, status_code=502, details=details)


class WorkflowException(ProcureFlowException):
    def __init__(self, message: str = "Workflow execution error", details: Optional[Any] = None):
        super().__init__(message, status_code=422, details=details)


class RateLimitException(ProcureFlowException):
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Any] = None):
        super().__init__(message, status_code=429, details=details)
