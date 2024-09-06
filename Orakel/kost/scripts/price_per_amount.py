import numpy as np
import re

def find_information_amount(amount_text, price):
	amount = find_amount(amount_text, price)

	if amount != None:
		return amount

	amount = amount_sub(amount_text)

	return amount


def find_amount(amount_text, price):
	price_per_text = sort_amount(amount_text).replace(",", ".")
	price_per = float(price_per_text.split("k")[0])
	amount = None
	
	if price_per_text.split("/")[1] == "kg":
		if price_per == 0:
			amount = 0
		else:
			amount = str(round((price/price_per)*1000)) + " g"

	elif price_per_text.split("/")[1] == "stk":
		amount = str(round((price/price_per))) + " stk"

	elif price_per_text.split("/")[1] == "l":
		amount = str(round((price/price_per)*1000)) + " ml"

	return amount # in grams

def sort_amount(amount_text):
	"""
	Input the amount in question, finds amout from price and kg. 
	"""
	strings = ["kr/kg", "kr/stk", "kr/l"]

	for i in strings:
		if i in amount_text:
			if get_number_before(amount_text, i) != None:
				return get_number_before(amount_text, i)
			else:
				continue

	return "0k/."

def amount_sub(sub_text):
	"""Only to be used if sort_amount doesnt find anything."""

	strings = ["pk", "stk", "kg", "stykk"]

	for i in strings:
		if i in sub_text:
			if get_number_before(sub_text, i) != None:
				return get_number_before(sub_text, i)
			else:
				continue
	
	return "1 stk"


def get_number_before(string, n):
    # Use regular expression to match the number followed by "g"

    pattern = r'(\d{1,3}(?:[.,]\d{3})*[,\.]\d{2})\s*' + re.escape(n)
    match = re.search(pattern, string)

    # If no match is found, return None
    if not match:
        return None

    # Extract the matched number
    number = match.group(1)

    # Return the number followed by "g"
    return number + n
