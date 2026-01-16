#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW17
import random

#1. Create a def function that plays a single round of rock, paper, scissors where the user inputs
#1 for rock, 2 for paper, or 3 for scissors and compares it to a random number generated to serve
#as the "opponent's hand".
def rps():
    userInput = int(input("Enter 1 for rock, 2 for paper, 3 for scissors: "))
    opp = random.randint(1, 3)
    if opp == 1:
        print("Rock")
    elif opp == 2:
        print("Paper")
    else:
        print("Scissors")

    if userInput == opp:
        print("Tie")
    elif userInput > opp:
        print("You win")
    else:
        print("You lose")
    playAgain()


#2. Create a def function that prompts the user to input if they want to play another round, and
#repeats the RPS def function if they do or exits the code if they don't.
def playAgain():
    userPlay = input("Do you want to play again? (y/n): ")
    if userPlay == "y" or userPlay == "Y":
        rps()
    else:
        print("Thank you for playing")
rps()