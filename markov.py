ROOT = 'datasets'

class MarkovTextBot:
	""" A probabilistic text generator that uses Markov Chains
	to model relations between words
	"""
	def __init__(self, file):
		""" Initalizes a MarkovTextBot with a file handler,
		a file name, and a markov chain
		"""
		self.data = open(ROOT + file)
		self.file = ROOT + file
		self.chart = {}

		for line in self.data:
			words = line.split()
			for word in words:
				if not self.chart.get(word, None):
					self.chart[word] = []

	def __repr__(self):
		""" String representation """
		return "MarkovChain(" + self.file + ")"

	def fill_chart(self, k=1):
		""" Creates a markov chain linking each word to the next
		'k' words after it
		"""
		self.data = open(self.file) # go back to the first line
		for line in self.data:
			words = line.split()
			for i in range(len(words) - 1):
				for j in range(k):
					if i + j + 1 < len(words) - 1: 
						self.chart[words[i]] += [words[i+j+1]]
					else: break


	def generate_text(self, words, seed=None):
		""" Generate a text with 'words' words in it,
		starting with 'seed' if the parameter is set
		"""
		import random
		# set the first word of the sentence
		if not seed: 
			first_word = random.choice(list(self.chart.keys()))
			while first_word[0].islower():
				first_word = random.choice(list(self.chart.keys()))
			line = [first_word]
		else: line = [seed]

		while len(line) < words: # generate the rest of the text
			prev_word = line[-1]
			transitions = self.chart[prev_word]
			if transitions:
				next_word = random.choice(self.chart[prev_word])
				line += [next_word]
			else: break
		return ' '.join(line)

	def merge_model(self, model):
		""" Merge two markov chains, treating their contents as one file
		"""
		for word in model.chart:
			if word in list(self.chart.keys()):
				self.chart[word] += model.chart[word]
			else:
				self.chart[word] = model.chart[word]
