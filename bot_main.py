#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telepot
import urllib3
import time
import re
import random
from bs4 import BeautifulSoup

from models import DBsession
from dbfacade import DBFacade

def handle(msg):
	pass


TOKEN = input()
query = 'https://www.idealista.com/areas/alquiler-viviendas/con-precio-hasta_900,pisos,de-dos-dormitorios,de-tres-dormitorios,amueblado_amueblados,publicado_ultimas-24-horas/?shape=%28%28y%7BuuFvxmUor%40yBeq%40%7BDaqAs%40aCajAnWQ%7Co%40hRKih%40aAeX%7DNiw%40kHrHe%5DvQ_e%40h%60%40k%5Cre%40iOwP%60L_%5DbP%7BRlSaO~f%40g%60%40fTq%5CoCal%40%7Cb%40q%5Dd%5D~vAlUtaBlSxo%40hl%40s%40uDjmA%29%29'
bot = telepot.Bot(TOKEN)
http = urllib3.PoolManager()
bot.message_loop(handle)

def request(uri):
	return http.request('GET', uri, headers={ 'User-Agent' : 'Mozilla/5.0' }).data

while 1:
	idealistaSplash = BeautifulSoup(request(query), 'html.parser')
	itemLinkList = idealistaSplash.find_all('a', class_= 'item-link')
	# TODO check if there are more links
	buildings = []  
	for itemLink in itemLinkList:
		buildingID = itemLink['href'].split('/')[-2] # '/inmueble/39379837/'.split('/') =>  ['', 'inmueble', '39379837', '']
		buildings.append( 'https://www.idealista.com/inmueble/' + buildingID)
	
	# Filter those that are not new
	session = DBsession()
	prev_buildings = []
	for building in DBFacade.get_all_buildings(session):
		prev_buildings.append(building.url)
	session.close()
	buildings = set(buildings) - set(prev_buildings)
	if len(buildings) > 0:
		print('Found new buildings')
	else:
		print('Not found new buildings')
	for building in buildings:
		buildingMainInfo = ''
		buildingTagsInfo = ''
		buildingHTML = str(request(building),'utf-8')
		# Main Info
		houseDescBS = BeautifulSoup(buildingHTML, 'html.parser')
		mainInfoHTML = houseDescBS.find_all('div', class_='main-info')
		if len(mainInfoHTML) > 0:
			buildingMainInfo = re.sub(' +', ' ', mainInfoHTML[0].text).rstrip(' ').lstrip(' ')
		# Info tags
		tagsInfoHTML = houseDescBS.find_all('div', class_='info-tags')
		if len(tagsInfoHTML) > 0:
			buildingTagsInfo = re.sub(' +', ' ', tagsInfoHTML[0].text).rstrip(' ').lstrip(' ')
		# Contact number or email
		
		# Image List
		# TO DO: download and combine all images in one via converting to same width
		pattern = 'data-service="([^"]*)'
		imgItems = re.finditer(pattern, buildingHTML)
		imgs = []
		for img in imgItems:
			imgs.append(img.group(1)[:-11])
		message = buildingMainInfo + '\n' + buildingTagsInfo + '\n' + building
		bot.sendMessage(os.environ['TELEGRAM_CHAT_ID'], message)
		session = DBsession()
		new_building = DBFacade.add_building(session, building)
		DBFacade.commit(session) # id created for new_building
		DBFacade.add_building_images(session, new_building.id, imgs)
		DBFacade.commit(session)
		session.close()

	sleepTime = random.randint(360,720)
	print('Going to sleep for', sleepTime, 'seconds.')
	time.sleep(sleepTime)
