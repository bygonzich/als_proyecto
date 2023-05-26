# RutinaDTO

class RutinaDto:
	def __init__(self, monitor, numEjer, musculo):
		self.__monitor = monitor
		self.__numEjer = numEjer
		self.__musculo = musculo
		
	@property
	def monitor(self):
		return self.__monitor
		
	@property
	def numEjer(self):
		return self.__numEjer

	@property
	def musculo(self):
		return self.__musculo
