import json
import random
import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
import re
import mysql.connector
import time
from tqdm import tqdm

eng_norsk = {}

# Function to translate English words to Norwegian
def translate(word):
    if word in eng_norsk:
        return eng_norsk[word]  # If translation exists in dictionary, return it
    else:
        translat = GoogleTranslator(source='en', target='no').translate(f"{word}")
        eng_norsk[word] = translat
        return translat  # If translation doesn't exist, return an error message

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host name or IP address
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="ingredients"  # Replace with the name of your MySQL database
)

# Load Recipe1M+ dataset from JSON file
recipe_data = pd.read_csv("full_dataset.csv")

# Perform data processing and analysis
# For example, you can access recipe information from the loaded JSON data
random_integers = np.arange(100)

recipes = []

nr = 0


for i in tqdm(random_integers):
    steps = recipe_data.iloc[i]['directions']
    sentences = re.findall(r'"([^"]*)"', steps)

    ingrediets = recipe_data.iloc[i]['NER']
    ingr = re.findall(r'"([^"]*)"', ingrediets)
    ingrlen = len(ingr)

    conituehmm = 0
    continuefind = 0

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    for ingrediet in ingr:
        splitigr = ingrediet.split(" ")
        for singr in splitigr:
            if singr in steps:
                conituehmm += 1 
                break

    if ingrlen == 0:
        ingrlen = 0.1

    if conituehmm/ingrlen < 1:
        cursor.close()
        continue

    for ingrediet in ingr:

        translat = translate(ingrediet)

        # Execute a SELECT query to fetch one row from the 'products' table
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + translat + '%',))

        # Fetch the first row from the result cursor
        rows = cursor.fetchall()
        
        if len(rows) > 0:
            continuefind += 1

    if continuefind/ingrlen < 0.8:
        continue

    recipes.append(i)
    nr += 1

    title = recipe_data.iloc[i]['title']
    ingre = np.array(recipe_data.iloc[i]['ingredients'])
    print(ingre)
    steps = np.array(steps)
    print(steps)
    
# Close the cursor and database connection
conn.close()
print(nr)


