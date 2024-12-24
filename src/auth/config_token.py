from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "ABCDfdslkfjsue213131,mdsfjkfjdsu231313k213j219fds"  # Убедитесь, что ключ надежный
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Проверка наличия user_id и username
    if "user_id" not in to_encode or "username" not in to_encode:
        raise ValueError("user_id or username is missing in data")
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")  # Assuming the token contains a 'username' field
        if user_id is None or username is None:
            raise ValueError("user_id or username is missing in token")
        return {"username": username, "user_id": user_id}  # Returning just the username as a string
    except JWTError:
        raise ValueError("Token verification failed")
