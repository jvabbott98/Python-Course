import pickle

# Prints a recipe to the screen for users to see
def display_recipe(recipe):
    print("------------------------------")
    print(recipe['name'])
    print(f"Cooking time: {recipe['cooking_time']}")
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(f"Difficulty: {recipe['difficulty']}")

# Uses a for loop to display an indexed list of ingredients and allows the user 
# to choose one ingredient and search for recipes that contain that ingredient.
def search_ingredient(data):
    for i in enumerate(data['all_ingredients']):
        print(i)

# Trys to search for recipes that contain the ingredient selected by the user. 
# On success, displays recipes that contain that ingredient.
# On failure, displays error message.
    try:
        a = int(input("Type the number of the ingredient you want: "))
        ingredient_searched = data['all_ingredients'][a]
    except ValueError:
        print("Input must be an integer.")
    except IndexError:
        print('The number you entered is not within the index of ingredients.')
    except:
        print("An unknown error has occured.")
    else:
        for recipe in data['recipe_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

file_searched = input('Type the name of the file that contains your recipe data: ')

# Trys to open and deserialize a binary file containing recipe data.
# On success, runs the search_ingredient function with data from the file.
# On fail, displays error message
try:
    with open (file_searched, 'rb') as recipe_file:
        data = pickle.load(recipe_file)
except FileNotFoundError:
    print('File not found.')
except:
    print('An unknown error has occured')
else: 
    search_ingredient(data)
