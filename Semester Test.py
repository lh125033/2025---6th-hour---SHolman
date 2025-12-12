# Name:
# Class: 6th Hour
# Assignment: Semester Project 1

import random
import time

# Due to weird time travelling circumstances beyond explanation, you find yourself in 2018 or so
# working for Larian Studios. Currently, they are working on the early prototypes of the hype
# upcoming game "Baldur's Gate 3". BG3 is a game that uses the Dungeons & Dragons 5th edition rules
# as its framework for gameplay. You have been given a basic dictionary of some of the main hero
# characters and some of the enemies they may face, and are tasked with making an early prototype
# of one of the party members fighting against an enemy until one of them hits zero HP (dies).

partyDict = {
    "LaeZel": {
        "HP": 48,
        "Init": 1,
        "AC": 17,
        "AtkMod": 6,
        "Damage": random.randint(1, 6) + random.randint(1, 6) + 3
    },
    "Shadowheart": {
        "HP": 40,
        "Init": 1,
        "AC": 18,
        "AtkMod": 4,
        "Damage": random.randint(1, 6) + 3,
    },
    "Gale": {
        "HP": 32,
        "Init": 1,
        "AC": 14,
        "AtkMod": 6,
        "Damage": random.randint(1, 10) + random.randint(1, 10),
    },
    "Astarion": {
        "HP": 40,
        "Init": 3,
        "AC": 14,
        "AtkMod": 5,
        "Damage": random.randint(1, 8) + random.randint(1, 6) + 4,
    }
}

enemyDict = {
    "Goblin": {
        "HP": 7,
        "Init": 0,
        "AC": 12,
        "AtkMod": 4,
        "Damage": random.randint(1, 6) + 2
    },
    "Orc": {
        "HP": 15,
        "Init": 1,
        "AC": 13,
        "AtkMod": 5,
        "Damage": random.randint(1, 12) + 3
    },
    "Troll": {
        "HP": 84,
        "Init": 1,
        "AC": 15,
        "AtkMod": 7,
        "Damage": random.randint(1, 6) + random.randint(1, 6) + 4
    },
    "Mindflayer": {
        "HP": 71,
        "Init": 1,
        "AC": 15,
        "AtkMod": 7,
        "Damage": random.randint(1, 10) + random.randint(1, 10) + 4
    },
    "Dragon": {
        "HP": 127,
        "Init": 2,
        "AC": 18,
        "AtkMod": 7,
        "Damage": random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 8) + 4
    },
}

# Combat consists of these steps:

# 1. Rolling for 'initiative' to see who goes first. This is determined by rolling a
# 20-sided die (d20) and adding their initiative modifier (If the roll is the same,
# assume the hero goes first).

#There are quiet a few redundant lines and things of a similar nature, however I fear removing them.

gMove = False
tMove = True

iroll1 = random.randint(1, 20) + partyDict["Gale"]["Init"]
iroll2 = random.randint(1, 20) + enemyDict["Troll"]["Init"]

if iroll1 > iroll2:
    gMove = True
    print(f"Gale rolled {iroll1}, and goes first.")
    print(f"Troll rolled {iroll2}, and goes last")
else:
    tMove = True
    print(f"Troll rolled {iroll2}, and goes first.")
    print(f"Gale rolled {iroll1}, and goes last.")

# 2. Rolling to attack. This is determined by rolling a 20-sided die (d20) and adding their
# attack modifier. The attack hits if it matches or is higher than the target's Armor Class (AC).
# If the d20 rolled to attack is an unmodified ("natural") 20, the attack automatically hits and
# the character deals double damage. If the d20 rolled to attack is an unmodified ("natural") 1,
# the attack automatically misses


gHP = partyDict["Gale"]["HP"]
gAC = partyDict["Gale"]["AC"]
gDMG = partyDict["Gale"]["Damage"]
gMOD = partyDict["Gale"]["AtkMod"]

tHP = enemyDict["Troll"]["HP"]
tAC = enemyDict["Troll"]["AC"]
tDMG = enemyDict["Troll"]["Damage"]
tMOD = partyDict["Gale"]["AtkMod"]

while gHP >= 0 or tHP >= 0:

    gNat = random.randint(1, 20)
    gMODROLL = gNat + gMOD
    tNat = random.randint(1, 20)
    tMODROLL = tNat + tMOD

    if gMove == True:
        if gHP <= 0:
            print(f"Gale was killed")
            break
    if tMove == True:
        if tHP <= 0:
            print(f"Gale killed the Troll")
            break

    if tMove == True:
        if tNat == 20:
            gHP -= tDMG * 2
            print(f"The Troll rolled a natural 20, and did {tDMG * 2} damage. Gale now has {gHP} HP.")
            tNat == 0
            tDMG == 0
            tMove = False
            gMove = True
            if gHP <= 0:
                print(f"Gale was killed")
                break

    if tMove == True:
        if tNat == 1:
            print("The Troll rolled a natural 1, and missed the attack.")
            tNat == 0
            tDMG == 0
            tMove = False
            gMove = True
            if gHP <= 0:
                print(f"Gale was killed")
                break

    if gMove == True:
        if gNat == 20:
            tHP -= gDMG * 2
            print(f"Gale rolled a natural 20, and did {gDMG * 2} damage. The Troll now has {tHP} HP.")
            gNat == 0
            gDMG == 0
            gMove = False
            tMove = True
            if tHP <= 0:
                print(f"Gale killed the Troll")
                break

    if gMove == True:
        if gNat == 1:
            print("Gale rolled a natural 1, and missed the attack.")
            gNat == 0
            gDMG == 0
            gMove = False
            tMove = True
            if tHP <= 0:
                print(f"Gale killed the Troll")
                break

    if tMove == True:
        if tMODROLL < 10:
            print(f"The Troll rolled a modified {tMODROLL}, and missed. Gale has {gHP} HP.")
            tNat == 0
            tDMG == 0
            tMove = False
            gMove = True
            if gHP <= 0:
                print(f"Gale was killed")
                break

        if tMove == True:
            if tDMG < gAC:
                print(
                    f"The Troll tried to deal {tDMG} damage, but can't break through the Gale's armor class of {gAC}.")
                tNat == 0
                tDMG == 0
                gMove = True
                tMove = False
                if gHP <= 0:
                    print(f"Gale was killed")
                    break

        if tMove == True:
            if tDMG > gAC:
                gHP -= tDMG
                print(f"The Troll broke through the Gale's armor, and dealt {tDMG} damage. Gale now has {gHP} HP.")
                tNat == 0
                tDMG == 0
                gMove = True
                tMove = False
                if gHP <= 0:
                    print(f"Gale was killed")
                    break

    if gMove == True:
        if gMODROLL < 10:
            print(f"Gale rolled a modified {gMODROLL}, and missed. The Troll has {tHP} HP.")
            gNat == 0
            gDMG == 0
            gMove = False
            tMove = True
            if tHP <= 0:
                print(f"Gale killed the Troll")
                break

        if gMove == True:
            if gDMG < tAC:
                print(f"Gale tried to deal {gDMG} damage, but can't break through the Troll's armor class of {tAC}.")
                gNat == 0
                gDMG == 0
                gMove = False
                tMove = True
                if tHP <= 0:
                    print(f"Gale killed the Troll")
                    break

        if gMove == True:
            if gDMG > tAC:
                tHP -= gDMG
                print(f"Gale broke through the Troll's armor, and dealt {gDMG} damage. The Troll has {tHP} HP.")
                gNat == 0
                gDMG == 0
                gMove = False
                tMove = True
                if tHP <= 0:
                    print(f"Gale killed the Troll")
                    break

    if gHP <= 0:
        print(f"Gale was killed")
        break
    elif tHP <= 0:
        print(f"Gale killed the Troll")
        break