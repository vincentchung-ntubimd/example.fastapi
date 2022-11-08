from sqlalchemy import TIMESTAMP, Column, Integer, Boolean, String, text, ForeignKey
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship
from database import Base

class ORM_Post(Base):
    __tablename__ = 'orm_posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("orm_users.id", ondelete="CASCADE"), nullable = False)

    owner = relationship("ORM_User")

class ORM_User(Base):
    __tablename__ = 'orm_users'
    id = Column(Integer, primary_key =True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )


class ORM_Vote(Base):
    __tablename__ = 'orm_votes'
    user_id =  Column(Integer, ForeignKey("orm_users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("orm_posts.id", ondelete="CASCADE"), primary_key=True)