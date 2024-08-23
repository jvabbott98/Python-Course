import pickle

def display_recipe(recipe):
    print("------------------------------")
    print(recipe['name'])
    print(f"Cooking time: {recipe['cooking_time']}")
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data):
    for i in enumerate(data['all_ingredients']):
        print(i)
    try:
        a = int(input("Type the number of the ingredient you want: "))
        ingredient_searched = data['all_ingredients'][a]
    except:
        print('The number you entered is not within the index of ingredients')
    else:
        for recipe in data['recipe_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

file_searched = input('Type the name of the file that contains your recipe data: ')
try:
    with open (file_searched, 'rb') as recipe_file:
        data = pickle.load(recipe_file)
except FileNotFoundError:
    print('File not found.')
except:
    print('An unknown error has occured')
else: 
    search_ingredient(data)
