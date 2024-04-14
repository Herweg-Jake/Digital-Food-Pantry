#Database Using MongoDB

from pymongo import MongoClient
from FDCAPI import search
from FDCAPI import  fetch_nutrients

class Database():

    # Creates an Intial Connection Do a MongoDB Database, uses default port 27017
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client['FoodTracker']
        self.food = self.database['food']


    #Add a food to the MongoDB database with the given parameters, Food itself is a nested page within username, and macros is a nested page within food 
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

    # Removes a food within a specific account
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

    #Edit food is responsible for updating the serving amount of food by a given amount
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

    #Returns one specified food name information
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

    #Returns the user entire "pantry" or otherwise their entire collection of foods in the database
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

    #A subroutine to create a user
    def createUser(self, username):

        exists = self.food.find_one({"username": username})
        if not exists:
            self.food.insert_one({"username": username, "foods": {}})
            print(f"New user {username} created with an empty ")
        else:
            print(f"User {username} already exists")

if __name__ == "__main__":
    foodPantry = Database()

    #foodPantry.addFood(username = "Joe Fatha", name = "Hot Dogs", purchaseCost = 1.00, currentServing = 5, intialServingCount = 10, purchaseDate = "2024-04-13", expireDate = "2024-04-20", macros = nutrients)
    #foodPantry.remove_food("Rino", "Joe Beans")
    #foodPantry.editFood("Rino", "Joe Fruits", 8)
    #print(foodPantry.getFood("Rino", "Joe Beans"))
    """
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
    """