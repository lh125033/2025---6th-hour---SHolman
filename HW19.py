#Name:Shane Holman
#Class: 6th Hour
#Assignment: HW19

#1. Import the def functions created in problem 1-4 from HW16
from HW16 import howdy
from HW16 import average
from HW16 import animals
from HW16 import max

#2. Call the functions here and run HW19
howdy()
average(2, 4, 16)
animals("Monkey", "Gorilla", "Ethan", "Donkey", "Pig")
max(100)
#3. Delete all calls for problem 5 in HW16 and run HW19 again.

#4. Create a try catch that tries to print variable x (which has no value), but prints "Hello World!" instead.
try:
    print(x)
except:
    print("Hello world")

#5. Create a try catch that tries to divide 100 by whatever number the user inputs, but prints an exception for Divide By Zero errors.
try:
    UserDiv = int(input("Enter an integer: "))
    print(100/UserDiv)
except ZeroDivisionError:
    print("You can't divide by zero")

#6. Create a variable that asks the user for a number. If the user input is not an integer, prints an exception for Value errors.
try:
    NewInput = int(input("Enter another integer: "))
    print(NewInput)
except ValueError:
    print("You didn't enter an integer")
#7. Create a while loop that counts down from 5 to 0, but raises an exception when it counts below zero.

y = 5
while y >= 0:
    print(y)
    y -= 1
    if y < 0:
        raise Exception("It's below zero")