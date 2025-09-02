#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW4


#1. Print Hello World!
print("Hello World!")
#1. Create a list with 5 strings containing 5 different names in it.
name_list = ["Washita", "Brook", "Camden", "Kansa", "Aberalter"]
#2. Append a new name onto the Name List.
name_list.append("Case")
#3. Print out the 4th name on the list.
print(name_list[3])
#4. Create a list with 4 different integers in it.
numbered_list = [67, 16165, 4657, 1]
#5. Insert a new integer into the 2nd spot and print the new list.
numbered_list.insert(1, 4)
#6. Sort the list from lowest to highest and print the sorted list.
numbered_list.sort()
print(numbered_list)
#7. Add the 1st three numbers on the sorted list together and print the sum.
numbered_list[0] + numbered_list[1] + numbered_list[2]
print(sum(numbered_list))
#8. Create a list with two strings, two variables, and too boolean values.
varied_list =  ["Sinatra", "Blue", numbered_list, name_list, True, False]
#9. Create a print statement that asks the user to input their own index value for the list on #8.
print(varied_list[int(input("What do you want? 0 - 7 "))])
