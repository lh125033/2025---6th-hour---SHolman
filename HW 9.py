#Name:Shane Holman
#Class: 6th Hour
#Assignment: HW9

import random
#1. Print "Hello World!"
print("Hello World!")
#2. Create a list with three variables that each randomly generate a number between 1 and 100
rando_list = [random.randint(1, 100) for _ in range(3)]
#3. Print the list.
print(rando_list)
#4. Create an if statement that determines which of the three numbers is the highest and prints the result.
max_value = rando_list[0]

for i in range(1, len(rando_list)):
    if rando_list[i] > max_value:
        max_value = rando_list[i]

print("The largest out of the three is", max_value)
#5. Tie the result (the largest number) from #4 to a variable called "num".
num = max_value
#6. Create a nested if statement that prints if num is divisible by 2, divisible by 3, both, or neither.
print(num)

if num % 2 == 0:
    if num % 3 == 0:
        print("Is divisible by 2 and 3")
    else:
        print("Is divisible by 2 but not 3")
else:
    if num % 3 == 0:
        print("Is divisible by 3 but not 2")
    else:
        print("Is divisible by neither")



