#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW15

#1. import the "random" library
import random
#2. print "Hello World!"
print("Hello World")
#3. Create three variables named a, b, and c, and allow the user to input an integer for each.
print("Please slect 3 numbers")
a = int(input())
b  = int(input())
c = int(input())
#4. Add a and b together, then divide the sum by c. Print the result.
d = a + b
e = d / c
print(e)

#5. Round the result from #3 up or down, and then determine if it is even or odd.
e = round(e)
if e % 2 == 0:
    print("Even")
else:
    print("Odd")


#6. Create a list of five different random integers between 1 and 10.
randlist = [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)]

#7. Print the 4th number in the list.
print(randlist[3])

#8. Append another integer to the end of the list, also random from 1 to 10.
randlist.append(random.randint(1, 10))

#9. Sort the list from lowest to highest and then print the 4th number in the list again.
randlist.sort()
print(randlist[3])

#10. Create a while loop that starts at 1, prints i and then adds i to itself until it is greater than 100.
i = 1

while i <= 100:
    i += i
    print(i)

#11. Create a list containing the names of five other students in the classroom.
namelist = ["Ethan", "Greg", "Kash", "Devon", "Aiden"]

#12. Create a for loop that individually prints out the names of each student in the list.
for j in namelist:
    print(j)

#13. Create a for loop that counts from 1 to 100, but ends early if the number is a multiple of 10.
for k in range(100):
    k += 1
    print(k)
    if k % 10 == 0:
        break


#14. Free space. Do something creative. :)

coinflip = random.randint(1, 3)

if coinflip == 1:
    print("Heads")
elif coinflip == 2:
    print("Tails")
else:
    print("You lost the coin, try again")