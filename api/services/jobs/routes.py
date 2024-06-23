# app/services/jobs/routes.py
from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.services.auth.auth_service import token_auth
from api.schemas import JobSchema, JobIndustriesSchema, JobCategorySchema, \
    JobExperienceSchema, JobCareerLevelSchema, JobContractTypeSchema, EmptySchema
from api.services.jobs.job_service import JobService
from api.decorators import paginated_response

job_service = JobService()
jobs = Blueprint('jobs', __name__)

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
job_industry_schema = JobIndustriesSchema()
job_industries_schema = JobIndustriesSchema(many=True)
job_category_schema = JobCategorySchema()
jobs_categories_schema = JobCategorySchema(many=True)
job_experience_schema = JobExperienceSchema()
job_experiences_schema = JobExperienceSchema(many=True)
job_career_level_schema = JobCareerLevelSchema()
jobs_career_levels_schema = JobCareerLevelSchema(many=True)
job_contract_type_schema = JobContractTypeSchema()
job_contract_types_schema = JobContractTypeSchema(many=True)

@jobs.route('/', methods=['POST'])
@authenticate(token_auth)
@body(job_schema, location='form', media_type='multipart/form-data')
@response(job_schema, 201)
def create_job(args):
    """Register a new job"""
    auth_user = token_auth.current_user()
    args['user_id'] = auth_user.id
    return job_service.create_job(args)


@jobs.route('/', methods=['GET'])
@paginated_response(jobs_schema)
def get_jobs():
    """Retrieve all jobs"""
    return job_service.get_jobs()


@jobs.route('/industries', methods=['GET'])
@paginated_response(job_industries_schema)
def get_job_industries():
    """Retrieve all job industries"""
    return job_service.get_job_industries()


@jobs.route('/categories', methods=['GET'])
@paginated_response(jobs_categories_schema)
def get_job_categories():
    """Retrieve all job categories"""
    return job_service.get_job_categories()


@jobs.route('/experiences', methods=['GET'])
@paginated_response(job_experiences_schema)
def get_job_experiences():
    """Retrieve all job experiences"""
    return job_service.get_job_experiences()


@jobs.route('/career-levels', methods=['GET'])
@paginated_response(jobs_career_levels_schema)
def get_job_career_levels():
    """Retrieve all job career level"""
    return job_service.get_job_career_levels()


@jobs.route('/contract-types', methods=['GET'])
@paginated_response(job_contract_types_schema)
def get_job_contract_types():
    """Retrieve all contract job types"""
    return job_service.get_job_contract_types()


@jobs.route('/<int:id>', methods=['GET'])
@response(job_schema)
@other_responses({404: 'job not found'})
def get_job_by_id_or_404(id):
    """Retrieve a job by id"""
    return job_service.get_job_by_id_or_404(id)
