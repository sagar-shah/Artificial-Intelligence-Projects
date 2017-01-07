from __future__ import division
import os, re, glob
import errno
import math
from decimal import Decimal
import heapq
import re, random, collections
import pickle
import sys
from classfile import TrainedModel


# The problem has been solved using Naive bayes. We train a model based on the fraction of documents that we are
# allowed to read the topics of. The data is split into labelled and unlabelled data sets. Using the labelled data
# we calculate the probabilities of unlabelled data and build our model. The training model consists of topic_wordfreq_dic
# which stores the frequency of words based on topic.  topic_doc_count_dic conists of number of documents in each topic.
# cachedStopWords consist of all word that we want to ignore that add no semantic meaning. 

# Fraction	Accuracy
#    1 			80.41%
#    0.75       56.42%
#	0.5 		54.12
#	0.1 		42.27
#	0    		5.29



(mode, dataset_directory, modelFile) = sys.argv[1:4]

# print mode,dataset_directory,modelFile

if mode=='train':
	fraction = sys.argv[4]
	# print fraction




		
def can_read(fraction):

	# print random.random(),fraction
	if random.random() <= float(fraction):
		return True 
	return False
# def can_read_demo(name):
# 	if name=='unlabel_1' or name=='unlabel_3':
# 		return False
# 	return True

def train(path,fraction):
	
	topics_list = get_immediate_subdirectories(path)
	# print "topics_list",topics_list
	# cachedStopWords = ['0', '1', '2', '3', '4', '5', '6', '7','8','9','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you','your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',  'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',  'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',  'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',  'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',  'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',  'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',  'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',  'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',  'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll',  'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven',  'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
	
	cachedStopWords = ['0', '1', '2', '3', '4', '5', '6', '7','8','9','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \
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
	  u'whom', u'why', u"why's", u'with', u"won't", u'would', u"wouldn", u'you' \
	  u'your', u'yours', u'yourself', u'yourselves']

	uglyWords = ["also","value", "a","abbr","acronym","address","area","b","base","bdo","big","blockquote","body","br","button","caption","cite","code","col","colgroup","dd","del","dfn","div","dl","DOCTYPE","dt","em","fieldset","form","h1","h2","h3","h4","h5","h6","head","html","hr","i","img","input","ins","kbd","label","legend","li","link","map","meta","noscript","object","ol","optgroup","option","p","param","pre","q","samp","script","select","small","span","strong","style","sub","sup","table","tbody","td","textarea","tfoot","th","thead","title","tr","tt","ul","var"]

	USStates = ['washington', 'wisconsin', 'virginia', 'florida', 'wyoming', 'hampshire', 'jersey', 'mexico', 'national', 'carolina', 'dakota', 'nebraska', 'york', 'rhode island', 'nevada', 'guam', 'colorado', 'california', 'georgia', 'connecticut', 'oklahoma', 'ohio', 'kansas', 'kentucky', 'oregon',  'delaware', 'columbia', 'hawaii', 'puerto rico', 'texas', 'louisiana', 'tennessee', 'pennsylvania', 'virginia', 'virgin islands', 'alaska', 'alabama', 'american samoa', 'arkansas', 'vermont', 'illinois', 'indiana', 'iowa', 'arizona', 'idaho', 'maine', 'maryland', 'massachusetts', 'utah', 'missouri', 'minnesota', 'michigan', 'montana', 'northern mariana islands', 'mississippi']

	directions = ['north', 'south', 'east', 'west']

	technicalWords = ['example','version','emails','daemon','index','ascii','sites','site','msmail','mailto',	\
	'outlook','yahoo','hotmail','com', 'net', 'type', 'radio', 'name', 'smtp', 'localhost', \
	'mime','mail','email','align','mailing','linux','imap','center']

	# cachedStopWords.append(stopWords1)
	# cachedStopWords.append(uglyWords)
	# cachedStopWords.append(USStates)
	# cachedStopWords.append(directions)
	# cachedStopWords.append(technicalWords)

	otherwords = ['ax', 'edu', 'x', '_', 'g', 'one', 'w', 'r','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

	cachedStopWords_set = set(cachedStopWords + stopWords1 + uglyWords + USStates + directions + technicalWords + otherwords)
	# cachedStopWords_set.add(set(stopWords1))
	# cachedStopWords_set.add(set(uglyWords))
	# cachedStopWords_set.add(set(USStates))
	# cachedStopWords_set.add(set(directions))
	# cachedStopWords_set.add(set(technicalWords))
	# print topics_list
	# topic_wordfreq_dic = {}
	# topic_doc_count_dic = {}

	#1st iteration on entire daataset. Goal is to split data into labelled and unlabelled
	if fraction == 1:
		topic_wordfreq_dic = {}
		topic_doc_count_dic = {}
		for topic in topics_list:
			topic_wordfreq_dic[topic] = {}
			topic_doc_count_dic[topic] = 0

			sub_topic_path = path + "\\" + topic
			
			sub_topic_path = sub_topic_path.replace("\\","/")
			# print sub_topic_path  + "/*.*"
			
			files = os.listdir(sub_topic_path)   
			topic_doc_count_dic[topic] = len(files)

			# print "topic doc count"
			# print topic_doc_count_dic
			# print files
			for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
				
				# can_read_topic = can_read(fraction)
				
				try:
					with open(sub_topic_path  + "/" + name) as f: #in 1 file
						# print name		

					    l = [re.findall("\w+",line.rstrip().lower())  for line in f if line.strip()]
					    # print "l= " +str(l)

					    for word_l in l:
							for word in word_l:
								word = re.sub('[^a-zA-Z]', '', word)
								if word in topic_wordfreq_dic[topic]:
									topic_wordfreq_dic[topic][word] += 1
								else:
									topic_wordfreq_dic[topic][word] = 1 
								# print w
				except IOError as exc:
					if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
						raise # Propagate other kinds of IOError

		
		for topic2 in topics_list:
			entries_to_remove(cachedStopWords,topic_wordfreq_dic[topic2])

		
	else:
		labelled = []
		unlabelled = []
		topic_wordfreq_dic = {}
		topic_doc_count_dic = {}
		
		#initialize topic doc count and topic_wordfreq_dic for all topics
		for t in topics_list:
			topic_wordfreq_dic[t] = {}
			topic_doc_count_dic[t] = 0

		for topic in topics_list:
			sub_topic_path = path + "\\" + topic
			
			sub_topic_path = sub_topic_path.replace("\\","/")
			# print sub_topic_path  + "/*.*"
			
			files = os.listdir(sub_topic_path)   

			# print "topic doc count"
			# print topic_doc_count_dic
			# print files
			for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
				can_read_topic = can_read(fraction)
				# can_read_topic = can_read_demo(name)
				# print can_read_topic
				try:
					with open(sub_topic_path  + "/" + name) as f: #in 1 file
						# print name		

						sentence_list = [re.findall("\w+",line.rstrip().lower())  for line in f if line.strip()]
						# print "l= " +str(l)
						all_words_in_doc = []
						
						if can_read_topic:
							
							for word_list in sentence_list:
								for word in word_list:
									if word not in cachedStopWords_set:
										all_words_in_doc.append(word)
										if word in topic_wordfreq_dic[topic]:
											# print "Updated word",word,"for topic",topic,"file name",name
											topic_wordfreq_dic[topic][word] += 1
										else:
											# print "------------------Added word",word,"for topic",topic,"file name",name
											topic_wordfreq_dic[topic][word] = 1 
						
							# print all_words_in_doc
							words_freq_in_doc = collections.Counter(all_words_in_doc)

							words_freq_in_doc = remove_low_frequency_words(words_freq_in_doc)

							# print words_freq_in_doc
							topics_prob = {}


							topics_prob[topic] = 1
							labelled.append(list((words_freq_in_doc,topics_prob)))
							topic_doc_count_dic[topic] += 1
							

							# print "LLLLLLLLLLLLLLL ", labelled
						else:
							# print "unl  " , topic
							for word_list in sentence_list:
								for word in word_list:
									if word not in cachedStopWords_set:
										all_words_in_doc.append(word)

							words_freq_in_doc = collections.Counter(all_words_in_doc)

							words_freq_in_doc = remove_low_frequency_words(words_freq_in_doc)

							# print words_freq_in_doc
							topics_prob = {}

							for temp_topic in topics_list:
								topics_prob[temp_topic] = 0
							unlabelled.append(list((words_freq_in_doc,topics_prob)))
							# print "UUUUUUUUUUUUUUUU " ,unlabelled
							topic_doc_count_dic[topic] += 1

				except IOError as exc:
					if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
						raise # Propagate other kinds of IOError

		# print "labelled ", labelled
		# print "unlabelled " ,unlabelled
		# print "topic_wordfreq_dic", topic_wordfreq_dic
		 # print "topic_doc_count_dic", topic_doc_count_dic

		#Iterate over unlabelled dataset and build probabilities for all topics
		for doc in unlabelled:
			updated_topic_prob = doc[1]
			# print "-------------------------------------------------------------------"
			for temp_topic2 in topics_list:
				updated_topic_prob[temp_topic2] = get_posterior_topic_given_allwords(temp_topic2,doc[0],topic_wordfreq_dic,topic_doc_count_dic,topics_list,cachedStopWords_set)
				
			total_partial_prob = sum(updated_topic_prob.itervalues())
			

			# if(total_partial_prob == 0.0):
			# 	print updated_topic_prob
			# 	raw_input()

			#normalize prob in updated_topic_prob
			for temp_topic3 in updated_topic_prob.iterkeys():
				updated_topic_prob[temp_topic3] /= total_partial_prob	

			#update topic_doc_count_dic
			for temp_topic4 in updated_topic_prob.iterkeys():
				topic_doc_count_dic[temp_topic4] += updated_topic_prob[topic]



		#update topic_wordfreq_dic before merging unlbelled with labelled
		# print "unlabelled doc count:",len(unlabelled)
		# i=1
		for doc in unlabelled:
			# print "unlabelled doc",i
			# i +=1
			word_list_freq = doc[0]

			word_list_freq = remove_low_frequency_words(word_list_freq)

			for word in word_list_freq.iterkeys():
				if word not in cachedStopWords_set:
					normalized_topic_freq = doc[1]
					for temp_topic5,prob in normalized_topic_freq.iteritems():
						if word in topic_wordfreq_dic[temp_topic5]:
							topic_wordfreq_dic[temp_topic5][word] += prob*word_list_freq[word]
						else:
							# topic_wordfreq_dic[topic][word] = 1/(sum(topic_wordfreq_dic[topic].itervalues())+len(topics_list))
							topic_wordfreq_dic[temp_topic5][word] = 0.000001




		#save unlabbed data start index
		x = len(labelled)
		# print "unlabelled data starts at index",x

		#add unlabelled data to labelled - update topic_wordfreq_dic and topic_doc_count_dic too
		labelled = labelled + unlabelled

		#multiple iterations for unlabelled data
		for iterations in xrange(0,0):
			for i in xrange(x,len(labelled)):
				doc2 = labelled[i]

				updated_topic_prob = doc2[1]
				# print "-------------------------------------------------------------------"
				for temp_topic8 in topics_list:
					updated_topic_prob[temp_topic8] = get_posterior_topic_given_allwords(temp_topic8,doc2[0],topic_wordfreq_dic,topic_doc_count_dic,topics_list,cachedStopWords_set)
					
				total_partial_prob = sum(updated_topic_prob.itervalues())
				

				# if(total_partial_prob == 0.0):
				# 	print updated_topic_prob
				# 	raw_input()

				#normalize prob in updated_topic_prob
				for temp_topic9 in updated_topic_prob.iterkeys():
					updated_topic_prob[temp_topic9] /= total_partial_prob	

				#update topic_doc_count_dic
				for temp_topic10 in updated_topic_prob.iterkeys():
					topic_doc_count_dic[temp_topic10] += updated_topic_prob[topic]

			#update topic_wordfreq_dic before merging unlbelled with labelled
			for i in xrange(x,len(labelled)):
				doc3 = labelled[i]
				word_list_freq = doc3[0]

				word_list_freq = remove_low_frequency_words(word_list_freq)

				for word in word_list_freq.iterkeys():
					if word not in cachedStopWords_set:
						normalized_topic_freq = doc3[1]
						for temp_topic11,prob in normalized_topic_freq.iteritems():
							if word in topic_wordfreq_dic[temp_topic11]:
								topic_wordfreq_dic[temp_topic11][word] += prob*word_list_freq[word]
							else:
								# topic_wordfreq_dic[topic][word] = 1/(sum(topic_wordfreq_dic[topic].itervalues())+len(topics_list))
								topic_wordfreq_dic[temp_topic11][word] = 0.000001

	w = open("distinctive_words.txt","w")
	# print topic_wordfreq_dic
	for temp_topic6 in topics_list:
		top10 = heapq.nlargest(10, topic_wordfreq_dic[temp_topic6], key=topic_wordfreq_dic[temp_topic6].get)
		write_words = "" + str(temp_topic6) + "" + str(top10) + "\n"
		w.write(write_words)
		# print write_words
	w.close()
	print "done"
	# print "labelled2 ", labelled
	# print "unlabelled2 " ,unlabelled
	# print "topic_wordfreq_dic2", topic_wordfreq_dic
	# print "topic_doc_count_dic2", topic_doc_count_dic
	# print "Training complete"
	return topic_wordfreq_dic,topic_doc_count_dic,cachedStopWords_set
	# return 1

def remove_low_frequency_words(dic):
	freq_cutoff = 3
	low_freq_words = []
	for word,freq in dic.iteritems():
		if freq < freq_cutoff:
			low_freq_words.append(word)
		
	entries_to_remove(low_freq_words,dic)

	return dic

def entries_to_remove(entries, the_dict):
	for key in entries:
		if key in the_dict:
			del the_dict[key]


def get_posterior_topic_given_allwords(topic,all_words,topic_wordfreq_dic,topic_doc_count_dic,topics_list,cachedStopWords_set): # topics are atheism, autos..etc, all_words are all words in a document
	
	# topic = "read"
	# all_words=['linux','website']

	num = []
	no_of_topics = len(topics_list)
	total_docs = sum(topic_doc_count_dic.itervalues())
	# print total_docs

	x = (topic_doc_count_dic[topic]+1) / total_docs   #+1 for smoothing
	num.append(x)
	# print num
	# raw_input()	
	total_words_in_topic = sum(topic_wordfreq_dic[topic].itervalues())
	# print "Topic word freq ",topic_wordfreq_dic
	for word in all_words:
		if word not in cachedStopWords_set:
			try:
				# if word not in set_cachedStopWords:
				num.append((topic_wordfreq_dic[topic][word]+1) / total_words_in_topic) # +1 for smoothing
			except KeyError:
				# missing_words_count += 1
				num.append(0.000001)  
	
	#print "topic processed : ",topic
	# print topic_wordfreq_dic[topic]
	
	# print topic
	# print num
	# raw_input()
	total = 0.0
	# print "NUM",str(num)
	for y in num:
		# print"y:",y
		total += math.log(y)

	return total
	# return math.exp(total)
	# for word in all_words:
	# 	word_given_topic(word,topic)

# def word_given_topic(word,topic):




def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]


def get_estimate(f,topic_wordfreq_dic,topic_doc_count_dic,topics_list,actual_topic,total_docs,cachedStopWords_set):

	# print topic_wordfreq_dic
	# print topic_doc_count_dic
	# print f
	best_topic = 'None'
	best_total = Decimal('-Infinity')
	missing_words_count = 0

	
	# print "total docs",total_docs

	all_words_in_doc = []
	list_of_lines = [re.findall("\w+",line.rstrip().lower())  for line in f if line.strip()]
	for word_list in list_of_lines:
		for word in word_list:
			if word not in cachedStopWords_set:
				word = re.sub('[^a-zA-Z]', '', word)
				all_words_in_doc.append(word)

	# all_words_in_doc = re.sub('[^a-zA-Z \n]', '', all_words_in_doc).lower()

	all_words_in_doc_freq = collections.Counter(all_words_in_doc)
	all_words_in_doc_freq = remove_low_frequency_words(all_words_in_doc_freq)

	# print topics_list
	for topic in topics_list:
		num = []

		x = topic_doc_count_dic[topic] / total_docs
		num.append(x)
		# print num
		# raw_input()	
		total_words_in_topic = sum(topic_wordfreq_dic[topic].itervalues())
		for word in all_words_in_doc_freq.iterkeys():
			if word not in cachedStopWords_set:
				try:
					# if word not in set_cachedStopWords:
					num.append(topic_wordfreq_dic[topic][word] / total_words_in_topic)
				except KeyError:
					missing_words_count += 1
					num.append(0.000001)
		
		#print "topic processed : ",topic
		# print topic_wordfreq_dic[topic]
		
		# print topic
		# print num
		# raw_input()
		total = 0.0
		# print "NUM",str(num)
		for y in num:
			# print "y ",y
			total += math.log(y)
		
		if total > best_total:
			# print total,best_total		
			best_total = total
			best_topic = topic

	# print "missing words:",missing_words_count,"Actual topic:",actual_topic,
	return best_topic


def test(path,topic_wordfreq_dic,topic_doc_count_dic,cachedStopWords_set):

	correct_prediction = 0
	total_docs = 0
	topics_list = get_immediate_subdirectories(path)

	confusion_matrix = {}
	for t in topics_list:
		confusion_matrix[t] = {}
		for t2 in topics_list:
			confusion_matrix[t][t2] = 0



	for topic in topics_list:

		sub_topic_path = path + "\\" + topic
		
		sub_topic_path = sub_topic_path.replace("\\","/")
		# print sub_topic_path  + "/*.*"
		
		files = os.listdir(sub_topic_path)   
		total_docs += len(files)
		# print files
		for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
			try:
				with open(sub_topic_path  + "/" + name) as f: #in 1 file
					# print name,		
				    
		 			# print "l= " +str(l)
		 			estimated_topic = get_estimate(f,topic_wordfreq_dic,topic_doc_count_dic,topics_list,topic,total_docs,cachedStopWords_set) 
		 			# print estimated_topic

		 			confusion_matrix[topic][estimated_topic] += 1

		 			if estimated_topic == topic:
		 				correct_prediction += 1

			except IOError as exc:
				if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
					raise # Propagate other kinds of IOError

	for key in confusion_matrix.iterkeys():
		print key,":",confusion_matrix[key]

	# correct_prediction2 = 0
	# for k2 in confusion_matrix.iterkeys():
	# 	correct_prediction2 += confusion_matrix[k2][k2]

	# total_docs2 = 0
	# for k3 in confusion_matrix.iterkeys():
	# 	total_docs2 += sum(confusion_matrix[k3].itervalues()) 
	print "Accuracy =",correct_prediction / total_docs * 100
	# print "Accuracy =",correct_prediction2 / total_docs2


# train_path = "C:\\Users\\Sagar\\Google Drive\\Study\\Elements of Artificial Intelligence\\Assignments\\Assignment 4\\askarand-sasshah-tejakumt-a4\\part2\\train"
# sample_train_path = "C:\\Users\\Sagar\\Google Drive\\Study\\Elements of Artificial Intelligence\\Assignments\\Assignment 4\\askarand-sasshah-tejakumt-a4\\part2\\sample_train"
# code_debug_train_path = "C:\\Users\\Sagar\\Google Drive\\Study\\Elements of Artificial Intelligence\\Assignments\\Assignment 4\\askarand-sasshah-tejakumt-a4\\part2\\code_debug_train"

# test_path = "C:\\Users\\Sagar\\Google Drive\\Study\\Elements of Artificial Intelligence\\Assignments\\Assignment 4\\askarand-sasshah-tejakumt-a4\\part2\\test" 
# sample_test_path = "C:\\Users\\Sagar\\Google Drive\\Study\\Elements of Artificial Intelligence\\Assignments\\Assignment 4\\askarand-sasshah-tejakumt-a4\\part2\\sample_test"
# code_debug_test_path = "C:\\Users\\Sagar\\Google Drive\\Study\\Elements of Artificial Intelligence\\Assignments\\Assignment 4\\askarand-sasshah-tejakumt-a4\\part2\\code_debug_test"


if(mode=='train'):
	train_data = train(dataset_directory,fraction)
	# train_data = train(sample_train_path)
	# train_data = train(code_debug_train_path)

	currDir = os.path.dirname(os.path.realpath(__file__))
	# modelFile = "trained_model"
	modelFilePath = os.path.join(currDir, modelFile)


	trainedModel = TrainedModel(train_data[0],train_data[1],train_data[2])

	with open(modelFilePath, "wb") as outfile:
		print "writing to ",modelFilePath
		pickle.dump(trainedModel, outfile, -1)

	print "done training"


# topic_wordfreq_dic = train_data[0]
# topic_doc_count_dic = train_data[1]
# cachedStopWords_set = train_data[2]

if(mode=='test'):
	dtModel = None
	with open(modelFile, 'rb') as infile:
		dtModel = pickle.load(infile)
	print("done reading training model")
	#print dtModel.topic_wordfreq_dic2,dtModel.topic_doc_count_dic2,dtModel.cachedStopWords_set2
	test(dataset_directory,dtModel.topic_wordfreq_dic2,dtModel.topic_doc_count_dic2,dtModel.cachedStopWords_set2)



# test(sample_test_path,topic_wordfreq_dic,topic_doc_count_dic,cachedStopWords_set)
# test(code_debug_test_path,topic_wordfreq_dic,topic_doc_count_dic,cachedStopWords_set)




