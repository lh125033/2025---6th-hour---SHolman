#Name: Shane Holman
#Class: 6th Hour Alexnder au Arcos, Grandson to Lorn au Arcos - Rage Knight of the Scociety, Imperator of the Republic, Howler, Deceased - Killed by Lysander au Lune
#Assignment: HW-R6
import random

#1. Create a def function that prints out "Hello World!". Call the function.
def intro():
    print("Hellow World!")
intro()
#2. Create a def function that prints your name. Call the function with the name as the argument.
def my_name(name):
    print("Welcome", name)
my_name("Shane")
#3. Create a def function that calculates the average of a list. Call the function with the list as the argument.
def calc(list):
    print(sum(list)/len(list))
calc([random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)])
#4. Call the function from #3 but with a new list of different numbers.
calc([random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)])
#5. Create a def function that takes two numbers as arguments, x and y. Inside the function, create a for loop
#with a range of 10. Inside the loop, print x, make z equal the sum of x and y, make x equal y, then y equal z.
def numbers(x, y):
    for i in range(10):
        print(x)
        z = x + y
        x = y
        y = z

#6. Call the function from #5 with the arguments for x and y being 0 and 1.
numbers(0,1)