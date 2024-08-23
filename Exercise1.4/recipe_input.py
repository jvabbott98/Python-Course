import pickle

def take_recipe():
    name_input = input("Recipe name: ")
    cooking_time_input = int(input("Cooking time: "))
    ingredients_input = input("Enter ingredients seperated by commas: ")
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]

    recipe = {
        'name': name_input,
        'cooking_time': cooking_time_input,
        'ingredients': ingredients,
    }
    recipe['difficulty'] = calc_difficulty(recipe)
    return recipe

def calc_difficulty(recipe):
    if recipe['cooking_time'] < 10:
        if len(recipe['ingredients']) < 4:
            difficulty = 'Easy'
        else:
            difficulty = 'Medium'
    else:
        if len(recipe['ingredients'])< 4:
            difficulty = 'Intermediate'
        else:
            difficulty = 'Hard'
    return difficulty




file_name = input('Enter a file name: ')
try:
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {
        'recipe_list': [],
        'all_ingredients': []
    }
except:
    data = {
        'recipe_list': [],
        'all_ingredients': []
    }
finally:
    recipe_list = data['recipe_list']
    all_ingredients = data['all_ingredients']

n = int(input("How many recipes would you like to enter? "))
for i in range(n):
    recipe = take_recipe()
    recipe_list.append(recipe)
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data['recipe_list'] = recipe_list
data['all_ingredients'] =  all_ingredients

with open(f'{file_name}.bin', 'wb') as file:
        pickle.dump(data, file)
print(file)
