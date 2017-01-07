import pickle 
from DTree import DTree
from DTree_Continuous import DTree_Continuous
from DecisionTreeModel import DTModel

# from BayesClassifierModel import bayesClassifierModel
dt = None
with open("dt.model","rb") as dtFile:
	dt = pickle.load(dtFile)
print DTree.printTreeInLevel(dt.rootBin)
raw_input()
print DTree_Continuous.printTreeInLevel(dt.rootContinuous)


# with open("dt")
	