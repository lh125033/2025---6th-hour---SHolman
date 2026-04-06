#Name:
#Class: 6th Hour Cassius Bellona Morning Knight of the Republic, Mentor to Lysander au Lune, Brother to Darrow of Lykos, Fear Killer, Deceased Killed by Lysander au Lune
#Assignment: HW-R5

#1. Fix the "class" comment at the top to "6th Hour"

#2. Create a list of the names of all the students in the classroom.
Name_List= ["Connor", "Devon", "Alaya", "Shane", "Ally", "Tristan","Ethan", "Greg"]
#3. Create a for loop that prints the names of every student in the list.
for i in Name_List:
    print(i)
#4. Using the "in" operator (hint: Google), create a for loop that only prints
#the name of a student if the letter "e" is in it.
print("These Students have an 'e' or 'E' in their name")
for j in Name_List:
    if "e" in j or "E" in j:
        print(j)