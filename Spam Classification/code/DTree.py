# source https://github.iu.edu/AppliedMachineLearning/AML-FA16/blob/master/FinalDT/DecisionTree.py
from __future__ import division
from DTNode import DTNode
import math, random
import sys

global spam
spam = 1
global notspam
notspam = 0
global STOPPING_GENERATION
STOPPING_GENERATION = 8

best_entropy = sys.maxint

class DTree:

	spamDocs = None # this is a list of indices indicating which spam docs are being processed
	notSpamDocs = None # this is a list of indices indicating which not spam docs are being processed
	totalDocs = None
	wordsPerDocSpam = None
	wordsPerDocNotSpam = None
	wordSet = None

	# init method
	@staticmethod
	def setDocs(spamDocs, notSpamDocs, wordsPerDocSpam, wordsPerDocNotSpam, wordSet):
		DTree.spamDocs = list(spamDocs)
		DTree.notSpamDocs = list(notSpamDocs)
		DTree.totalDocs = len(spamDocs) + len(notSpamDocs)
		DTree.wordsPerDocSpam = dict(wordsPerDocSpam)
		DTree.wordsPerDocNotSpam = dict(wordsPerDocNotSpam)
		DTree.wordSet = set(wordSet)

	@staticmethod
	def buildTree():
		root = None
		root = DTree.buildDecisionTree(root, DTree.spamDocs, DTree.notSpamDocs, DTree.wordSet, 0)
		return root 

	# AI code
	@staticmethod
	def buildDecisionTree(root, spamDocs, notSpamDocs, wordSet, generation):
		if DTree.terminatingConditionReached(len(spamDocs), len(notSpamDocs), len(wordSet), generation):
			#print "Terminating condition reached. Generation = ",generation
			leaf = DTNode()
			leaf.label = DTree.getClassLabel(spamDocs, notSpamDocs)
			#print "Class Label assigned = (",leaf.label,")"
			return leaf
		else:
			if root == None:
				print "."
				#print "Generation ", generation, ": root is None"
				root = DTNode()
				#print "Generation ", generation, " Before building wordMetaDict."
				wordMetaDict = DTree.buildWordMetaDict(wordSet, spamDocs, notSpamDocs)
				# print "Generation ", generation, " wordMetaDict is built now." , len(wordMetaDict)
				root.word = DTree.getBestSplit(wordMetaDict, wordSet)
				root.generation = generation

				if root.word == None:
					# Split not found thus it is a terminal state
					#print "Generation ", generation, " Best split not found. Getting class label"
					root.label = DTree.getClassLabel(spamDocs, notSpamDocs)
					#print "Generation ", generation, " Class label assigned : ",root.label
					return root

				print "Generation ", generation, " Valid split found."
				print "Best split: ",root.word,":",wordMetaDict[root.word]
				
				# Valid split is found.
				root.wordSet = set(wordSet)
				# remove the current word from the wordSet and provide it to the next level of building the tree
				nextLevelWordSet = wordSet - set([root.word])
				#print "Generation ", generation, " Purging data."
				notPresent_spamDocs, notPresent_notSpamDocs, present_spamDocs, present_notSpamDocs = DTree.purgeData(root.word, spamDocs, notSpamDocs)
				#print "Generation ", generation, "Purged the data. (",len(notPresent_spamDocs),len(notPresent_notSpamDocs),len(present_spamDocs),len(present_notSpamDocs),")"
				#print "Generation ", generation, " Building left generation."
				root.left = DTree.buildDecisionTree(root.left, notPresent_spamDocs, notPresent_notSpamDocs, nextLevelWordSet, generation+1)
				#print "Generation ", generation, " Building right generation."
				root.right = DTree.buildDecisionTree(root.right, present_spamDocs, present_notSpamDocs, nextLevelWordSet, generation+1)
				#print "Generation ", generation, " Done with this generation. Returning to parent gen."
				return root

	@staticmethod
	def getLog(probVal):
		if probVal == 0:
			return 0
		return math.log(probVal)

	@staticmethod
	def getEntropy(wordMetaDict, word):
		# for 'not present' class
		not_in_spam = wordMetaDict[word][0][spam]
		not_in_not_spam = wordMetaDict[word][0][notspam]
		not_present_class_total = not_in_spam + not_in_not_spam

		# for 'present' class
		in_spam = wordMetaDict[word][1][spam]
		in_not_spam = wordMetaDict[word][1][notspam]
		present_class_total = in_spam + in_not_spam
		if not_present_class_total == 0 or present_class_total == 0:
			return sys.maxint

		PsW_np = not_in_spam / not_present_class_total
		PnsW_np = not_in_not_spam / not_present_class_total

		
		EnpW = (- PsW_np * DTree.getLog(PsW_np)- PnsW_np * DTree.getLog(PnsW_np)) * (not_present_class_total)



		PsW_p = in_spam / present_class_total
		PnsW_p = in_not_spam / present_class_total
		EpW = (- PsW_p * DTree.getLog(PsW_p) - PnsW_p * DTree.getLog(PnsW_p)) * (present_class_total)

		return ((EnpW + EpW) / DTree.totalDocs)

	@staticmethod
	def getBestSplit(wordMetaDict, curr_word_list):
		global best_entropy
		best_entropy = sys.maxint
		best_word = None
		for word in curr_word_list:
			currWordEntropy = DTree.getEntropy(wordMetaDict, word)
			if currWordEntropy < best_entropy:
				best_entropy = currWordEntropy
				best_word = word
		return best_word

	@staticmethod
	def buildWordMetaDict(curr_word_list, spamDocs, notSpamDocs):
		wordMetaDict = {}
		for word in curr_word_list:
			#print "Word : ", word
			val = DTree.getMetaForWord(word, spamDocs, notSpamDocs)
			key = word
			wordMetaDict[key] = val
			# print wordMetaDict[key] if val[0]<>[0,0] or val[1]<>[0,0] else ""
		return wordMetaDict

	@staticmethod
	def getMetaForWord(word, spamDocs, notSpamDocs):
		# the following values are for each word.
		# this method would return 
		c_in_spam = 0
		c_not_in_spam = 0
		c_in_not_spam = 0
		c_not_in_not_spam = 0

		for k,v in DTree.wordsPerDocSpam.iteritems():
			if word in v:
				c_in_spam += 1
			else:
				c_not_in_spam += 1
		for k,v in DTree.wordsPerDocNotSpam.iteritems():
			if word in v:
				c_in_not_spam += 1
			else:
				c_not_in_not_spam += 1	
		return [[c_not_in_not_spam, c_not_in_spam],[c_in_not_spam, c_in_spam]]

	@staticmethod
	def getClassLabel(spamDocs, notSpamDocs):
		if len(spamDocs) == 0 and len(notSpamDocs) == 0:
			return notspam if random.randint(0,1) == 0 else spam
		elif len(spamDocs) == 0:
			return notspam
		elif len(spamDocs) == 0:
			return spam
		elif len(spamDocs) >= len(notSpamDocs):
			return spam
		else:
			return notspam

	@staticmethod
	def terminatingConditionReached(lspamDocs, lnotSpamDocs, lwordSet, generation):
		print "Testing terminating condition for generation : ",generation
		return True if lspamDocs == 0 or lnotSpamDocs == 0 or lwordSet == 0 or generation >= STOPPING_GENERATION else False

		#return True if node<>None and node.generation >= STOPPING_GENERATION else False

	@staticmethod
	def purgeData(word, spamDocs, notSpamDocs):
		# must return in this format:
		# notPresent_spamDocs, notPresent_notSpamDocs, present_spamDocs, present_notSpamDocs
		notPresent_spamDocs=[]
		notPresent_notSpamDocs=[]
		present_spamDocs=[]
		present_notSpamDocs=[]
		for k,v in DTree.wordsPerDocSpam.iteritems():
			if word in v and k in spamDocs:
				# add the index of this document ot present_spamDocs list
				present_spamDocs.append(k)
			else:
				# add the index of this document ot notPresent_spamDocs list
				notPresent_spamDocs.append(k)

		for k,v in DTree.wordsPerDocNotSpam.iteritems():
			if word in v and k in notSpamDocs:
				# add the index of this document ot present_notSpamDocs list
				present_notSpamDocs.append(k)
			else:
				# add the index of this document ot notPresent_notSpamDocs list
				notPresent_notSpamDocs.append(k)

		return notPresent_spamDocs, notPresent_notSpamDocs, present_spamDocs, present_notSpamDocs

	@staticmethod
	def testTree(root, test_words):
		if root == None:
			return None
		if root.label <> None:
			return root.label
		# root.word in test_words
		if root.word in test_words:
			#print "Right of ",root.word
			#raw_input()
			# go to the right
			# remove the current word which matched
			test_words.remove(root.word)
			return DTree.testTree(root.right, test_words)
		else:
			#print "Left of ",root.word
			# go to the left
			#test_words.remove(root.word)
			return DTree.testTree(root.left, test_words)


	@staticmethod
	def printTreeInLevel(root):
		exit_level = 4
		print "Printing the Decision Tree (binary) Class 0 : notspam, class 1 : spam"
		print "Traverse upto level ",exit_level
		DTree.printTree(root,0,exit_level)

	@staticmethod
	def printTree(root, curr_level, exit_level):
		if root==None:
			return
		if curr_level>=exit_level:
			return
		if root.label == None:
			print "Level : ",curr_level," = (",root.word,")"
		elif root.label <> None:
			print "Level : ",curr_level," Class = (",root.label,")"
		DTree.printTree(root.left,curr_level+1,exit_level)
		DTree.printTree(root.right, curr_level+1, exit_level)