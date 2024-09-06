import mysql.connector
from getpass import getpass
import numpy as np
import nltk
from nltk.corpus import wordnet

#passw = getpass()

# Connect to MySQL database
conn_res = mysql.connector.connect(
  host="localhost",
  user="root",
  password="western12345",
  database="recipes_db"
)

# Connect to the MySQL database
conn_ing = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host name or IP address
    user="root",  # Replace with your MySQL username
    password="western12345",  # Replace with your MySQL password
    database="ingredients"  # Replace with the name of your MySQL database
)

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)

def find_similar_ingredients(ingredient):
    similar_ingredients = []
    for syn in get_synonyms(ingredient):
        similar_ingredients.extend(get_synonyms(syn))
    return set(similar_ingredients)


cursor_res = conn_res.cursor()
cursor_ing = conn_ing.cursor()
cursor_res.execute("SELECT * FROM recipes")


# Fetch all the rows and print them
recipies = cursor_res.fetchall()
perfect = 0
notperfect = 0

for recipe in recipies:
	eng_ing = eval(recipe[-2])	
	finds = 0
	unfinds = 0

	if len(eng_ing) < 1:
		continue
	
	for ingredient in eng_ing:
		try:
			cursor_ing.execute("SELECT * FROM products WHERE {} LIKE '%{}%'".format("english", ingredient))
			search = cursor_ing.fetchall()

			if len(search) == 0:
				similar_ingredients = list(find_similar_ingredients(ingredient.split()[-1]))
				found = False

				for similar in similar_ingredients:
					cursor_ing.execute("SELECT * FROM products WHERE {} LIKE '% {} %'".format("english", similar)) # Doing strict search, shoudl do smarter regex search I guess. 
					newsearch = cursor_ing.fetchall()

					if len(newsearch) > 0:
						finds += 1
						print(similar, ingredient)
						found = True
						break

				if not found:
					unfinds += 1

			else:
				finds += 1

		except mysql.connector.Error:
			pass

# Commit the changes and close the connection
cursor_res.close()
cursor_ing.close()
conn_res.close()
conn_ing.close()
