import mysql.connector
import numpy as np
from tqdm import tqdm
from deep_translator import GoogleTranslator

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host name or IP address
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="ingredients"  # Replace with the name of your MySQL database
)

def add_product(name, price, amount, preprice, store, typ, english):
	# Check if the product already exists in the "products" table
	
	product_data = (name, price, amount, preprice, store, typ, english)

	try:
		cursor.execute("""
		    INSERT INTO products (name, price, amount, before_price, store, type, english)
		    VALUES (%s, %s, %s, %s, %s, %s, %s)
		""", product_data)
		conn.commit()  # Commit the changes to the database
	except mysql.connector.Error:
		pass

# Create a cursor object to interact with the database
ingredient_type = ["dinner", "drink", "dinner", "dinner", "dinner", "dinner", "breakfast", "dessert", "dinner", "dinner", "snacks", "dinner", "dinner"]
cursor = conn.cursor()


with open("meny/metadata.txt") as categories:
	count = 0
	documents = categories.readlines()
	for document in documents:
		with open("meny/" + document.split("\n")[0]) as test:
			lines = test.readlines()[1:]
			for line in lines:
				splitline = line.split(",")
				name = splitline[0]
				price = splitline[1]
				amount = splitline[2]
				preprice = splitline[3]
				butikk = splitline[4].split('\n')[0]
				typ = ingredient_type[count]
				if typ == "dinner":
					english = GoogleTranslator(source='no', target='en').translate(f"{name}")
					add_product(name, price, amount, preprice, butikk, typ, english)
				else:
					add_product(name, price, amount, preprice, butikk, typ, None)
		print(count)
		count += 1

conn.commit()

# Close the cursor and database connection
cursor.close()
conn.close()
