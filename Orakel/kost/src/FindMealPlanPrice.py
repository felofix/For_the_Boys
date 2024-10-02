import numpy as np
import random
from deap import tools

class FindMealplanPrice:
    recipies = None
    prices = None
    non_repeating = False  # Optional flag for non-repeating recipes

    def __init__(self, r, p, m, non_repeating=False):
        self.recipies = r
        self.prices = p
        self.maxxer = m
        self.non_repeating = non_repeating  # Set the non-repeating flag

    def calculate_fitness(self, recipy_set):
        """
        Finds the price of the recipe set. This fitness can 
        be calculated based on price, number of calories, etc.
        """
        recipy = self.recipies[np.array(recipy_set)]
        fitness = np.dot(self.ceil_maxxer(np.sum(recipy, axis=0)), self.prices)
        return fitness

    def ceil_maxxer(self, sums):
        """
        Finds the ceiling of stuff that needs to be bought. 
        """
        ceiling = np.ceil(sums / self.maxxer)
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
        available_indices = set(range(len(self.recipies)))

        for i in range(size):
            if self.non_repeating:
                # Non-repeating: sample without replacement
                individual = random.sample(available_indices, num_recipies)
            else:
                # Repeating: sample with replacement
                individual = random.choices(list(available_indices), k=num_recipies)
            population[i] = individual

        return population.astype(int)

    def find_parents(self, population, fitness):
        parentsize = population.shape[0] // 2
        if parentsize % 5 == 0:
            parentsize += 1

        parents = np.zeros((parentsize, population.shape[1]))

        idx = np.argsort(fitness)
        for i in range(parentsize):
            parents[i] = population[idx[i]]

        return parents.astype(int)

    def find_children(self, parents):
        children = np.zeros((parents.shape[0] * 2, parents.shape[1]))
        for i in range(parents.shape[0]):
            parent1 = list(random.choice(parents))
            parent2 = list(random.choice(parents))
            if self.non_repeating:
                # Custom non-repeating crossover
                child1, child2 = self.cx_non_repeating(parent1, parent2)
            else:
                # Use standard crossover
                child1, child2 = tools.cxOnePoint(parent1, parent2)
            children[i * 2], children[i * 2 + 1] = child1, child2
        return children.astype(int)

    def cx_non_repeating(self, parent1, parent2):
        """
        Custom crossover function to ensure children have no duplicate recipes.
        """
        size = len(parent1)
        child1, child2 = [-1] * size, [-1] * size

        # Copy a random segment from parent1 to child1
        start, end = sorted(random.sample(range(size), 2))
        child1[start:end] = parent1[start:end]

        # Fill the remaining spots in child1 from parent2, ensuring no duplicates
        current_pos = end
        for recipe in parent2:
            if recipe not in child1:
                if current_pos >= size:
                    current_pos = 0
                child1[current_pos] = recipe
                current_pos += 1

        # Do the same for child2 (copy segment from parent2 and fill from parent1)
        child2[start:end] = parent2[start:end]
        current_pos = end
        for recipe in parent1:
            if recipe not in child2:
                if current_pos >= size:
                    current_pos = 0
                child2[current_pos] = recipe
                current_pos += 1

        return child1, child2

    def swap_mutation(self, child):
        fitness_before = self.calculate_fitness(child)
        childcopy = child.copy()

        rndres = random.randrange(len(self.recipies))
        rndidx = random.randrange(len(child))

        # Ensure no repetition if non-repeating flag is set
        if self.non_repeating and rndres in child:
            while rndres in child:
                rndres = random.randrange(len(self.recipies))

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
                pop_idx.pop(0)
            else:
                survivors[i] = mutants[chi_idx[0]]
                chi_idx.pop(0)

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



            if minimum_fit[i] == minimum_fit[i - 1]:
                cutoff_count += 1
            else:
                cutoff_count = 0

        return population, pop_fitness, minimum_fit[1:]