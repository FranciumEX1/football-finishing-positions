import pandas
import getLeagueData

worstPosition = {}
worstPosition["Team"] = []
worstPosition["Position"] = []

def getWorstPosition(fixtures, fullTable, topToBottomTeams):
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
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                    secondDict["Team"].append(value[1])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                elif (reachedTeam == value[1]) and (reachedTeam == teamName):
	                    secondDict["Team"].append(value[0])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                    secondDict["Team"].append(value[1])
	                    secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                #--------------------------------------------------------------------#
	                
	                if (reachedTeam != value[0]) and (reachedTeam != value[1]):
	                    if (value[0] in vincTeams and value[0] != teamName) and (value[1] not in vincTeams):
	                        secondDict["Team"].append(value[0])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                        secondDict["Team"].append(value[1])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                    elif (value[0] not in vincTeams) and (value[1] in vincTeams and value[1] != teamName):
	                        secondDict["Team"].append(value[0])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                        secondDict["Team"].append(value[1])
	                        secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                    elif (value[0] in vincTeams) and (value[1] in vincTeams):
	                        if (value[1] == teamName):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                        elif (value[0] == teamName):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                        elif (valueTwoPoints >= valueOnePoints) and (value[1] != teamName or value[0] != teamName):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])
	                        elif (valueTwoPoints < valueOnePoints) and (value[1] != teamName or value[0] != teamName):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0])
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0] + 3)
	                    elif (value[0] not in vincTeams) and (value[1] not in vincTeams):
	                            secondDict["Team"].append(value[0])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[0]].values[0] + 3)
	                            secondDict["Team"].append(value[1])
	                            secondDict["Points"].append(fullTable["Points"].loc[fullTable["Team"] == value[1]].values[0])

	    collectedTable = pandas.DataFrame(secondDict)
	    collectedTable = collectedTable.sort_values("Points", ascending=False)
	    print(teamName)
	    worstPosition["Team"].append(teamName)
	    collectedTable = collectedTable.drop_duplicates(subset="Team")
	    collectedTable = collectedTable.reset_index(drop=True)
	    samePoints = collectedTable["Points"].loc[collectedTable["Team"] == teamName].values[0]
	    currentTeamPos = collectedTable[collectedTable["Points"] == samePoints]
	    currentTeam = int(currentTeamPos[currentTeamPos["Team"] == teamName].iloc[0].name)
	    firstTeam = int(currentTeamPos.iloc[-1].name)
	    tTeam = collectedTable.iloc[firstTeam]
	    sTeam = collectedTable.iloc[currentTeam]
	    collectedTable.iloc[firstTeam] = sTeam
	    collectedTable.iloc[currentTeam] = tTeam
	    worstPosition["Position"].append(collectedTable.loc[collectedTable["Team"] == teamName].index.item() + 1)
	    secondDict = {}
	    secondDict["Team"] = []
	    secondDict["Points"] = []
	fullWorstTable = pandas.DataFrame(worstPosition)
	return fullWorstTable
