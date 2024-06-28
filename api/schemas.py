from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from flask_marshmallow import validate as flask_ma_validate

from api import ma, db
from api.services.auth.routes import token_auth
from api.models import User, Portfolio, Job, JobCategory, JobIndustry, \
    JobExperience, JobCareerLevel, JobContractType, JobApplicant, Organization, \
    Recruiter, Employer, Country, State

paginated_schema_cache = {}


class EmptySchema(ma.Schema):
    pass


class DateTimePaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.DateTime(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class StringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.String(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


def PaginatedCollection(schema, pagination_schema=StringPaginationSchema):
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(pagination_schema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = 'Paginated{}'.format(schema.__class__.__name__)
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    id = ma.auto_field(dump_only=True)
    first_name = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))
    last_name = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))
    email = ma.auto_field(required=True, validate=[validate.Length(max=120),
                                                   validate.Email()])
    password = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    username = ma.String(required=False)
    gender = ma.String(required=False)
    role = ma.String(required=True)
    dob = ma.Date(required=False)
    mobile_number = ma.String(required=False)
    has_password = ma.Boolean(dump_only=True)
    last_seen = ma.auto_field(dump_only=True)
    country = ma.String(dump_only=True)
    state = ma.String(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)

    @validates('username')
    def validate_username(self, value):
        if not value[0].isalpha():
            raise ValidationError('Username must start with a letter')
        user = token_auth.current_user()
        old_username = user.username if user else None
        if value != old_username and \
                db.session.scalar(User.query.filter_by(username=value)):
            raise ValidationError('Username already exits.')

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if value != old_email and \
                db.session.scalar(User.query.filter_by(email=value)):
            raise ValidationError('Email already exits.')


class UserDetailsSchema(ma.Schema):
    id = ma.Integer(required=True)
    first_name = ma.String(required=False)
    last_name = ma.String(required=False)
    email = ma.String(required=False)
    username = ma.String(required=False)
    gender = ma.String(required=False)
    dob = ma.Date(required=False)
    mobile_number = ma.String(required=False)
    role = ma.String(required=False)
    country_id = ma.Integer(required=False)
    org_id = ma.Integer(required=False)
    state_id = ma.Integer(required=False)
    country = ma.String(dump_only=True)
    state = ma.String(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if value != old_email and \
                db.session.scalar(User.query.filter_by(email=value)):
            raise ValidationError('Email already exits.')


class UpdateUserSchema(UserSchema):
    old_password = ma.String(load_only=True, validate=validate.Length(min=3))
    country_id = ma.Integer(required=False)
    state_id = ma.Integer(required=False)


    @validates('old_password')
    def validate_old_password(self, value):
        if not token_auth.current_user().verify_password(value):
            raise ValidationError('Password is incorrect')


class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
    refresh_token = ma.String()


class PasswordResetRequestSchema(ma.Schema):
    class Meta:
        ordered = True

    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])


class PasswordResetSchema(ma.Schema):
    class Meta:
        ordered = True

    token = ma.String(required=True)
    new_password = ma.String(required=True, validate=validate.Length(min=3))


class OAuth2Schema(ma.Schema):
    code = ma.String(required=True)
    state = ma.String(required=True)


class PortfolioSchema(ma.Schema):
    class Meta:
        model = Portfolio
        ordered = True

    id = ma.Integer(dump_only=True)
    about = ma.String(required=False)
    hourly_rate = ma.String(required=False)
    work_preference = ma.List(ma.String(), required=False)
    job_industries = ma.List(ma.String(), required=False)
    skills = ma.List(ma.String(), required=False)
    portfolio_link = ma.String(required=False)
    linkedin_link = ma.String(required=False)
    job_category_id = ma.Integer(required=True)
    job_career_level_id = ma.Integer(required=False)
    job_experience_id = ma.Integer(required=True)
    resume = ma.File(required=True, validate=flask_ma_validate.FileSize(max="2 MiB"))
    photo = ma.File(required=False, validate=flask_ma_validate.FileSize(max="2 MiB"))
    resume_attachment = ma.String(dump_only=True)
    photo_attachment = ma.String(dump_only=True)
    category = ma.String(dump_only=True)
    experience = ma.String(dump_only=True)
    career_level = ma.String(dump_only=True)
    user_id = ma.Integer(required=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)

class PatchPortfolioSchema(ma.Schema):

    id = ma.Integer(dump_only=True)
    about = ma.String(required=False)
    hourly_rate = ma.String(required=False)
    work_preference = ma.List(ma.String(), required=False)
    job_industries = ma.List(ma.String(), required=False)
    skills = ma.List(ma.String(), required=False)
    portfolio_link = ma.String(required=False)
    linkedin_link = ma.String(required=False)
    job_category_id = ma.Integer(required=False)
    job_career_level_id = ma.Integer(required=False)
    job_experience_id = ma.Integer(required=False)
    resume_attachment = ma.String(dump_only=True)
    photo_attachment = ma.String(dump_only=True)
    category = ma.String(dump_only=True)
    experience = ma.String(dump_only=True)
    career_level = ma.String(dump_only=True)
    user_id = ma.Integer(required=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)

class JobSchema(ma.Schema):
    class Meta:
        model = Job
        ordered = True

    id = ma.Integer(dump_only=True)
    title = ma.String(required=False)
    slug = ma.String(dump_only=True)
    summary = ma.String(required=True)
    description = ma.String(required=True)
    featured = ma.Boolean(dump_only=True)
    status = ma.String(dump_only=True)
    user_id = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class JobIndustriesSchema(ma.Schema):
    class Meta:
        model = JobIndustry
        ordered = True

    id = ma.Integer(dump_only=True)
    name = ma.String(required=False)
    slug = ma.String(dump_only=True)
    description = ma.String(required=False)
    status = ma.Boolean(dump_only=True)
    created_by = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class JobCategorySchema(ma.Schema):
    class Meta:
        model = JobCategory
        ordered = True

    id = ma.Integer(dump_only=True)
    name = ma.String(required=False)
    slug = ma.String(dump_only=True)
    description = ma.String(required=False)
    status = ma.Boolean(dump_only=True)
    job_industry_id = ma.Integer(dump_only=True)
    created_by = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class JobExperienceSchema(ma.Schema):
    class Meta:
        model = JobExperience
        ordered = True

    id = ma.Integer(dump_only=True)
    experience = ma.String(required=True)
    slug = ma.String(dump_only=True)
    description = ma.String(required=False)
    status = ma.Boolean(dump_only=True)
    created_by = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class JobCareerLevelSchema(ma.Schema):
    class Meta:
        model = JobCareerLevel
        ordered = True

    id = ma.Integer(dump_only=True)
    level = ma.String(required=True)
    slug = ma.String(dump_only=True)
    description = ma.String(required=False)
    status = ma.Boolean(dump_only=True)
    created_by = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class JobContractTypeSchema(ma.Schema):
    class Meta:
        model = JobContractType
        ordered = True

    id = ma.Integer(dump_only=True)
    type = ma.String(required=True)
    slug = ma.String(dump_only=True)
    description = ma.String(required=False)
    status = ma.Boolean(dump_only=True)
    created_by = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class EmployerSchema(ma.Schema):
    class Meta:
        model = Employer
        ordered = True

    id = ma.Integer(dump_only=True)
    about = ma.String(required=False)
    state_id = ma.Integer(required=False)
    country_id = ma.Integer(required=False)
    address_id = ma.Integer(required=False)
    status = ma.Boolean(dump_only=True)
    is_approved = ma.Boolean(dump_only=True)
    user_id = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)

class JobOrganizationSchema(ma.Schema):
    class Meta:
        model = Organization
        ordered = True

    id = ma.Integer(dump_only=True)
    title = ma.String(required=False)
    slug = ma.String(required=False)
    about = ma.String(required=False)
    is_approved = ma.Boolean(dump_only=True)
    status = ma.Boolean(dump_only=True)
    employer_id = ma.Integer(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class RecruiterSchema(ma.Schema):
    class Meta:
        model = Recruiter
        ordered = True

    id = ma.Integer(dump_only=True)
    scope = ma.String(required=False)
    scope_attachment = ma.File(required=False, validate=flask_ma_validate.FileSize(max="2 MiB"))
    work_preference = ma.String(required=False)
    contract_type = ma.String(required=False)
    org_id = ma.Integer(required=False)
    user_id = ma.Integer(required=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)


class CountrySchema(ma.Schema):
    class Meta:
        model = Recruiter

    id = ma.Integer(dump_only=True)
    name = ma.String(dump_only=False)


class StateSchema(ma.Schema):
    class Meta:
        model = State

    id = ma.Integer(dump_only=True)
    name = ma.String(dump_only=False)
    country_name = ma.String(dump_only=False)
    country_code = ma.String(dump_only=False)
