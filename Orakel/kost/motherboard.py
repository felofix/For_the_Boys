import numpy as np 
import mysql.connector
import FindMealPlanPrice as fmpp
import Levenshtein  # Importing Levenshtein for string comparison
import User as u


# Connect to MySQL database
conn = mysql.connector.connect(
	host="localhost",
	user="root",
	password="western12345",
	database="recipes_databaze"
)

conn_ing = mysql.connector.connect(
	host="localhost",
	user="root",
	password="western12345",
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

	cursor = conn_ing.cursor()
	
	# Query to select name and price from the products table
	query = "SELECT name, price FROM products"
	
	cursor.execute(query)
	rows = cursor.fetchall()
		
	# Print each entry
	for row in rows:
		try: 
			prices.append(float(row[1]))
			names.append(row[0])
		except:
			continue
			
	cursor.close()

	return np.array(names), np.array(prices)

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

	return closest_match[1]

def create_recipe_vector(ingredients_names, user):
	"""
	Will need sparse matrices when the matrix becomes to big. 
	"""
	recepies = []

	# Create a cursor object
	cursor = conn.cursor()
	cursor_ing = conn_ing.cursor()

	if user.is_vegetarian:
		query = "SELECT title, ingredient_search, amounts FROM recipe_data_siloed WHERE category = 'vegetar';"
	else:
		query = "SELECT title, ingredient_search, amounts FROM recipe_data_siloed;"  # No filter applied

	# Execute the query
	cursor.execute(query)

	# Fetch all recipes and their ingredients
	recipes = cursor.fetchall()

	if len(recipes) > 1000:
		print("USE SPARSE MATRICES.")

	# Loop through the results and print the title and ingredients of each recipe
	counter = 0
	for recipe in recipes:
		ingredients = recipe[1]  # Recipe ingredients
		amount = recipe[2]
		amounts_array = np.fromstring(amount, sep=',')
		new_recipe = np.zeros(len(ingredients_names))
		c = 0
		print(counter)
		# Assuming ingredients are stored as a list, separated by commas or newlines
		for ingredient in ingredients.split(","):  # Modify the separator if necessary
			ingredient = ingredient.lstrip()
			cursor_ing.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + ingredient + '%',))
			
			search = cursor_ing.fetchall()
			if len(search) != 0:

				#name = find_cheapest_ingredient(np.array(search))
				name = find_closest_ingredient(search, ingredient)
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

	return np.array(recepies)

def create_vectors(user):
	"""
	For now it just chooses the cheapest product. 
	
	"""
	names, prices = create_ingredient_vector()
	recepies = create_recipe_vector(names, user)

	return prices, recepies, names

def display_shopping_list(recepies, best_plan, names):
	buying_amounts = np.zeros(len(recepies[0]))

	print(best_plan)

	for recipe in best_plan:
		buying_amounts += recepies[recipe]

	ingredients = np.where(buying_amounts != 0)[0]
	
	for i in range(len(ingredients)):
		print(f'{i}. {names[ingredients[i]]} x {buying_amounts[ingredients][i]}')

def return_information(recepies, best_plan, names):
	unique = set(best_plan)


# Creating test user.
user_test = u.User("odeau", is_vegetarian=True, is_repetitive=False)

# Creating vectors. 
prices, recepies, names = create_vectors(user_test)

# Finding meal plan. 
findit = fmpp.FindMealplanPrice(recepies, prices)
evolved, pop_fitness, minn = findit.evolve(10, 10000, 5, 1000)
minimum_price = np.min(pop_fitness)
minimum_recipe = evolved[np.where(pop_fitness == minimum_price)]
best_plan = minimum_recipe[0] 
#display_shopping_list(recepies, best_plan, names)
return_information(recepies, best_plan, names)
