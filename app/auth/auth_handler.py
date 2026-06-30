from jose import jwt

from datetime import datetime,timedelta

from app.config import *


def create_access_token(data):

    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=60)

    to_encode.update({"exp":expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )