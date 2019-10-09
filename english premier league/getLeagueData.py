import requests
from bs4 import BeautifulSoup
import pandas

def getLeagueTable(leagueRound):
	leagueDict = {}
	leagueDict["Position"] = []
	leagueDict["Team"] = []
	leagueDict["Played"] = []
	leagueDict["Won"] = []
	leagueDict["Draw"] = []
	leagueDict["Loss"] = []
	leagueDict["GF"] = []
	leagueDict["GA"] = []
	leagueDict["GD"] = []
	leagueDict["Points"] = []
	columnCount = 0

	columnLooker = [
    "Position", "Team", "Played", "Won", "Draw", 
    "Loss", "GF", "GA", "GD", "Points"
	]

	rawPageTableData = requests.get("https://en.wikipedia.org/wiki/2019%E2%80%9320_Premier_League")
	scrapedTablePage = BeautifulSoup(rawPageTableData.text, "html.parser")
	leagueTable = scrapedTablePage.find_all("table", {"class": "wikitable"})

	rawFixtureData = requests.get("https://www.worldfootball.net/schedule/eng-premier-league-2019-2020-spieltag/{}/".format(leagueRound))
	scrapedFixtureData = BeautifulSoup(rawFixtureData.text, "html.parser")
	fixtureTable = scrapedFixtureData.find("table", {"class": "standard_tabelle"})

	for tableRows in leagueTable[3].find_all("tr"):
	    columnCount = 0
	    for tableData in tableRows.find_all(["th", "td"]):
	        if tableData.get("rowspan") is None and tableData.get("scope") != "col":
	            element = tableData.text
	            if columnLooker[columnCount] == "Team": # or columnLooker[columnCount] == "GD" or columnLooker[columnCount] == "Points":
	                leagueDict[columnLooker[columnCount]].append(str(element.replace("\n", "")))
	                columnCount = columnCount + 1
	            else:
	                singleElement = element.replace("\n", "")
	                singleElement = element.replace("+", "")
	                singleElement = element.replace("−", "")
	                leagueDict[columnLooker[columnCount]].append(int(singleElement))
	                columnCount = columnCount + 1
	fullTable = pandas.DataFrame(leagueDict)
	fullTable = fullTable.sort_values("Position", ascending=False)
	return fullTable

def getFixtures(leagueRound):
	fixtures = {"Match 1": [], "Match 2": [], "Match 3": [], "Match 4": [], "Match 5": [],
	"Match 6": [], "Match 7": [], "Match 8": [], "Match 9": [], "Match 10": []}

	rawPageTableData = requests.get("https://en.wikipedia.org/wiki/2019%E2%80%9320_Premier_League")
	scrapedTablePage = BeautifulSoup(rawPageTableData.text, "html.parser")
	leagueTable = scrapedTablePage.find_all("table", {"class": "wikitable"})

	rawFixtureData = requests.get("https://www.worldfootball.net/schedule/eng-premier-league-2019-2020-spieltag/{}/".format(leagueRound))
	scrapedFixtureData = BeautifulSoup(rawFixtureData.text, "html.parser")
	fixtureTable = scrapedFixtureData.find("table", {"class": "standard_tabelle"})

	matchCounter = 1
	for tableRow in fixtureTable.find_all("tr"):
	    tableData = tableRow.find_all("td")
	    firstTeam =  tableData[2].text
	    secondTeam = tableData[4].text
	    if "AFC" not in firstTeam:
	        firstTeam = firstTeam.replace("FC", "")
	        firstTeam = firstTeam.replace("\n", "")
	        firstTeam = firstTeam.strip()
	    if "AFC" not in secondTeam:
	        secondTeam = secondTeam.replace("FC", "")
	        secondTeam = secondTeam.replace("\n", "")
	        secondTeam = secondTeam.strip()
	    if "AFC" in firstTeam:
	        firstTeam = firstTeam.replace("AFC", "")
	        firstTeam = firstTeam.replace("\n", "")
	        firstTeam = firstTeam.strip()
	    if "AFC" in secondTeam:
	        secondTeam = secondTeam.replace("AFC", "")
	        secondTeam = secondTeam.replace("\n", "")
	        secondTeam = secondTeam.strip()
	    fixtures["Match {}".format(matchCounter)].append(firstTeam)
	    fixtures["Match {}".format(matchCounter)].append(secondTeam)
	    matchCounter = matchCounter + 1
	return fixtures