import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class CompanyName(Base):
    __tablename__ = 'companyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="companyname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class ItemName(Base):
    __tablename__ = 'itemname'
    id = Column(Integer, primary_key=True)
    name = Column(String(370), nullable=False)
    description = Column(String(160))
    price = Column(String(24))
    feedback = Column(String(270))
    date = Column(DateTime, nullable=False)
    companynameid = Column(Integer, ForeignKey('companyname.id'))
    companyname = relationship(
        CompanyName, backref=backref('itemname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="itemname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'description': self. description,
            'price': self. price,
            'feedback': self. feedback,
            'date': self. date,
            'id': self. id
            }
engin = create_engine('sqlite:///cosmetics.db')
Base.metadata.create_all(engin)

# Database is created
