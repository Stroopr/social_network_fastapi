from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__= "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE' ,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("NOW()"))
    owner_id = Column(Integer, ForeignKey(column="users.id",ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("NOW()"))


class Vote(Base):
    __tablename__="votes"

    post_id = Column(Integer, ForeignKey(column="posts.id",ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(column="users.id",ondelete="CASCADE"), primary_key=True, nullable=False)