#Name:Shane Holman
#Class: 6th Hour
#Assignment: HW14


#1. Create a for loop with variable i that counts down from 5 to 1 and then prints "Hello World!"
#at the end.
for i in range(6):
    print(i)
else:
    print("hello world")
#2. Create a for loop that counts up and prints only even numbers between 1 and 30.
for j in range(2, 31, 2):
    print(j)
#3. Create a for loop that prints from 1 to 30 and continues (skips the number) if the number is
#divisible by 3.
for k in range(1, 30):
    if k % 3 == 0:
        continue
    print(k)
#4. Create a for loop that prints 5 different animals from a list.
animals = ['cat', 'dog', 'rabbit', 'monkey', 'lion']
for l in animals:
    print(l)
#5. Create a for loop that spells out a word you input backwards.
#(HINT: Google "How to reverse a string in Python")
for d in input("Give me a word and I'll spell it backwards: ")[::-1]:
    print(d)

#6. Create a list containing 10 integers of your choice and print the list.
numb_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(numb_list)
#7. Create two empty variables named evenNumbers and oddNumbers.
evenNumbers = 0
oddNumbers = 0
#8. Make a loop that counts the number of even and odd numbers in the list, and prints the
#result after the loop.
for f in numb_list:
    if f % 2 == 0:
        evenNumbers += 1
    else:
        oddNumbers += 1
    print("Even numbers", evenNumbers, "Odd numbers", oddNumbers)
#9. Create a variable that asks the user for an integer and an empty integer variable.
int_var = 1
ask_var = int(input("Enter a number: "))
#10. Create a loop with a range from 1 to the number the user input. Use the loop to find the
#factorial of that number and print the result. A factorial of a number is that number multiplied
#by every number before it until you reach 1. (For example: 5! is 5 x 4 x 3 x 2 x 1 = 120)
for v in range(1, ask_var + 1):
    int_var *= v
print(int_var)
