#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW6


#1. Import the "random" library
import random
#2. print "Hello World!"
print("Hello World")
#3. Create three different variables that each randomly generate an integer between 1 and 10
rando_1 = random.randint(1,10)
rando_2 = random.randint(1,10)
rando_3 = random.randint(1,10)
#4. Print the three variables from #3 on the same line.
print(rando_1, rando_2, rando_3)
#5. Add 2 to the first variable in #3, Subtract 4 from the second variable in #3, and multiply by 1.5 the third variable in #3.
added_rando = rando_1 + 2
sub_rando = rando_2 - 4
multi_rando = rando_3 * 1.5
#6. Print each result from #5 on the same line.
print(added_rando, sub_rando, multi_rando)
#7. Create a list containing four variables that each randomly generate an integer between 1 and 6
new_rando_1 = random.randint(1,6)
new_rando_2 = random.randint(1,6)
new_rando_3 = random.randint(1,6)
new_rando_4 = random.randint(1,6)
rando_list = [new_rando_1, new_rando_2, new_rando_3, new_rando_4]
#8. Sort the list in #7 and print it.
rando_list.sort()
print(rando_list)
#9. Add together the highest three numbers in the list from #7 and print the result.
rando_list.sort(reverse=True)
added_list = rando_list[0] + rando_list[1] + rando_list[2]
print(added_list)
#10. Create a list with 5 names of other students in this class and print the list.
name_list = ["Greg", "Kash", 'Brodie', 'Ethan', 'Tristan']
print(name_list)
#11. Shuffle the list in #10 and print the list again.
random.shuffle(name_list)
print(name_list)
#12. Print a random choice from the list of names from #10.
rando_choice = random.choice(name_list)
print(rando_choice)
