from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class Token(BaseModel):
	access_token : str
	token_type : str

class TokenData(BaseModel):
	id : Optional[str]

class UserCreate(BaseModel):
	email : EmailStr
	password : str
	phone_number : str

class UserResponse(BaseModel):
	id : int
	email : EmailStr
	created_at : datetime

	class Config:
		orm_mode = True

class UserPostResponse(BaseModel):
	id : int
	email : EmailStr

	class Config:
		orm_mode = True

class VoteData(BaseModel):
	post_id : int
	vote_dir : bool

class VoteResponse(BaseModel):
	no_of_votes : int

class PostBase(BaseModel):
	title : str
	content : str
	published : bool = True

class PostCreate(PostBase):
	published : bool = False

class PostUpdate(PostBase):
	pass

class PostResponse(BaseModel):
	id : int
	title : str
	content : str
	created_at : datetime
	user : UserPostResponse

	class Config:
		orm_mode = True

class PostVoteResponse(BaseModel):
	Post : PostResponse
	votes_count : int
