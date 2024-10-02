import mysql.connector
import subprocess

#Deletes all entries. 
# Connect to MySQL database
conn = mysql.connector.connect(
	host="localhost",
	user="root",
	password="western12345",
	database="recipes_databaze"
)

# Connect to the MySQL database
conn_ingr = mysql.connector.connect(
	host="localhost",
	user="root",
	password="western12345",
	database="ingredients"
)

# Create a cursor object
cursor = conn.cursor()

def delete_all_entries():
	# Create a cursor object
	cursor = conn.cursor()

	# Delete all entries in the recipes_data_siloed table
	delete_query = "DELETE FROM recipe_data_siloed"
	cursor.execute(delete_query)
	conn.commit()  # Commit the changes

	# Check if the table is empty by selecting all entries
	select_query = "SELECT * FROM recipe_data_siloed"
	cursor.execute(select_query)
	results = cursor.fetchall()

	# Print results to confirm deletion
	if not results:
		print("All entries in 'recipes_data_siloed' have been successfully deleted.")
	else:
		print("There are still some entries in the 'recipes_data_siloed' table:")
		for row in results:
			print(row)

	# Close the cursor and connection
	cursor.close()
	conn.close()

# Assuming 'conn' is your database connection object
def find_recipes(recipes_to_search):
	# Create a cursor object
	cursor = conn.cursor()

	# Create a query to search for the recipes in the list
	# Using placeholders for parameterized query
	search_query = """
	SELECT * FROM recipe_data_siloed 
	WHERE title IN (%s)
	""" % ', '.join(['%s'] * len(recipes_to_search))

	# Execute the search query with the recipes_to_search list
	cursor.execute(search_query, recipes_to_search)
	search_results = cursor.fetchall()

	# Print the search results
	if search_results:
		print("Recipes found in 'recipe_data_siloed' table:")
		for row in search_results:
			print(row)
	else:
		print("No matching recipes found in the 'recipe_data_siloed' table.")

	# Close the cursor and connection
	cursor.close()
	conn.close()

def delete_recipe_by_title(conn, title):
	"""
	Delete a recipe entry from the 'recipe_data_siloed' table based on the recipe title.

	Parameters:
	conn (object): The database connection object.
	title (str): The title of the recipe to be deleted.

	Returns:
	str: A message indicating the result of the deletion.
	"""
	cursor = conn.cursor()

	# Delete query with parameterized input to avoid SQL injection
	delete_query = "DELETE FROM recipe_data_siloed WHERE title = %s"

	# Execute the delete query
	cursor.execute(delete_query, (title,))

	# Commit the changes
	conn.commit()

	# Check if any rows were affected
	if cursor.rowcount > 0:
		result = f"The recipe '{title}' has been successfully deleted."
	else:
		result = f"No recipe with the title '{title}' was found in the table."

	# Close the cursor
	cursor.close()

def update_ingredient_in_recipe(conn, title, old_ingredient, new_ingredient):
	"""
	Update a specific ingredient in a recipe with a given title.

	Parameters:
	conn (object): The database connection object.
	title (str): The title of the recipe where the ingredient needs to be updated.
	old_ingredient (str): The ingredient to be replaced.
	new_ingredient (str): The new ingredient to replace the old one.

	Returns:
	str: A message indicating the result of the update operation.
	"""
	# Create a cursor object
	cursor = conn.cursor()

	# SQL query to update the ingredient in the recipe
	update_query = """
	UPDATE recipe_data_siloed
	SET ingredient_search = REPLACE(ingredient_search, %s, %s)
	WHERE title = %s
	"""

	# Execute the update query
	cursor.execute(update_query, (old_ingredient, new_ingredient, title))

	# Commit the changes
	conn.commit()

	# Check if any rows were affected
	if cursor.rowcount > 0:
		result = f"The ingredient '{old_ingredient}' has been successfully replaced with '{new_ingredient}' in the recipe '{title}'."
	else:
		result = f"No matching recipe found for title '{title}' or no change needed."

	# Close the cursor
	cursor.close()

	return result

def update_ingredient_amount(conn, name, new_amount):
	"""
	Update the amount of a specific ingredient in a recipe with a given title.

	Parameters:
	conn (object): The database connection object.
	title (str): The title of the recipe where the ingredient amount needs to be updated.
	ingredient (str): The ingredient whose amount needs to be updated.
	new_amount (float): The new amount for the specified ingredient.

	Returns:
	str: A message indicating the result of the update operation.
	"""
	# Create a cursor object
	cursor = conn.cursor()

	# SQL query to update the amount of the ingredient in the recipe
	update_query = """
	UPDATE products
	SET price = %s
	WHERE name = %s"""

	# Execute the update query
	cursor.execute(update_query, (new_amount, name))

	# Commit the changes
	conn.commit()

	# Check if any rows were affected
	if cursor.rowcount > 0:
		result = f"The amount of ingredient '{name}' has been successfully updated to {new_amount}'."
	else:
		result = f"No matching recipe found for title '{name}' or no change needed."

	# Close the cursor
	cursor.close()

	return result

def print_all_recipe_names(conn):
	"""
	Queries and prints all recipe names from the 'recipe_data_siloed' table.

	Parameters:
	conn: A database connection object.
	"""
	try:
		# Create a cursor object to interact with the database
		cursor = conn.cursor()
		
		# Query to select all recipe names from the table
		query = "SELECT title FROM recipe_data_siloed;"
		cursor.execute(query)
		
		# Fetch all results
		recipes = cursor.fetchall()
		
		# Print out each recipe name
		for recipe in recipes:
			print(recipe[0])  # Assuming recipe_title is the first column in the result
		
	except Exception as e:
		print(f"An error occurred: {e}")
	finally:
		cursor.close()

import mysql.connector
import os
import json
import difflib


def find_closest_ingredient(search_results, ingredient):
	# Extract product names from search results
	product_names = [row[1] for row in search_results]  # Assuming 'name' is at index 1

	# Use difflib to find the closest match
	closest_matches = difflib.get_close_matches(ingredient, product_names, n=1, cutoff=0.6)
	if closest_matches:
		return closest_matches[0]
	else:
		return None

def manual_recipe_fix(ingredient_search, title, instructions, filename):
	cursor_ing = conn_ingr.cursor()

	while True:
		# Write the ingredients, instructions, and title to the file
		with open(filename, 'w') as file:
			for ingredient in ingredient_search:
				ingredient = ingredient.strip()  # Strip leading and trailing whitespace

				cursor_ing.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + ingredient + '%',))
				search = cursor_ing.fetchall()
				closest = find_closest_ingredient(search, ingredient)

				# Write the ingredient and the closest match to the file
				file.write(f"{ingredient},{closest}\n")

			file.write("\n")  # New line to separate ingredients from instructions

			# Write each instruction on a new line
			for instruction in instructions:
				file.write(f"{instruction}\n")

			file.write("\n")  # New line to separate instructions from the title

			# Write the title
			file.write(title)

		# Prompt the user
		user_input = input("Please review and modify the file. Type 'done' to re-read the file, or 'finished' to exit: ").strip().lower()

		if user_input == "finished":
			print("Exiting the manual recipe fix process.")
			break

		if user_input == "done":
			# Read the file back into the lists
			new_ingredient_search = []
			new_instructions = []
			new_title = ""

			with open(filename, 'r') as file:
				lines = file.readlines()
				i = 0
				# Read ingredients (until we reach a blank line)
				while i < len(lines) and lines[i].strip():
					# Get the value after the comma (new ingredient)
					parts = lines[i].strip().split(',')
					if len(parts) >= 2:
						_, new_ingredient = parts
						new_ingredient_search.append(new_ingredient.strip())
					else:
						print(f"Invalid line in ingredients: {lines[i]}")
					i += 1

				# Skip the blank line
				i += 1

				# Read instructions (until we reach another blank line)
				while i < len(lines) and lines[i].strip():
					new_instructions.append(lines[i].strip())
					i += 1

				# Skip the blank line
				i += 1

				# Read the title (it should be the last line)
				if i < len(lines):
					new_title = lines[i].strip()

			# Display the new values
			print("Updated Ingredients:", new_ingredient_search)
			print("Updated Instructions:", new_instructions)
			print("Updated Title:", new_title)

			# Perform a new search with the updated ingredients
			print("\nPerforming a new search with the updated ingredients...\n")
			for new_ingredient in new_ingredient_search:
				cursor_ing.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + new_ingredient + '%',))
				new_search = cursor_ing.fetchall()
				closest = find_closest_ingredient(new_search, new_ingredient)

				if new_search:
					if closest is None:
						print("No exact close match found. Here are some options:")
						for search in new_search:
							print(search[1])  # Assuming 'name' is at index 1
					else:
						print(f"Found matches for '{new_ingredient}': {closest}")
				else:
					print(f"No matches found for '{new_ingredient}'.")

			# Update the original lists with the new data
			ingredient_search = new_ingredient_search
			instructions = new_instructions
			title = new_title

	cursor_ing.close()

	if os.path.exists(filename):
		os.remove(filename)
		print(f"File '{filename}' has been deleted.")
	else:
		print(f"File '{filename}' does not exist.")

def process_recipes():
	cursor = conn.cursor()
	cursor.execute("SELECT id, ingredient_search, title, instructions FROM recipe_data_siloed")
	recipes = cursor.fetchall()

	for recipe in recipes:
		recipe_id = recipe[0]
		ingredient_search = recipe[1]
		title = recipe[2]
		instructions = recipe[3]

		# Parse 'ingredient_search' into a list
		# Try to parse as JSON first
		try:
			ingredient_list = json.loads(ingredient_search)
			if not isinstance(ingredient_list, list):
				ingredient_list = [ingredient_search]
		except json.JSONDecodeError:
			# Not JSON, split by commas
			ingredient_list = [ing.strip() for ing in ingredient_search.split(',')]

		# Similarly parse 'instructions'
		try:
			instruction_list = json.loads(instructions)
			if not isinstance(instruction_list, list):
				instruction_list = [instructions]
		except json.JSONDecodeError:
			# Not JSON, split by periods
			instruction_list = [instr.strip() for instr in instructions.split('.') if instr.strip()]

		# Generate a filename, e.g., 'recipe_{id}.txt'
		filename = f'recipe_{recipe_id}.txt'

		# Call manual_recipe_fix
		manual_recipe_fix(ingredient_list, title, instruction_list, filename)

	cursor.close()

def save_database_as_sql(host, user, password, database, output_file):
	try:
		# Command to dump the database into a .sql file
		dump_command = [
			'mysqldump',
			'-h', host,
			'-u', user,
			f'-p{password}',  # Using f-string to include the password (no space between -p and password)
			database
		]
		
		# Open the output file and run the command to save the dump
		with open(output_file, 'w') as output:
			subprocess.run(dump_command, stdout=output)
		
		print(f"Database saved successfully as {output_file}")
		
	except Exception as e:
		print(f"An error occurred: {e}")

# Usage example
save_database_as_sql(
	host="localhost",
	user="root",
	password="western12345",
	database="recipes_databaze",
	output_file="recipes_databaze_backup.sql"
)

