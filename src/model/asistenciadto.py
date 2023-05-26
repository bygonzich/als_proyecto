# AsistenciaDTO

from datetime import datetime as date
import itertools


class AsistenciaDto:
	id_count = itertools.count()

	def __init__(self, usuario):
		self.__id = next(AsistenciaDto.id_count)
		self.__usuario = usuario
		self.__fecha = date.now().strftime("%H:%M - %d/%m/%Y")

	@property
	def id(self):
		return self.__id

	@property
	def usuario(self):
		return self.__usuario
		
	@property
	def fecha(self):
		return self.__fecha
