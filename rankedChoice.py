import pyrankvote
import pandas as pd
import numpy as np
from pyrankvote import Candidate, Ballot

numOfChoices = 3

resultsFile = pd.read_csv("C:/Users/brian/Brian-Workspaces/sga-workspace/faculty-award/misc/sample-votes.csv")
resultsFile = resultsFile.drop(['Timestamp'], axis=1)

allCandidatesWithDupes = pd.concat([resultsFile['First'], resultsFile['Second'], resultsFile['Third']])#, resultsFile['Fourth'], resultsFile['Fifth']])

uniqueCandidates = allCandidatesWithDupes.unique()

for i in range(0, uniqueCandidates.__len__()):
    if(pd.isna(uniqueCandidates[i])):
        uniqueCandidates = np.delete(uniqueCandidates, i)

# CANDIDATES
candidates = []

for i in range(0, uniqueCandidates.__len__()):
    candidates.append(Candidate(uniqueCandidates[i]))

# BALLOTS
ballots = []

ballotEnd = 0

for i in range(0, resultsFile.size):
    try:
        resultsFile.iloc[i]
        ballotEnd += 1
    except IndexError as e:
        break

for i in range(0, ballotEnd):
    ballotEntry = resultsFile.iloc[i]
    newBallotEntry = []
    for x in range(0, numOfChoices):
        if(not pd.isna(ballotEntry.iat[x]) and x == numOfChoices - 1):
            for j in range(0, ballotEntry.size):
                if(Candidate(ballotEntry.iat[j]) in newBallotEntry):
                    break
                else:
                    newBallotEntry.append(Candidate(ballotEntry.iat[j]))
            ballots.append(Ballot(ranked_candidates = newBallotEntry))
            break
        if(pd.isna(ballotEntry.iat[x])):
            ballotEntry = ballotEntry[0:x]
            for j in range(0, ballotEntry.size):
                if(Candidate(ballotEntry.iat[j]) in newBallotEntry):
                    break
                else:
                    newBallotEntry.append(Candidate(ballotEntry.iat[j]))
            ballots.append(Ballot(ranked_candidates = newBallotEntry))
            break

# You can use your own Candidate and Ballot objects as long as they implement the same properties and methods
election_result = pyrankvote.instant_runoff_voting(candidates, ballots)

winners = election_result.get_winners()
# Returns: [<Candidate('Al Gore (Democratic)')>]

print(election_result)
