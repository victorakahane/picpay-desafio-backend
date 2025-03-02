class DomainException(Exception):
    """Base exception for domain error."""
    pass

class UserAlreadyExistsException(DomainException):
    """Raised when a user already exists in database (by document or e-mail)."""
    pass

class UserCreationException(DomainException):
    """Indicates error for internal reasons on user creation."""
    pass
