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

def getCoaches(gId,cData, cData2):
	#print(cData)
	managerCell = cData.find_all('th')
	managers = []

	if len(managerCell) == 0:
		managerCell = cData2.find_all('th')

	for i, cell in enumerate(managerCell):
		manTag = cell.find('a')
		#print manTag
		if manTag != None:
			managers.append(manTag.contents[0])
		else:
			managers.append(u'Unknown')
	#print (managerTag[0].string)
	#print managers
	#print type(managers[0])
	#print type(managers[1])

	homeManager = uniclean(managers[0])
	awayManager = uniclean(managers[1])

	coachesRow = '{0},{1},{2}\n'.format(gId, homeManager, awayManager)
	#print coachesRow

	with open("game_managers.csv",'a') as f:
		f.write(coachesRow)

def getGoals(gId, gData, nGoals):
	goalRows = gData.find_all('tr')

	with open("goals.csv",'a') as f:
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

				if scoringTeam == "away":
					goalDiff = int(partialAway) - int(partialHome)
				else:
					goalDiff = int(partialHome) - int(partialAway)

				if (int(scoringMinute) == 90) and (int(partialHome)+int(partialAway)==nGoals) and (goalDiff<2):
					pointEarner = "yes"
				else:
					pointEarner = "no"
				#print scoringMinute + " " + str(int(partialHome)+int(partialAway)) + " (" + str(nGoals)+ ") " + str(goalDiff)
				printRow = '{},{},{},{},{},{},{},{}\n'.format(gId, scoringMinute, scoringTeam, scorerName, partialHome, partialAway, goalDiff, pointEarner)
				#print printRow
				f.write (printRow)






def getGameData(gameId, site, numGoals):
	delay(4)
	page = requests.get(site)
	soup = BeautifulSoup(page.content, 'html.parser')
	print "processing match number " + str(gameId)
	raw_report_data = soup.find_all("div", {"class": "box"})

	report_data = raw_report_data[0].find_all("table")

	goals_data = report_data[1]
	manager_data = report_data[5]
	manager_data_secondary = report_data[6]

	getCoaches(gameId,manager_data, manager_data_secondary)

	if numGoals>0:
		getGoals(gameId,goals_data,numGoals)

	'''with open("matchReportTest.txt", 'w') as f:
		for i,itable in enumerate(report_data):
			f.write(str(itable.contents))
			f.write("\n ******************************** END TABLE {} \n".format(i))
			'''''



	#print str(len(report_data))
