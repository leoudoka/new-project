# app/services/portfolio/i_portfolio_service.py
from abc import ABCMeta, abstractmethod

class IPortfolio(metaclass=ABCMeta):
	@abstractmethod
	def get_portfolios(self):
		raise NotImplementedError

	@abstractmethod
	def create_portfolio(self):
		raise NotImplementedError
	
	@abstractmethod
	def patch_new_portfolio(self):
		raise NotImplementedError

	@abstractmethod
	def get_portfolio_by_id_or_404(self, id: int):
		raise NotImplementedError
	
	@abstractmethod
	def update_portfolio(self, args: dict):
		raise NotImplementedError
	
	@abstractmethod
	def delete_portfolio(self, id: int):
		raise NotImplementedError