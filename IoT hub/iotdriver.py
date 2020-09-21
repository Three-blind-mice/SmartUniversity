from abc import ABCMeta, abstractmethod

class Driver(metaclass=ABCMeta):
	"""Базовый класс, предоставляющий методы для работы с IoT.
	Для корректной работы, дочерние классы должны описывать 
	все методы этого класса."""
	@abstractmethod
	def turn_on(self):
		pass

	@abstractmethod
	def turn_off(self):
		pass

	@abstractmethod
	def set_session(self, params):
		pass