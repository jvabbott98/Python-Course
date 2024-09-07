class Recipe(object):
    all_ingredients = set()

    # Initialize the object with name, cooking_time, ingredients then calculates difficulty.
    def __init__(self, name, cooking_time, ingredients):
        self.name = name
        self.ingredients = [ingredient.lower() for ingredient in ingredients]
        self.cooking_time = cooking_time
        self.difficulty = None
        self.calculate_difficulty()
        self.update_all_ingredients()

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_cooking_time(self):
        return self.cooking_time
    def set_cooking_time(self, time):
        self.cooking_time = int(time)
    
    # Accepts a variable number of arguments and adds those arguments to the recipe's set of ingredients.
    # Updates the class variable all_ingredients
    def add_ingredients(self, *ingredients):
        ingredients = [ingredient.lower() for ingredient in ingredients]
        self.ingredients.update(ingredients)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients
    
    # Calculates a recipe's difficulty based off of cooking time and number of ingredients.
    def calculate_difficulty(self):
        if self.cooking_time < 10:
            if len(self.ingredients) < 4:
                self.difficulty = 'Easy'
            else:
                self.difficulty = 'Medium'
        else:
            if len(self.ingredients)< 4:
                self.difficulty = 'Intermediate'
            else:
                self.difficulty = 'Hard'
    
    # Checks if a recipe has a difficulty set. If not, it calls calculate_diffculty() and returns the difficulty.
    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty

    # Returns True if ingredient is in self.ingredients. Else false.
    def search_ingredient(self, ingredient):
        ingredient = ingredient.lower()
        return ingredient in self.ingredients

    # Adds ingredients from the recipe to all_ingredients.
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)

        # for ingredient in self.ingredients:
        #     if ingredient not in Recipe.all_ingredients:
        #         Recipe.all_ingredients.set(ingredient)

    def __str__(self):
        self.get_difficulty()
        output = f"{self.name}\nCooking Time: {self.cooking_time}\nIngredients: \n"
        for ingredient in self.ingredients:
            output += ingredient + '\n'
        output += f"Difficulty: {self.difficulty}\n" + 30*'-'
        return output
    
    # Accepts a list of recipes and the name of an ingredient as parameters.
    # Goes through each recipe in the list of recipes and searches for the search_term.
    # On success, prints the recipe. On fail, prints an error message.
    def recipe_search(data, search_term):
        for recipe in data:
            try:
                if recipe.search_ingredient(search_term):
                    print(recipe)
            except:
                print("No recipe with that ingredient could be found.")


tea = Recipe('Tea', 5, ['Tea', 'Sugar', 'Water'])


coffee = Recipe('Coffee', 5, ['Coffee Grounds', 'Sugar', 'Water'])



cake = Recipe('Cake', 50, ['Sugar', 'Butter', 'Eggs', 'Vanilla', 'Flour', 'Baking Powder', 'Milk'])


banana_smoothie = Recipe('Banana Smoothie', 5, ['Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes'])



recipes_list = [tea, coffee, cake, banana_smoothie]


for ingredient in ['Water', 'Sugar', 'Bananas']:
    print(f"\n***Contains {ingredient}***\n ")
    Recipe.recipe_search(recipes_list, ingredient)



    
        
