class Recipe(object):
    all_ingredients = []
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = None
        self.difficulty = None
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_cooking_time(self):
        return self.cooking_time
    def set_cooking_time(self, time):
        self.cooking_time = int(time)
    def add_ingredients(self, *args):
        self.ingredients.extend(list(args))
        self.update_all_ingredients()
    def get_ingredients(self):
        return self.ingredients
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
    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
    def __str__(self):
        self.get_difficulty()
        output = f"{self.name}\nCooking Time: {self.cooking_time}\nIngredients: "
        for ingredient in self.ingredients:
            output += ingredient + '\n'
        output += f"Difficulty: {self.difficulty}\n" + 30*'-'
        return output
    def recipe_search(data, search_term):
        for recipe in data:
            try:
                if recipe.search_ingredient(search_term):
                    print(recipe)
            except:
                print("No recipe with that ingredient could be found.")


tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)


coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Poweder', 'Sugar', 'Water')
coffee.set_cooking_time(5)


cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)


banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)


recipes_list = [tea, coffee, cake, banana_smoothie]


for ingredient in ['Water', 'Sugar', 'Bananas']:
    print(f"\n***Contains {ingredient}***\n ")
    Recipe.recipe_search(recipes_list, ingredient)



    
        
