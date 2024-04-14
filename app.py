from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from FDCAPI import search
from FDCAPI import fetch_nutrients
from FDCAPI import food_details
from forms import FoodSearchForm
from Database import Database
import os

def getfooddata(foodList):
    formatted_foods = []
    for food_name, attributes in foodList.items():
        food_data = {
            'name': food_name,
            'cost': attributes.get('purchaseCost'),
            'quantity': attributes.get('currentServing'),
            'initialServingCount': attributes.get('intitalServingCount', attributes.get('initialServingCount')),  # Handle typo in key
            'purchaseDate': attributes.get('purchaseDate'),
            'expireDate': attributes.get('expireDate'),
            'macros': attributes.get('macros')
            #'cpServing': int(attributes.get('purchaseCost'))/int(attributes.get('intitalServingCount', attributes.get('initialServingCount')))
        }
        formatted_foods.append(food_data)
    return formatted_foods

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('pantry'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    print('E')
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def food_search():
    form = FoodSearchForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            food_name = form.food_name.data
            search_results = search(food_name)
            print(f"Form validated. Food name: {food_name}")
            print(f"Search results: {search_results}")
            return render_template('results.html', search_results=search_results, food_name=food_name)
        else:
            print("Form did not validate")
            print(form.errors)
    return render_template('search.html', form=form)

@app.route('/select_result', methods=['POST'])
def select_result():
    fdc_id = request.form['fdc_id']
    name = request.form.get('name', 'No description provided')
    description = request.form.get('description', 'No description provided')
    data_type = request.form.get('dataType', 'Unknown')
    brand_owner = request.form.get('brandOwner', 'Unknown')

    food_det = {
        'name': name,
        'fdc_id': fdc_id,
        'Description': description,
        'Data Type': data_type,
        'Brand Owner': brand_owner,
    }
    nutrients = fetch_nutrients(fdc_id)
    return render_template('nutrients.html', nutrients=nutrients, fdc_id=fdc_id, food_details=food_det)

@app.route('/pantry', methods=['GET'])
def pantry():
    username = session['username']
    db = Database()
    pantry = db.returnPantry(username)

    foods = getfooddata(pantry)
    return render_template('food_list.html', foods=foods, user=username)

@app.route('/update_usage_amount', methods=['POST'])
def update_usage_amount():
    data = request.get_json()
    # we were using this somehow?


@app.route('/update_actions', methods=['POST'])
def update_actions():
    action = request.form['action']
    quantities = request.form.getlist('quantity')
    print("Received quantities:", quantities, action)

    if action == 'update':
        print('update')
        db = Database()
        pantry = db.returnPantry(session['username'])
        total_nutrients = {}
        
        
        if pantry:
            recipe_facts = []
            for index, (foodKey, details) in enumerate(pantry.items()):
                if index < len(quantities):
                    food_info = {
                        'name': foodKey,
                        'quantity': quantities[index],
                        'expiry': details.get('expiry', 'N/A'),
                        'cost': details.get('cost', '0')
                    }
                    recipe_facts.append(food_info)
                    if isinstance(details, dict) and 'macros' in details:
                        nutrients = details['macros']
                        quantity = int(quantities[index])

                        for key, value in nutrients.items():
                            amount, unit = value
                            total_amount = amount * quantity

                            if key in total_nutrients: 
                                total_nutrients[key][0] += total_amount
                            else:
                                total_nutrients[key] = [total_amount, unit]
                    else:
                        print(f"Expected a dictionary for details, but got {type(details)}")
            for nutrient, values in total_nutrients.items():
                print(f"{nutrient}: {values[0]} {values[1]}")
            # return a new template with the right hand side filled out by this
        return render_template('food_list.html', foods=getfooddata(db.returnPantry(session['username'])), user=session['username'], total_nutrients=total_nutrients, recipe_facts=recipe_facts)
    elif action == 'add':
        db = Database()
        pantry = db.returnPantry(session['username'])
    
        if pantry:
            length = len(pantry)
            i=0
            for foodKey, details in pantry.items():
                if i < len(quantities):
                    print(details)
                    db.editFood(session['username'], foodKey, int(details.get('currentServing')) + abs(int(quantities[i])))
                i = i + 1
            print("Adding Item with Quantities:", quantities)
    elif action == 'remove':
        print('remove')
        db = Database()
        pantry = db.returnPantry(session['username'])
    
        food_name = request.form['food_name']
        username = session['username']
        
        if pantry:
            length = len(pantry)
            i=0
            for foodKey, details in pantry.items():
                if i < len(quantities):
                    print(details)
                    db.editFood(session['username'], foodKey, int(details.get('currentServing')) - abs(int(quantities[i])))

                    print(details.get('currentServing'))
                    if int(details.get('currentServing')) <= 0:
                        db.remove_food(session['username'], foodKey)
                i = i + 1

    
    return render_template('food_list.html', foods=getfooddata(db.returnPantry(session['username'])), user=session['username'], total_nutrients=0)  # Redirect back to the pantry or appropriate page

@app.route('/save_food_details/<int:fdc_id>', methods=['POST'])
def save_food_details(fdc_id):
    # Fetching form data
    cost = request.form['cost']
    servings = request.form['servings']
    expire_date = request.form['expire_date']

    # Fetching nutrient details using the fdc_id
    nutrients = fetch_nutrients(fdc_id)

    # Printing form and nutrient details
    print("Received data:")
    print("FDC ID:", fdc_id)
    print("Cost:", cost)
    print("Servings:", servings)
    print("Expire Date:", expire_date)
    print("Nutrient Details:")
    for nutrient, values in nutrients.items():
        print(f"{nutrient}: {values[0]} {values[1]}")

    db = Database()
    db.addFood(session['username'], request.form.get('name', 'No description provided'), cost, servings, servings, expire_date, expire_date, nutrients)

    print("Food details saved successfully.", "success")
    return redirect(url_for('pantry')) 

if __name__ == '__main__':
    app.run(debug=True)