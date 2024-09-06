import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from getpass import getpass
from deep_translator import GoogleTranslator
import re
import encoder as en
import mysql.connector


passw = getpass()

# Connect to MySQL database
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password=passw,
  database="recipes_db"
)

def get_recipies(url):
	driver = webdriver.Chrome()
	driver.get(url)
	links = driver.find_elements(By.ID, "allrecipes-schema_1-0")[0]
	html = links.get_attribute('innerHTML')
	urls = re.findall(r'"url":\s*"([^"]+)"', html)

	for url in range(len(urls)):
		get_recipe(urls[url])

def get_recipe(url):
	# Get hold of relevant information from a recipe ones on the recipe page.
	"""
	Input: String - Url of website to get information from.
	Returns: 
	- ingredients, list of strings containing english ingredients. 
	- instructions, list of strins containt english instructions.
	- total_time, string of english time.
	- servings, string number of serviings.
	
	# Need to write some code to check for fraction symbols. !!!
	"""
	driver = webdriver.Chrome()  # Make sure you have downloaded the Chrome driver and set its path
	driver.get(url)
	
	# What to return.
	total_time = None
	servings = None
	ingredients = []
	instructions = []
	nutrition = []

	# Extracting information from website. 
	title = driver.find_element(By.ID, "article-heading_1-0").text
	ingredients_s = driver.find_elements(By.CLASS_NAME, "mntl-structured-ingredients__list-item")
	cooking_info_s = [i.text for i in driver.find_elements(By.CLASS_NAME, "mntl-recipe-details__item")]
	nutrition_s = driver.find_elements(By.CSS_SELECTOR, "td.mntl-nutrition-facts-summary__table-cell.type--dog-bold")

	try:
		real_instrutions_s = driver.find_element(By.ID, "recipe__steps_1-0")
		instructions_s = real_instrutions_s.find_elements(By.CSS_SELECTOR,"p.comp.mntl-sc-block.mntl-sc-block-html")
	except NoSuchElementException:
		instructions_s = driver.find_elements(By.CSS_SELECTOR,"p.comp.mntl-sc-block.mntl-sc-block-html")

	# Extracting information.
	for item in cooking_info_s:
	    if 'Total Time:' in item:
	        total_time = decypther_time(item.split(':')[1].strip())
	    elif 'Servings:' in item:
	        servings = item.split(':')[1].strip()

	for ingredient in ingredients_s:
		ingredients.append(ingredient.text)

	for instruction in instructions_s:
		instructions.append(instruction.text)

	if len(nutrition_s) != 0:
		for i in range(4):
			types = ["Kalorier", "Fett", "Karbohydrater", "Protein"]
			nutrition.append(nutrition_s[i].text + " " + types[i])
	
	driver.close()

	print(title)

	NSA = en.find_type_ingredient(en.parse_all(ingredients), instructions)

	insert_database(title, NSA, instructions, total_time, servings, nutrition)

	return title, ingredients, instructions, total_time, servings, nutrition, NSA

def translate(instruction):
	# Transelate the instructions to norwegian.
	transelated = GoogleTranslator(source='en', target='no').translate(f"{instruction}")
	return transelated

def decypther_time(times):
	# Returns time and yeild in nowegian. 
	new_time = times.replace('hrs', 'timer')
	new_time = new_time.replace('mins', 'minutter')
	return new_time

def create_norwegian_ingredient(name, amount, unit, gram):
	grammer = {'ounce': '28.34', 'pound': '453.5', 'ounces': '28.34', 'pounds': '453.5'}
	fluid = {'cup': '2.5 ', 'fluid ounce': '0.3', 'cups': '2.5 ', 'fluid ounces': '0.3'}
	transelated = False

	# Removing multiples.
	if unit == None:
		unit = "stk"
		transelated = True

	if unit in grammer:
		amount = str(round(float(amount)*float(grammer[unit]))) + " g"
		unit = ""
		transelated = True

	if unit in fluid:
		amount = str(round(float(amount)*float(fluid[unit]))) + " dl"
		unit = ""
		transelated = True

	if unit != None and not transelated:
		if unit[-1] == 's':
			unit = unit[:-1]
			unit = GoogleTranslator(source='en', target='no').translate(f"{unit}") + "er"
		else:
			unit = GoogleTranslator(source='en', target='no').translate(f"{unit}")

	name = GoogleTranslator(source='en', target='no').translate(f"{name}")

	if name != None and amount != None:
		norw_ingredient = amount + " " + unit + " " + name
		return norw_ingredient

	else:
		return " "

def insert_database(title, NSA, instructions, total_time, servings, nutrition):
	# Insert the information into a database. 
	norw_title = GoogleTranslator(source='en', target='no').translate(f"{title}")
	norw_ingr_names = []
	english_ingr_names = []
	grams = []

	for i in range(len(NSA)):
		gram = NSA[i]['grams']
		norw_ingredient = create_norwegian_ingredient(NSA[i]['name'], NSA[i]['quantity'], NSA[i]['unit'], gram)
		norw_ingr_names.append(norw_ingredient)
		english_ingr_names.append(NSA[i]['name'])
		grams.append(gram)


	for i in range(len(instructions)):
		instructions[i] = str(i + 1) + ". " + GoogleTranslator(source='en', target='no').translate(f"{instructions[i]}")

	recipe_data = (norw_title, str(norw_ingr_names), str(instructions), total_time, servings, str(nutrition), str(english_ingr_names), str(grams))

	try:
		cursor.execute("""
			    INSERT INTO recipes (title, ingredients, instructions, total_time, servings, nutrition, english_ingredients, grams)
			    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
			""", recipe_data)
		conn.commit()  # Commit the changes to the database
	except mysql.connector.Error:
		pass

cursor = conn.cursor()
get_recipies("https://www.allrecipes.com/recipes/17562/dinner/")
conn.commit()
cursor.close()
conn.close()


