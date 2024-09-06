import mysql.connector

# Connect to the MySQL database containing ingredients
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="western12345",
    database="ingredients"
)

def update_ingredients_to_grams():
    """
    Aubergine weight is 80, needs to be changed. 
    """

    cursor = conn.cursor(dictionary=True)

    # SQL query to select ingredients where the amount is '1 stk' and type is 'dinner'
    query = "SELECT id, name, amount FROM products WHERE amount = '1 stk' AND type = 'dinner'"

    try:
        # Execute the query
        cursor.execute(query)
        
        # Fetch all the ingredients with amount '1 stk' and type 'dinner'
        ingredients = cursor.fetchall()

        if ingredients:
            for ingredient in ingredients:
                print(f"Ingredient: {ingredient['name']}, Current Amount: {ingredient['amount']}")
                
                # Ask the user for the amount in grams
                while True:
                    try:
                        grams = float(input(f"Please enter the amount for {ingredient['name']} in grams: "))
                        break
                    except ValueError:
                        print("Invalid input, please enter a number.")
                
                # Update the ingredient amount in the database
                update_query = "UPDATE products SET amount = %s WHERE id = %s"
                cursor.execute(update_query, (f"{grams} grams", ingredient['id']))
                conn.commit()  # Commit the changes to the database
                
                print(f"Updated {ingredient['name']} to {grams} grams.")
        else:
            print("No dinner ingredients found with '1 stk' amount.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()


# Call the functions
#update_ingredients_to_grams()
update_aubergine_weight()
# Close the connection to the database
conn.close()