import plotly
from getLeagueData import getLeagueTable
from getLeagueData import getFixtures
from bestFinish import getBestPosition
from worstFinish import getWorstPosition
from plotly.graph_objs import Bar
from plotly.graph_objs import Layout
from plotly.graph_objs import Figure


leagueRound = 9

fixtures = getFixtures(9)
fullTable = getLeagueTable(9)
allTeams = fullTable["Team"]
fullWorstTable = getWorstPosition(fixtures, fullTable, allTeams)
fullBestTable = getBestPosition(fixtures, fullTable, allTeams)

fullWorstTable = fullWorstTable.sort_values("Position", ascending=False)
fullBestTable = fullBestTable.sort_values("Position", ascending=False)

visualTablePlaces = Bar(
    y=fullTable["Team"],
    x=fullTable["Position"],
    orientation="h",
    text=fullTable["Position"],
    textposition="inside",
    name="Current Position",
    insidetextanchor="start",
    width=[0.8 for team in fullTable["Team"]],
    marker=dict(
        color="rgb(102, 168, 255)",
        opacity=0.4,
        line=dict(
            color="rgb(92, 92, 92)", 
            width=0.5
        )
    )
)

visualWorstPlaces = Bar(
    y=fullTable["Team"],
    x=fullWorstTable["Position"],
    orientation="h",
    text=fullWorstTable["Position"],
    textposition="inside",
    name="Worst Position",
    width=[0.9 for team in fullWorstTable["Team"]],
    marker=dict(
        color="rgb(230, 38, 34)",
        opacity=0.3,
        line=dict(
            color="rgb(92, 92, 92)", 
            width=0.5
        )
    )
)

visualBestPlaces = Bar(
    y=fullTable["Team"],
    x=fullBestTable["Position"],
    orientation="h",
    text=fullBestTable["Position"],
    textposition="inside",
    name="Best Position",
    width=[0.6 for team in fullBestTable["Team"]],
    marker=dict(
        color="rgb(136, 255, 0)",
        opacity=0.4,
        line=dict(
            color="rgb(92, 92, 92)", 
            width=0.5
        )
    )
)

layout = Layout(
    paper_bgcolor="rgb(255, 248, 196)",
    plot_bgcolor="rgb(255, 248, 196)"
)
 
fullVisual = Figure(data=[visualTablePlaces, visualWorstPlaces, visualBestPlaces], layout=layout)
fullVisual.update_layout(barmode='overlay', height=700, margin=dict(t=25))
fullVisual.update_xaxes(nticks=20, showgrid=False)
plotly.offline.plot(fullVisual)