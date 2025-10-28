#Name:
#Class: 6th Hour
#Assignment: SC2

import math
#A local health clinic is looking to add a quick BMI calculator to their website so that their
#patients can quickly input their height and weight and be given a number as well as their
#classification. The classifications are as follows:

# - Underweight: Less than 18.5 BMI
# - Normal Weight: 18.5 to 24.9 BMI
# - Overweight: 25 to 29.9 BMI
# - Obese: 30 or more BMI

#It is up to you to figure out the calculation for an accurate BMI reading and tying it to
#the right classification

#Code Here:

bmi_weight = float(input("BMI weight (Kg): "))
bmi_height = float(input("BMI height (m): "))**2

bmi_class = bmi_weight / bmi_height

if bmi_class <= 18.5:
    print(bmi_class, "You are under weight")
elif bmi_class >= 18.5 and bmi_class <= 24.9:
    print(bmi_class, "You are normal weight")
elif bmi_class >= 25 and bmi_class <= 29.9:
    print(bmi_class, "You are over weight")
else:
    print(bmi_class, "You are obese")



