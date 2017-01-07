class DTModel():
	"""docstring for DTModel"""
	# rootBin = None
	# rootContinuous = None
	
	def __init__(self, dtnode, dtnode_continuous):
		self.rootBin = dtnode
		#print "Bin word:",self.rootBin.word
		self.rootContinuous = dtnode_continuous
		#print "Con word:",self.rootContinuous.word

	def __str__(self):
		return "dtnode word "+str(self.rootBin.word)+", dtnode continuous word "+str(self.rootContinuous.word) + " ."
