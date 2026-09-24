from fastapi import Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import decode_access_token
bearer=HTTPBearer(auto_error=False)
def get_current_user(c:HTTPAuthorizationCredentials|None=Depends(bearer),db:Session=Depends(get_db)):
    if not c: raise HTTPException(status_code=401,detail='Authentication required')
    u=db.get(User,int(decode_access_token(c.credentials)))
    if not u: raise HTTPException(status_code=401,detail='User not found')
    return u
