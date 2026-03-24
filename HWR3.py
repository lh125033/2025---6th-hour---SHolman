#Name: Shane Holman
#Class: Virgina au Augustus, Mustang, Imperator of House Artemis, Sovereign of the Republic, Wife to Darrow of Lykos, Mother to Pax
#Assignment: HW-R3


#1. import random and print "Hello World!"
import random
print("Hello World!")
#2. Create three variables that each randomly generate an integer between 1 and 10, print each number on the same line.
Rando_1 = random.randint(1, 10)
Rando_2 = random.randint(1, 10)
Rando_3 = random.randint(1, 10)
print(Rando_1, Rando_2, Rando_3)
#3. Create a list containing 5 strings listing 5 colors.
Color_list = ["Gold", "Silver", "Copper", "Grey", "Red"]
#4. Use a function to randomly choose one of the 5 colors from the list and print the result.
print(random.choice(Color_list))
#5. Create an if statement that determines which of the three variables from #2 is the lowest.
if Rando_1 < Rando_2 and Rando_1 < Rando_3:
    print(f"{Rando_1} is the lowest")
elif Rando_2 < Rando_1 and Rando_2 < Rando_3:
    print(f"{Rando_2} is the lowest")
else:
    print(f"{Rando_3} is the lowest")