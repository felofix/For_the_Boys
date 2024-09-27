import mysql.connector

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


"""
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="western12345",
    database="ingredients"
)

# Create a cursor object
cursor = conn.cursor()

# List of ingredients to search for
ingredient_list = ['tofu', 'sennep']

# Loop through each ingredient and perform the search
for ingredient in ingredient_list:
    # Prepare the SQL query to search for the ingredient in the products table
    query = "SELECT * FROM products WHERE name LIKE %s"
    cursor.execute(query, ('%' + ingredient + '%',))

    # Fetch all results that match the query
    results = cursor.fetchall()

    # Print the search results
    if results:
        print(f"Found matches for '{ingredient}':")
        for row in results:
            print(row)
    else:
        print(f"No matches found for '{ingredient}'.")

# Close the cursor and connection
cursor.close()
conn.close()
"""

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

print_all_recipe_names(conn)