#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW7

#1. Print Hello World!
print("Hello World!")
#2. Create a dictionary with 3 keys and a value for each key. One of the keys must have a value with a list containing
#three numbers inside.
value_dict = {
    "Key1": [1, 10, 100],
    "Key2": [2, 20, 200],
    "Key3": [3, 30, 300]
}
#3. Print the keys of the dictionary from #2.
print(value_dict.keys)
#4. Print the values of the dictionary from #2
print(value_dict.values)
#5. Print one of the three numbers from the list by itself
print(value_dict["Key1"])
#6. Using the update function, add a fourth key to the dictionary and give it a value.
value_dict.update({"Key4": [4, 40, 400]})
#7. Print the entire dictionary from #2 with the updated key and value.
print(value_dict)
#8. Make a nested dictionary with three entries containing the name of another classmate and two other pieces of information
#within each entry.
my_class = {
    'cm1' : {
        'Name' : 'Kash',
        'Grade' : '12',
        'Sports' : False
    },
    'cm2' : {
        'Name' : 'Greg',
        'Grade' : '12',
        'Sports' : False
    },

    'cm3' : {
        'Name' : 'Brodie',
        'Grade' : '11',
        'Sports' : True
    },

}


#9. Print the names of all three classmates on the same line.
print(my_class['cm1']['Name'], my_class['cm2']['Name'], my_class['cm3']['Name'])

#10. Use the pop function to remove one of the nested dictionaries inside and print the full dictionary from #8.
my_class.pop('cm1')
print(my_class)