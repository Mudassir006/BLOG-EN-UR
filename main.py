from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import create_engine, SQLModel, Session, select
import uvicorn

import models.blog_model
from models.blog_model import Blog, Author

app = FastAPI()
connect_args = {"check_same_thread": False}
engine = create_engine('sqlite:///database.db', echo=True, connect_args=connect_args)
blog = Blog()


@app.on_event("startup")
def on_startup():
    create_tables()


def get_session():
    with Session(engine) as session:
        yield session


@app.post('/create-blog')
async def create_blog(blog: Blog, session: Session = Depends(get_session), ):
    db_blog = Blog.from_orm(blog)
    session.add(db_blog)
    session.commit()
    return db_blog


@app.post('/create-author')
async def create_author(author: Author, session: Session = Depends(get_session), ):
    db_author = Author.from_orm(author)
    session.add(db_author)
    session.commit()
    return db_author


@app.get('/read_blog/{blog_id}')
async def read_blog(blog_id, session: Session = Depends(get_session), ):
    result = session.get(Blog, blog_id)

    if not result:
        raise HTTPException(status_code=404, detail="Blog Not Found")

    print(result)
    return result


@app.delete('/delete_blog/{blog_id}')
async def delete_blog(blog_id, session: Session = Depends(get_session), ):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="No blog found")
    session.delete(blog)
    session.commit()
    return {"ok Blog deleted"}


@app.put('/create-blog/{blog_id}')
async def update_blog(*, session: Session = Depends(get_session), blog_id: int, blog: Blog):
    db_blog = session.query(models.blog_model.Blog).filter(models.blog_model.Blog.blog_id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Not Found")
    db_blog.author_id = blog.author_id
    db_blog.title = blog.title
    db_blog.slug = blog.slug
    db_blog.blog_ = blog.blog_
    db_blog.lang = blog.lang
    db_blog.is_published = blog.is_published
    db_blog.views = blog.views
    session.add(db_blog)
    session.commit()
    return db_blog

def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
    create_tables()
    read_blog()
    create_author()
    delete_blog()
    update_blog()
