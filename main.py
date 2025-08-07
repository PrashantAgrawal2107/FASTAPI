from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Blog(BaseModel):
    title : str
    body : str
    published : Optional[bool] = None


@app.post('/blog')
def create_blog(request : Blog):
    return {'data' : 'Blog is created'}


@app.get('/blogs')
def blog(limit:int = 10, pub:bool = True , sort: Optional[str] ='asc'):
    return {'data' : f'blog list -- {limit} blogs which ar {pub} sorted by {sort}'}

@app.get('/blog/hii')
def index():
    return {'data' : 'hii'}

@app.get('/blog/{id}')
def index(id):
    return {'data' : {'name' : 'string'}}

# @app.get('/blog/{id}')
# def index(id:int):
#     return {'data' : {'name' : 'PK'}}

@app.get('/about')
def about():
    return 'About Page'



# ------- RUN USING python3 main.py  -------

# if __name__ == '__main__':
#     uvicorn.run(app , host = 'localhost' , port=5000)