import requests
import random
import time
import re
import unicodedata
from bs4 import BeautifulSoup

def delay(secs):
	time.sleep(random.randint(1,secs))

def uniclean(s):
	return unicodedata.normalize('NFKD',s).encode('ascii', 'ignore')

def getCoaches(gId,cData):
	managerTag = cData.find_all('a')
	#print (managerTag[0].string)

	homeManager = uniclean(managerTag[0].string)
	awayManager = uniclean(managerTag[1].string)

	coachesRow = '{0},{1},{2}\n'.format(gId, homeManager, awayManager)
	print coachesRow
	'''
	with open("game_managers.csv",'a') as f:
		f.write(coachesRow) '''

def getGoals(gId, gData, nGoals):
	goalRows = gData.find_all('tr')

	for i,row in enumerate(goalRows):
		if i>0:
			goal_data = row.find_all('td')
			for td in goal_data:
				if (td.find('b')!=None):
					partialScore = str(td.find('b').string)
					separator = partialScore.find(':')
					partialHome = partialScore[:separator-1]
					partialAway = partialScore[separator+2:]

				else:
					separator = td.contents[2].find('.')
					scoringMinute = td.contents[2][1:separator]

					scorerName = uniclean(td.find('a').string)
					if td.get('style')=='padding-left: 50px;':
						scoringTeam = "away"
					else:
						scoringTeam = "home"

			#if (int(scoringMinute) == 90) and (int(partialHome)+int(partialHome)==nGoals)





			print str(gId) + " -- " + scoringMinute + ". " + partialHome + " - " + partialAway + " / " + scorerName + " _" + scoringTeam





def getGameData(gameId, site, numGoals):
	delay(3)
	page = requests.get(site)
	soup = BeautifulSoup(page.content, 'html.parser')

	raw_report_data = soup.find_all("div", {"class": "box"})

	report_data = raw_report_data[0].find_all("table")

	goals_data = report_data[1]
	manager_data = report_data[5]

	#getCoaches(gameId,manager_data)

	if numGoals>0:
		getGoals(gameId,goals_data,numGoals)

	'''with open("matchReportTest.txt", 'w') as f:
		for i,itable in enumerate(report_data):
			f.write(str(itable.contents))
			f.write("\n ******************************** END TABLE {} \n".format(i))
			'''''



	#print str(len(report_data))
