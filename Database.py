#Database Using MongoDB

from pymongo import MongoClient

class Database():

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client['FoodTracker']
        self.food = self.database['food']

    def addFood(self,username,  name, purchaseCost, currentServing, intialServingCount, purchaseDate, expireDate, macros):

        foodItem = {
            "name": name,
            "purchase_cost": purchaseCost,
            "currentServing": currentServing,
            "initialServingCount": intialServingCount,
            "purchaseDate": purchaseDate,
            "expire_date": expireDate,
            "macros": macros
        }

        self.food.update_one({"username": username}, {"$push": {"foods": foodItem}}, upsert = True)

    def remove_food(self, username, foodName):

        result = self.food.update_one({"username": username}, {"$pull": {"foods": {"name": foodName}}})
        print(result.modified_count)
        if result.modified_count > 0:
            print(f"Remove Item: {foodName} from {username} Pantry")
        else:
            print(f"No food item found with name: {foodName} in {username} Pantry")

if __name__ == "__main__":
    foodPantry = Database()

    macrosList = {
        "calories": 10,
        "protien": 10
    }

    #foodPantry.addFood(username = "Rino", name = "Fruit Snacks", purchaseCost = 1.00, currentServing = 5, intialServingCount = 10, purchaseDate = "2024-04-13", expireDate = "2024-04-20", macros = macrosList)
    foodPantry.remove_food("Rino", "Fruit Snacks")



