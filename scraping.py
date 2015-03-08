import requests
import random
import re
from scrapeGame import *
from bs4 import BeautifulSoup


def processGameRow(gameData, prevDate, roundNo, gameNo):
	baseURL='http://www.worldfootball.net'
	# get the date
	if str(gameData[0].string) != 'None':
		somedate = gameData[0].string
	else:
		somedate = prevDate

	#save the date somewhere


	# get home team
	hometeam = str(gameData[2].string)

	# get away team
	awayteam = str(gameData[4].string)

	# process scores
	rawscore = gameData[5].find_all("a")
	scoretext = str(rawscore[0].string)

	halfSeparator = scoretext.find(' ')
	finalScore = scoretext[:halfSeparator]
	fullSeparator = finalScore.find(':')
	homeScore = finalScore[:fullSeparator]
	awayScore = finalScore[fullSeparator+1:]

	# get game report url

	detailslink = baseURL + str(rawscore[0]["href"])

	print (str(gameNo) + " - " + str(roundNo) + "\t" + somedate +"\t" +  hometeam +"\t" +  awayteam + "\t" + homeScore + "\t" + awayScore + "\t" + detailslink)
	return somedate



def main():

	seasonURLs = []
	initialYear = 1992
	finalYear = 1993

	counter = initialYear
	globalGameNo = 1

	while counter<=finalYear:
		url = 'http://www.worldfootball.net/all_matches/eng-premier-league-{0:d}-{1:d}/'.format(counter,counter+1)
		seasonURLs.append(url)
		counter = counter+1

	for address in seasonURLs:
		page = requests.get(address)
		seasonYears =  address[-10:-1]
		print "processing " + seasonYears
		saveFileName = r'games/{0}.txt'.format(seasonYears)
		soup = BeautifulSoup(page.content, 'html.parser')
		delay(5)
		#soup = BeautifulSoup(open("season.htm"), 'html.parser')

		#print soup.prettify()

		season_data = soup.find_all("div", {"class": "box"})
		#print type(season_data[0])


		rows = season_data[0].find_all("tr")
		gameDate =''
		roundNumber = ''

		with open(saveFileName,'w') as f:
			for i,tr in enumerate(rows):
				'''
				if (i>25):
					break
				'''
				dataCells = tr.find_all("td")
				if (len(dataCells)>0):
					#print ("\t there is game data here")
					gameDate = processGameRow(dataCells,gameDate,roundNumber, globalGameNo)
					globalGameNo += 1
				else:
					roundLink = tr.find_all("a")
					rawRound = str(roundLink[0].string)
					roundNumber = rawRound[:rawRound.find('.')]
					#print str(roundLink[0].string) + " -- " + str(roundLink[0]["href"])



				'''
				for cell in tr.contents:
					f.write(str(cell))
					f.write("\n*\t*\t*\n")
				f.write("\n**  **  **  ** END tr lookup**  **  **  **\n")
				#f.write()
				# if len(tr.find_all("th"))>0:
				# 	print tr.contents
				# else:
				# 	print "--results here"



	#for item in season_data:
	#	print item.contents

	'''

if __name__ == '__main__':
  main()