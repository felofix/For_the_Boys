import numpy as np
from User import User
from FindMealPlanPrice import FindMealplanPrice

if __name__ == "__main__":
    number_of_recipies = 10
    numb_of_ingredients = 100
    maxxer = np.ones(numb_of_ingredients)
    re = np.random.randint(0, 10, (number_of_recipies, numb_of_ingredients)) / 10
    prices = np.random.randint(1, 101, size=numb_of_ingredients)

    # Non-wanted recipes (e.g., 1, 2, and 3)
    non_wanted_recipies = [1,2,3]

    # Initialize the meal plan generator, excluding the non-wanted recipes
    mealplan = FindMealplanPrice(re, prices, maxxer, non_repeating=True, non_wanted_recipies=non_wanted_recipies)
    evolved, pop_fitness, minn = mealplan.evolve(50, 1000, 5, 100)

    if evolved is not None:
        # Get the best solution
        minimum_price = np.min(pop_fitness)
        minimum_recipe = evolved[np.argmin(pop_fitness)]
        print(f"Minimum Price: {minimum_price}")
        print(f"Selected Recipes: {minimum_recipe}")