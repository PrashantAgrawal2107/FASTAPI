from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data' : {'name' : 'PK'}}

@app.get('/about')
def about():
    return 'About Page'