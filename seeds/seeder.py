import os

from flask_seeder import Seeder, Faker, generator
from werkzeug.security import generate_password_hash

from api.models import JobIndustry, JobCategory, JobExperience, JobCareerLevel, \
    User, JobContractType, Employer, Organization
from SQL.jobs_data import INDUSTRY_DATA, INDUSTRY_CATEGORY_DATA, \
        INDUSTRY_JOB_EXPERIENCE_DATA, INDUSTRY_JOB_CAREER_LEVEL_DATA, \
            INDUSTRY_JOB_CONTRACT_TYPE_DATA, EMPLOYERS_DATA, EMPLOYER_ORG_DATA

class AdminUserSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 1

    def run(self):
        args = {
            'first_name': 'Super',
            'last_name': 'Admin',
            'email': os.environ.get('SUPER_ADMIN_EMAIL'),
            'role': 'admin',
            'password_harsh': generate_password_hash(os.environ.get('SUPER_ADMIN_PASSWORD'))
        }
        user = User(**args)
        print('Adding user: %s' % user)
        self.db.session.add(user)
        try:
            self.db.session.commit()
        except:
            self.db.session.rollback()

class EmployersUserSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 2

    def run(self):
        faker = Faker(
            cls=User,
            init={
                'first_name': generator.Name(),
                'last_name': '',
                'email': generator.Email(),
                'role': 'employer',
                'password_harsh': generate_password_hash('Password123#')
            }
        )

        for user in faker.create(5):
            try:
                print("Adding user: %s" % user)
                self.db.session.add(user)
                self.db.session.commit()
            except:
                self.db.session.rollback()


class JobIndustrySeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 2

    def run(self):
        industries = []
        for industry in INDUSTRY_DATA:
            industry['slug'] = JobIndustry.generate_slug(industry['name'])
            industry['created_by'] = 1 # default Admin ID
            print('Adding rate: %s' % industry)
            industries.append(JobIndustry(**industry))
        self.db.session.add_all(industries)


class EmployersSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 3

    def run(self):
        employers = []
        for employer in EMPLOYERS_DATA:
            print('Adding employer: %s' % employer)
            employers.append(Employer(**employer))
        self.db.session.add_all(employers)


class JobIndustryCategorySeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 3

    def run(self):
        industry_job_categories = INDUSTRY_CATEGORY_DATA
        for industry_name, job_categories in industry_job_categories.items():
            industry = JobIndustry.query.filter_by(name=industry_name).first()
            if not industry:
                print(f"Industry '{industry_name}' not found, skipping job categories.")
                continue

            for job_category_name in job_categories:
                slug = JobIndustry.generate_slug(job_category_name)
                job_category = JobCategory(
                    name=job_category_name, job_industry_id=industry.id,
                    slug=slug, created_by=1
                )
                self.db.session.add(job_category)

        self.db.session.commit()


class JobExperienceSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 4

    def run(self):
        experiences = []
        for experience in INDUSTRY_JOB_EXPERIENCE_DATA:
            experience['slug'] = JobExperience.generate_slug(experience['experience'])
            experience['created_by'] = 1 # default Admin ID
            print('Adding experience: %s' % experience)
            experiences.append(JobExperience(**experience))
        self.db.session.add_all(experiences)


class JobCareerLevelSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 5

    def run(self):
        career_levels = []
        for career_level in INDUSTRY_JOB_CAREER_LEVEL_DATA:
            career_level['slug'] = JobCareerLevel.generate_slug(career_level['level'])
            career_level['created_by'] = 1 # default Admin ID
            print('Adding career level: %s' % career_level)
            career_levels.append(JobCareerLevel(**career_level))
        self.db.session.add_all(career_levels)


class JobContractTypeSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 6

    def run(self):
        job_contract_types = []
        for job_contract_type in INDUSTRY_JOB_CONTRACT_TYPE_DATA:
            job_contract_type['slug'] = JobContractType.generate_slug(job_contract_type['type'])
            job_contract_type['created_by'] = 1 # default Admin ID
            print('Adding job contract type: %s' % job_contract_type)
            job_contract_types.append(JobContractType(**job_contract_type))
        self.db.session.add_all(job_contract_types)


class OrganizationSeeder(Seeder):
    def __init__(self):
        super().__init__()
        self.priority = 7

    def run(self):
        orgs = []
        for org in EMPLOYER_ORG_DATA:
            print('Adding employer: %s' % org)
            orgs.append(Organization(**org))
        self.db.session.add_all(orgs)