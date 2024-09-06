from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import sorting_script as ss
import time
from tqdm import tqdm
import numpy as np

# Set up the Chrome driver
driver = webdriver.Chrome()  # Make sure you have downloaded the Chrome driver and set its path
driver.get("https://meny.no/varer/")

def get_meny():
	f = open("meny/metadata.txt", "w")

	for cat in range(8, len(driver.find_elements(By.CLASS_NAME, "cw-categories__title")) - 6):
		category = driver.find_elements(By.CLASS_NAME, "cw-categories__title")[cat]
		reference_link = category.get_attribute("href")
		name = (category.text).replace(" ", "_")
		print("Extracting " + name + "...")
		create_ingredients("meny/" + name + ".txt", reference_link)
		print("Finished with " + name + ".")
		driver.get("https://meny.no/varer/")
		time.sleep(3)
		f.write(name + ".txt" + "\n")

	f.close()

def create_ingredients(filename, url):
	# Navigate to the URL
	driver.get(url)
	time.sleep(2)
	scroll()
	find_ingredients(filename)

def scroll():
	"""
	Scrolling script to get to the buttom of the page.
	"""
	print("Scrolling through site...")
	last_height = driver.execute_script("return document.body.scrollHeight")
	new_height = 0
	time.sleep(2)

	# This works. 
	while last_height != new_height:
		new_height = last_height
		driver.execute_script(f"window.scrollTo(0, {last_height-1000});")
		time.sleep(1)
		button = driver.find_elements(By.CLASS_NAME, "ngr-button")

		for i in button:
			text = i.find_element(By.CLASS_NAME, "ngr-button__text")
			if text.text == "Vis flere":
				text.click()

		last_height = driver.execute_script("return document.body.scrollHeight")
		time.sleep(1)

	time.sleep(2)


def find_ingredients(filename):
	# Find the element by its item id
	items = driver.find_elements(By.CLASS_NAME, "ws-product-list-vertical__item")
	print("Fetching information...")

	f = open(filename, "w")
	f.write("#Navn #Pris #Mengde #Før #Butikk \n")

	for i in tqdm(range(len(items))):
		# Information.
		name = items[i].find_element(By.CLASS_NAME, "ws-product-vertical__title")
		price = items[i].find_element(By.CLASS_NAME, "ws-product-vertical__price")
		pricetext = ((price.text).split(" "))[0].replace(",", ".")
		former = find_former(items[i])
		mengde = find_amount(items[i], pricetext)

		if mengde == None:
			mengde = find_sub_amount(items[i], pricetext)

		f.write(f"{name.text},{pricetext},{mengde}, {former}, Meny\n")

	f.close()


def find_former(item):
	try:
		former = item.find_element(By.CLASS_NAME, "ws-product-vertical__price-former")
		former = (former.text.split(" ")[1]).split(",")[0] + '.' + (former.text.split(" ")[1]).split(",")[1]
		return former
	except NoSuchElementException:
		return None

def find_amount(item, pricetext):
	try:
		mengde = item.find_element(By.CLASS_NAME, "ws-product-vertical__price-unit")
		mengde = ss.find_information_amount(mengde.text, float(pricetext))
		return mengde
	except NoSuchElementException:
		return None

def find_sub_amount(item, pricetext):
	mengde = None

	try:
		mengde = item.find_element(By.CLASS_NAME, "ws-product-vertical__subtitle")
	except NoSuchElementException:
		pass

	if mengde != None:
		mengde = ss.find_information_amount(mengde.text, float(pricetext.split(" ")[0]))

	return mengde

get_meny()

# Close the driver
driver.quit()
