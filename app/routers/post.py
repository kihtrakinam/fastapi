from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from ..database import get_db

router = APIRouter(prefix = "/posts", tags = ["Posts"])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
	new_post = models.Post(user_id = current_user.id, **post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post

@router.get("/", response_model = List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user),
 limit : int = 5, skip : int = 0, search : Optional[str] = ""):
	posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).\
		join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).\
		filter(models.Post.user_id == current_user.id).\
		filter(func.lower(models.Post.title).contains(search.lower())).\
		group_by(models.Post.id).\
		order_by(models.Post.id.desc()).offset(skip).limit(limit)
	posts = posts_query.all()
	return posts

@router.get("/latest", response_model = schemas.PostVoteResponse)
def get_latest_post(db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
	id = db.query(func.max(models.Post.id)).filter(models.Post.user_id == current_user.id).scalar()
	if id is None:
		raise HTTPException(status_code = status.HTTP_204_NO_CONTENT)
	posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).\
		join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
		filter(models.Post.id == id).group_by(models.Post.id).first()
	return posts

@router.get("/{id}", response_model = schemas.PostVoteResponse)
def get_specific_post(id : int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
	posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).\
		join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
		filter(models.Post.id == id).group_by(models.Post.id).first()
	if posts == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} does not exist")
	if posts.Post.user_id != current_user.id:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")
	return posts

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	posts = post_query.first()
	if posts == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} does not exist")
	if posts.user_id != current_user.id:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")
	post_query.delete(synchronize_session=False)
	db.commit()

@router.put("/{id}", response_model = schemas.PostVoteResponse)
def update_post(id : int, post : schemas.PostUpdate, db: Session = Depends(get_db), 
current_user : models.User = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	posts = post_query.first()
	if posts == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} does not exist")
	if posts.user_id != current_user.id:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")
	post_query.update(post.dict(),synchronize_session=False)
	db.commit()

	## Getting details of updated post with votes
	updated_posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).\
		join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).\
		filter(models.Post.id == id).group_by(models.Post.id).first()
	return updated_posts
