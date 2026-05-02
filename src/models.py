from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime, timezone

db = SQLAlchemy()

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    #FK's:
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable= False)

    #Relaciones:
    follower: Mapped["User"] = relationship(foreign_keys=[follower_id],back_populates="following")
    following: Mapped["User"] = relationship(foreign_keys=[following_id], back_populates = "followers")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id
         }

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

     # RELACIONES:
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates= "author")
    
        
    # Usuarios que sigo
    following: Mapped[List["Follower"]] = relationship(
    "Follower",
    foreign_keys=[Follower.follower_id],
    back_populates="follower"
)

    # Usuarios que me siguen
    followers: Mapped[List["Follower"]] = relationship(
    "Follower",
    foreign_keys=[Follower.following_id],
    back_populates="following"
)
  

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name":self.name,
            "last_name":self.last_name,
            "user_name":self.user_name
            # do not serialize the password, its a security breach
        }
    

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # FK:
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    #Relaciones:
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates= "post")
    media: Mapped[List["Media"]] = relationship(back_populates= "post")
                                    

    def serialize(self):
        return {
           "id":self.id,
           "caption":self.caption,
           "created_at":self.created_at,
           "user_id":self.user_id
        }
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
   
    #FK's:
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] =  mapped_column(ForeignKey("post.id"), nullable=False)

    #Relaciones:
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates= "comments")                                         
    

    def serialize(self):
        return {
           "id":self.id,
           "comment_text":self.comment_text,
           "created_at":self.created_at,
           "author_id":self.author_id,
           "post_id":self.post_id
        }
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)

    #FK's:
    post_id:Mapped[int] =  mapped_column(ForeignKey("post.id"), nullable=False)


    #Relaciones:
    post: Mapped["Post"] = relationship(back_populates= "media")  

    def serialize(self):
        return{
            "id":self.id,
            "type":self.type,
            "url":self.url,
            "post_id":self.post_id
        }

