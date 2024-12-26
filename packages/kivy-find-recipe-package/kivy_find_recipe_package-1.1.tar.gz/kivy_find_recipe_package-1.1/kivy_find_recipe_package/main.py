from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import requests

# all variables needed for the API request
APIKey = ""
url = f"https://api.spoonacular.com/recipes/findByIngredients"
NRecipes = 20
IgnP = True

# function that calls the API and returns the recipes
def searchByIngredientsAPI(ingredients):
    paramss = {
        "ingredients": ingredients,
        "number": NRecipes,
        "ranking": 1,
        "ignorePantry": IgnP,
        "apiKey": APIKey
    }
    data = requests.get(url, params=paramss)
    recipes = data.json()
    if data.status_code == 200:
        return recipes
    else:
        return []
    
# class of the popup that shows the detailed recipe information, it isnt as big as I hopped, but this is all the useful information from the API
class RecipePopup(Popup):
    def __init__(self, recipe):
        super(RecipePopup, self).__init__()
        self.recipe = recipe
        self.ids.ImageR.add_widget(AsyncImage(source=recipe["image"]))
        self.ids.recipeName.text = recipe["title"]
        missing = ""
        for i in recipe["missedIngredients"]:
            missing += i["name"] + ", "
        if missing != "":
            self.ids.missingIngredients.text ="Missing ingredients: " + missing[:-2]

# class of the widget that shows the recipe in the main screen
class RecipeWidget(GridLayout):
    def __init__(self, recipe):
        super(RecipeWidget, self).__init__()
        self.recipe = recipe
        title = recipe["title"]
        if len(title) > 20:
            title = title[:20] + "..."
        self.ids.recipeName.text = title
        self.ids.ingredients.text = str(recipe["usedIngredientCount"]) + '/' + str(recipe["missedIngredientCount"] + recipe["usedIngredientCount"])
    def view(self):
        popup = RecipePopup(self.recipe)
        popup.open()

# class of the settings popup
class SettingsPopup(Popup):
    def __init__(self, caller):
        global APIKey, NRecipes, IgnP
        super(SettingsPopup, self).__init__()
        self.caller = caller
        self.ids.apiKeyInput.text = APIKey
        self.ids.numRecipesInput.text = str(NRecipes)
        self.ids.ignorePantry.active = IgnP
    def save(self):
        global APIKey, NRecipes, IgnP
        if self.ids.apiKeyInput.text != "":
            APIKey = self.ids.apiKeyInput.text
        if self.ids.numRecipesInput.text != "":
            NRecipes = int(self.ids.numRecipesInput.text)
        IgnP = self.ids.ignorePantry.active
        self.dismiss()

# class of the widget with the information of what the things in the recipe widget mean
class InfoWidget(GridLayout):
    pass

# class of the main grid
class MainGrid(GridLayout):
    def search(self):
        if self.ids.searchInput.text != "":
            self.recipes = searchByIngredientsAPI(self.ids.searchInput.text)
            if self.recipes != []:
                self.ids.errorLabel.size_hint = (1, 0)
                self.ids.errorLabel.text = ""
                self.ids.mealList.clear_widgets()
                self.ids.mealList.height = 60
                self.ids.mealList.add_widget(InfoWidget())
                for recipe in self.recipes:
                    self.ids.mealList.height += 50
                    self.ids.mealList.add_widget(RecipeWidget(recipe))
            else:
                self.ids.errorLabel.size_hint = (1, 0.1)
                self.ids.errorLabel.text = "There was an error with your request"
    def settings(self):
        popup = SettingsPopup(self)
        popup.open()

# class of the app
class FindMealsApp(App):
    def build(self):
        return MainGrid()

# running the app
def main():
    FindMealsApp().run()