from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey

import os

Base = declarative_base()

class BuildingImage(Base):
	__tablename__ = 'building_image'

	# Attributes
	id = Column(Integer, primary_key=True)
	building_id = Column(Integer, ForeignKey('building.id'))
	url = Column(String(500), unique=True)
	byte_img = Column(LargeBinary)

	# Relationships
	building = relationship('Building', back_populates='images')
	
	def __init__(self, building_id=0, url= '', byte_img= b''):
		self.building_id = building_id
		self.url = url
		self.byte_img = byte_img

class Building(Base):
	__tablename__ = 'building'

	# Attributes
	id = Column(Integer, primary_key=True)
	url = Column(String(500), unique=True)
	name = Column(String(50))

	# Relationships
	images = relationship('BuildingImage', back_populates='building')
	
	def __init__(self, url="", name=""):
		 self.url = url
		 self.name = name

class Service(Base):
	__tablename__ = 'service'

	# Attributes
	building_id = Column(Integer, ForeignKey('building.id'), primary_key=True) 
	chat_id = Column(Integer)

	def __init__(self, building_id=0,chat_id=""):
		 self.building_id = building_id
		 self.chat_id = chat_id

from sqlalchemy import create_engine
engine = create_engine(os.environ['DATABASE_URL'])

from sqlalchemy.orm import sessionmaker
DBsession = sessionmaker()
DBsession.configure(bind=engine)
Base.metadata.create_all(engine)
