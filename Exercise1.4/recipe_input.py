import pickle

# Takes in information about a recipe from the user (name, cooking_time, 
# ingredients) and returns a dictionary of the recipe's information.
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

# Determines and assigns a recipe's difficulty based on cooking_time and number
# of ingredients
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

# Attempts to open and deserialize data from binary file and if successful 
# assings that data to recipe_list and all_ingredients. If it fails, it assigns 
# recipe_list and all_ingredients to empty lists.
data = {
    'recipe_list': [],
    'all_ingredients': []
}
recipe_list = []
all_ingredients = []
try:
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("We were unable to find the file name you entered.")
except:
    print("An unknwon error has occured")
else:
    recipe_list = data['recipe_list']
    all_ingredients = data['all_ingredients']

n = int(input("How many recipes would you like to enter? "))

# Executes take_recipe() a number of times equal to the number of recipes the 
# user would like to enter. 
for i in range(n):
    recipe = take_recipe()
    recipe_list.append(recipe)
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data['recipe_list'] = recipe_list
data['all_ingredients'] =  all_ingredients

with open(f'{file_name}', 'wb') as file:
        pickle.dump(data, file)
print(f'The recipe has been saved to {file_name}')
