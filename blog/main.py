from fastapi import FastAPI , Depends , status , Response , HTTPException
from . import schemas , models
from .database import engine , SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()

@app.post('/blog' , status_code = status.HTTP_201_CREATED)
def createBlog(request : schemas.Blog , db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title , body = request.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=list[schemas.ShowBlog])
def getBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}' , status_code=200 , response_model=schemas.ShowBlog)
def showBlog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f'Blog with id {id} is not available')
    return blog

@app.delete('/blog/{id}' , status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f'Blog with id {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Done'

@app.put('/blog/{id}' , status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id ,request : schemas.Blog , db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f'Blog with id {id} is not available')
    blog.update({'title':request.title , 'body' : request.body})
    db.commit()
    return 'Done'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    request.password = hashed_password
    new_user = models.User(name=request.name, email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 