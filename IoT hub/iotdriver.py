from abc import ABCMeta, abstractmethod

class Driver(metaclass=ABCMeta):
	@abstractmethod
	def turn_on(self):
		pass

	@abstractmethod
	def turn_off(self):
		pass

	@abstractmethod
	def set_session(self, params):
		pass
