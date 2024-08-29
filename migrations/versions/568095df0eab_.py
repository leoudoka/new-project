"""empty message

Revision ID: 568095df0eab
Revises: 
Create Date: 2024-08-29 21:45:36.836578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '568095df0eab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('iso3', sa.String(length=3), nullable=True),
    sa.Column('numeric_code', sa.String(length=3), nullable=True),
    sa.Column('iso2', sa.String(length=2), nullable=True),
    sa.Column('phonecode', sa.String(length=255), nullable=True),
    sa.Column('capital', sa.String(length=255), nullable=True),
    sa.Column('currency', sa.String(length=255), nullable=True),
    sa.Column('currency_name', sa.String(length=255), nullable=True),
    sa.Column('currency_symbol', sa.String(length=255), nullable=True),
    sa.Column('tld', sa.String(length=255), nullable=True),
    sa.Column('native', sa.String(length=255), nullable=True),
    sa.Column('region', sa.String(length=255), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('subregion', sa.String(length=255), nullable=True),
    sa.Column('subregion_id', sa.Integer(), nullable=True),
    sa.Column('nationality', sa.String(length=255), nullable=True),
    sa.Column('timezones', sa.Text(), nullable=True),
    sa.Column('translations', sa.Text(), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=True),
    sa.Column('emoji', sa.String(length=191), nullable=True),
    sa.Column('emojiU', sa.String(length=191), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('flag', sa.Boolean(), nullable=True),
    sa.Column('wikiDataId', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', 'not-specified'), nullable=True),
    sa.Column('role', sa.Enum('admin', 'sub-admin', 'employer', 'recruiter', 'talent', 'student', 'not-specified'), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('password_harsh', sa.String(length=256), nullable=True),
    sa.Column('email_verified_at', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_dob'), ['dob'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_last_name'), ['last_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_middle_name'), ['middle_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('attachments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('entity_type', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('attachments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_attachments_entity_type'), ['entity_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_attachments_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_attachments_path'), ['path'], unique=False)
        batch_op.create_index(batch_op.f('ix_attachments_user_id'), ['user_id'], unique=False)

    op.create_table('job_career_levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_career_levels', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_career_levels_created_by'), ['created_by'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_career_levels_level'), ['level'], unique=True)
        batch_op.create_index(batch_op.f('ix_job_career_levels_slug'), ['slug'], unique=True)

    op.create_table('job_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_categories', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_categories_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_categories_slug'), ['slug'], unique=True)

    op.create_table('job_contract_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_contract_types', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_contract_types_created_by'), ['created_by'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_contract_types_slug'), ['slug'], unique=True)
        batch_op.create_index(batch_op.f('ix_job_contract_types_type'), ['type'], unique=True)

    op.create_table('job_experiences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('experience', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_experiences', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_experiences_experience'), ['experience'], unique=True)
        batch_op.create_index(batch_op.f('ix_job_experiences_slug'), ['slug'], unique=True)

    op.create_table('job_industries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_industries', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_industries_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_industries_slug'), ['slug'], unique=True)

    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('country_code', sa.String(length=2), nullable=True),
    sa.Column('fips_code', sa.String(length=255), nullable=True),
    sa.Column('iso2', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=191), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('flag', sa.Boolean(), nullable=True),
    sa.Column('wikiDataId', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(length=64), nullable=False),
    sa.Column('access_expiration', sa.DateTime(), nullable=False),
    sa.Column('refresh_token', sa.String(length=64), nullable=False),
    sa.Column('refresh_expiration', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tokens_access_token'), ['access_token'], unique=False)
        batch_op.create_index(batch_op.f('ix_tokens_refresh_token'), ['refresh_token'], unique=False)
        batch_op.create_index(batch_op.f('ix_tokens_user_id'), ['user_id'], unique=False)

    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('postal_code', sa.String(length=8), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_addresses_country_id'), ['country_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_addresses_state_id'), ['state_id'], unique=False)

    op.create_table('portfolios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('hourly_rate', sa.String(length=30), nullable=True),
    sa.Column('work_preference', sa.PickleType(), nullable=True),
    sa.Column('job_industries', sa.PickleType(), nullable=True),
    sa.Column('skills', sa.PickleType(), nullable=True),
    sa.Column('portfolio_link', sa.String(length=255), nullable=True),
    sa.Column('linkedin_link', sa.String(length=255), nullable=True),
    sa.Column('job_category_id', sa.Integer(), nullable=False),
    sa.Column('job_career_level_id', sa.Integer(), nullable=True),
    sa.Column('job_experience_id', sa.Integer(), nullable=False),
    sa.Column('resume_attachment', sa.String(length=255), nullable=True),
    sa.Column('photo_attachment', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['job_career_level_id'], ['job_career_levels.id'], ),
    sa.ForeignKeyConstraint(['job_category_id'], ['job_categories.id'], ),
    sa.ForeignKeyConstraint(['job_experience_id'], ['job_experiences.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('portfolios', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_portfolios_job_category_id'), ['job_category_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_portfolios_user_id'), ['user_id'], unique=False)

    op.create_table('employers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('approved_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('employers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_employers_address_id'), ['address_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_employers_approved_by'), ['approved_by'], unique=False)
        batch_op.create_index(batch_op.f('ix_employers_user_id'), ['user_id'], unique=False)

    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('summary', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('job_category_id', sa.Integer(), nullable=False),
    sa.Column('job_industry_id', sa.Integer(), nullable=False),
    sa.Column('job_experience_id', sa.Integer(), nullable=False),
    sa.Column('job_contract_type_id', sa.Integer(), nullable=False),
    sa.Column('featured', sa.Boolean(), nullable=False),
    sa.Column('status', sa.Enum('open', 'paused', 'closed'), nullable=True),
    sa.Column('employer_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], ),
    sa.ForeignKeyConstraint(['job_category_id'], ['job_categories.id'], ),
    sa.ForeignKeyConstraint(['job_contract_type_id'], ['job_contract_types.id'], ),
    sa.ForeignKeyConstraint(['job_experience_id'], ['job_experiences.id'], ),
    sa.ForeignKeyConstraint(['job_industry_id'], ['job_industries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_jobs_employer_id'), ['employer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_jobs_slug'), ['slug'], unique=True)
        batch_op.create_index(batch_op.f('ix_jobs_summary'), ['summary'], unique=False)
        batch_op.create_index(batch_op.f('ix_jobs_title'), ['title'], unique=False)

    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('employer_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_organizations_employer_id'), ['employer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_organizations_slug'), ['slug'], unique=True)
        batch_op.create_index(batch_op.f('ix_organizations_title'), ['title'], unique=False)

    op.create_table('job_applicants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('employer_id', sa.Integer(), nullable=False),
    sa.Column('cover_letter_attachment_id', sa.Integer(), nullable=False),
    sa.Column('cv_attachment_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('accepted', 'pending', 'rejected'), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('vetted_by', sa.Integer(), nullable=False),
    sa.Column('approved_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['cover_letter_attachment_id'], ['attachments.id'], ),
    sa.ForeignKeyConstraint(['cv_attachment_id'], ['attachments.id'], ),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], ),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vetted_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_applicants', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_applicants_approved_by'), ['approved_by'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_applicants_cover_letter_attachment_id'), ['cover_letter_attachment_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_applicants_cv_attachment_id'), ['cv_attachment_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_applicants_employer_id'), ['employer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_applicants_job_id'), ['job_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_applicants_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_applicants_vetted_by'), ['vetted_by'], unique=False)

    op.create_table('recruiters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scope', sa.String(length=255), nullable=True),
    sa.Column('work_preference', sa.String(length=64), nullable=True),
    sa.Column('contract_type', sa.String(length=64), nullable=True),
    sa.Column('org_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recruiters', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recruiters_org_id'), ['org_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_recruiters_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recruiters', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recruiters_user_id'))
        batch_op.drop_index(batch_op.f('ix_recruiters_org_id'))

    op.drop_table('recruiters')
    with op.batch_alter_table('job_applicants', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_applicants_vetted_by'))
        batch_op.drop_index(batch_op.f('ix_job_applicants_user_id'))
        batch_op.drop_index(batch_op.f('ix_job_applicants_job_id'))
        batch_op.drop_index(batch_op.f('ix_job_applicants_employer_id'))
        batch_op.drop_index(batch_op.f('ix_job_applicants_cv_attachment_id'))
        batch_op.drop_index(batch_op.f('ix_job_applicants_cover_letter_attachment_id'))
        batch_op.drop_index(batch_op.f('ix_job_applicants_approved_by'))

    op.drop_table('job_applicants')
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_organizations_title'))
        batch_op.drop_index(batch_op.f('ix_organizations_slug'))
        batch_op.drop_index(batch_op.f('ix_organizations_employer_id'))

    op.drop_table('organizations')
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_jobs_title'))
        batch_op.drop_index(batch_op.f('ix_jobs_summary'))
        batch_op.drop_index(batch_op.f('ix_jobs_slug'))
        batch_op.drop_index(batch_op.f('ix_jobs_employer_id'))

    op.drop_table('jobs')
    with op.batch_alter_table('employers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_employers_user_id'))
        batch_op.drop_index(batch_op.f('ix_employers_approved_by'))
        batch_op.drop_index(batch_op.f('ix_employers_address_id'))

    op.drop_table('employers')
    with op.batch_alter_table('portfolios', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_portfolios_user_id'))
        batch_op.drop_index(batch_op.f('ix_portfolios_job_category_id'))

    op.drop_table('portfolios')
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_addresses_state_id'))
        batch_op.drop_index(batch_op.f('ix_addresses_country_id'))

    op.drop_table('addresses')
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tokens_user_id'))
        batch_op.drop_index(batch_op.f('ix_tokens_refresh_token'))
        batch_op.drop_index(batch_op.f('ix_tokens_access_token'))

    op.drop_table('tokens')
    op.drop_table('states')
    with op.batch_alter_table('job_industries', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_industries_slug'))
        batch_op.drop_index(batch_op.f('ix_job_industries_name'))

    op.drop_table('job_industries')
    with op.batch_alter_table('job_experiences', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_experiences_slug'))
        batch_op.drop_index(batch_op.f('ix_job_experiences_experience'))

    op.drop_table('job_experiences')
    with op.batch_alter_table('job_contract_types', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_contract_types_type'))
        batch_op.drop_index(batch_op.f('ix_job_contract_types_slug'))
        batch_op.drop_index(batch_op.f('ix_job_contract_types_created_by'))

    op.drop_table('job_contract_types')
    with op.batch_alter_table('job_categories', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_categories_slug'))
        batch_op.drop_index(batch_op.f('ix_job_categories_name'))

    op.drop_table('job_categories')
    with op.batch_alter_table('job_career_levels', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_career_levels_slug'))
        batch_op.drop_index(batch_op.f('ix_job_career_levels_level'))
        batch_op.drop_index(batch_op.f('ix_job_career_levels_created_by'))

    op.drop_table('job_career_levels')
    with op.batch_alter_table('attachments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_attachments_user_id'))
        batch_op.drop_index(batch_op.f('ix_attachments_path'))
        batch_op.drop_index(batch_op.f('ix_attachments_name'))
        batch_op.drop_index(batch_op.f('ix_attachments_entity_type'))

    op.drop_table('attachments')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_middle_name'))
        batch_op.drop_index(batch_op.f('ix_users_last_name'))
        batch_op.drop_index(batch_op.f('ix_users_first_name'))
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_index(batch_op.f('ix_users_dob'))

    op.drop_table('users')
    op.drop_table('countries')
    # ### end Alembic commands ###
