import plotly
from getLeagueData import getLeagueTable
from getLeagueData import getFixtures
from bestFinish import getBestPosition
from worstFinish import getWorstPosition
from plotly.graph_objs import Bar
from plotly.graph_objs import Layout
from plotly.graph_objs import Figure

LEAGUE_ROUND = 12

fixtures = getFixtures(LEAGUE_ROUND)
fullTable = getLeagueTable(LEAGUE_ROUND)
allTeams = fullTable["Team"]
fullWorstTable = getWorstPosition(fixtures, fullTable, allTeams)
fullBestTable = getBestPosition(fixtures, fullTable, allTeams)

fullWorstTable = fullWorstTable.sort_values("Position", ascending=False)
fullBestTable = fullBestTable.sort_values("Position", ascending=False)
finalTable = fullBestTable.merge(fullWorstTable, on="Team").sort_values("Position_x", ascending=False)
finalTable["BestToWorst"] = finalTable["Position_y"]-finalTable["Position_x"]

visualTablePlaces = Bar(
    y=fullTable["Team"],
    x=[(position if position != 0 else 0.5) for position in finalTable["BestToWorst"]],
    orientation="h",
    text=finalTable["Position_x"],
    textposition="inside",
    name="Current Position",
    insidetextanchor="start",
    base=finalTable["Position_x"],
    width=[0.8 for team in fullTable["Team"]],
    marker=dict(
        color="rgb(226, 230, 4)",
        opacity=0.4,
        line=dict(
            color="rgb(92, 92, 92)", 
            width=0.5
        )
    )
)

layout = Layout(
    paper_bgcolor="rgb(56, 56, 56)",
    plot_bgcolor="rgb(56, 56, 56)"
)
 
fullVisual = Figure(data=[visualTablePlaces], layout=layout)
fullVisual.update_layout(barmode='overlay', height=700, margin=dict(t=25), xaxis=dict(tickmode='array', tickvals=fullTable["Position"]))
fullVisual.update_xaxes(nticks=20, showgrid=False, tickfont=dict(family='Helvetica', color='yellow'))
fullVisual.update_yaxes(tickfont=dict(family="Helvetica", size=18, color="yellow"))
plotly.offline.plot(fullVisual)
