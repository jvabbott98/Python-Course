recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time: "))
    n = int(input("Please enter the number of ingredients: "))
    ingredients = []
    for i in range(0, n):
        ingredient = input("Enter an ingredient: ")
        ingredients.append(ingredient)
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
    }
    return recipe

n = int(input("How many recipes would you like to enter? "))
for i in range(0, n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient in ingredients_list:
            continue
        else:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        difficulty = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        difficulty = "Intermediate"
    else:
        difficulty = 'Hard'
    print("Recipe:", recipe['name'])
    print("Cooking Time (min):", recipe['cooking_time'])
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficulty level:", difficulty)

print("Ingredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
    print(ingredient)