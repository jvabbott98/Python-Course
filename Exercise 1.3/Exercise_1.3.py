recipes_list = []
ingredients_list = []

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
    return recipe

n = int(input("How many recipes would you like to enter? "))
for i in range(0, n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in recipe['ingredients']:
            ingredients_list.append(ingredient)
            recipes_list.append(recipe)

for recipe in recipes_list:
    
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
    recipe["difficulty"] = difficulty

    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(f"Difficulty level: {recipe['difficulty']}")

print("Ingredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
    print(ingredient)