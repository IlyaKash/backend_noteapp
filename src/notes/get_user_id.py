from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from auth.config_token import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        user_id = payload['user_id']
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=401, detail="user_id is missing in token")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
