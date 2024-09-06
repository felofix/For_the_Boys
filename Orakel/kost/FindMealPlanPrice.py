import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import math
import random
from deap import tools
import time

class FindMealplanPrice:
	recipies = None 
	prices = None

	def __init__(self, r, p, m):
		self.recipies = r 
		self.prices = p
		self.maxxer = m

	def calculate_fitness(self, recipy_set):
		"""
		Finds the price of the recipy set. This fitness can 
		be calculated based on price, number of calories, etc. etc.
		"""
		recipy = self.recipies[np.array(recipy_set)]
		fitness = np.dot(self.ceil_maxxer(np.sum(recipy, axis=0)), self.prices)
		
		return fitness

	def ceil_maxxer(self, sums):
		"""
		Finds the ceiling of stuff that needs to be bought. 
		"""
		ceiling = np.ceil(sums/self.maxxer)
		return ceiling

	def calculate_all_fitness(self, population):
		"""
		Finds the fitness of the population, textbook EA algo.
		"""
		fitness_all = np.zeros(len(population))
		for i in range(len(population)):
			fitness_all[i] = self.calculate_fitness(population[i])
		return fitness_all

	def create_population(self, size, num_recipies):
	    population = np.zeros((size, num_recipies))
	    ranger = set(np.arange(len(self.recipies))) #remove later
	    
	    for i in range(size):
	        population[i] = random.sample(set(ranger), num_recipies)
	    
	    return population.astype(int)

	def find_parents(self, population, fitness):
	    parentsize = population.shape[0]//2
	    if parentsize % 5 == 0:
	        parentsize += 1

	    parents = np.zeros((parentsize, population.shape[1]))
	    
	    idx = np.argsort(fitness)
	    for i in range(parentsize):
	        parents[i] = population[idx[i]]

	    return parents.astype(int)

	def find_children(self, parents):
	    children = np.zeros((parents.shape[0]*2, parents.shape[1]))
	    for i in range(parents.shape[0]):
	        parent1 = list(random.choice(parents))
	        parent2 = list(random.choice(parents))
	        childr = tools.cxOnePoint(parent1, parent2)
	        children[i*2], children[i*2+1] = childr[0], childr[1]

	    return children.astype(int)

	def swap_mutation(self, child):
	    fitness_before = self.calculate_fitness(child)
	    childcopy = child

	    rndres = random.randrange(len(self.recipies))
	    rndidx = random.randrange(len(child))

	    childcopy[rndidx] = rndres

	    if self.calculate_fitness(childcopy) < fitness_before:
	    	return childcopy
	    else:
	        return child

	def mutate(self, children):
	    for i in range(len(children)):
	        children[i] = self.swap_mutation(children[i])
	    return children

	def survivors(self, population, pop_fitness, mutants, mut_fitness):
	    survivors = np.zeros((population.shape))
	    pop_idx = list(np.argsort(pop_fitness))
	    chi_idx = list(np.argsort(mut_fitness))

	    for i in range(population.shape[0]):
	        if pop_fitness[pop_idx[0]] < mut_fitness[chi_idx[0]]:
	            survivors[i] = population[pop_idx[0]]
	            pop_idx.remove(pop_idx[0])
	        else:
	            survivors[i] = mutants[chi_idx[0]]
	            chi_idx.remove(chi_idx[0])
	    return survivors.astype(int)

	def evolve(self, size, generations, num_recipies, num_cutoff):
	    population = self.create_population(size, num_recipies)
	    pop_fitness = []
	    minimum_fit = np.zeros(generations)
	    cutoff_count = 0

	    for i in range(1, generations):
	    	if cutoff_count == num_cutoff:
	    		break
	    
	    	pop_fitness = self.calculate_all_fitness(population)
	    	parents = self.find_parents(population, pop_fitness)
	    	children = self.find_children(parents)
	    	mutants = self.mutate(children)
	    	mut_fitness = self.calculate_all_fitness(mutants)
	    	population = self.survivors(population, pop_fitness, mutants, mut_fitness)
	    	minimum_fit[i] = np.min(pop_fitness)
	    	
	    	if minimum_fit[i] == minimum_fit[i-1]:
	    		cutoff_count += 1
	    	else:
	    		cutoff_count = 0

	    return population, pop_fitness, minimum_fit[1:]

if __name__ == "__main__":
	"""
	number_of_recipies = 100
	numb_of_ingridients = 100
	re = np.random.randint(0,10, (number_of_recipies, numb_of_ingridients))/10
	prices = np.random.randint(1, 101, size=numb_of_ingridients)

	mealplan = FindMealplanPrice(re, prices)
	evolved, pop_fitness, minn = mealplan.evolve(10, 10000, 5, 1000)
	minimum_price = np.min(pop_fitness)
	minimum_recipe = evolved[np.where(pop_fitness == minimum_price)]
	print(minimum_price, minimum_recipe)
	"""
	

