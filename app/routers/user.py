from .. import models, utils, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(tags = ["Users"])

@router.post("/register_user", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
	hashed_password = utils.hash(user.password)
	user.password = hashed_password
	new_user = models.User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

@router.get("/users/{id}", response_model = schemas.UserResponse)
def get_user(id : int, db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
	user = db.query(models.User).filter(models.User.id == id).first()
	if user == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id : {id} does not exist")
	return user