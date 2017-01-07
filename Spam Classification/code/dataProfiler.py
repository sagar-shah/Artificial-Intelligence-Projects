from __future__ import division
import os, re, glob, string
from helper import Helper
from treeHelper import TreeHelper
from heapq import nlargest,nsmallest
from collections import Counter
from DTree import DTree
from DTNode import DTNode
from cleaner import cleanLine

global spam
spam = 1
global notspam
notspam = 0

# http://stackoverflow.com/questions/8703017/remove-sub-string-by-using-python
tagFilter = "<.*?>" 
# http://emailregex.com/
emailIdFilter = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" #2

ipFilter = "[0-9]+(?:\.[0-9]+){3}" #3

punctuationFilter = re.escape(string.punctuation)
# http://stackoverflow.com/questions/5197959/how-do-i-remove-hex-values-in-a-python-string-with-regular-expressions
hexFilter = "^\x20-\x7a"

# http://stackoverflow.com/questions/10340615/matching-multiple-kinds-of-dates-timestamps-using-regex
full_pattern = r'\w{3,4}\W\s\d{1,2}\s\w{3}\s\d{4}\s\d{2}:\d{2}:\d{2}'
time_pattern = r'\d{1,2}:\d{2}(\s(A|P)M)?'
combo_regex = '(%s)' % ('|'.join([full_pattern, time_pattern]),)

# http://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string
nonNumeric = "[^a-zA-Z]{3,4}"

cachedStopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \
'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', \
'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', \
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', \
'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', \
'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', \
'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', \
'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', \
'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', \
'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', \
'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', \
'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', \
'isnt', 'may', 'mightnt', 'mustnt', 'neednt', 'shant', 'shouldnt', 'wasnt', 'werent', 'wont', 'wouldnt']

stopWords1 = [u'a', u'about', u'above', u'after', u'again', u'against', u'all', u'am', u'an', \
u'and', u'any', u'are', u"aren't", u'as', u'at', u'be', u'because', u'been', u'before', \
u'being', u'below', u'between', u'both', u'but', u'by', u"can't", u'cannot', u'could', \
u"couldn't", u'did', u"didn't", u'do', u'does', u"doesn't", u'doing', u"don't", u'down',\
 u'during', u'each', u'few', u'for', u'from', u'further', u'had', u"hadn't", u'has', u"hasn't",\
  u'have', u"haven't", u'having', u'he', u"he'd", u"he'll", u"he's", u'her', u'here', u"here's", \
  u'hers', u'herself', u'him', u'himself', u'his', u'how', u"how's", u'i', u"i'd", u"i'll", u"i'm", \
  u"i've", u'if', u'in', u'into', u'is', u"isn't", u'it', u"it's", u'its', u'itself', u"let's", u'me', \
  u'more', u'most', u"mustn't", u'my', u'myself', u'no', u'nor', u'not', u'of', u'off', u'on', u'once', \
  u'only', u'or', u'other', u'ought', u'our', u'ours', u'ourselves', u'out', u'over', u'own', u'same', u"shan't", \
  u'she', u"she'd", u"she'll", u"she's", u'should', u"shouldn't", u'so', u'some', u'such', u'than', u'that', \
  u"that's", u'the', u'their', u'theirs', u'them', u'themselves', u'then', u'there', u"there's", u'these', \
  u'they', u"they'd", u"they'll", u"they're", u"they've", u'this', u'those', u'through', u'to', u'too', \
  u'under', u'until', u'up', u'very', u'was', u"wasn't", u'we', u"we'd", u"we'll", u"we're", u"we've", u'were', \
  u"weren't", u'what', u"what's", u'when', u"when's", u'where', u"where's", u'which', u'while', u'who', u"who's", \
  u'whom', u'why', u"why's", u'with', u"won't", u'would', u"wouldn't", u'you', u"you'd", u"you'll", u"you're", \
  u"you've", u'your', u'yours', u'yourself', u'yourselves']



class DataProfiler:

	word_dic = {}
	word_dic_doc = {}
	vocabulary_size = 0
	wordsPerClass = [0,0]
	wordsPerDocSpam = {}
	wordsPerDocNotSpam = {}
	wordsPerDocContinuous = []	# binary tree for continuous values
	wordSet = set()
	spamDocs = []			# list of indices holding spam docs (index refers to the keys in wordsPerDocSpam)
	notSpamDocs = []		# list of indices holding not spam docs (index refers to the keys in wordsPerDocNotSpam)
	doc_count = [0,0]		# 0th index holds counts for notspam, while 1st index is for spam counts
	ratio = [0.0,0.0,0,0]
	TP=0
	FP=0
	FN=0
	TN=0

	rootBin = None
	rootContinuous = None
	dTNode_root = None
	dTNode_Continuous_root = None

	# binary
	@staticmethod
	def getDocCounts(filePath, idx, label):
		with open(filePath,"r") as f:
	        # global word_dic
			# l = [re.findall("\w+",line.rstrip().lower())  for line in f if line.strip()]
			total = []
			# cleaner line
			l = [cleanLine(line) for line in f if line.strip()]
			for e in l:
				#total.update(e)
				for i in e:
					total.append(i)
			c = Counter(total)
			big_list = Counter(el for el in c.elements() if c[el] > 1)
			big_list = big_list.most_common(int(len(big_list)*0.1))
			
			for w in big_list:
				if w[0] not in DataProfiler.word_dic_doc:
					DataProfiler.word_dic_doc[w[0]] = [[0,-1],[0,-1]]
				if DataProfiler.word_dic_doc[w[0]][label][1] <> idx:
					DataProfiler.word_dic_doc[w[0]][label][1] = idx
					DataProfiler.word_dic_doc[w[0]][label][0] += 1

	# multinomial
	@staticmethod
	def getWordCounts(filePath, label):
	    with open(filePath,"r") as f:
			total = []
			# cleaner line
			l = [cleanLine(line) for line in f if line.strip()]
			for e in l:
				for i in e:
					total.append(i)
			c = Counter(total)
			big_list = Counter(el for el in c.elements() if c[el] > 1)
			big_list = big_list.most_common(int(len(big_list)))
			
			for w in big_list:    
				if w[0] not in DataProfiler.word_dic:
					DataProfiler.word_dic[w[0]] = [0,0]
				DataProfiler.wordsPerClass[label] += 1
				DataProfiler.word_dic[w[0]][label] += 1

	#dt multinomial
	@staticmethod
	def getWordCountsPerDocContinuous(filePath, label):
		counts = None
		with open(filePath,"r") as f:
			total = []
			l = [cleanLine(line) for line in f if line.strip()]
			for e in l:
				for i in e:
					total.append(i)
			c = Counter(total)
			big_list = Counter(el for el in c.elements() if c[el] > 1)

			factor = 1 if len(big_list) < 100 else int(len(big_list)*0.01)

			big_list = big_list.most_common(factor)
			wordlist = []
			for b in big_list:
				alpha = b[0]
				freq = b[1]
				for i in range(freq):
					wordlist.append(alpha)
			DataProfiler.wordSet.update(wordlist)
			counts = Counter(wordlist)
		DataProfiler.wordsPerDocContinuous.append([counts, label])

	@staticmethod
	def testDecisionTree(file, label, method):
		with open(file,"r") as f:
			total = []
			# cleaner line
			l = [cleanLine(line) for line in f if line.strip()]
			for e in l:
				#total.update(e)
				for i in e:
					total.append(i)
			c = Counter(total)
			big_list = Counter(el for el in c.elements() if c[el] > 1)
			big_list = big_list.most_common(int(len(big_list)*0.1))

			wordlist = []
			for b in big_list:
				alpha = b[0]
				freq = b[1]
				for i in range(freq):
					wordlist.append(alpha)
			binaryWordSet = set(wordlist)
			continuousWordCounter = Counter(wordlist)

			if method == "binary":
				predicted_label = TreeHelper.getLabel(DataProfiler.rootBin, method, binaryWordSet)
			else:
				predicted_label = TreeHelper.getLabel(DataProfiler.rootContinuous, method, continuousWordCounter)

			if label == 1:
				if predicted_label == 1:
					DataProfiler.TP+=1
				else:
					DataProfiler.FN+=1
			else:
				if predicted_label == 0:
					DataProfiler.TN+=1
				else:
					DataProfiler.FP+=1

	# dt binary
	@staticmethod
	def getWordCountsPerDoc(filePath, doc_idx, label):
		counts = None
		with open(filePath, "r") as f:
			total = []

			l = [cleanLine(line) for line in f if line.strip()]
			for e in l:

				for i in e:
					total.append(i)
			c = Counter(total)
			big_list = Counter(el for el in c.elements() if c[el] > 1)
			big_list = big_list.most_common(int(len(big_list)*0.1))
			
			wordlist = []
			for b in big_list:
				alpha = b[0]
				freq = b[1]
				for i in range(freq):
					wordlist.append(alpha)
			binaryWordSet = set(wordlist)
			counts = Counter(wordlist)

			DataProfiler.wordSet.update(wordlist)

		if label == spam:
			DataProfiler.wordsPerDocSpam[doc_idx] = counts
			DataProfiler.spamDocs = list(DataProfiler.wordsPerDocSpam)
		else:
			DataProfiler.wordsPerDocNotSpam[doc_idx] = counts
			DataProfiler.notSpamDocs = list(DataProfiler.wordsPerDocNotSpam)




	@staticmethod
	def getLabelsForTestData(filePath, label, method):
		with open(filePath,"r") as f:
			total = []

			l = [cleanLine(line) for line in f if line.strip()]
			for e in l:
				for i in e:
					total.append(i)
			c = Counter(total)
			big_list = Counter(el for el in c.elements() if c[el] > 1)
			big_list = big_list.most_common(int(len(big_list)*0.1))

			wordlist = []
			for b in big_list:
				alpha = b[0]
				freq = b[1]
				for i in range(freq):
					wordlist.append(alpha)
			binaryWordSet = set(wordlist)
			continuousWordCounter = Counter(wordlist)			


			if method == "binary":
				predicted_label = Helper.getLabel(DataProfiler.word_dic, DataProfiler.word_dic_doc, DataProfiler.doc_count, \
							 DataProfiler.vocabulary_size, DataProfiler.wordsPerClass, binaryWordSet, label, method)
			else:
				predicted_label = Helper.getLabel(DataProfiler.word_dic, DataProfiler.word_dic_doc, DataProfiler.doc_count, \
							 DataProfiler.vocabulary_size, DataProfiler.wordsPerClass, wordlist, label, method)
			if label == 1:
				if predicted_label == 1:
					DataProfiler.TP+=1
				else:
					DataProfiler.FN+=1
			else:
				if predicted_label == 0:
					DataProfiler.TN+=1
				else:
					DataProfiler.FP+=1


	@staticmethod
	def readDir(dirPath, technique, method, mode, label):
		listOfFiles = glob.glob(dirPath)
		if mode == "train" and DataProfiler.doc_count[label] == 0:
			DataProfiler.doc_count[label] = len(listOfFiles)

		idx = 0
		for file in listOfFiles:
			if os.path.isdir(file):
				continue
			
			if technique == "bayes":
				if mode=="train":
					if method == "binary":
						DataProfiler.getDocCounts(file, idx, label)
					else:
						DataProfiler.getWordCounts(file, label)
				elif mode=="test":
					DataProfiler.getLabelsForTestData(file, label, method)
				idx+=1
			elif technique == "dt":
				if mode=="train":
					if method=="binary":
						DataProfiler.getWordCountsPerDoc(file, idx, label)
					else:
						DataProfiler.getWordCountsPerDocContinuous(file, label)
				elif mode=="test":
					DataProfiler.testDecisionTree(file, label, method)
				idx+=1

	@staticmethod
	def display():

		total_words_in_spam = 0
		for k in DataProfiler.word_dic.iterkeys():
			total_words_in_spam += DataProfiler.word_dic[k][spam]
		prob_dic = {}
		for k,v in DataProfiler.word_dic.iteritems():
			num =  DataProfiler.word_dic[k][spam] / total_words_in_spam
			deno = (DataProfiler.word_dic[k][notspam] + DataProfiler.word_dic[k][spam]) / DataProfiler.vocabulary_size
			prob_dic[k] = num/deno

		print "Top 10 most associated:.... "
		print nlargest(10, prob_dic, key=prob_dic.get)
		print "Least 10 associated: " 
		print nsmallest(10, prob_dic, key=prob_dic.get)