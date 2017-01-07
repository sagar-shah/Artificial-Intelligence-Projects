# source https://github.iu.edu/AppliedMachineLearning/AML-FA16/blob/master/FinalDT/DecisionTree.py
from __future__ import division
from DTNode_Continuous import DTNode_Continuous
import math, random
import sys
from copy import deepcopy
import copy
global spam
spam = 1
global notspam
notspam = 0
global STOPPING_GENERATION
STOPPING_GENERATION = 8


class DTree_Continuous:
	docs = None
	wordSet = None
	root = None
	@staticmethod
	def setDocs(docs, wordSet):
		DTree_Continuous.docs = list(docs)
		DTree_Continuous.wordSet = set(wordSet)

	@staticmethod
	def buildTree():
		
		DTree_Continuous.root = DTree_Continuous.buildDecisionTree(DTree_Continuous.root, DTree_Continuous.docs, DTree_Continuous.wordSet, 0)
		# print "returning Root: ",DTree_Continuous.root.word
		return DTree_Continuous.root

	@staticmethod
	def buildDecisionTree(root, docs, wordSet, generation):
		#print len(docs), len(wordSet)

		if DTree_Continuous.terminatingConditionReached(docs, len(wordSet), generation):
			print "Terminating condition reached. Generation = ",generation
			leaf = DTNode_Continuous()
			leaf.label = DTree_Continuous.getClassLabel(docs)
			print "Class Label assigned = (",leaf.label,")"
			return leaf
		else:
			if root == None:
				print "."
				# print "Generation ", generation, ": root is None"
				root = DTNode_Continuous()
				#print "Generation ", generation, " Before building wordMetaDict."
				
				# print "Generation ", generation, " wordMetaDict is built now." , len(wordMetaDict)
				bestWordSplit = DTree_Continuous.getBestSplit(docs, wordSet)
				print "Hoping to get best split... for generation ", generation
				root.generation = generation

				if not bestWordSplit:
					# no word found as best split
					root.label = DTree_Continuous.getClassLabel(docs)
					return root

				
				root.word = bestWordSplit[0][0]
				print "Best split found at ",root.word
				

				#print bestWordSplit
				
				# idx = bestWordSplit[0][2]
				# print "Docs word: ",docs[idx][0]
				# print "---(",idx,")---: ",docs[idx][0]
				root.value = bestWordSplit[0][1]
				print "val: ",root.value#," type: ",type(root.value)
				# docs[idx][0][word]
				# print "Value of node set to : ",root.value
				root.wordSet = set(wordSet)
				nextLevelWordSet = wordSet - set([root.word])

				#print "Generation ", generation, " Valid split found."
				#print "word : ",root.word
				# Valid split is found.
				root.wordSet = set(wordSet)
				# remove the current word from the wordSet and provide it to the next level of building the tree
				nextLevelWordSet = wordSet - set([root.word])
				#print "Generation ", generation, " Purging data."
				_idx = bestWordSplit[0][1]
				leftNodeDocs = copy.deepcopy(docs[:_idx])
				rightNodeDocs = copy.deepcopy(docs[_idx:])
				#print "Going to left."
				root.left = DTree_Continuous.buildDecisionTree(root.left, leftNodeDocs, nextLevelWordSet, generation+1)
				#print "Going to right."
				root.right = DTree_Continuous.buildDecisionTree(root.right, rightNodeDocs, nextLevelWordSet, generation+1)

				#notPresent_spamDocs, notPresent_notSpamDocs, present_spamDocs, present_notSpamDocs = DTree_Continuous.purgeData(root.word, spamDocs, notSpamDocs)
				#print "Generation ", generation, "Purged the data. (",len(notPresent_spamDocs),len(notPresent_notSpamDocs),len(present_spamDocs),len(present_notSpamDocs),")"
				#print "Generation ", generation, " Building left generation."
				# root.left = DTree_Continuous.buildDecisionTree(root.left, notPresent_spamDocs, notPresent_notSpamDocs, nextLevelWordSet, generation+1)
				#print "Generation ", generation, " Building right generation."
				# root.right = DTree_Continuous.buildDecisionTree(root.right, present_spamDocs, present_notSpamDocs, nextLevelWordSet, generation+1)
				#print "Generation ", generation, " Done with this generation. Returning to parent gen."
				return root

	@staticmethod
	def getEntropy(docs):
		# get the entropy. Here the split test is the idx for the sorted docs
		# thus get the count of spam and not spam docs lying on both the sides of idx
		classColumn = zip(*docs)
		countClassNotSpam = classColumn[1].count(notspam)
		countClassSpam = classColumn[1].count(spam)
		defaultEntropy = 0.0
		if countClassNotSpam <> 0 and countClassSpam <> 0:
			defaultEntropy = countClassNotSpam * math.log(countClassNotSpam,2) + countClassSpam * math.log(countClassSpam,2)
			defaultEntropy *= -1
		return defaultEntropy

	# reference https://github.iu.edu/askarand/Harp3.0_RandomForest/blob/master/edu/iu/randomForest/RFTree.java
	@staticmethod
	def evalSplit(docs, idx):
		leftNodeDocs = docs[:idx]	#DTree_Continuous.getLeftNodeDocs(docs, idx)
		rightNodeDocs = docs[idx:] 	#DTree_Continuous.getRightNodeDocs(docs, idx)
		if len(leftNodeDocs) == 0 or len(rightNodeDocs) == 0:
			return sys.maxint
		leftNodeEntropy = DTree_Continuous.getEntropy(leftNodeDocs)
		rightNodeEntropy = DTree_Continuous.getEntropy(rightNodeDocs)
		totalEntropy = (len(leftNodeDocs) * leftNodeEntropy + len(rightNodeDocs) * rightNodeEntropy) / len(docs)
		return totalEntropy

	@staticmethod
	def getBestSplit(docs, curr_word_list):
		# iterate over all words and calculate its entropy
		print "Getting best split"
		bestWordSplit = []		# a tuple (word, idx) - current best word split
		i=0
		# bestWord = None
		# bestValue = None
		for word in curr_word_list:
			docs.sort(key=lambda x: x[0][word])
			# print "="				
			# print i
			i+=1
			docs, classCandidates = DTree_Continuous.getClassCandidates(word, docs)
			bestIdx = -1
			minEntropy = sys.maxint
			# now get the best index to split
			# print "len Candidates : ",len(classCandidates)
			# print len(docs)
			# raw_input()
			for idx in classCandidates:

				# print idx
				entropy = DTree_Continuous.evalSplit(docs, idx)
				if entropy < minEntropy:
					# update the minEntropy
					minEntropy = entropy
					# this is the best index so far, so update the bestIdx
					bestIdx = idx
			
			if bestIdx == -1:
				continue
			# here we have an idx for the word 'word' 
			# thus insert
			if len(bestWordSplit)==0:
				# not bestWordSplit checks if list is empty
				bestWordSplit = []
				#print "First word: ",word
				# print "first entry: ",bestWordSplit
				#print "-------New--------"
				val  = docs[bestIdx][0][word]
				#print "Doc : ",docs[bestIdx]
				#print "value of the word : ",val
				bestWordSplit.append([word, val,bestIdx, minEntropy])
				#print "Updated: ",bestWordSplit
				#print "-----------------"
				#raw_input()
			else:
				if bestWordSplit[0][3] < minEntropy:
					#print "Current word : ",word
					# update the bestWordSplit tuple
					#print  "-------Update------------"
					counter_val = docs[bestIdx][0]
					val = counter_val[word]
					#print "Doc: (Counter):",docs[bestIdx][0]
					#print "value of the word : ",docs[bestIdx][0][word]
					#print "from the counter = ",counter_val[word]
					bestWordSplit = []
					bestWordSplit.append([word, val, bestIdx, minEntropy])
					#print "Updated: ",bestWordSplit
					#print "--------------------"
		if not bestWordSplit:
			return None
		return bestWordSplit


	@staticmethod
	def getClassLabel(docs):
		classCounts = DTree_Continuous.countClassSamples(docs)
		if classCounts[spam] == 0:
			# notspam class count is 0
			#print "all are spam"
			return spam
		elif classCounts[notspam] == 0:
			#print "all are notspam"
			# spam class count is 0
			return notspam
		
		if classCounts[0] > classCounts[1]:
			# notspam class count is > than spam class count
			# thus return notspam as class label
			return notspam
		elif classCounts[0] < classCounts[1]:
			# notspam class count is < than spam class count
			# thus return spam as class label
			return spam
		else:
			# here both the class count is equal. 
			# assign class label randomly
			#print "returning random!"
			return notspam if random.randint(0,1) == 0 else spam


	@staticmethod 
	def uniClassSamples(classCounts):
		return True if classCounts[0] == 0 or classCounts[1] == 0 else False

	@staticmethod
	def terminatingConditionReached(docs, lwordSet, lgeneration):
		print "Testing terminating condition for generation : ",lgeneration
		if lgeneration <= STOPPING_GENERATION and lwordSet > 0 and not DTree_Continuous.uniClassSamples(DTree_Continuous.countClassSamples(docs)):
			return False
		return True



	@staticmethod
	def sortDocs(word, docs):
		# reference: http://stackoverflow.com/questions/18595686/how-does-operator-itemgetter-and-sort-work-in-python
		docs.sort(key=lambda x: x[0][word])
		#return docs

	# returns the sorted documents according to the attribute word and the classCandidates list
	@staticmethod
	def getClassCandidates(word, docs):
		# Now iterate over the sorted docs and see where's is the class change for the values for this attribute
		# reference : https://github.iu.edu/askarand/Harp3.0_RandomForest/blob/master/edu/iu/randomForest/RFTree.java
		classSpam = False
		classNotSpam = False
		classCandidates = []
		prevClassLabel = None
		idx = 0
		for en in docs:
			if word in en[0]:
				if prevClassLabel == None:
					prevClassLabel = en[1]
				elif prevClassLabel<>en[1]:
					prev = en[1]
					classCandidates.append(idx)
			idx+=1
		return docs, classCandidates

	@staticmethod
	def countClassSamples(docs):
		class0_cnt = 0
		class1_cnt = 0
		for doc in docs:
			if doc[1] == notspam:
				class0_cnt += 1
			else:
				class1_cnt += 1
		return class0_cnt, class1_cnt


	@staticmethod
	def testTree(root, test_words):
		if root == None:
			return None
		if root.label <> None:
			return root.label

		if root.word in test_words:
			# based on the count, go to either right or left
			if test_words[root.word] < root.value:
				# count less than root.value
				del test_words[root.word]
				return DTree_Continuous.testTree(root.left, test_words)
			else:
				# count greater than root.value
				del test_words[root.word]
				return DTree_Continuous.testTree(root.right, test_words)
		else:
			# if the word is not present, assume that the count is 0 
			# and thus move to the left
			del test_words[root.word]
			return DTree_Continuous.testTree(root.left, test_words)


	@staticmethod
	def printTreeInLevel(root):
		exit_level = 4
		print "Printing the Decision Tree (multinomial): Class 0 : notspam, class 1 : spam"
		print "Traverse upto level ",exit_level
		DTree_Continuous.printTree(root,0,exit_level)

	@staticmethod
	def printTree(root, curr_level, exit_level):

		if root==None:
			return
		if curr_level>=exit_level:
			return
		if root.label == None:
			print "Level : ",curr_level," = (",root.word,"<",root.value,")"
			# print "Word: ",root.word," < ",root.value
		elif root.label <> None:
			print "Level : ",curr_level," Class = (",root.label,")"
		# print "Going to left."
		DTree_Continuous.printTree(root.left,curr_level+1,exit_level)
		# print "Going to right."
		DTree_Continuous.printTree(root.right, curr_level+1, exit_level)