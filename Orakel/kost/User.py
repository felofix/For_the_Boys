import numpy 

class User:
    """
    Simple user class to hold user-specific meal plan preferences.
    """
    def __init__(self, name, is_vegetarian=False, non_repeating=False, non_wanted_recipies=None):
        self.name = name
        self.is_vegetarian = is_vegetarian
        self.non_repeating = non_repeating  # User flag for non-repeating recipes
        self.non_wanted_recipies = non_wanted_recipies if non_wanted_recipies else []  # User flag for unwanted recipes

    def __str__(self):
        repetition = ("Non-repeating" if self.non_repeating else "Repeating")
        return (f"User: {self.name}, "
                f"Vegetarian: {'Yes' if self.is_vegetarian else 'No'}, "
                f"Repetition: {repetition}, "
                f"Non-wanted Recipes: {self.non_wanted_recipies}")
