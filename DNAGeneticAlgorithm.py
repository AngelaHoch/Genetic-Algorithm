#This is a simple genetic algorithm
#This algoritm is tested to see how many generations it takes to produce the target gene, 1010101010
import sys
import random
import time
from tabulate import tabulate

num_chromos = 20
pco = [0, 0.3, 0.5, 0.7, 0.9]   #constants used to determine how may genes are crossbred
target_gene = 682              #decimal of 1010101010; this is our goal gene
mask = 992                      #decimal of 1111100000; this is used to mask half of a gene to to new gene
inverse_mask = ~mask            #decimal of 0000011111; this is used to mask the other half of the gene

random.seed()

#class chromosome contains genes and the fitness value
class chromosome:
	gene = 0
	fit = 0
	cumulative_fit = 0

	def __init__(self, gene):
		self.gene = gene

	#less than function for making comparisons
	def __lt__(self, other):
		return self.fit < other.fit

	#bitwise operations to calculate fitness
	def calc_fit(self):
		self.fit = 1 + (10 - (bin(target_gene ^ self.gene).count("1")))

#function loops through all chromosomes and updates fitness. returns boolean for if target gene is found
def set_fit(current_generation):
	not_found = True
	for i in current_generation:
		i.calc_fit()
		if (i.fit == 11):
			not_found = False
	return not_found

#function loops through all chromosomes and updates cumulative fitness. this is used for probability calculation
def set_cumul_fit(current_generation):
	current_cumulative_fit = 0
	for i in current_generation:
		current_cumulative_fit += i.fit
		i.cumulative_fit = current_cumulative_fit
	return current_cumulative_fit

#bitwise operation to crossbreed genes
def cross_breed(gene1, gene2):
	temp_gene = gene1
	gene1 = ((gene1 & mask) | (gene2 & inverse_mask))       #uses a bitwise mask to determine the first five bits of the 1st gene and the last 5 bits of the second gene 
	gene2 = ((gene2 & mask) | (temp_gene & inverse_mask))   #combines the two masked 5 bit numbers together
	return (gene1, gene2)

all_avg_gens = []
init_generation_population = []

#generate random population
for i in range(num_chromos):
	gene = random.randint(0, 1023) #generate random bits from 0 to 1111111111
	init_generation_population.append(chromosome(gene))

#run entire algorithm for each pco value
for h in pco:

	avg_gens = 0
	all_num_gens = []

	#run evolution algorithm 20 times to get average per pco value
	for j in range(20):

		current_generation = init_generation_population
		not_found = set_fit(current_generation)
		curr_fit_cumul = set_cumul_fit(current_generation)

		gens = 1

		#evolve chromosomes to find target gene
		while not_found:
			evolved = []

			#replication
			for i in range(int(((1 - h) * num_chromos) + 0.5)):
				rand = random.randint(1, curr_fit_cumul)
				chosen = 0
				for k in current_generation:
					if (rand > k.cumulative_fit):
						chosen += 1
				evolved.append(chromosome(current_generation[chosen].gene))

			#crossover
			for i in range(int(((h * num_chromos) / 2) + 0.5)):
				same_chromosome = True
				while same_chromosome:
					rand1 = random.randint(1, curr_fit_cumul)
					rand2 = random.randint(1, curr_fit_cumul)
					chosen1 = 0
					chosen2 = 0
					for k in current_generation:
						if (rand1 > k.cumulative_fit):
							chosen1 += 1
						if (rand2 > k.cumulative_fit):
							chosen2 += 1
					if (chosen1 != chosen2):
						same_chromosome = False
				evolved_genes1, evolved_genes2 = cross_breed(current_generation[chosen1].gene, current_generation[chosen2].gene)
				evolved.append(chromosome(evolved_genes1))
				evolved.append(chromosome(evolved_genes2))

			#bit mutation
			rand1 = random.randint(0, 19)
			rand2 = (1 << random.randint(0, 9))
			if ((evolved[rand1].gene & rand2) == rand2):
				evolved[rand1].gene -= rand2
			else:
				evolved[rand1].gene += rand2

			current_generation = evolved
			not_found = set_fit(current_generation)
			curr_fit_cumul = set_cumul_fit(current_generation)
			gens += 1

			#calculate average fitness
			avg_fit = 0
			for i in current_generation:
				avg_fit += i.fit
			avg_fit /= 20

			#print genes for each generation in a table
			print("\n\nGeneration ", gens, "\n")
			table = []
			for current in current_generation:
				table.append([current.gene, (current.fit - 1)])
			print(tabulate(table, headers=['Genes', 'Fitness']) + '\n')
			print(avg_fit)

		all_num_gens.append(gens)
		avg_gens += gens

	#print table with number of generations for each trial and average generations across all trials
	print("Number of Generations for ", h, ":")
	table = []
	numslol = 1
	for i in all_num_gens:
		table.append([numslol, i])
		numslol += 1
	print(tabulate(table, headers=['Trial', 'Number of Generations']) + '\n')
	all_avg_gens.append(avg_gens / 20)
	print("\nAverage generations for pco ", h, ": ", (avg_gens / 20))

	input("Press Enter")

print("\n\n")

#finally, print initial population
print("Initial Population")
table = []
for current in init_generation_population:
	table.append([current.gene, (current.fit - 1)])
print(tabulate(table, headers=['Genes', 'Fitness']) + '\n')


