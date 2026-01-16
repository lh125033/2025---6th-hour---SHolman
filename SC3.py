#Name:
#Class: 6th Hour
#Assignment: SC3

#You have been transferred to a new team working on a mobile game that allows you to dress up a
#model and rate other models in a "Project Runway" style competition.

#They want to start prototyping the rating system and are asking you to make it.
#This prototype needs to allow the user to input the number of players, let each player rate
#a single model from 1 to 5, and then give the average score of all of the ratings.

player_sum = 0

playercount = int(input("How many players? "))
print(playercount)

for i in range(1, playercount + 1):
    vote = int(input("Place your vote for each, 1-5 "))
    vote_limit = 5
    if vote > vote_limit:
        print("Invalid score")
        break
    player_sum += vote

print(player_sum / playercount)







