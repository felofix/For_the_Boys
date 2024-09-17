import numpy as np 
import mysql.connector
import FindMealPlanPrice as fmpp
import Levenshtein  # Importing Levenshtein for string comparison
import User as u

# Connect to MySQL database
conn = mysql.connector.connect(
	host="localhost",
	user="root",
	password="kostnation69",
	database="recipes_database"
)

conn_ing = mysql.connector.connect(
	host="localhost",
	user="root",
	password="kostnation69",
	database="ingredients"
)
"""
TBA:

A check to see if an item is a dinner item or not, discard if not dinner item. 

"""

# 1 and 2. 
def create_ingredient_vector():
	names = []
	prices = []
	maxxer = []

	cursor = conn_ing.cursor()
	
	# Query to select name and price from the products table
	query = "SELECT name, price, amount FROM products"
	
	cursor.execute(query)
	rows = cursor.fetchall()
		
	# Print each entry
	for row in rows:
		try: 
			if row[2].split(" ")[0] != "None":
				prices.append(float(row[1]))
				names.append(row[0])
				maxxer.append(row[2].split(" ")[0])

		except:
			continue
			
	cursor.close()

	

	return np.array(names), np.array(prices), np.array(maxxer,dtype=float)

def find_cheapest_ingredient(search):
	prices = search[:, 2]
	# Assuming prices is your list
	cleaned_prices = []

	for price in prices:
		try:
			cleaned_prices.append(float(price))
		except ValueError:
			# Skip elements that cannot be converted to float
			continue

	# Now find the minimum price from the cleaned list
	cheapest = np.min(np.array(cleaned_prices))
	where = np.argwhere(np.array(cleaned_prices) == cheapest)[0][0]
	name = search[where][1]

	return name

def find_closest_ingredient(search, ingredient):
	closest_match = None
	closest_distance = float('inf')

	for result in search:
		distance = Levenshtein.distance(result[1], ingredient)
		
		if distance < closest_distance:
			closest_distance = distance
			closest_match = result

	if closest_distance < 5:
		return closest_match[1]
	else:
		return None

def create_recipe_vector(ingredients_names, user):
	"""
	Will need sparse matrices when the matrix becomes to big. 
	"""
	recepies = []
	instructions = []
	titles = []

	# Create a cursor object
	cursor = conn.cursor()
	cursor_ing = conn_ing.cursor()

	if user.is_vegetarian:
		query = "SELECT title, ingredient_search, grams, instructions FROM recipe_data_siloed WHERE category = 'vegetar';"
	else:
		query = "SELECT title, ingredient_search, grams, instructions FROM recipe_data_siloed;"  # No filter applied

	# Execute the query
	cursor.execute(query)

	# Fetch all recipes and their ingredients
	recipes = cursor.fetchall()

	# Make sure non_wanted recepies are removed from the search
	if user.non_wanted_recipies:recipes = [recipe for recipe in recipes if recipe[0] not in user.non_wanted_recipies]

	if len(recipes) > 1000:
		print("USE SPARSE MATRICES.")
		print("Make sure instructions vectors arnt too big. ")

	# Loop through the results and print the title and ingredients of each recipe
	counter = 0
	for recipe in recipes:
		title = recipe[0]
		titles.append(title)
		instruction = recipe[3]
		instructions.append(instruction)
		ingredients = recipe[1]  # Recipe ingredients
		amount = recipe[2][1:-1]
		amounts_array = np.fromstring(amount, sep=',')
		new_recipe = np.zeros(len(ingredients_names))
		c = 0
		#print(counter)
		# Assuming ingredients are stored as a list, separated by commas or newlines
		for ingredient in ingredients.split(","):  # Modify the separator if necessary
			ingredient = ingredient.lstrip()
			cursor_ing.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + ingredient + '%',))

			search = cursor_ing.fetchall()
			if ingredient == "":
				c+= 1
				continue

			if len(search) != 0:
				name = find_closest_ingredient(search, ingredient)
				if name != None: 
					ingredient_idx = np.argwhere(ingredients_names == name)[0][0]
					new_recipe[ingredient_idx] = amounts_array[c]

			else:
				cursor_ing.execute("SELECT * FROM products")
				all_ingredients = cursor_ing.fetchall()
				name = find_closest_ingredient(all_ingredients, ingredient)

				if name != None:
					ingredient_idx = np.argwhere(ingredients_names == name)[0][0]
					new_recipe[ingredient_idx] = amounts_array[c]

			c += 1

		counter += 1
		recepies.append(new_recipe)

	# Close the connection
	cursor.close()
	cursor_ing.close()
	conn.close()
	conn_ing.close()

	return np.array(recepies), np.array(instructions), np.array(titles)

def test_recipe(title):
	"""
	Testing the searching and locating of recipe. 
	Need to have a max amount, which is how many grams in the whole thing. 
	I might have that. So its simple:
	If there is a max, then if it is over that limit a new one has to be bought.
	If no max, then you can buy as much as you want.
	"""

	cursor = conn.cursor()
	cursor_ing = conn_ing.cursor()

	# Correct query execution
	query = "SELECT * FROM recipe_data_siloed WHERE title = %s"
	cursor.execute(query, (title,))

	# Fetch the results after executing the query
	result = cursor.fetchall()

	print(result) 

	# Close the cursor and connection after processing the results
	cursor.close()
	cursor_ing.close()
	conn.close()
	conn_ing.close()

def create_vectors(user):
	"""
	For now it just chooses the cheapest product. 
	
	"""
	names, prices, maxxer = create_ingredient_vector()
	recepies, instructions, titles = create_recipe_vector(names, user)

	return prices, recepies, names, instructions, titles, maxxer

def return_information(recepies, best_plan, names, instructions, prices, titles, maxxer):
	"""
	Returns:
	- Ingredient names.
	- Instructions.
	- Buying amounts. 
	"""
	buying_amounts = np.zeros(len(recepies[0]))

	for recipe in best_plan:
		buying_amounts += recepies[recipe]

	ingredients = np.where(buying_amounts != 0)[0]

	finished_ingredients = []
	finished_amounts = []
	finished_instructions = []
	finished_prices = []
	finished_titles = []
	
	# Printing information.
	for i in range(len(ingredients)):
		finished_ingredients.append(names[ingredients[i]])
		finished_amounts.append(np.ceil(buying_amounts[ingredients][i]/maxxer[ingredients[i]]))
		finished_prices.append(finished_amounts[i]*prices[ingredients][i])

	unique = np.unique(best_plan)

	for u in unique:
		finished_instructions.append([instructions[u]])
		finished_titles.append(titles[u])
	
	for i in range(len(finished_prices)):
		print(f'{finished_ingredients[i]} x {finished_amounts[i]} = {finished_prices[i]}')

	print(finished_ingredients)
	print(best_plan)
	print(finished_instructions)
	
	
	return finished_ingredients, finished_amounts, finished_instructions
	
# Creating test user.
user_test = u.User(
    name="odeau",
    is_vegetarian=True,
    non_repeating=True,  # User flag for non-repeating recipes
    non_wanted_recipies=[1, 2]  # Replace with actual recipe titles
)

# Creating vectors
prices, recepies, names, instructions, titles, maxxer = create_vectors(user_test)

# Finding meal plan, passing the user's non_repeating preference
findit = fmpp.FindMealplanPrice(recepies, prices, maxxer, non_repeating=user_test.non_repeating)
evolved, pop_fitness, minn = findit.evolve(10, 10000, 5, 1000)

minimum_price = np.min(pop_fitness)
minimum_recipe = evolved[np.where(pop_fitness == minimum_price)]
best_plan = minimum_recipe[0] 
ingredients, amounts, instructions = return_information(recepies, best_plan, names, instructions, prices, titles, maxxer)


#test_recipe("Kikertgryte med oregano og tomat")

