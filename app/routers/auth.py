from datetime import timedelta, datetime
from typing import Dict

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

from services import UserService

SECRET_KEY = "your-secret-key"
DEFAULT_EXPIRATION_TIME = 15
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_service = UserService()


@router.post("/token", response_model=Dict[str, str])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           expiration_min: int = Form(DEFAULT_EXPIRATION_TIME)):
    if user_service.validate_credentials(form_data.username, form_data.password):
        if 5 <= expiration_min <= 240:
            access_token, expiration = create_access_token(form_data.username, expiration_min)
            return {"token": access_token, "expires": expiration}
        raise HTTPException(status_code=400, detail="Expiration time must be between 5 and 240 minutes")
    raise HTTPException(status_code=401, detail="Incorrect username or password")


def create_access_token(username, expiration_min):
    current_time = datetime.utcnow()
    expiration = current_time + timedelta(minutes=expiration_min)
    access_token = jwt.encode({"sub": username, "iat": current_time, "exp": expiration}, SECRET_KEY, ALGORITHM)
    expiration = expiration + timedelta(hours=3)  # Для приведения к MSK(UTC+3), т.к. при кодировке используется UTC+0
    return access_token, expiration.strftime("%A, %B %d, %Y, %H:%M:%S")


def get_current_user(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, [ALGORITHM])
        return payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
