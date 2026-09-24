from datetime import datetime,timedelta,timezone
import hashlib,hmac,secrets,jwt
from fastapi import HTTPException
from app.config import get_settings
ALG='HS256'
def hash_password(p):
    salt=secrets.token_bytes(16); d=hashlib.pbkdf2_hmac('sha256',p.encode(),salt,120000); return f'pbkdf2_sha256$120000${salt.hex()}${d.hex()}'
def verify_password(p,s):
    try:
        scheme,rounds,salt,digest=s.split('$'); cand=hashlib.pbkdf2_hmac('sha256',p.encode(),bytes.fromhex(salt),int(rounds)).hex(); return scheme=='pbkdf2_sha256' and hmac.compare_digest(cand,digest)
    except Exception:return False
def create_access_token(sub):
    exp=datetime.now(timezone.utc)+timedelta(minutes=get_settings().access_token_expire_minutes); return jwt.encode({'sub':str(sub),'exp':exp},get_settings().secret_key,algorithm=ALG)
def decode_access_token(token):
    try:
        p=jwt.decode(token,get_settings().secret_key,algorithms=[ALG]); return str(p['sub'])
    except Exception: raise HTTPException(status_code=401,detail='Invalid or expired token')
