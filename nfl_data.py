#!python

import nflgame
import pandas as pd
from pandas import Series

games = nflgame.games(2018)

# Convert the current season to a pandas dataframe so it's easy to work with
game_results = pd.DataFrame(games)
print(game_results)

# Define this dictionary outside the loop so we can access it in a non iterative context
# It is a composed of lists for values, with the matchup as it's key
matchups = {}


# This creates the index for our dataframe. In this case it is team matchups for a given game. (Away-Home)
# This API returns game objects with information about the game stored as attributes i.e. game.away, game.score_home.
for game in games:
	# Convert the names to strings if they aren't and combine them for our matchup
	matchup = str(game.away)+'-'+str(game.home)
	print(matchup)
	print('\n')

	# This a key value pair we will use to store the absolute scoring differential
	# It contains the same index we created above in order to easily insert it later with the winning team's abbriviation
	winner = game.home if game.score_home >= game.score_away else game.away
	loser = game.home if game.score_home < game.score_away else game.away

	matchups[matchup] = [(abs(game.score_home-game.score_away)), str(winner),str(loser)]
print(matchups)


# Create our columns as they appeared initially in the gsheet (alphabetical order) then point diferential
# We are also adding that index we just created to the same dataframe that includes our desired columns
export_list = pd.DataFrame(index=pd.Index(matchups.keys()),columns=['ARI','ATL','BAL','BUF','CAR','CHI','CIN','CLE','DAL','DEN','DET','GB','HOU','IND','JAX','KC','LAC','LAR','MIA','MIN','NE','NO','NYG','NYJ','OAK','PHI','PIT','SEA','SF','TB','TEN','WAS','point_diff'])



# Fancy logic to decide when to mark a team as winner/loser
for index, row in export_list.iterrows():
	for name, column in row.iteritems():
		name = str(name)

		if name == str(matchups[index][1]) and int(matchups[index][0]) > 0:
			export_list.loc[index,name] = 1

		elif int(matchups[index][0]) == 0:
			teams = index.split("-")
			if name == teams[0] or name == teams[1]:
			 	export_list.loc[index,name] = 1

			else:
				export_list.loc[index,name] = 0

		elif name == str(matchups[index][2]):
			export_list.loc[index,name] = -1

		else:
			export_list.loc[index,name] = 0
	export_list.loc[index,'point_diff'] = matchups[index][0]


export_list.to_csv('NFL_2018_19.csv')

