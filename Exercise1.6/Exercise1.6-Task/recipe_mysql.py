import mysql.connector

# Set up cursor so and database so that we can interact with the mysql database through python
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    passwd = 'password'
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
               )''')

# Returns difficulty of recipe based on number of ingredients and cooking time. 
def calculate_difficulty(self):
    if self['cooking_time'] < 10:
        if len(self['ingredients']) < 4:
            return 'Easy'
        else:
            return 'Medium'
    else:
        if len(self['ingredients'])< 4:
            return 'Intermediate'
        else:
            return 'Hard'

# Takes input about a recipe from the user and returns the data as a dictionary
def take_recipe():
    name_input = input("Recipe name: ")
    cooking_time_input = int(input("Cooking time: "))
    ingredients_input = input("Enter ingredients seperated by commas: ")
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
    ingredients_string = ", ".join(ingredients)

    recipe = {
        'name': name_input,
        'cooking_time': cooking_time_input,
        'ingredients': ingredients_string,
    }
    recipe['difficulty'] = calculate_difficulty(recipe)
    return recipe

# Takes the recipe dictionary from take_recipe() and inserts it into the mysql databse.
def create_recipe(conn, cursor):
    recipe = take_recipe()

    cursor.execute("SELECT name FROM Recipes")
    results = cursor.fetchall()
    results = [item[0] for item in results]
    if recipe['name'] not in results:
        cursor.execute('''INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)''', (recipe['name'], recipe['ingredients'], recipe['cooking_time'], recipe['difficulty']))
        conn.commit()
    else:
        print("Recipe already exists")

# Searches for and displays a list of recipes that contain a particular ingredient selected by the user. 
def search_recipe(conn, cursor):

    # Gathers all unique ingredients from the database and displays for the user to choose from.
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []
    for result in results:
        for ingredient in result[0].split(", "):
            ingredient = ingredient.lower().strip()
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i} - {ingredient}")
    search_ingredient = int(input("Please select an ingredient from the list above: "))
    search_ingredient = all_ingredients[search_ingredient]

    # Seaches the databse for recipes containing the selected ingredient and displays them to the user
    cursor.execute('''SELECT * FROM Recipes WHERE ingredients LIKE %s''', ('%' + search_ingredient + '%', ))
    results = cursor.fetchall()
    if results:
        for row in results:
            print("id: ", row[0])
            print("Name: ", row[1])
            print("Ingredients: ", row[2])
            print("Cooking_time: ", row[3])
            print("Difficulty: ", row[4])
            print("-"*30)
    else:
        print("No matches found.")

# Updates the name, cooking time, and ingredients fields of a recipe that the user selects. 
def update_recipe(conn, cursor):
    # Displays a list of recipes for the user to choose from. \
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()
    for item in results:
        print(f"{item[0]} - {item[1]}")
    selection = int(input("Select the recipe you would like to modify by typing its id number: "))
    print("-"*30)

    # Displays the categories available for the user to update and their current values.
    cursor.execute("SELECT name, cooking_time, ingredients FROM Recipes WHERE id = %s", 
    (selection,))
    results= cursor.fetchall()
    print(f"Name: {results[0][0]}")
    print(f"Cooking time: {results[0][1]}")
    print(f"Ingredients: {results[0][2]}")
    print("-"*30)
    
    # A loop that allows the categories they wish and exit out when finished.
    category = ''
    while(category != 'quit'):
        print("Please type the category you would like to modify.")
        print("When you are done modifying this recipe, type 'quit'.")
        category = input("Category to modify: ").lower()
        if category == 'name':
            new_name = input("New name: ")
            cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, selection))
        elif category == 'cooking time':
            new_cooking_time = int(input("New cooking time: "))
            cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_cooking_time, selection))
        elif category == 'ingredients':
            new_ingredients = input("Please type new ingredients seperated by commas: ")
            new_ingredients = new_ingredients.strip()
            cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients, selection))
        elif category == 'quit':
            return
        else:
            print("Please type 'name', 'cooking time', 'ingredients', or 'quit'.")
    
    # Calculates and assings a new difficulty based on the updated information and saves all of the new data to the database.
    cursor.execute("SELECT name, cooking_time, ingredients FROM Recipes WHERE id = %s", (selection,))
    results = cursor.fetchall()
    updated_ingredients = [ingredient.strip() for ingredient in results[0][2].split(",")]
    updated_recipe = {
        'name': results[0][0],
        'cooking_time': results[0][1],
        'ingredients': updated_ingredients
    }
    new_difficulty = calculate_difficulty(updated_recipe)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id =%s", (new_difficulty, selection))
    conn.commit()

# Deletes a recipe selected by the user
def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()
    for item in results:
        print(f"{item[0]} - {item[1]}")
    selection = int(input("Select the recipe you would like to delete by typing its id number: "))
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (selection,))

# A loop through which the user can choose between creating, searching for, updating, and deleting recipes.
def main_menu(conn, cursor):
    choice = ''
    while(choice != 'quit'):
        print("What would you like to do?")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient.")
        print("3. Modify an existing recipe.")
        print("4. Delete a recipe.")
        print("Type 'quit' to exit the program.")
        choice = input("Your choice: ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice =='quit':
            conn.commit()
            conn.close()
        else:
            print("Please type the number corresponding to your choice or type 'quit' to exit the application.")

main_menu(conn, cursor)