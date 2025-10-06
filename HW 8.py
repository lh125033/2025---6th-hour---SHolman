#Name:Shane Holman
#Class: 6th Hour
#Assignment: HW8
import random
#1. Print "Hello World!"
print("Hello World!")
#2. Create 3 variables that each randomly generate a number between 1 and 10, named A, B, and C.
var_A = random.randint(1, 10)
var_B = random.randint(1, 10)
var_C = random.randint(1, 10)

#3. Print A, B, and C on the same line.
print(var_A, var_B, var_C)
#4. Make an if statement that prints if variable A is greater than, less than, or equal to 5.
if var_A > 5:
    print(var_A, "is greater than 5")
elif var_A < 5:
    print(var_A, "is less than 5")
else:
    print(var_A, "is equal to 5")
#5. Make an if statement that prints if variable B is between 3 and 7, or not.
if var_B >= 3 and var_B <= 7:
    print(var_B, "is between 3 and 7")
else:
    print(var_B, "is not between 3 and 7")
#6. Make an if statement that prints if variable C is even or odd.
if var_C % 2 == 0:
    print(var_C, "is even")
else:
    print(var_C, "is odd")
#7. Create a variable whose value is 3 + a randomly generated number between 1 and 20
var_rando = 3 + random.randint(1, 20)
print(var_rando)
#8. Make an if statement that prints if the variable from #7 is greater than, less than, or equal to A + B + C.
added_var = var_A + var_B + var_C
if added_var > var_rando:
    print(added_var, "is greater than", var_rando)
if added_var < var_rando:
    print(added_var, "is less than", var_rando)
else:
    print(added_var, "is equal to", var_rando)