class TrainedModel:
	topic_wordfreq_dic2 = {}
	topic_doc_count_dic2 = {}
	cachedStopWords_set2 = []

	def __init__(self, topic_wordfreq_dic3, topic_doc_count_dic3, cachedStopWords_set3):
		self.topic_wordfreq_dic2 = topic_wordfreq_dic3
		self.topic_doc_count_dic2 = topic_doc_count_dic3
		self.cachedStopWords_set2 = cachedStopWords_set3