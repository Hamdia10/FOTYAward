#The purpose of this program is determine the winner Marist Student Government Association's (SGA)
#   Faculty of the Year Award using Ranked choice voting

#NOTE: This is currently a rough draft and still has some general issues that need to be debugged
#       by SGA's Chief Information Officer (CIO) and the Information Technology Council (ITC)
#
#HOW IT RUN: When writing this program I used Idle to run and test the program on my Windows Computer. Currently unsure how it will run on MAC
#            contact CIO if there are any issues.
#
#HOW IT WORKS:
#           Must install PANDAS on python inorder to run file
#
#           There are two custom made classes used for this program:
#                - Candidates : Holds stores a candidate's name, number of votes, a boolean determining wether the Candidate is still running
#                - UserVotes  : I need this class because I needed a means of keeping track of each individual user's vote along with the current
#                              valid index on the array. This is required because each User Vote could be pointing to a separate index. On each array 
#
#               When the program runs the idea is t sift through all of the columns of the excel file after the first round. Then depedening on which
#                   Canididate has the least amount of votes we count the UserVote's next pick on the next iteration. After a round of voting is complete
#                   a Canidate will be dropped and then the user votes that currently had the Candidate as their top pick will be recalculated on the next
#                   round. The program should end when there

#Current Issues: - Counts still need to be reset and generally debugged after each round of votes.
#                   Currently, the count is accumulated after each round per vote.
#
#               - Need to verify the logic with ITC
#
#               - Need to automate for various types of file
#                   Current implementation is bruteforced for this specific xlsx file.


import pandas as pd
from Candidate import Candidate
from UserVotes import UserVotes


def main():
    #For those downloading off of github make sure you 
    #EDIT THE FILE PATH linking to the votes xlsx file
    df = pd.read_excel(r'C:\Users\brian\Brian-Workspaces\sga-workspace\faculty-award\FOTYAward\votes.xlsx')
    #print(df)

    firstData = pd.DataFrame(df, columns=['First'])
    #Store the dataFrames values into an array
    firstPicks = firstData.values.tolist()
    #print(firstPicks)


    #init all Candidates
    candidateNames = ['Richard Forbes','Gary Jacobi','Donald Meltz',
                          'Glenn Tunstull']

    c0 = Candidate(str(candidateNames[0]),0, True)
    c1 = Candidate(str(candidateNames[1]),0, True)
    c2 = Candidate(str(candidateNames[2]),0, True)
    c3 = Candidate(str(candidateNames[3]),0, True)


    candidates = [c0, c1, c2, c3]
    allvotes = df.to_numpy()
    print(len(allvotes))

    #Create User Object Votes so we can keep track of each individual
    #   user's current valid vote

    voteObjs = [UserVotes() for _ in range(len(allvotes))]
    index = 0

    for index in range(len(allvotes)):
        voteObjs[index].picks = allvotes[index]

    
    
    colnumber = 0
    while colnumber < 3:
        for votes in voteObjs:
            for c in candidates:
                realVote = str(votes.picks[votes.topPickIndex])
                #print(realVote)
                #print(c.name)
                if c.isInRace == True:
                    if c.name == realVote:
                        c.votes = c.votes + 1
                else:
                    votes.topPickIndex=+1
                            
                #print(votes)

                    
        #DEBUGGING count votes after each round
        currMin = 10000000
        currLoser = Candidate("Loser",0,True)
        print("Round"+str(colnumber+1))
        for c in candidates:
            # 
            #If the previous pick was kicked out of the race
            #   AND the current pick is still in the race
            if c.isInRace == True:
                print(c.name+":"+str(c.votes))
                if currMin > c.votes:
                    currLoser = c

        currLoser.isInRace = False

        print("Dropped "+currLoser.name)
        
        colnumber = colnumber + 1
        print("---------------------------------------------------")


    print("---------------------------------------------------")
        
main()        

        


    
