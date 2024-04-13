#Database Using MongoDB

from pymongo import MongoClient
from FDCAPI import search
from FDCAPI import  fetch_nutrients

class Database():

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client['FoodTracker']
        self.food = self.database['food']

    def addFood(self,username,  name, purchaseCost, currentServing, intialServingCount, purchaseDate, expireDate, macros):

        foodKey = name.replace(' ', '_')
        self.food.update_one(
            {"username" : username},
            {"$set": {f"foods.{foodKey}": {
                "purchaseCost": purchaseCost,
                "currentServing": currentServing,
                "intitalServingCount": intialServingCount,
                "purchaseDate": purchaseDate,
                "expireDate": expireDate,
                "macros": macros
            }}},
            upsert = True
        )

    def remove_food(self, username, foodName):

        foodKey = foodName.replace(' ', '_')
        result = self.food.update_one(
            {"username": username},
            {"$unset": {f"foods.{foodKey}": ""}}
        )

        if result.modified_count > 0:
            print(f"Removed {foodName} from {username}'s pantry")
        else:
            print(f"No food found with name {foodName} in {username}'s pantry")

    def editFood(self, username, foodName, updatedServing):

        foodKey = foodName.replace(' ', '_')
        result = self.food.update_one(
            {"username": username},
            {"$set": {f"foods.{foodKey}.currentServing": updatedServing}}
        )

        if result.modified_count > 0:
            print(f"Updated {foodName} current serving to {updatedServing} for {username}")
        else:
            print(f"Failed to update serving count for {foodName} for {username}'s pantry")

    def getFood(self, username, foodName):

        foodKey = foodName.replace(' ', '_')
        result = self.food.find_one(
            {"username": username},
            {"_id": 0, f"foods.{foodKey}": 1}
        )

        if result and 'foods' in result and foodKey in result['foods']:
            return result['foods'][foodKey]
        else:
            print(f"No {foodName} found in {username}'s pantry")
            return None

    def returnPantry(self, username):

        exists = self.food.find_one({"username": username})
        if not exists:
            self.createUser(username)

        result = self.food.find_one(
            {"username": username}, {"_id": 0, "foods": 1}
        )

        if result and "foods" in result:
            return result['foods']
        else:
            print(f"No items in pantry found for {username}")
            return {}

    def createUser(self, username):

        exists = self.food.find_one({"username": username})
        if not exists:
            self.food.insert_one({"username": username, "foods": {}})
            print(f"New user {username} created with an empty ")
        else:
            print(f"User {username} already exists")

if __name__ == "__main__":
    foodPantry = Database()

    macrosList = {
        "calories": 10,
        "protien": 10
    }

    def fdcid_find(val, num):
        fdc = val[num]
        print(fdc['FDC ID'])
        return fdc['FDC ID']

    val = search('Carrot')
    fdc_id = fdcid_find(val, 1)
    nutrients = fetch_nutrients(fdc_id)

    foodPantry.addFood(username = "Joe Fatha", name = "Hot Dogs", purchaseCost = 1.00, currentServing = 5, intialServingCount = 10, purchaseDate = "2024-04-13", expireDate = "2024-04-20", macros = nutrients)
    #foodPantry.remove_food("Rino", "Joe Beans")
    #foodPantry.editFood("Rino", "Joe Fruits", 8)
    #print(foodPantry.getFood("Rino", "Joe Beans"))
    pantry = foodPantry.returnPantry("Joe Fatha")
    print(pantry)
    if pantry:
        for foodKey, details in pantry.items():
            print(f"{foodKey.replace('_', ' ')}: {details}")
    else:
        print("Nothing to display")

    if pantry:
        print(f"All the servings in pantry:")
        for foodKey, details in pantry.items():
            currentServing = details.get('currentServing', 'None')
            many = len(pantry)
            print(many)

            foodName = foodKey.replace('_', ' ')
            print(f"{foodName}: Current serving = {currentServing}")
    else:
        print("You ate everything")



