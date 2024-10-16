from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

from services import UserService

SECRET_KEY = "your-secret-key"
EXPIRATION_TIME = 15
ALGORITHM = "HS256"
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_service = UserService()


@router.post("/token", response_model=str)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if user_service.validate_credentials(form_data.username, form_data.password):
        return create_access_token(form_data.username)
    raise HTTPException(status_code=401, detail="Incorrect username or password")


def create_access_token(username):
    current_time = datetime.utcnow()
    expiration = current_time + timedelta(minutes=EXPIRATION_TIME)
    access_token = jwt.encode({"sub": username, "iat": current_time, "exp": expiration}, SECRET_KEY, ALGORITHM)
    return access_token


def get_current_user(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, [ALGORITHM])
        return payload.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
