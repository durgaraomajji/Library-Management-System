from passlib.context import CryptContext

pwd=CryptContext(schemes=["argon2"],deprecated="auto")


def hash(password):

    return pwd.hash(password)


def verify(password,hashed):

    return pwd.verify(password,hashed)