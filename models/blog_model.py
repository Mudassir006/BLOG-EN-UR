from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, Column


class Blog(SQLModel, table=True):
    blog_id: Optional[int] = Field(default=None, primary_key=True, )
    author_id: Optional[int] = Field(default=None, foreign_key='author.author_id')
    title: str
    slug: str
    blog_: str
    lang: str = Field(default='ENG')
    is_published: bool = Field(default=False)
    views: Optional[int] = Field(default=0)


class Author(SQLModel, table=True):
    author_id: Optional[int] = Field(default=None, primary_key=True, )
    user_id: int
    name_en: str
    title_en: str
    name_ur: str
    title_ur: str
    photo: str



