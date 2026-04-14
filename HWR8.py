#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW_R8


#1. Import all of HW_R7 into this assignment using the from/import function.
from HWR7 import *
#2. Create an object of three students in the classroom. Ask for their name, grade, and favorite color as need be.
Greg = Student("Greg", 12, "Purple")
Ethan = Student("Ethan", 9, "Red")
Devon = Student("Devon", 12, "Blue")
#3. Print the name of the first student.
print(Greg.name)
#4. Use the def function from HW_R7 to bump the grade level of the second student up by 1. Print the new grade.
Ethan.student_grade()
print(Ethan.grade)
#5. Use the def function from HW_R7 to ask the third student to change their favorite color to something else.
#Print the new color.
Devon.favorite_color()
print(Devon.color)