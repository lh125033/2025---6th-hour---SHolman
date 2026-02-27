#Name: Shane Holman
#Class: Darrow, Helldiver of Lykos, Reaper of Mars, the Slave King
#Assignment: Scenario 6

import random

#With a fresh perspective, the team lead wants you to look back and refactor the old combat code to
#be streamlined with classes so the character and enemy stats won't be built in bulky dictionaries anymore.


#(Translation: Rebuild Semester Project 1 using classes instead of dictionaries, include and refactor
#the combat test code below as well.)


class Stats:
    def __init__(self, health, initial, armor, atkm, damage,):
        self.health = health
        self.damage = damage
        self.initial = initial
        self.armor = armor
        self.atkm = atkm




LaeZel = Stats(48, 1, 17, 6,
               random.randint(1,6) + random.randint(1,6) + 3)
Shadowheart = Stats(40, 1, 18, 4, random.randint(1,6) + 3)
Gale = Stats(32, 1, 14, 6,
             random.randint(1, 6)+random.randint(1, 10))
Astarion = Stats(40, 3, 14, 6,
                 random.randint(1,10) + random.randint(1,10))



Goblin = Stats(7, 0, 12, 4, random.randint(1,6) + 2)
Orc = Stats(15, 1, 13, 5, random.randint(1,12)+3)
Troll = Stats(48, 1, 15, 7,
              random.randint(1,6) + random.randint(1,6) + 4)
Mindflayer = Stats(71, 1, 15, 7,
                   random.randint(1,10) + random.randint(1,10) + 4)
Dragon = Stats(127, 2, 18, 7,
               random.randint(1,10) + random.randint(1,10) + random.randint(1,8) + 4)





def initve():
    groll = random.randint(1,20) + Gale.initial
    oroll = random.randint(1,20) + Orc.initial
    if groll > oroll:
        print("Gale goes first")
        gattk()
    else:
        print("Orc goes first")
        oattk()


def gattk():
    while Gale.health > 0 or Orc.health > 0:
        GaleAccRoll = random.randint(1,20)
        if GaleAccRoll == 20:
            print(f"Gale hit and did double damage. Orc now has {Orc.health} hp")
            Orc.health -= Gale.damage * 2
        elif GaleAccRoll == 1:
            print("Gale missed")
        elif GaleAccRoll + Gale.atkm >= Orc.armor:
            Orc.health -= Gale.damage
            print(f"Gale hit and did damage. Orc now has {Orc.health} hp")
        else:
            print("Gale missed")


        if Gale.health <= 0 or Orc.health <= 0:
            print("Battle concluded")
            exit()
        else:
            oattk()



def oattk():
    while Gale.health > 0 or Orc.health > 0:
        OrcAccRoll = random.randint(1,20)
        if OrcAccRoll == 20:
            Gale.health -= Orc.damage * 2
            print(f"Orc hit and did double damage. Gale now has {Gale.health} hp")
        elif OrcAccRoll == 1:
            print("Orc missed")
        elif OrcAccRoll + Orc.atkm >= Gale.armor:
            Gale.health -= Orc.damage
            print(f"Orc hit and did damage. Gale now has {Gale.health} hp")
        else:
            print("Orc missed")


        if Gale.health <= 0 or Orc.health <= 0:
            print("Battle concluded")
            exit()
        else:
            gattk()



initve()