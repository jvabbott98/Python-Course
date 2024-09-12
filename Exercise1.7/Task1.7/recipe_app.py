from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base



engine = create_engine(f"mysql+pymysql://cf-python:password@localhost/task_database")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"Recipe ID: {str(self.id)} - {str(self.name)} - {str(self.difficulty)}"
    
    def __str__(self):
        print('_'*50)
        print('Recipe: ', str(self.name))
        print('Recipe ID: ', str(self.id))
        print('Cooking time: ', str(self.cooking_time))
        print('Ingredients: ', str(self.ingredients))
        print('Difficulty: ', str(self.difficulty))
        print('-'*50)

    # Determines difficulty based on number of ingredients and cooking time
    def calculate_difficulty(self):
        ingredients = list(self.ingredients.split(", "))
        if self.cooking_time < 10:
            if len(ingredients) < 4:
                self.difficulty = 'Easy'
            else:
                self.difficulty =  'Medium'
        else:
            if len(ingredients) < 4:
                self.difficulty = 'Intermediate'
            else:
                self.difficulty = 'Hard'
        session.commit()

    def return_ingredients_as_list(self):
        if self.ingredients:
            return self.ingredients.split(', ')
        else:
            return []
    Base.metadata.create_all(engine)

# Takes name of recipe from user an makes sure its is alphanumeric.
def input_name():
    name_input = input("Recipe name: ")
    while name_input.isalpha() == False or len(name_input) < 1 or len(name_input) > 50:
        print('Please enter a name of type string that is less than 50 characters in length.')
        name_input = input('Recipe name: ')
    return name_input

# Takes cooking time from the user and makes sure it is an integer.
def input_cooking_time():
    cooking_time_input = input("Cooking time: ")
    while cooking_time_input.isnumeric() == False:
        print('Your response must be an integer.')
        cooking_time_input = input('Cooking time: ')
    return int(cooking_time_input)

# Asks user how many ingredients they would like to enter and takes them one by one.
def input_ingredients():
    ingredients = []
    number_of_ingredients = int(input('How many ingredients would you like to enter? Please type the number here: '))
    for i in range(number_of_ingredients):
        ingredient = input("Enter an ingredient: ")
        ingredients.append(ingredient)
    ingredients_string = ', '.join(ingredients)
    return ingredients_string

# Creates a recipe and adds it to the table.
def create_recipe():
    name_input = input_name()
    recipe_tuples = session.query(Recipe.name).all()
    recipe_list = [recipe[0].lower() for recipe in recipe_tuples]
    if name_input.lower() in recipe_list:
        print('Recipe already exists.')
        return None
    else:
        cooking_time_input = input_cooking_time()
        ingredients_input = input_ingredients()

        recipe_entry = Recipe(
            name = name_input,
            cooking_time = cooking_time_input,
            ingredients = ingredients_input
        )
        recipe_entry.calculate_difficulty()
        session.add(recipe_entry)
        session.commit()

# Displays all recipes in the table.
def view_all_recipes():
    if session.query(Recipe).all():
        recipe_list = session.query(Recipe).all()
        for recipe in recipe_list:
            recipe.__str__()
    else:
        print("There are no entries in this database.")
        return None

# Displays recipes that contain ingredients that the user selects.
def search_by_ingredients():
    search_ingredients = []
    if session.query(Recipe).count() < 1:
        print("There are no entries in this table.")
        return None
    else:
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []
        for tuple in results:
            item_list = tuple[0].split(', ')
            for item in item_list:
                if item not in all_ingredients:
                    all_ingredients.append(item)
        i = 1
        print('-'*50)
        for ingredient in all_ingredients:
            print(f"{i} - {ingredient}")
            i += 1
        print('-'*50)
        user_selection = input("Select ingredients from the list above by typing their corresponding numbers seperated by commas: ")
        user_selection = list(user_selection.split(', '))
        for number in user_selection:
            if int(number) > len(all_ingredients) or int(number) < 1:
                print("User selection does not match any of the listed ingredients.")
            else:
                search_ingredients.append(all_ingredients[int(number) - 1])
        conditions = []
        for ingredient in search_ingredients:
            like_term = f"%{ingredient}%"
            conditions.append(like_term)
        for condition in conditions:
            fetched_recipes = session.query(Recipe).filter(Recipe.ingredients.like(condition)).all()

            for recipe in fetched_recipes:
                recipe.__str__()

# Allows the user to change name, cooking_time, or ingredients of a recipe and calculates a new difficulty.
def edit_recipe():
    if session.query(Recipe).all():
        recipe_list = session.query(Recipe).all()
        results = []
        ids = []
        for recipe in recipe_list:
            id_and_name = []
            id_and_name.append(recipe.id)
            ids.append(recipe.id)
            id_and_name.append(recipe.name)
            results.append(id_and_name)
        print('-'*50)
        for result in results:
            print(f"{result[0]} - {result[1]}")
        print('-'*50)
        user_selection = int(input("Please select a recipe to edit by typing its id number: "))
        if user_selection not in ids:
            print("Chosen id does not exist.")
            return None
        else:
            edit_input = ''
            while edit_input != 'quit':
                recipe_to_edit = session.query(Recipe).get(user_selection)
                print("-"*50)
                print('1. Name: ', recipe_to_edit.name)
                print('2. Cooking Time: ', recipe_to_edit.cooking_time)
                print('3. Ingredients: ', recipe_to_edit.ingredients)
                print("-"*50)
                edit_input = input("Select the attribute you would like to edit by typing the corresponding number from the list above, or type 'quit' to return to the main-menu:  ")
                if edit_input == '1':
                    session.query(Recipe).filter(Recipe.id == recipe_to_edit.id).update({Recipe.name: input_name()})
                elif edit_input == '2':
                    session.query(Recipe).filter(Recipe.id == recipe_to_edit.id).update({Recipe.cooking_time: input_cooking_time()})
                elif edit_input =='3':
                    session.query(Recipe).filter(Recipe.id == recipe_to_edit.id).update({Recipe.ingredients: input_ingredients()})
            edited_recipe = session.query(Recipe).get(user_selection)
            edited_recipe.calculate_difficulty()
            
# IMPLEMENT CALCULATE DIFFICULTY HERE

    else:
        print("There are no recipes in this database.")
    session.commit()

# Deletes recipe of the user's choice.
def delete_recipe():
    if session.query(Recipe).all():
        recipe_list = session.query(Recipe).all()
        results = []
        ids = []
        for recipe in recipe_list:
            id_and_name = []
            id_and_name.append(recipe.id)
            ids.append(recipe.id)
            id_and_name.append(recipe.name)
            results.append(id_and_name)
        print('-'*50)
        for result in results:
            print(f"{result[0]} - {result[1]}")
        print('-'*50)
        user_selection = int(input("Please select a recipe to delete by typing its id number: "))
        if user_selection not in ids:
            print("Chosen id does not exist.")
            return None
        else:
            recipe_to_delete = session.query(Recipe).get(user_selection)
            print('-'*50)
            print('Name: ', recipe_to_delete.name)
            print('Cooking time: ', recipe_to_delete.cooking_time)
            print('Ingredients: ', recipe_to_delete.ingredients)
            print('-'*50)
            yes_no = input("Are you sure you would like to delete the above recipe? If yes type 'yes', if no type 'no': ")
            if yes_no == 'yes':
                session.delete(recipe_to_delete)
                session.commit()
            else:
                print('Recipe will not be deleted.')
                return None

    else:
        print('There are no entries in this database.')
        return None

# Runs a loop that acts as the primary interface with the user.
def main_menu():
    user_selection = ''
    while user_selection != 'quit':
        print('-'*50)
        print('1 - Create a recipe.')
        print('2 - View all recipes.')
        print('3 - Search for recipes by ingredients')
        print('4 - Edit a recipe.')
        print('5 - Delete a recipe.')
        print('Type "quit" to exit the program.')
        print('-'*50)

        user_selection = input('Select an option from the list above by typing the corresponding number: ')

        if user_selection == '1':
            create_recipe()
        elif user_selection == '2':
            view_all_recipes()
        elif user_selection == '3':
            search_by_ingredients()
        elif user_selection == '4':
            edit_recipe()
        elif user_selection == '5':
            delete_recipe()
        elif user_selection =='quit':
            return
        else:
            print('Please type "1", "2", "3", "4", "5", or "quit"')
    session.close()
    engine.close()

main_menu()







