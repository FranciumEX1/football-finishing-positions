import pandas
import getLeagueData

bestPosition = {}
bestPosition["Team"] = []
bestPosition["Position"] = []

def getBestPosition(fixtures, fullTable, topToBottomTeams):
	secondDict = {}
	secondDict["Team"] = []
	secondDict["Points"] = []
	for teamName in topToBottomTeams:
	    limit = fullTable["Points"].loc[fullTable["Team"] == teamName].values[0]     
	    reachers = pandas.DataFrame(fullTable[["Team", "Points", "GD"]].loc[(fullTable["Points"] >= (limit - 3)) & (fullTable["Points"] <= (limit + 3))].sort_values(
	        ["Points", "GD"], ascending=False))
	    restOfTheTable = pandas.DataFrame(fullTable[["Team", "Points", "GD"]].loc[(fullTable["Points"] < (limit - 3)) | (fullTable["Points"] > (limit + 3))].sort_values(
	        ["Points", "GD"], ascending=False))
	    vincTeams = reachers["Team"].tolist()	  
	    for reachedTeam in vincTeams:
	        for key, value in fixtures.items():
	            if (value[0] not in secondDict["Team"]) and (value[1] not in secondDict["Team"]): 
	                valueOnePoints = fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0]
	                valueTwoPoints = fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0]
	                if (reachedTeam == value[0]) and (reachedTeam == teamName):
	                    secondDict["Team"].append(value[0])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                    secondDict["Team"].append(value[1])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                elif (reachedTeam == value[1]) and (reachedTeam == teamName):
	                    secondDict["Team"].append(value[0])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                    secondDict["Team"].append(value[1])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                #--------------------------------------------------------------------#
	                
	                if (reachedTeam != value[0]) and (reachedTeam != value[1]):
	                    if (value[0] in vincTeams and value[0] != teamName) and (value[1] not in vincTeams):
	                        secondDict["Team"].append(value[0])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                        secondDict["Team"].append(value[1])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                    elif (value[0] not in vincTeams) and (value[1] in vincTeams and value[1] != teamName):
	                        secondDict["Team"].append(value[0])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                        secondDict["Team"].append(value[1])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                    elif (value[0] in vincTeams) and (value[1] in vincTeams):
	                        homeTeamPoints = fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0]
	                        awayTeamPoints = fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0]                    
	                        if (value[1] == teamName):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                        elif (value[0] == teamName):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                        elif (value[0] != teamName) and (value[1] != teamName):
	                            if (homeTeamPoints > limit) and (awayTeamPoints <= limit):
	                                secondDict["Team"].append(value[0])
	                                secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                                secondDict["Team"].append(value[1])
	                                secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                            elif (homeTeamPoints <= limit) and (awayTeamPoints > limit):
	                                secondDict["Team"].append(value[0])
	                                secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                                secondDict["Team"].append(value[1])
	                                secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                            else:
	                                secondDict["Team"].append(value[0])
	                                secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 1)
	                                secondDict["Team"].append(value[1])
	                                secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 1)
	                    elif (value[0] not in vincTeams) and (value[1] not in vincTeams):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 1)
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])

	    collectedTable = pandas.DataFrame(secondDict)
	    collectedTable = collectedTable.sort_values("Points", ascending=False)
	    print(teamName)
	    bestPosition["Team"].append(teamName)
	    collectedTable = collectedTable.drop_duplicates(subset="Team")
	    collectedTable = collectedTable.reset_index(drop=True)
	    samePoints = collectedTable["Points"].loc[collectedTable["Team"] == teamName].values[0]
	    currentTeamPos = collectedTable[collectedTable["Points"] == samePoints]
	    currentTeam = int(currentTeamPos[currentTeamPos["Team"] == teamName].iloc[0].name)
	    firstTeam = int(currentTeamPos.iloc[0].name)
	    tTeam = collectedTable.iloc[firstTeam]
	    sTeam = collectedTable.iloc[currentTeam]
	    collectedTable.iloc[firstTeam] = sTeam
	    collectedTable.iloc[currentTeam] = tTeam
	    bestPosition["Position"].append(collectedTable.loc[collectedTable["Team"] == teamName].index.item() + 1)
	    secondDict = {}
	    secondDict["Team"] = []
	    secondDict["Points"] = []	    
	fullBestTable = pandas.DataFrame(bestPosition)
	return fullBestTable
