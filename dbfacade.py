from models import BuildingImage, Building, Service
from datetime import datetime, timedelta
from pytz import timezone

from sqlalchemy.exc import IntegrityError

class DBFacade(object):

	@staticmethod
	def get_all_buildings(session):
		return session.query(Building).all()

	@staticmethod
	def add_building(session, building_url):
		new_building = Building(url= building_url)
		session.add(new_building)
		return new_building

	@staticmethod
	def add_building_images(session, building_id, building_image_list):
		new_images = []
		for image_url in building_image_list:
			#getimage:
			new_image = BuildingImage(building_id= building_id, url= image_url)
			new_images.append(new_image)
			session.add(new_image)
		return new_images

	@staticmethod
	def commit(session):
		session.commit()
