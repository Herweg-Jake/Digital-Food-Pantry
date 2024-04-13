import requests

# global temp vars
api_key = '6Rfmv8d36afO9Ptmf0PU79WV22ZdnSaFZi5zshaO'


def search(food_item):
    base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": food_item,
        "api_key": api_key,
        "pageSize": 20  # return results
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # response -> JSON
        return search_results(response.json())
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return False


def search_results(foods):
    food_list = []
    if foods and 'foods' in foods:
        for food in foods['foods']:
            detail = {
                'FDC ID': food.get('fdcId'),
                'Description': food.get('description'),
                'Data Type': food.get('dataType'),
                'Brand Owner': food.get('brandOwner', 'N/A')
                # 'Ingredients': food.get('ingredients', 'N/A')
            }
            food_list.append(detail)
    return food_list


def fetch_nutrients(fdc_id):
    base_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": api_key}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        food_data = response.json()
        nutrients = {}
        for nutrient in food_data.get('foodNutrients', []):
            interesting_nutrients = ['Energy', 'Water', 'Protein', 'Total lipid (fat)', 'Ash',
                                     'Carbohydrate, by difference', 'Fiber, total dietary', 'Total Sugars',
                                     'Calcium, Ca', 'Iron, Fe', 'Magnesium, Mg', 'Phosphorus, P',
                                     'Potassium, K', 'Sodium, Na', 'Zinc, Zn', 'Copper, Cu', 'Manganese, Mn',
                                     'Selenium, Se', 'Vitamin C, total ascorbic acid', 'Thiamin', 'Riboflavin',
                                     'Niacin', 'Pantothenic acid', 'Vitamin B-6', 'Folate, total',
                                     'Vitamin B-12', 'Vitamin A, RAE', 'Vitamin E (alpha-tocopherol)',
                                     'Vitamin D (D2 + D3)', 'Vitamin K (phylloquinone)', 'Fatty acids, total saturated',
                                     'Fatty acids, total monounsaturated', 'Fatty acids, total polyunsaturated',
                                     'Cholesterol']

            # Check if the 'name' is in the list
            if nutrient['nutrient']['name'] in interesting_nutrients:
                # Print the unit name and amount
                nutrients[nutrient['nutrient']['name']] = [nutrient['amount'], nutrient['nutrient']['unitName']]
        return nutrients
    else:
        print(f"Failed to fetch nutrient data: {response.status_code}")
        return None


def list_detailed_food_items(food_items):
    return food_items