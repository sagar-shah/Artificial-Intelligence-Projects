from __future__ import division
import math

global spam
spam = 1
global notspam
notspam = 0



class Helper:
	word_dic = {}
	word_dic_doc = {}
	vocabulary_size = 0
	doc_count = [0,0]
	ratio=[0.0,0.0,0,0]
	wordsPerClass = [0,0]
	
	@staticmethod
	def wordFrequency(word, label):
		return Helper.word_dic[word][label]

	@staticmethod
	def documentFrequency(word, label):
		return Helper.word_dic_doc[word][label][0]

	@staticmethod
	def count(label):
		return Helper.wordsPerClass[label]

	@staticmethod
	def getLikelihood(word, label):
		# if word in Helper.word_dic:
		# 	return Helper.word_dic[word][label] / Helper.doc_count[label]
		# return 1/Helper.doc_count[label]
		# if method == "binary":
			# val = 1
			# if word in Helper.word_dic_doc:
				# val = Helper.documentFrequency(word, label) / Helper.doc_count[label]
			# return val
		# else:
		val = 0
		if word in Helper.word_dic:
			val = Helper.wordFrequency(word, label)
		return (val + 1) / (Helper.count(label) + Helper.vocabulary_size)


	@staticmethod
	def applyBernoulli(test_Words):
		score=[]
		for label in (notspam, spam):
			score.append(math.log(Helper.getPrior(label)))
			for word in Helper.word_dic_doc.iterkeys():
				if word in test_Words:
					# word present
					# print Helper.doc_count[label]
					# print word,"-",Helper.documentFrequency(word, label),"-",Helper.doc_count[label]
					# print Helper.doc_count[label]
					# raw_input()
					if Helper.documentFrequency(word, label) <> 0:
						score[label] += math.log(Helper.documentFrequency(word, label) / Helper.doc_count[label])

				else:
					# word not present
					# print word,"-",Helper.documentFrequency(word, label),"-",Helper.doc_count[label]
					if Helper.documentFrequency(word, label) <> 0:
						if (Helper.documentFrequency(word, label) / Helper.doc_count[label]) == 1:
							score[label] += math.log(0.001)
		return score

	@staticmethod
	def getPrior(label):
		return Helper.doc_count[label] / (Helper.doc_count[notspam] + Helper.doc_count[spam])


	@staticmethod
	def getOdds(words):
		num = 0.0
		deno = 0.0
		# P(S|w1,w2..wn)
		for word in words:
			n = Helper.getLikelihood(word, spam)
			#print "n ",n

			d = Helper.getLikelihood(word, notspam)
			#print "d ",d
			if n and d:
				num += math.log(n)
				deno += math.log(d)
		num += math.log(Helper.getPrior(spam))
		deno += math.log(Helper.getPrior(notspam))
		# print "ratio : ",num/deno
		return num, deno



	@staticmethod
	def getLabel(word_dic, word_dic_doc, doc_count, vocabulary_size, wordsPerClass, words, actual_label, method):
		Helper.word_dic = word_dic
		Helper.doc_count = doc_count
		Helper.vocabulary_size = vocabulary_size
		Helper.wordsPerClass = wordsPerClass
		Helper.word_dic_doc = word_dic_doc

		if method == "multinomial":
			num, deno = Helper.getOdds(words)
			if  num > deno:
				return spam
			return notspam
		else:
			score = Helper.applyBernoulli(words)
			if score[spam] > score[notspam]:
				return spam
			return notspam
		#Helper.ratio[actual_label] += num / deno
		#Helper.ratio[actual_label+2] += 1

		# 

		# if r <1.07108975892:
		# 	return spam
		# return notspam