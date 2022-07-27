from operator import truediv
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app= FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="FastApi_learning", user="postgres",
                                password="UaU648jw", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [
    {"title": "Football is awesome", "content": "T. Henry is the best showman", "id":1},
    {"title": "Broke my anckle...", "content": "...playing foot", "id":2}
]

def find_index_post(id):
    for idx, post in enumerate(my_posts):
        if post["id"]==id:
            return idx

def find_post(id):

    for post in my_posts:
        if post["id"]==id:
            return post

@app.get("/")
async def root():
    return {"Stroop Robotics API": "Welcome"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}", status_code=status.HTTP_201_CREATED)
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} was not found")
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Post created successfully": new_post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    deleted_post = cursor.fetchone
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exit.")
    conn.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""",
                 (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exit.")
    conn.commit()
    return {'data': updated_post}
 