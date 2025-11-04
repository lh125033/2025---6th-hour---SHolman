#Name:Shane Holman
#Class: 6th Hour
#Assignment: HW12
import random
#1. Create a while loop with variable i that counts down from 5 to 0 and then prints
#"Hello World!" at the end.
i = 5
while i >= 0:
    print(i)
    i -= 1
else:
    print("Hello world")
#2. Create a while loop that prints only even numbers between 1 and 30 (HINT: modulo).
i2 = 1
while i2 <= 30:
    if i2 % 2 == 0:
        print(i2)
    i2 += 1
#3. Create a while loop that prints from 1 to 30 and continues (skips the number) if the
#number is divisible by 3.
i3 = 1
while i3 <= 30:
    if i3 % 3 == 0:
        i3 += 1
        continue
    print(i3)
    i3 += 1

#4. Create a while loop that randomly generates a number between 1 and 6, prints the result,
#and then breaks the loop if it's a 1.
i4 = 1
while i4 >= 1:
    i4 = random.randint(1,6)
    print(i4)
    if i4 == 1:
        break
#5. Create a while loop that asks for a number input until the user inputs the number 0.

i5 = 10
while i5 >= 1:
    i5 = int(input("Enter a number: "))
    if i5 > 0:
        print(i5)
        continue
    else:
        print("Thank you")
