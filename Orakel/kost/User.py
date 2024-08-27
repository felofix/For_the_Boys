import numpy 

class User:
	"""
	Very simple testing user class. 
	"""
	def __init__(self, name, is_vegetarian=False, is_repetitive=False):
		self.name = name
		self.is_vegetarian = is_vegetarian
		self.is_repetitive = is_repetitive

	def __str__(self):
		return (f"User: {self.name}, "
				f"Vegetarian: {'Yes' if self.is_vegetarian else 'No'}, "
				f"Repetitive: {'Yes' if self.is_repetitive else 'No'}")
