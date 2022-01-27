from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data : dict):
	to_encode = data.copy()

	expire = datetime.now() + timedelta(minutes = settings.access_token_expire_minutes)
	expire_json = expire.isoformat()
	to_encode.update({"expiration" : expire_json})

	encoded_jwt = jwt.encode(to_encode, key = settings.secret_key, algorithm = settings.algorithm)
	return encoded_jwt

def verify_expiry(expire : datetime):
	diff = datetime.now() - expire
	expiry = True if diff.total_seconds() > 0 else False
	return expiry

def verify_access_token(token : str, credentials_exception):
	try:
		payload = jwt.decode(token, key = settings.secret_key, algorithms = settings.algorithm)
		id :str = payload.get("user_id")
		expire : datetime = datetime.fromisoformat(payload.get("expiration"))
		expiry_verification = verify_expiry(expire)
		
		if id is None or expiry_verification:
			raise credentials_exception

		token_data = schemas.TokenData(id = id)
		return token_data
	except JWTError as e:
		print(e)
		raise credentials_exception

def get_current_user(token : str =  Depends(oauth2_scheme), db : Session = Depends(get_db)):
	credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
	detail = f"Could not validate Credentials", headers = {"WWW-Authenticate" : "Bearer"})
	token = verify_access_token(token,credentials_exception).id
	user = db.query(models.User).filter(models.User.id == token).first()
	return user