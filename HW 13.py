
#Name:
#Class: 5th Hour
#Assignment: HW13

#A common exercise in computer science is "FizzBuzz". The rules of
#the game are simple. Count from 1 to 100 but with every number that
#is divisible by 3 you say "Fizz" instead of the number,
#every number divisible by 5 you say "Buzz" instead,
#and if it's divisible by both you say "FizzBuzz".

#Create a while loop that follows the rules of the game.

#Something similar to this
'''i3 = 1
while i3 <= 30:
    if i3 % 3 == 0:
        i3 += 1
        continue
    print(i3)
    i3 += 1'''


i = 1
while i <= 100:
    print(i)
    i += 1
    if i % 3 == 0:
        print("Fizz")
        i += 1
        continue
    elif i % 5 == 0:
        print("Buzz")
        i += 1
        continue
    elif i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
        i += 1
        continue