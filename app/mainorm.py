from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

## models.Base.metadata.create_all(bind= engine) ##creating tables in Postgresql using sqlalchemy before migrating to Alembic

app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_credentials = True, allow_methods = ["*"],\
	allow_headers=["*"])

@app.get("/")   ## Path operation / Route
def root(db: Session = Depends(get_db)): #, current_user : models.User = Depends(oauth2.get_current_user)
	users_count = db.query(func.count(distinct(models.User.id))).scalar()
	posts_count = db.query(func.count(distinct(models.Post.id))).scalar()
	#my_posts_count = db.query(func.count(distinct(models.Post.id))).filter(models.Post.user_id == current_user.id).scalar()
	return {"message" : "Welcome to my API", "Active_users" : users_count, "Active_posts" : posts_count} #, "My_posts" : my_posts_count

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)