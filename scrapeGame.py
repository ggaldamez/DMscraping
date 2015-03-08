import requests
import random
import time
import re
from bs4 import BeautifulSoup

def delay(secs):
	time.sleep(random.randint(1,secs))

def getGameData(gameId, site):
	delay(5)
	page = requests.get(site)
	soup = BeautifulSoup(page.content)
