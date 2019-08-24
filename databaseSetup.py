from sqlalchemy import Column,ForeignKey,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#Tables

#Users Table
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    email = Column(String(250),nullable = False)
    name = Column(String(250),nullable = False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'name'      : self.name,
            'email'     : self.email
        }

#Categories Table
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(30))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'name'      : self.name,
            'createdBy' : self.user.name
        }

#Items Table
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer,primary_key = True)
    name = Column(String(250))
    description = Column(String(250))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)

    @property    
    def serialize(self):
        return{
            'name'          : self.name,
            'description'   : self.description,
            'category'      : self.category.name,
            'createdBy'     : self.user.name
        }


#Configuration
engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.create_all(engine) 