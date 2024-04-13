#Database Using MongoDB

from pymongo import MongoClient

class Database():

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client['FoodTracker']
        self.food = self.database['food']

    def add_food(self, name, purchaseCost, currentServing, intialServingCount, purchaseDate, expireDate, macros):

        foodItem = {
            "name": name,
            "purchase_cost": purchaseCost,
            "currentServing": currentServing,
            "initialServingCount": intialServingCount,
            "purchaseDate": purchaseDate,
            "expire_date": expireDate,
            "macros": macros
        }

        self.food.insert_one(foodItem)

    def remove_food(self, name):

        result = self.food.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Remove Item: {name}")
        else:
            print(f"No food item found with name: {name}")

if __name__ == "__main__":
    foodPantry = Database()

    macrosList = {
        "calories": 10,
        "protien": 10
    }

    #foodPantry.add_food(name = "Fruit Snacks", purchaseCost = 1.00, currentServing = 5, intialServingCount = 10, purchaseDate = "2024-04-13", expireDate = "2024-04-20", macros = macrosList)
    foodPantry.remove_food("Fruit Snacks")



