import requests
from bs4 import BeautifulSoup

# Make a GET request to the webpage
# Bare en av linkene for rema. Må gå igjennom alle å lagre de i en sql. 

url = "https://oda.com/no/products/brand/550-rema-1000/"
response = requests.get(url)

# Use BeautifulSoup to parse the HTML source code
soup = BeautifulSoup(response.text, "html.parser")
categories = soup.find_all("ul", class_="nav nav-pills")
link = categories[1].find_all('a', href=True)[:96]
length = len(link)
counter = 0

# For rema.
for i in link:
	print(f"{counter} of {length} links.")
	# Looping through all categories on the oda website. 
	splitter = str(i).split('"')
	newlink = splitter[1]
	name = splitter[2].strip('>').split('<')[0]

	newurl = "https://oda.com" + newlink
	
	newresponse = requests.get(newurl)
	newsoup = BeautifulSoup(newresponse.text, "html.parser")
	newproducts = newsoup.find_all("div", class_="col-xs-6 col-sm-3 col-md-2")


	file = open('rema1000/' + name + ".txt", 'w')

	for product in newproducts:
		name = product.find("div", class_='name-main wrap-two-lines').text.strip()
		price = (product.find("p", class_="price label label-price").text.strip()).split("\xa0")[1].split(",")
		amount = product.find("div", class_="name-extra wrap-one-line").text.strip().split(" ")[-2]
		file.write(name + "," + price[0] + "." + price[1] + "," + amount + "\n")

	file.close()

	# Find all the products on the page
	products = soup.find_all("div", class_="col-xs-6 col-sm-3 col-md-2")
	counter+=1

	
""" # Finding for specific recipies. 
# Find all the products on the page
products = soup.find_all("div", class_="col-xs-6 col-sm-3 col-md-2")

# Loop through each product and extract its name and price
for product in products:
	name = product.find("div", class_='name-main wrap-two-lines').text.strip()
	price = (product.find("p", class_="price label label-price").text.strip()).split("\xa0")[1].split(",")
	amount = product.find("div", class_="name-extra wrap-one-line").text.strip().split(" ")[-2]
	file.write(name + "," + price[0] + "." + price[1] + "," + amount + "\n")

file.close()
"""