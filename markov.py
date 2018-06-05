class MarkovTextBot:
	""" A probabilistic text generator that uses Markov Chains
	to model relations between words
	"""
	def __init__(self, file, path=""):
		""" Initalizes a MarkovTextBot with a file handler,
		a file name, and a markov chain
		"""
		self.data = open(path + file)
		self.file = path + file
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
		""" Generate a text with at least 'words' words in it,
		starting with 'seed' if the parameter is set
		"""
		import random
		# set the first word of the sentence
		if not seed: 
			first_word = random.choice(list(self.chart.keys()))
			# loop to make sure sentence does not begin awkwardly 
			while first_word[0].islower() or not first_word[0].isalpha():
				first_word = random.choice(list(self.chart.keys()))
			line = [first_word]
		else: line = [seed]

		# generate the rest of the text probabilistically
		while len(line) < words:
			prev_word = line[-1]
			transitions = self.chart[prev_word]
			if transitions:
				next_word = random.choice(transitions)
				line += [next_word]
			else: break

		# another loop to ensure the paragraph does not end abruptly
		# might go over word count
		final_word = line[-1] 
		while final_word[-1] not in '.!?':
			transitions = self.chart[final_word]
			if transitions: 
				final_word = random.choice(transitions)
				line += [final_word]
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
