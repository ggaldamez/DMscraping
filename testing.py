from scrapeGame import *



def main():
	g1 = ['http://www.worldfootball.net/report/premier-league-1994-1995-manchester-city-tottenham-hotspur/',7]
	g2 = ['http://www.worldfootball.net/report/premier-league-1997-1998-leicester-city-manchester-united/',0]
	g3 = ['http://www.worldfootball.net/report/premier-league-2000-2001-arsenal-fc-charlton-athletic/',8]
	g4 = ['http://www.worldfootball.net/report/premier-league-2009-2010-manchester-united-manchester-city/',7]
	g5 = ['http://www.worldfootball.net/report/premier-league-2011-2012-blackburn-rovers-wolverhampton-wanderers/', 3]
	g6 = ['http://www.worldfootball.net/report/premier-league-2012-2013-manchester-city-aston-villa/',5]

	games = [g1,g2,g3,g4,g5,g6]
	#games = [g5]


	for i,game in enumerate(games):
		getGameData(i+1,game[0],game[1])


if __name__ == '__main__':
	main()