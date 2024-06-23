# app/services/jobs/i_job_service.py
from abc import ABCMeta, abstractmethod

class IJob(metaclass=ABCMeta):
	@abstractmethod
	def get_jobs(self):
		raise NotImplementedError
	
	@abstractmethod
	def get_job_industries(self):
		raise NotImplementedError
	
	@abstractmethod
	def get_job_categories(self):
		raise NotImplementedError
	
	@abstractmethod
	def get_job_experiences(self):
		raise NotImplementedError
	
	@abstractmethod
	def get_job_career_levels(self):
		raise NotImplementedError
	
	@abstractmethod
	def get_job_contract_types(self):
		raise NotImplementedError

	@abstractmethod
	def create_job(self):
		raise NotImplementedError

	@abstractmethod
	def get_job_by_id_or_404(self, id: int):
		raise NotImplementedError
	
	@abstractmethod
	def update_job(self, args: dict):
		raise NotImplementedError
	
	@abstractmethod
	def delete_job(self, id: int):
		raise NotImplementedError