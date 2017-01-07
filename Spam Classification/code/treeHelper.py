from __future__ import division
from DTree import DTree
from DTree_Continuous import DTree_Continuous

class TreeHelper:
	DTNode_root = None
	DTNode_Continuous_root = None

	@staticmethod
	def getLabel(root, method, test_words):
		if method == "binary":
			DTNode_root = root
			return DTree.testTree(DTNode_root, test_words)
		else:
			DTNode_Continuous_root = root
			# return False
			return DTree_Continuous.testTree(DTNode_Continuous_root, test_words)
		
