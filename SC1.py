#Name: Shane Holman
#Class: 6th Hour
#Assignment: Scenario 1

#Scenario 1:
#You are a programmer for a fledgling game developer. Your team lead has asked you
#to create a nested dictionary containing five enemy creatures (and their properties)
#for combat testing. Additionally, the testers are asking for a way to input changes
#to the enemy's damage values for balancing, as well as having it print those changes
#to confirm they went through.

#It is up to you to decide what properties are important and the theme of the game.

enemies_dict = {
    "Slime" : {
        "Health" : 5,
        "Damage" : 2,
        "Speed" : 3
    },
    "Goblin" : {
        "Health" : 10,
        "Damage" : 15,
        "Speed" : 12
    },
    "Skeleton" : {
        "Health" : 50,
        "Damage" : 25,
        "Speed" : 20
    },
    "Arch Angel" : {
        "Health" : 500,
        "Damage" : 300,
        "Speed" : 400
    },
    "God" : {
        "Health" : 1000000,
        "Damage" : 20000,
        "Speed" : 300500
    },
}
user_input = input("Slime, Goblin, Skeleton, Arch Angel, God: ")
print(enemies_dict[user_input])
enemies_dict[user_input].update({"Damage" : int(input("Change damage "))})
print(enemies_dict[user_input])


