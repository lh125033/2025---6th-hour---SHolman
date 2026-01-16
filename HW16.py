#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW16

#1. Create a def function that prints out "Hello World!"
def howdy():
    print("Hello World!")

howdy()
#2. Create a def function that calculates the average of three numbers (set the 3 numbers as your arguments).
def average(a , b, c):
    d = (a + b + c) / 3
    print(d)

average(33 , 3, 333)
#3. Create a def function with the names of 5 animals as arguments, treats it like a list, and
#prints the name of the third animal.
def animals(*animal):
    print("The fourth animal is",animal[2])

animals("Monkey", "Gorilla", "Greg", "Donkey", "Pig")

#4. Create a def function that loops from 1 to the number put in the argument.
def max(number):
    for i in range(1, number + 1):
        print(i)

max(10)



#5. Call all the functions created in 1 - 4 with relevant arguments.
howdy()
average(2, 4, 16)
animals("Monkey", "Gorilla", "Ethan", "Donkey", "Pig")
max(100)

#6. Create a variable x that has the value of 2. Print x
x = 2
print(x)
#7. Create a def function that multiplies the value of 2 by a random number between 1 and 5.
import random

def multi():
    global x
    x *= random.randint(1, 5)
#8. Print the new value of x.
multi()
print(x)
