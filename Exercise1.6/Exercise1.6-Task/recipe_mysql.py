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
def calculate_difficulty(cooking_time, ingredients):

    ingredients = list(ingredients.split(", "))

    if cooking_time < 10:
        if len(ingredients) < 4:
            return 'Easy'
        else:
            return 'Medium'
    else:
        if len(ingredients)< 4:
            return 'Intermediate'
        else:
            return 'Hard'

def input_name():
    name = input("Recipe name: ")
    return name

def input_cooking_time():
    cooking_time = int(input("Cooking Time: "))
    return cooking_time

def input_ingredients():
    ingredients = input("Enter ingredients seperated by commas: ").rstrip()
    return ingredients

# Takes the recipe dictionary from take_recipe() and inserts it into the mysql databse.
def create_recipe(conn, cursor):
    name = input_name()

    cursor.execute("SELECT name FROM Recipes")
    results = cursor.fetchall()
    results = [item[0] for item in results]
    if name not in results:

        cooking_time = input_cooking_time()
        ingredients = input_ingredients()
        difficulty = calculate_difficulty(cooking_time, ingredients)

        cursor.execute("SELECT name FROM Recipes")
        results = cursor.fetchall()
        results = [item[0] for item in results]
        if name not in results:
            cursor.execute('''INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)''', (name,ingredients, cooking_time, difficulty))
            conn.commit()
            print("-"*50)
    else:
        print("Recipe already exists")
        print("-"*50)

# Searches for and displays a list of recipes that contain a particular ingredient selected by the user. 
def search_recipe(conn, cursor):

    # Gathers all unique ingredients from the database and displays them for the user to choose from.
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = set()
    for row in results:
        ingredients = row[0]
        all_ingredients.update(ingredients.split(', '))
    
    list_ingredients = list(all_ingredients)

    for i, ingredient in enumerate(all_ingredients):
        print(f"{i} - {ingredient}")
    search_ingredient = int(input("Please select an ingredient from the list above: "))
    print("-"*50)
    search_ingredient = list_ingredients[search_ingredient]

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
    cursor.execute("SELECT name, cooking_time, ingredients FROM Recipes WHERE id = %s", (selection,))
    results= cursor.fetchall()
    print(f"Name: {results[0][0]}")
    print(f"Cooking time: {results[0][1]}")
    print(f"Ingredients: {results[0][2]}")
    print("-"*30)
    
    # A loop that allows the user to select the categories they wish and exit out when finished.
    print("From the list above, please type the category you would like to modify.")
    print("When you are done modifying this recipe, type 'quit'.")
    category = ''
    while(category != 'quit'):
        category = input("Category to modify: ").lower()
        if category == 'name':
            new_name = input_name()
            cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, selection))
        elif category == 'cooking time':
            new_cooking_time = input_cooking_time()
            cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_cooking_time, selection))
        elif category == 'ingredients':
            new_ingredients = input_ingredients()
            cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients, selection))
        else:
            print("Please type 'name', 'cooking time', 'ingredients', or 'quit'.")
    
    # Calculates and assings a new difficulty based on the updated information and saves all of the new data to the database.
    cursor.execute("SELECT name, cooking_time, ingredients FROM Recipes WHERE id = %s", (selection,))
    results = cursor.fetchall()
    updated_ingredients = results[0][2].rstrip()
    cooking_time = results[0][1]
    ingredients = updated_ingredients
    new_difficulty = calculate_difficulty(cooking_time, ingredients)
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
    conn.commit()

# A loop through which the user can choose between creating, searching for, updating, and deleting recipes.
def main_menu(conn, cursor):
    print("-"*50)
    choice = ''
    while(choice != 'quit'):
        print("What would you like to do?")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient.")
        print("3. Modify an existing recipe.")
        print("4. Delete a recipe.")
        print("Type 'quit' to exit the program.")
        choice = input("Your choice: ")
        print("-"*50)

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
cursor.close()
conn.close()
print('Resources cleaned. Goodbye!')