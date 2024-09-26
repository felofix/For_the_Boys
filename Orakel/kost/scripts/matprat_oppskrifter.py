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
import json
import Levenshtein 
import os
import beepy

with open("../data/igr.txt", 'r', encoding='utf-8') as file:
    # Read file contents
    content = file.read()

    # Split by whitespace (space, newlines, etc.) into an array of strings
    igr_data = content.split()


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

def get_recipies(url):
	# Sort trough all recipies.
	return 0

def get_recipe(url, category = 'all'):
    # Get hold of relevant information from a recipe page.
    driver = webdriver.Chrome()  # Ensure you have downloaded the Chrome driver and set its path
    driver.get(url)
    
    # Initialize variables
    title = driver.find_element(By.CLASS_NAME, "article-title.lp_is_start").text
    ingredients_s = driver.find_elements(By.CLASS_NAME, "ingredientsList")
    amounts_s = driver.find_elements(By.CLASS_NAME, "amount")
    units_s = driver.find_elements(By.CLASS_NAME, "unit")
    portion_count = int(driver.find_element(By.ID, "portionsInput").get_attribute("value"))
    instructions_s = driver.find_elements(By.CLASS_NAME, "step-description")

    ingredient_names = []   # The actual names for the ingredient.
    ingredient_search = []  # The search that is used. 
    instructions = []
    amounts = []
    units = []
    grams = []
    
    # Extract instructions
    for i in instructions_s:
        instructions.append(i.text)

    if len(instructions) == 0:
        return
    
    ingr_count = 0
    
    # Extract ingredients, amounts, and units
    for i in ingredients_s:
        splitingr = i.text.split("\n")
        
        if splitingr[0] == '':
            continue
        
        for ingr in splitingr:
            unit = units_s[ingr_count].text
            amount = amounts_s[ingr_count].text
            ingr_count += 1
            
            ingredient_names.append(ingr)
            ingredient_name = (ingr.replace(unit + " ", '')).replace(amount, '')
            ingredient_name = remove_extra_words(ingredient_name)
            ingredient_search.append(ingredient_name)
            amount = float(amount.replace(',','.')) / portion_count
            amounts.append(amount)
            units.append(unit)
            grams.append(find_grams(amount, unit))


    # Convert grams list to JSON string
    grams_json = json.dumps(grams)
    ingredient_search, correctness = ingredient_names_overhaul(ingredient_names, ingredient_search)

    if correctness != 100:
        new_ingredient_search, new_instructions, new_title = manual_recipe_fix(ingredient_search, title, instructions, "recipe.txt")
        ingredient_search =  new_ingredient_search
        title = new_instructions
        instructions = new_title

    # Insert data into the database
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO recipe_data_siloed (title, ingredient_names, ingredient_search, instructions, amounts, units, grams, total_time, category)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        title,
        ", ".join(ingredient_names),
        ", ".join(ingredient_search),
        "\n".join(instructions),
        ", ".join(map(str, amounts)),
        ", ".join(units),
        grams_json,  # Store JSON string in the database
        None,
        category
    )
    try:
        cursor.execute(insert_query, data)
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    cursor.close()
    driver.close()

def manual_recipe_fix(ingredient_search, title, instructions, filename):
    cursor_ing = conn_ing.cursor()

    beepy.beep(sound=3)

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

        # Wait for the user to type 'done' or 'finished' in the terminal
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
                    _, new_ingredient = lines[i].strip().split(',')
                    new_ingredient_search.append(new_ingredient)
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
                    if closest == None:
                        print("This closest return none, please choose an ingredient that is closer in name. ")
                        for search in new_search:
                            print(search)

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

    beepy.beep(sound=1)

    return ingredient_search, instructions, title

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


def ingredient_names_overhaul(ingredient_names, ingredient_search):
    correct = 0
    max_correct = len(ingredient_names)
    new_list = []
    non_words = ["Salt", "salt", "Pepper", "pepper", "Vann", "vann", "olje", "kokende vann"]

    for w in range(len(ingredient_names)):
        newword = check_in_data(ingredient_names[w])
        if newword != None:
            correct += 1
            new_list.append(newword)
        else:
            print(ingredient_names[w])
            new_list.append(ingredient_search[w])

    final_list = []

    for w in range(len(new_list)):
        if new_list[w] in non_words:
            final_list.append("")
        else:
            final_list.append(new_list[w])

    final_list = [item for item in final_list if item]

    correctness = (correct/max_correct)*100

    print(final_list)

    return np.array(final_list), correctness

def check_in_data(ingredient):
    splitigr = ingredient.split(" ")
    
    for word in splitigr:

        capital = word[0].upper() + word[1:]
        
        if capital in igr_data:
            return word

    return None

def find_grams(amount, unit):
	"""
	.stken er altfor generell, men funker til å få en generell antydning. Dl og L er også altfor generelt. 
	"""
	unit_trans = {'ss': '15', 'dl': '100','l':'1000', 'kg': '1000', 'ts': '4.2', 'stk.': '132.86'}
	if unit in unit_trans:
		gram = float(amount) * float(unit_trans[unit])
	else:
		gram = amount
	return gram

def remove_extra_words(ingredient):
	"""
	Very badly written word removerm, hehe. 
	"""
	unwords = ["revet", "finhakket", "annen", "frosne", "nøytral", "frisk", "grovmalt", "tørket", "hakket", " til ", "syrlig", "sterk", "hel", "varm stekt"]

	new_ingr = ingredient

	if "eller" in ingredient:
		split_phrase = ingredient.split('eller')
		new_ingr = split_phrase[0].rstrip()

	if "gjerne" in ingredient:
		split_phrase = ingredient.split('gjerne')
		new_ingr = split_phrase[0].rstrip()

	if ',' in new_ingr:
		split_phrase = ingredient.split(',')
		new_ingr = split_phrase[0].rstrip()

	if '(' in new_ingr:
		split_phrase = ingredient.split('(')
		new_ingr = split_phrase[0].rstrip()

	if ' i ' in new_ingr:
		split_phrase = ingredient.split(' i ')
		new_ingr = split_phrase[0].rstrip()

	if 'crème fraîche' in new_ingr:
		new_ingr = "creme fraiche"

	if 'tortillalefse' in new_ingr:
		new_ingr = 'tortilla'

	if 'dijonsennep' in new_ingr:
		new_ingr = 'dijon'

	if 'nykål' in new_ingr:
		new_ingr = 'kål'
	
	for word in unwords:
		if word in new_ingr:
			new_ingr = new_ingr.replace(word, '')

	new_ingr = new_ingr.lstrip()

	# Remove comments. 
	return new_ingr

"""# Vegetar. 
get_recipe("https://www.matprat.no/oppskrifter/kos/gyoza-vegetar/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/moussaka-vegetar/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/minestronesuppe-vegetar/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/vegetar-wellington-med-tilbehor/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/vegetar-wellington-med-sotpotet/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/kos/vegetarburger-med-halloumi-og-aubergine/ ", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/risotto-med-gresskar/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/sunn/gronnsaksspagetti-med-sopp/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/pasta-med-jordskokk-og-sitron/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/bakt-blomkal-med-nottesmor/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/vegisterkaker/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/ostegratinert-purre/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/sotpotetsuppe/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/kos/gronn-bonneburger/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/asiatisk-soppomelett/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/selleribiffer-med-varm-linsesalat/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/sunn/kikertgryte-med-oregano-og-tomat/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/spinatsuppe-med-egg/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/rask/kikert--og-rodbeterosti/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/blomkal--og-potetcurry/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/kos/lasagne-med-sopp/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/tradisjon/vegetarpai-med-rotgronnsaker/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/taco-med-speilegg/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/gronnsaksuppe-med-gresskar-og-risoni/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/sunn/pannekaker-med-vegetarisk-fyll/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/sunn/brokkolisuppe-med-gronn-curry/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/aspargessuppe/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/sunn/pannekaker-med-vegetarisk-fyll/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/familien/vegetarisk-linsesuppe/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/kos/vegetarisk-nottestek/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/gjester/linseragu/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/kos/vegetarlasagne-med-spinat/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/kos/squash--og-kikertburger/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/rask/eggepanne-med-squash/", category = 'vegetar')
get_recipe("https://www.matprat.no/oppskrifter/sunn/rodbetkaker-med-gronnkal/", category = 'vegetar')

# Kjøtt
get_recipe("https://www.matprat.no/oppskrifter/kos/kebab-med-lam/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/rask/kyllinglar-i-airfryer/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/kebab-med-kylling/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/nyretapp-med-chimichurri/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/culotte-med-honningglaserte-rotgronnsaker/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/culotte-i-ovn/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/culotte-med-smordampet-sommerkal/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/culotte-i-sous-vide/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/brisket-med-bbq-saus/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/spareribs-med-bbq-saus-og-coleslaw/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/spareribs-med-asiatisk-glaze/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/brisket-med-syltede-gronnsaker/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/brisket-i-ovn/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/cheeseburger-med-hamburgerdressing/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/bbq-burger-med-coleslaw/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/kinesisk-sticky-svin/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/tradisjon/krydret-sideflesk-med-potetsalat/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/burritos-med-kylling-og-maiskrem/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/burrito-med-kjottdeig/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/rokt-svinekam-med-ovnsbakte-gronnsaker/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/crispy-svinekam-med-ovnsbakte-poteter/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/svinekam-med-sellerirotpure-og-appelsinsaus/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/nachos-i-form/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/helstekt-indrefilet-med-brokkolini/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/rask/burger-med-pulled-turkey-og-fetaost/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/rask/ribbe-med-gresk-salat/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/rask/ribbe-i-pita/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/ribbe-i-airfryer/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/biff-med-flotegratinerte-poteter/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/helstekt-indrefilet-med-flotegratinerte-poteter/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/tournedos-med-honningglaserte-rotgronnsaker/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/biff-med-jordskokkpure/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/gjester/chateaubriand-med-bearnaise-og-pommes-frites/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/halloween-burger/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/rask/blodig-spagetti/", category = 'kjøtt')
get_recipe("https://www.matprat.no/oppskrifter/kos/reinsdyrbiff-pa-primus/", category = 'kjøtt')
"""






