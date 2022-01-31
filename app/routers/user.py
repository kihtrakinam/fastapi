from .. import models, utils, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy import func
from typing import Optional, List

router = APIRouter(tags = ["Users"])

@router.post("/register_user", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def register_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
	hashed_password = utils.hash(user.password)
	user.password = hashed_password
	new_user = models.User(**user.dict())
	try:
		db.add(new_user)
		db.commit()
		db.refresh(new_user)
		return new_user
	except:
		raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"Mail ID - {user.email} already registered")

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(email : Optional[str] = "", phone_number : Optional[str] = "", 
current_user : models.User = Depends(oauth2.get_current_user), db : Session = Depends(get_db)):
	user_query = db.query(models.User).filter(func.lower(models.User.email).contains(email)).\
		filter(models.User.phone_number.startswith(phone_number)).order_by(models.User.id.asc())
	user = user_query.all()
	if user == []:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with required features does not exist")
	return user

@router.get("/users/{id}", response_model = schemas.UserResponse)
def get_user(id : int, db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
	user = db.query(models.User).filter(models.User.id == id).first()
	if user == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id : {id} does not exist")
	return user