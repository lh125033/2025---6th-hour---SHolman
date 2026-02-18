#Name: Shane Holman
#Class: 6th Hour
#Assignment: HW20

#1. Create a class containing a def function that inits self and 3 other attributes for store items (stock, cost, and weight).
class Store:
    def __init__(self, stock, cost,weight ):
        self.stock = stock
        self.cost = cost
        self.weight = weight
    def PriceGouge(self):
        self.cost *= 2
    def Buying(self):
        self.stock *= 1/4
#2. Make 3 objects to serve as your store items and give them values to those 3 attributes defined in the class.
EthanNguyen = Store(18, 5, 100)
GregReesce = Store(20, 30, 1000)
PorkLoin = Store(60, 20, 10)
#3. Print the stock of all three objects and the cost of the second store item.
print(f"There are {EthanNguyen.stock} Ethans available. There are {GregReesce.stock}"
      f" Gregs left, and the each cost {GregReesce.cost}. And {PorkLoin.stock} pork loins remain. ")
#4. Make a def function within the class that doubles the cost an item, double the cost of the second store item, and print the new cost below the original cost print statement.
GregReesce.PriceGouge()
print(f"There has been a price change, Greg now costs {GregReesce.cost}.")
#5. Directly change the stock of the third store item to approx. 1/4th the original stock and then print the new stock amount.
PorkLoin.Buying()
print(f"There are now {PorkLoin.stock} pork loins remain.")
#6. Delete the first store item and then attempt to print the weight of the first store item. Create a try/except catch to fix the error.
del EthanNguyen

try:
    print(f"Ethan weighs: {EthanNguyen.weight}")
except NameError:
    print("Ethan ran away")