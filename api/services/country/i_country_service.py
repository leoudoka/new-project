# app/services/country/i_country_service.py
from abc import ABCMeta, abstractmethod

class ICountry(metaclass=ABCMeta):
	@abstractmethod
	def get_countries(self):
		raise NotImplementedError
	
	@abstractmethod
	def get_states(self):
		raise NotImplementedError

	@abstractmethod
	def get_country_by_id_or_404(self, id: int):
		raise NotImplementedError
	
	@abstractmethod
	def get_state_by_id_or_404(self, id: int):
		raise NotImplementedError