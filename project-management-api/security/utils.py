"""
Module for password utilities
"""

from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verifies password against a hash

    :param plain_password: password to verify
    :param hashed_password: hash to verify against
    :return: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Returns a hash of the password

    :param password: password to hash
    :return: hashed password
    """
    return pwd_context.hash(password)
