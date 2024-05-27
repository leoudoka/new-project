# app/services/users/i_user.py
from abc import ABCMeta, abstractmethod

class IUser(metaclass=ABCMeta):
	@abstractmethod
	def get_users(self):
		raise NotImplementedError

	@abstractmethod
	def create_user(self):
		raise NotImplementedError

	@abstractmethod
	def get_user_by_id_or_404(self, id: int):
		raise NotImplementedError