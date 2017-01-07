# ./spam mode technique dataset-directory model-file

'''
1. Problem Formulation:
Bayes - Binary: Bernoulli Distribution
		Multinomial : Multinomial Distribution
dt - Binary: Dividing into 2 classes- present and not present,
		     if word is not present - left branch, else right branch, and recursively build.
	 Multinomial: Split is on word's frequency.
	 			  If it is less than best-split, traverse left branch, else right-branch is traversed.

2. Working of the Program:
	Binary - Number of documents in which a word occurs
	Multinomial - Number of times the word occurs

3. Assumptions:
	We have removed stopwords, US states, domain specific technical words.
	We have also restricted length of words within a specific range.
	Further, we have used regex filters such as tag, emailId, hex, ip etc
	We have eliminated words which have vowel-length ratio not within 0.3 and 0.7
	Saving the model file where the python code is.

    Design:
	 We have maintained modularity with Node and Tree classes, and also kept
	 cleaning process into separate file. model classes are dedicated for storing and printing
	 dt node and dt node continuous' word

4. Results:
	Bayes:

	Testing Bayes
	Testing binary:
	Confusion matrix :
	| TP-  289 | FN-  896 |
	| FP-  505 | TN- 864 |
	Accuracy :  45.1448707909 %
	Testing multinomial:
	Confusion matrix :
	| TP-  721 | FN-  464 |
	| FP-  78 | TN- 1291 |
	Accuracy :  78.7783868442 %


	Decision Tree:
	Testing dt- binary:
	Confusion matrix :
	| TP-  60 | FN-  1125 |
	| FP-  0 | TN- 1369 |
	Accuracy :  55.9514487079 %
	Testing dt- continuous (multinomial):
	Confusion matrix :
	| TP-  1245 | FN-  1125 |
	| FP-  1369 | TN- 1369 |
	Accuracy :  51.1746280345 %

	
5. Conclusion: 
	Bayes - Multinomial is better
	DT - Binary is better

'''

from __future__ import division
import sys, pickle, os
from DecisionTreeModel import DTModel
from dataProfiler import DataProfiler
from DTree import DTree
from DTree_Continuous import DTree_Continuous
from BayesClassifierModel import bayesClassifierModel
global spam
spam = 1
global notspam
notspam = 0

def usage():
	print "Usage ./spam mode technique dataset-directory model-file"



# @staticmethod
def train(technique, spamTrainingSetPath, notSpamTrainingSetPath, modelFilePath):
	if technique=="bayes":
		print "Training binary"
		DataProfiler.readDir(notSpamTrainingSetPath,technique,"binary","train", notspam)
		DataProfiler.readDir(spamTrainingSetPath,technique,"binary","train", spam)
		print "Training multinomial"
		DataProfiler.readDir(spamTrainingSetPath,technique,"multinomial","train", spam)
		DataProfiler.readDir(notSpamTrainingSetPath,technique,"multinomial","train", notspam)
		#raw_input()
		DataProfiler.vocabulary_size = len(DataProfiler.word_dic)
		DataProfiler.display()
		#print DataProfiler.doc_count
		bayesModel = bayesClassifierModel(DataProfiler.word_dic, DataProfiler.word_dic_doc, DataProfiler.vocabulary_size, DataProfiler.wordsPerClass, DataProfiler.doc_count)
		with open(modelFilePath, "wb") as outfile:
			print "writing to ",modelFilePath
			pickle.dump(bayesModel, outfile, -1)

	elif technique=="dt":
		# binary
		print "Decision tree."
		DataProfiler.readDir(notSpamTrainingSetPath, "dt", "binary", "train", notspam)
		print "Done reading notspam documents."
		DataProfiler.readDir(spamTrainingSetPath, "dt", "binary", "train", spam)
		print "Done reading spam documents."
		DTree.setDocs(DataProfiler.spamDocs, DataProfiler.notSpamDocs, DataProfiler.wordsPerDocSpam, DataProfiler.wordsPerDocNotSpam, DataProfiler.wordSet)
		print "Building decision tree. (Binary)."
		# DataProfiler.dTNode_root = DTree.buildTree()
		DataProfiler.rootBin = DTree.buildTree()
		#print DataProfiler.rootBin.word, " is the root for binary."		
		# raw_input()
		# multivalue split
		DataProfiler.readDir(notSpamTrainingSetPath, technique, "multinomial", "train", notspam)
		print "Done reading notspam documents."
		DataProfiler.readDir(spamTrainingSetPath, technique, "multinomial", "train", spam)
		print "Done reading spam documents."
		#print DataProfiler.wordsPerDocContinuous
		# raw_input()
		DTree_Continuous.setDocs(DataProfiler.wordsPerDocContinuous, DataProfiler.wordSet)
		print "Building decision tree. (Multinomial)."
		# raw_input()
		# DataProfiler.dTNode_Continuous_root =  DTree_Continuous.buildTree()
		DataProfiler.rootContinuous = DTree_Continuous.buildTree()

		#print DataProfiler.rootContinuous.word," is the root for multinomial"
		# DTree_Continuous.printTreeInLevel(DataProfiler.rootContinuous)

		# raw_input()
		print "-------------------------------------------------------"
		DTree.printTreeInLevel(DataProfiler.rootBin)
		print "-------------------------------------------------------"
		DTree_Continuous.printTreeInLevel(DataProfiler.rootContinuous)
		print "-------------------------------------------------------"
		# dtModel = DTModel(DataProfiler.dTNode_root, DataProfiler.dTNode_Continuous_root)
		'''
		dtModel = DTModel(DataProfiler.rootBin, DataProfiler.rootContinuous)
		with open(modelFilePath, "wb") as outfile:
			print "Writing to ", modelFilePath
			pickle.dump(dtModel, outfile, -1)
		print "done with tree"

		with open(modelFilePath, 'rb') as infile:
			dtModel = pickle.load(infile)

		DataProfiler.rootBin = dtModel.rootBin
		DataProfiler.rootContinuous = dtModel.rootContinuous
		'''
		'''
		print "Displaying top 4 layers (multinomial): \n"
		# DTree_Continuous.printTreeInLevel(DataProfiler.dTNode_Continuous_root)
		print DataProfiler.rootContinuous.word," is the root for multinomial"
		DTree_Continuous.printTreeInLevel(DataProfiler.rootContinuous)
		'''

		dtModel = DTModel(DataProfiler.rootBin, DataProfiler.rootContinuous)
		# print dtModel
		print DataProfiler.rootContinuous.word
		# raw_input()
		with open(modelFilePath, "wb") as outfile:
			print "Writing to ", modelFilePath
			pickle.dump(dtModel, outfile, -1)
		print "done with tree"
		#print "Displaying top 4 layers (binary method): \n"
		#DTree.printTreeInLevel(DataProfiler.dTNode_root)


# @staticmethod
def test(technique, spamDatasetPath, notSpamDataSetPath, modelFilePath):
	
	if technique=="bayes":
		print "Testing Bayes"
		bayesModel = None
		with open(modelFilePath, 'rb') as infile:
			bayesModel = pickle.load(infile)
		#print bayesModel
		DataProfiler.word_dic = bayesModel.word_dic
		DataProfiler.word_dic_doc = bayesModel.word_dic_doc
		DataProfiler.vocabulary_size = bayesModel.vocabulary_size
		DataProfiler.wordsPerClass = bayesModel.wordsPerClass
		DataProfiler.doc_count = bayesModel.doc_count
		print "Testing binary:"
		DataProfiler.readDir(notSpamDataSetPath,technique, "binary","test", notspam)
		DataProfiler.readDir(spamDatasetPath,technique, "binary","test", spam)
		print "Confusion matrix : "
		print "| TP- ",DataProfiler.TP,"| FN- ",DataProfiler.FN,"|"
		print "| FP- ",DataProfiler.FP,"| TN-",DataProfiler.TN,"|"
		print "Accuracy : ", ((DataProfiler.TP + DataProfiler.TN) / (DataProfiler.TP + DataProfiler.TN + DataProfiler.FP + DataProfiler.FN)) * 100, "%"
		
		DataProfiler.TP = 0
		DataProfiler.FN = 0
		DataProfiler.FP = 0
		DataProfiler.TN = 0
		print "Testing multinomial:"
		DataProfiler.readDir(notSpamDataSetPath,technique,"multinomial","test", notspam)
		DataProfiler.readDir(spamDatasetPath,technique,"multinomial","test", spam)
		print "Confusion matrix : "
		print "| TP- ",DataProfiler.TP,"| FN- ",DataProfiler.FN,"|"
		print "| FP- ",DataProfiler.FP,"| TN-",DataProfiler.TN,"|"
		print "Accuracy : ", ((DataProfiler.TP + DataProfiler.TN) / (DataProfiler.TP + DataProfiler.TN + DataProfiler.FP + DataProfiler.FN)) * 100, "%"

	elif technique=="dt":
		print "Testing Decision Tree"
		dtModel = None
		with open(modelFilePath, 'rb') as infile:
			dtModel = pickle.load(infile)
		#print "Model : ",dtModel
		# raw_input()
		DataProfiler.rootBin = dtModel.rootBin
		DataProfiler.rootContinuous = dtModel.rootContinuous
		#print DataProfiler.rootBin.word, " is the root for binary."
		#print "Root:::: ",DataProfiler.rootContinuous
		
		print "Testing dt- binary:"
		DataProfiler.readDir(notSpamDataSetPath,technique, "binary","test", notspam)
		DataProfiler.readDir(spamDatasetPath,technique, "binary","test", spam)
		print "Confusion matrix : "
		print "| TP- ",DataProfiler.TP,"| FN- ",DataProfiler.FN,"|"
		print "| FP- ",DataProfiler.FP,"| TN-",DataProfiler.TN,"|"
		print "Accuracy : ", ((DataProfiler.TP + DataProfiler.TN) / (DataProfiler.TP + DataProfiler.TN + DataProfiler.FP + DataProfiler.FN)) * 100, "%"
		
		print "Testing dt- continuous (multinomial):"
		DataProfiler.readDir(notSpamDataSetPath, technique, "continuous", "test", notspam)
		DataProfiler.readDir(spamDatasetPath, technique, "continuous", "test", spam)

		#DTree_Continuous.printTreeInLevel(DataProfiler.rootContinuous)

		print "Confusion matrix : "
		print "| TP- ",DataProfiler.TP,"| FN- ",DataProfiler.FN,"|"
		print "| FP- ",DataProfiler.FP,"| TN-",DataProfiler.TN,"|"
		print "Accuracy : ", ((DataProfiler.TP + DataProfiler.TN) / (DataProfiler.TP + DataProfiler.TN + DataProfiler.FP + DataProfiler.FN)) * 100, "%"

		# print DTree.testTree(dtModel.root)


		return 0	

# def train(technique, spamTrainingSetPath, notSpamTrainingSetPath):
# 	return 0


if __name__ == "__main__":
	#DataProfiler.readDir("../askarand-sasshah-tejakumt-a4/part1/train/notspam/*.*","binary","train",notspam)
	#print "Done"
	#print len(DataProfiler.wordsPerDocNotSpam)
	#DataProfiler.readDir("../askarand-sasshah-tejakumt-a4/part1/train/spam/*.*","binary","train",spam)
	#print "Done"
	#print len(DataProfiler.wordsPerDocSpam)

	if len(sys.argv) < 5:
		print len(sys.argv)
		usage()
		sys.exit()
	#mode = sys.argv[1]
	(mode, technique, datasetPath, modelFilePath) = sys.argv[1:5]
	currDir = dir_path = os.path.dirname(os.path.realpath(__file__))
	spamDatasetPath = os.path.join(datasetPath,"spam/*.*")
	notSpamDataSetPath = os.path.join(datasetPath,"notspam/*.*")

	print "Running now...", mode, technique

	#print modelFilePath
	spamDatasetPath = datasetPath.replace("\\","/") + "spam/*.*"
	notSpamDataSetPath = datasetPath.replace("\\","/") + "notspam/*.*"
	print spamDatasetPath, notSpamDataSetPath

	modelFilePath = os.path.join(currDir, modelFilePath)
	# print "model saved at ",modelFilePath

	if mode == "test":
		predictions = test(technique, spamDatasetPath, notSpamDataSetPath, modelFilePath)
	elif mode == "train":
		# train(technique, spamTrainingSetPath, notSpamTrainingSetPath, modelFilePath)
		train(technique, spamDatasetPath, notSpamDataSetPath, modelFilePath)
		# write this model to a file
	else:
		usage()
		sys.exit()
