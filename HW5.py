#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW5


#1. Create a list with 9 different numbers inside.
number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#2. Sort the list from highest to lowest.
number_list.sort(reverse=True)
#3. Create an empty list.
empty_list = []
#4. Remove the median number from the first list and add it to the second list.
holder_var = number_list[4]
number_list.pop(4)
empty_list.append(holder_var)
#5. Remove the first number from the first list and add it to the second list.
holder_var2 = number_list[0]
number_list.pop(0)
empty_list.append(holder_var2)
#6. Print both lists.
print(number_list)
print(empty_list)
#7. Add the two numbers in the second list together and print the result.
add_sum = empty_list[0] + empty_list[1]
print(add_sum)
#8. Move the number back to the first list (like you did in #4 and #5 but reversed).
empty_list.pop(0)
empty_list.pop(0)
number_list.append(add_sum)
#9. Sort the first list from lowest to highest and print it.
number_list.sort()
print(number_list)