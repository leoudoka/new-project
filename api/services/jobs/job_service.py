# app/services/jobs/job_service.py
import os

from flask import abort, request
import cloudinary
import cloudinary.uploader

from api import db
from api.models import Job, JobCategory, JobIndustry, \
    JobExperience, JobCareerLevel, JobContractType, JobApplicant
from .i_job_service import IJob


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

class JobService(IJob):
    def get_job_by_id_or_404(self, id):
        return db.session.get(Job, id) or abort(404)
    
    def get_jobs(self):
        return Job.query \
                .order_by(Job.id.desc())

    def get_job_industries(self):
        return JobIndustry.query \
                .order_by(JobIndustry.id.desc())

    def get_job_categories(self):
        return JobCategory.query \
                .order_by(JobCategory.id.desc())

    def get_job_experiences(self):
        return JobExperience.query \
                .order_by(JobExperience.id.desc())

    def get_job_career_levels(self):
        return JobCareerLevel.query \
                .order_by(JobCareerLevel.id.desc())

    def get_job_contract_types(self):
        return JobContractType.query \
                .order_by(JobContractType.id.desc())
    
    def get_job_by_given_column_name(self, column_name, value):
        if hasattr(Job, column_name):
            column_name = getattr(Job, column_name)
            return db.session.scalar(Job.query.filter_by(column_name=value))
        abort(404)
    
    def create_job(self, args: dict):
        try:
            job_data = Job(**args)
            db.session.add(job_data)
            db.session.commit()
            return job_data
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_job(self, args: dict):
        try:
            if args.get('id'):
                job_to_update = self.get_job_by_id_or_404(args.get('id'))
                if job_to_update:
                    job_to_update.update(args)
                    db.session.commit()
                    return job_to_update

        except Exception as e:
            db.session.rollback()
            raise e

    def delete_job(self, id: int)-> dict:
        job_to_delete = self.get_job_by_id_or_404(id)

        db.session.delete(job_to_delete)
        db.session.commit()
        return {}, 204