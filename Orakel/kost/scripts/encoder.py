from ingredient_parser.en import parse
import re
from itertools import combinations
import numpy as np

ingredients = ['2 pounds skinless, boneless chicken breasts', '1 (1 ounce) package dry ranch dressing mix (such as Hidden Valley Ranch)', '1 cup sliced and drained pepperoncini peppers', '1/4 cup pepper juice (from jar of pepperoncini peppers)', '4 tablespoons unsalted butter, sliced', '1/2 cup water']
instructions = ['Gather ingredients. Preheat the oven to 350 degrees F (175 degrees C).', 'Season chicken with ranch seasoning mix; place in bottom of a medium Dutch oven.', 'Add pepperoncini peppers and 1/4 cup reserved pepper juice; top with sliced butter and pour in 1/2 cup water. Cover with a tight fitting lid, and bake in preheated oven until chicken is fork tender, 1 hour to 1 hour 15 minutes. An instant-read thermometer inserted into the center should read 165 degrees F (74 degrees C).', 'Let stand 5 minutes. Shred chicken using two forks.', 'Season chicken with ranch seasoning mix and place in the bottom of 6-qt. slow cooker. Add pepperoncini peppers and 1/4 cup reserved pepper juice; top with butter and pour in 1/2 cup of water. Cover, and cook until chicken is fork-tender on LOW for 6 hours or on HIGH for 4 hours. An instant-read thermometer inserted into the center should read 165 degrees F (74 degrees C). Let stand 5 minutes. Shred chicken using two forks.']

def parse_all(ingredients):
    # maybe dead.
    ingredients = remove_comments(ingredients)
    ingredients = replace_symbols(ingredients)
    ingredients = remove_spices(ingredients)
    ingredients_parsed = []
    
    for ingredient in ingredients:
        parsed = parse(ingredient)
        parsednew = alter_amount(parsed)
        further_parse = parse(parsednew['measure'])
        ingr_dict = {}
        ingr_dict['name'] = parsednew['name']
        ingr_dict['quantity'] = further_parse['measure'].split(" ")[0]
        ingr_dict['unit'] = further_parse['name']

        if ingr_dict['unit'] == '':
            ingr_dict['unit'] = None

        ingredients_parsed.append(ingr_dict)

    return ingredients_parsed

def replace_symbols(ingredients):
    symbols = {"½": "0.5", "¼": "0.25", "¾": "0.75", "1/4": "0.25", "1/2": "0.5", "3/4": "0.75"}

    for i in range(len(ingredients)):
        for s in symbols:
            if s in ingredients[i]:
                ingredients[i] = ingredients[i].replace(s, symbols[s])

    return ingredients

def find_type_ingredient(ingredients, instructions):
    #mayube dead
    """
    Need to figure out something for salt and pepper, which is common. 
    """
    nonwords = ['wooden', 'diced','minced', 'taste', 'table', 'Italian','lean','roughly', 'fresh', 'peppers','sliced', 'of', 'salted', 'spice packet', 'elbow', 'dried', 'grated','finely', 'jar', 'container', 'or', '', 'as', 'ground', 'chopped', 'in', 'cup', '-', 'prepared', 'to', 'crushed', 'with', 'and', 'package', 'shredded'] # update as I go.
    pattern = r'\b(?:{})\b'.format('|'.join(nonwords))

    for ingredient in ingredients:
        ingredient['name'] = re.sub(pattern, '', ingredient['name']).strip()
        found = False  
        for sub_part in instructions:
            if ingredient['name'] in sub_part:
                found = True
                break

        if not found:
            for sub_part in instructions:
                ingr_split = ingredient['name'].split(" ")  
                for ingrs in set(ingr_split) - set(nonwords):
                    if ingrs in sub_part: 
                        ingredient['name'] = ingrs
                        break

        if ingredient['name'] == "skinless":
            ingredient['name'] = "chicken"

        ingredient['grams'] = find_grams(ingredient['quantity'], ingredient['unit'])

    return ingredients

def remove_spices(ingredients):
    saltnpeppa = ["salt and pepper to taste", "salt and black pepper to taste", 'salt and ground black pepper to taste (Optional)', 'brown sugar']

    for i in range(len(ingredients)):
        for salt in saltnpeppa:
            if salt in ingredients[i]:
                ingredients.remove(ingredients[i])
                return ingredients

    return ingredients

def remove_comments(ingredients):
    sizes = ["small", "medium", "large", "extra"]

    for i in range(len(ingredients)):
        splitter = ingredients[i].split(",")

        if len(splitter) == 1:
            ingredients[i] = splitter[0]
        else:
            ingredients[i] = "".join(ingredients[i].split(",")[:-1])

        for size in sizes:
            if size in ingredients[i]:
                ingredients[i] = ingredients[i].replace(size, "")


    return ingredients

def alter_amount(parsed):
    """If it containts paranthases that has anything measurable food wise."""
    amount_words = ["ounce", "pound"]

    splitter = [i.split(")") for i in parsed['name'].split("(")]
    
    for split in splitter:
        for part in split:
            for amount in amount_words:
                if amount in part:
                    parsed['name'] = parsed['name'].replace("(" + part + ")", "")
                    parsed['measure'] = part
                
    return parsed

def find_grams(amount, unit):
    unit_trans = {'tablespoon': '15', 'tablespoons': '15', 'ounce': '28.34', 'ounces': '28.34', 'pound': '453.5', 'pounds': '453.5', 'cup': '128', 'cloves': '10', 'clove': '10', 'fluid ounce': '28.34', 'sprigs': 0.5}
    if unit in unit_trans:
        gram = float(amount) * float(unit_trans[unit])
    else:
        gram = amount
    return gram

