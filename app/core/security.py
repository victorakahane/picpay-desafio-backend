from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def generate_password_hash(password: str) -> str:
    """Generate a password hash."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password hash."""
    return pwd_context.verify(plain_password, hashed_password)
