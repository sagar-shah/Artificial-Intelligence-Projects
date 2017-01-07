class bayesClassifierModel:
	word_dic = {}
	word_dic_doc = {}
	vocabulary_size = 0
	wordsPerClass = [0,0]
	doc_count = [0,0]	

	def __init__(self, word_dic, word_dic_doc, vocabulary_size, wordsPerClass, doc_count):
		self.word_dic = word_dic
		self.word_dic_doc = word_dic_doc
		self.vocabulary_size = vocabulary_size
		self.wordsPerClass = wordsPerClass
		self.doc_count = doc_count

	def __str__(self):
		return "word_dic "+str(self.word_dic)+", word_dic_doc "+str(self.word_dic_doc)+", vocabulary_size "+str(self.vocabulary_size)+", wordsPerClass "+str(self.wordsPerClass)+", doc_count "+str(self.doc_count)+"."