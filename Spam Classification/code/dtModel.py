class DTModel():
	"""docstring for DTModel"""
	dtnode = None
	dtnode_continuous = None
	
	def __init__(self, dtnode, dtnode_continuous):
		self.dtnode = dtnode
		self.dtnode_continuous = dtnode_continuous

	def __str__(self):
		return "dtnode word "+str(self.dtnode.word)+", dtnode continuous word "+str(self.dtnode_continuous.word) + " ."
