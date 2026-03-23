#Name: Shane Holman
#Class: Lysander au Lune, Last heir of Silenius the Lightbringer, Last of the Heir to the Lune name. Heir to the Morning Chair, Student of Cassius au Bellona.
#Assignment: HW-R2


#1. Print "Hello World!"
print("Hello World!")
#2. Create an empty list.
Empty_List = []
#3. Create a list that contains the names of everyone in the classroom.
Student_List = ["Triston","Devon","Ally", "Greg", "Shane", "Ethan", "Connor"]
#4. Print the list from #3, sort the list, then print the list again.
print(Student_List)
Student_List.sort()
print(Student_List)
#5. Append 5 different integers into the empty list from #2 and print the list.
Empty_List.append(5)
Empty_List.append(50)
Empty_List.append(500)
Empty_List.append(5000)
Empty_List.append(50000)
print(Empty_List)
#6. Add together the middle three numbers in the list from #2 and print the result.
Added_List = Empty_List[1] + Empty_List[2]+ Empty_List[3]
print(Added_List)
#7. Remove the very first number in the list from #2. Print the new first number.
print(Empty_List)
Empty_List.remove(5)
print(Empty_List[0])
#8. Create a dictionary with three keys with respective values: your name, your grade, and your favorite color.
Class_Dict = {
    "Name": "Shane",
    "Grade": 12,
    "Color": "Sea Green",
}
#9. Using the update function, add a fourth key and value determining your favorite candy.
Class_Dict.update({"Favorite Candy": "Twix"})
print(Class_Dict)
#10. Print ONLY the values of the dictionary from #8
Class_Dict.pop("Favorite Candy")
print(Class_Dict.values())