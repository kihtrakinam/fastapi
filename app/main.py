from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import time

app = FastAPI()

while True:
	try:
		conn = psycopg2.connect(host=settings.db_host, database=settings.db_name, user=settings.db_user, 
						password=settings.db_password, cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print('Database connection is successful')
		break
	except Exception as error:
		print('Database connection failed')
		print(f'Error : {error}')
		time.sleep(3)	

my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1},
{"title" : "title of post 2", "content" : "content of post 2", "id" : 2}]

def find_post(id):
	for post in my_posts:
		if post["id"] == id:
			return post

def find_index(id):
	for index, post in enumerate(my_posts):
		if post['id'] == id:
			return index

class Post(BaseModel):
	title : str
	content : str
	published : bool = True

@app.get("/")   ## Path operation / Route
def root():
	cursor.execute("""SELECT COUNT(*) FROM posts""")
	posts_count = cursor.fetchall()
	return {"message" : "Welcome to my API", "Active_posts" : posts_count}

@app.get("/posts")
def get_posts():
	cursor.execute("""SELECT * FROM posts""")
	posts = cursor.fetchall()
	return {"data" : posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post : Post):
	cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
				(post.title, post.content, post.published))
	new_post = cursor.fetchone()
	conn.commit()
	return {"message" : new_post}

@app.get("/posts/latest")
def get_latest_post():
	cursor.execute(f"""SELECT * FROM posts WHERE id = (SELECT MAX(id) FROM posts)""")
	post = cursor.fetchone()
	return {"post_detail" : post}

@app.get("/posts/{id}")
def get_specific_post(id : int, response : Response):
	cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
	post = cursor.fetchone()	
	if not post:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} does not exist")
	return {"post_detail" : post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
	cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
	post = cursor.fetchone()
	if not post:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} does not exist")
	else:
		conn.commit()

@app.put("/posts/{id}")
def update_post(id : int, post : Post):
	cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
				(post.title, post.content, post.published, id))
	post = cursor.fetchone()
	if not post:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} does not exist")
	else:
		conn.commit()
	return {"message" : "Post was updated successfuly", "post_detail" : post}