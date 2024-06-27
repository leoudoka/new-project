from datetime import datetime, timedelta
import secrets, enum

import jwt
from flask import current_app, url_for
from flask_login import UserMixin
from sqlalchemy import orm as so
import sqlalchemy as sa
from typing import Optional
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify
from decimal import Decimal

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Token(db.Model):
    __tablename__ = 'tokens'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    access_token: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    access_expiration: so.Mapped[datetime]
    refresh_token: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    refresh_expiration: so.Mapped[datetime]
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('users.id'), index=True)

    user: so.Mapped['User'] = so.relationship(back_populates='tokens')

    @property
    def access_token_jwt(self):
        return jwt.encode({'token': self.access_token},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256')

    def generate(self):
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=current_app.config['ACCESS_TOKEN_MINUTES'])
        self.refresh_token = secrets.token_urlsafe()
        self.refresh_expiration = datetime.utcnow() + \
            timedelta(days=current_app.config['REFRESH_TOKEN_DAYS'])

    def expire(self, delay=None):
        if delay is None:  # pragma: no branch
            # 5 second delay to allow simultaneous requests
            delay = 5 if not current_app.testing else 0
        self.access_expiration = datetime.utcnow() + timedelta(seconds=delay)
        self.refresh_expiration = datetime.utcnow() + timedelta(seconds=delay)

    @staticmethod
    def clean():
        """Remove any tokens that have been expired for more than a day."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        tokens = Token.query.filter(Token.refresh_expiration < yesterday)\
			.all()
        if tokens:
            for token in tokens:
                db.session.delete(token)
                db.session.commit()

    @staticmethod
    def from_jwt(access_token_jwt):
        access_token = None
        try:
            access_token = jwt.decode(access_token_jwt,
                                      current_app.config['SECRET_KEY'],
                                      algorithms=['HS256'])['token']
            return db.session.scalar(Token.query.filter_by(
                access_token=access_token))
        except jwt.PyJWTError:
            pass


class User(UserMixin, Updateable, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    middle_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, nullable=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                nullable=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    gender: so.Mapped[Optional[enum.Enum]] = so.mapped_column(
        'gender', sa.Enum('male', 'female', 'not-specified'), 
        default='not-specified', nullable=True)
    role: so.Mapped[enum.Enum] = so.mapped_column(
        'role', sa.Enum('admin', 'sub-admin', 'employer', 'recruiter', 'talent', 'student', 'not-specified'), 
        default='not-specified', nullable=True)
    dob: so.Mapped[Optional[datetime.date]] = so.mapped_column(sa.Date, index=True, nullable=True)
    mobile_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(15), nullable=True)
    password_harsh: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    email_verified_at: so.Mapped[datetime] = so.mapped_column(nullable=True)
    last_seen: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    tokens: so.WriteOnlyMapped['Token'] = so.relationship(back_populates='user')
    address: so.WriteOnlyMapped['Address'] = so.relationship(back_populates='user')
    attachments: so.WriteOnlyMapped['Attachment'] = so.relationship(back_populates='user')
    employer: so.Mapped['Employer'] = so.relationship(
        foreign_keys='Employer.user_id', back_populates='user')
    portfolio: so.WriteOnlyMapped['Portfolio'] = so.relationship(
        foreign_keys='Portfolio.user_id', back_populates='user')
    recruiter: so.WriteOnlyMapped['Recruiter'] = so.relationship(
        foreign_keys='Recruiter.user_id', back_populates='user')
    jobs: so.WriteOnlyMapped['Job'] = so.relationship(back_populates='user')
    applicantions: so.WriteOnlyMapped['JobApplicant'] = so.relationship(
        foreign_keys='JobApplicant.user_id', back_populates='user')
    job_approvals: so.WriteOnlyMapped['JobApplicant'] = so.relationship(
        foreign_keys='JobApplicant.approved_by', back_populates='approved_by_user')
    job_vet: so.WriteOnlyMapped['JobApplicant'] = so.relationship(
        foreign_keys='JobApplicant.vetted_by', back_populates='vetted_by_user')
    

    def __repr__(self):  # pragma: no cover
        return '<User {}>'.format(f"{self.first_name} {self.last_name}")

    def get_roles(self):
        return self.role

    @property
    def has_password(self):
        return self.password_harsh is not None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_harsh = generate_password_hash(password)

    def verify_password(self, password):
        if self.password_harsh:  # pragma: no branch
            return check_password_hash(self.password_harsh, password)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def generate_auth_token(self):
        token = Token(user=self)
        token.generate()
        return token

    @staticmethod
    def verify_access_token(access_token_jwt, refresh_token=None):
        token = Token.from_jwt(access_token_jwt)
        if token:
            if token.access_expiration > datetime.utcnow():
                token.user.ping()
                db.session.commit()
                return token.user

    @staticmethod
    def verify_refresh_token(refresh_token, access_token_jwt):
        token = Token.from_jwt(access_token_jwt)
        if token and token.refresh_token == refresh_token:
            if token.refresh_expiration > datetime.utcnow():
                return token

            # someone tried to refresh with an expired token
            # revoke all tokens from this user as a precaution
            token.user.revoke_all()
            db.session.commit()

    def revoke_all(self):
        db.session.execute(Token.delete().where(Token.user == self))

    def generate_reset_token(self):
        return jwt.encode(
            {
                'exp': time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
                'reset_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return db.session.scalar(User.select().filter_by(
            email=data['reset_email']))
    

class Address(Updateable, db.Model):
    __tablename__ = 'addresses'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    state_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('states.id'))
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'))   
    postal_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    user: so.Mapped[User] = so.relationship(back_populates='address')

    def __repr__(self):  # pragma: no cover
        return '<Address {}>'.format(self.address)
    

class Country(Updateable, db.Model):
    __tablename__ = 'countries'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    iso3: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), nullable=True)
    numeric_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(3), nullable=True)
    iso2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), nullable=True)
    phonecode: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    capital: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    currency: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    currency_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    currency_symbol: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    tld: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    native: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    region: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    region_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    subregion: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    subregion_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    nationality: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    timezones: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    translations: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    latitude: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.Numeric(10,8), nullable=True)
    longitude: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.Numeric(11, 8), nullable=True)
    emoji: so.Mapped[Optional[str]] = so.mapped_column(sa.String(191), nullable=True)
    emojiU: so.Mapped[Optional[str]] = so.mapped_column(sa.String(191), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    flag: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=True)
    wikiDataId: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)

    states: so.Mapped['State'] = so.relationship(back_populates='country')

    def __repr__(self):  # pragma: no cover
        return '<Country {}>'.format(self.name)
    

class State(Updateable, db.Model):
    __tablename__ = 'states'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Country.id))
    country_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2), nullable=True)
    fips_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    iso2: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(191), nullable=True)
    latitude: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.Numeric(10,8), nullable=True)
    longitude: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.Numeric(11, 8), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    flag: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=True)
    wikiDataId: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)

    country: so.Mapped[Country] = so.relationship(back_populates='states')

    def __repr__(self):  # pragma: no cover
        return '<States {}>'.format(self.name)


class Portfolio(Updateable, db.Model):
    __tablename__ = 'portfolios'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    hourly_rate: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30), nullable=True)
    work_preference: so.Mapped[Optional[list]] = so.mapped_column(sa.PickleType, nullable=True)
    job_industries: so.Mapped[Optional[list]] = so.mapped_column(sa.PickleType, nullable=True)
    skills: so.Mapped[Optional[list]] = so.mapped_column(sa.PickleType, nullable=True)
    portfolio_link: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    linkedin_link: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    job_category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('job_categories.id'), index=True)
    job_career_level_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('job_career_levels.id'))
    job_experience_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('job_experiences.id'))
    resume_attachment: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    photo_attachment: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    user: so.Mapped[User] = so.relationship(back_populates='portfolio')
    job_category: so.Mapped['JobCategory'] = so.relationship(back_populates='portfolios')

    def __repr__(self):  # pragma: no cover
        return '<Portfolio {}>'.format(self.about)
    
    @property
    def category(self):
        return self.job_category.name


class Recruiter(Updateable, db.Model):
    __tablename__ = 'recruiters'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scope: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    work_preference: so.Mapped[str] = so.mapped_column(sa.String(64))
    contract_type: so.Mapped[str] = so.mapped_column(sa.String(64))
    org_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey('organizations.id'), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    user: so.Mapped[User] = so.relationship(back_populates='recruiter')
    organization: so.Mapped['Organization'] = so.relationship(back_populates='recruiters')

    def __repr__(self):  # pragma: no cover
        return '<Recruiter {}>'.format(self.user.first_name)


class Attachment(Updateable, db.Model):
    __tablename__ = 'attachments'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    path: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    entity_id: so.Mapped[int]
    entity_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),  index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    user: so.Mapped[User] = so.relationship(back_populates='attachments')

    def __repr__(self):  # pragma: no cover
        return '<Attachment {}>'.format(self.path)
    

class JobContractType(Updateable, db.Model):
    __tablename__ = 'job_contract_types'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # TODO: create seeder @ full-time, contract, permanent, internship or temporary
    type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while JobContractType.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug


    def __repr__(self):  # pragma: no cover
        return '<Job Contract Type {}>'.format(self.type)
    
class JobCareerLevel(Updateable, db.Model):
    __tablename__ = 'job_career_levels'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    level: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while JobCareerLevel.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug


    def __repr__(self):  # pragma: no cover
        return '<Job Work Type {}>'.format(self.level)
    
class JobExperience(Updateable, db.Model):
    __tablename__ = 'job_experiences'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    experience: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while JobExperience.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug


    def __repr__(self):  # pragma: no cover
        return '<Job Experience Type {}>'.format(self.experience)
    
class JobCategory(Updateable, db.Model):
    __tablename__ = 'job_categories'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    job_industry_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('job_industries.id'), index=True)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    industry: so.Mapped['JobIndustry'] = so.relationship(back_populates='categories')
    portfolios: so.WriteOnlyMapped['Portfolio'] = so.relationship(back_populates='job_category')

    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while JobCategory.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug


    def __repr__(self):  # pragma: no cover
        return '<Job Category {}>'.format(self.name)
    

class JobIndustry(Updateable, db.Model):
    __tablename__ = 'job_industries'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True, nullable=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    categories: so.WriteOnlyMapped['JobCategory'] = so.relationship(back_populates='industry')

    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while JobIndustry.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug


    def __repr__(self):  # pragma: no cover
        return '<Job Industries {}>'.format(self.name)
    
class Job(Updateable, db.Model):
    __tablename__ = 'jobs'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True, unique=True)
    summary: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    job_category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobCategory.id))
    job_industry_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobIndustry.id))
    job_experience_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobExperience.id))
    job_contract_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobContractType.id))
    featured: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    status: so.Mapped[Optional[enum.Enum]] = so.mapped_column(
        sa.Enum('open', 'paused', 'closed'), 
        default='open')
    employer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('employers.id'), index=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    employer: so.Mapped['Employer'] = so.relationship(back_populates='jobs')
    user: so.Mapped[User] = so.relationship(back_populates='jobs')

    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while Job.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug

class Employer(Updateable, db.Model):
    __tablename__ = 'employers'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    state_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    country_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    address_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Address.id), index=True, nullable=True)
    is_approved: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    approved_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    jobs: so.WriteOnlyMapped['Job'] = so.relationship(back_populates='employer')
    applicants: so.Mapped['JobApplicant'] = so.relationship(back_populates='employer')
    user: so.Mapped['User'] = so.relationship(
        foreign_keys='Employer.user_id', back_populates='employer')
    organization: so.Mapped['Organization'] = so.relationship( back_populates='employer')
    

class JobApplicant(Updateable, db.Model):
    __tablename__ = 'job_applicants'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    job_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Job.id), index=True)
    employer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Employer.id),  index=True)
    cover_letter_attachment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Attachment.id),  index=True)
    cv_attachment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Attachment.id),  index=True)
    status: so.Mapped[Optional[enum.Enum]] = so.mapped_column(
        sa.Enum('accepted', 'pending', 'rejected'), 
        default='pending')
    is_approved: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    vetted_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    approved_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    employer: so.Mapped['Employer'] = so.relationship(
        foreign_keys='JobApplicant.employer_id', back_populates='applicants')
    # employer: so.WriteOnlyMapped['Employer'] = so.relationship(
    #     foreign_keys='JobApplicant.user_id', back_populates='applicants')
    user: so.Mapped['User'] = so.relationship(
        foreign_keys='JobApplicant.user_id', back_populates='applicantions')
    approved_by_user: so.Mapped['User'] = so.relationship(
        foreign_keys='JobApplicant.approved_by', back_populates='job_approvals')
    vetted_by_user: so.Mapped['User'] = so.relationship(
        foreign_keys='JobApplicant.vetted_by', back_populates='job_vet')
    

class Organization(Updateable, db.Model):
    __tablename__ = 'organizations'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True, unique=True)
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    is_approved: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    employer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Employer.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    
    employer: so.Mapped[Employer] = so.relationship(back_populates='organization')
    recruiters: so.WriteOnlyMapped['Recruiter'] = so.relationship(back_populates='organization')
    
    @staticmethod
    def generate_slug(slug):
        _slug = slugify(slug)
        unique_slug = _slug
        counter = 1
        
        while Organization.exists_slug(unique_slug):
            unique_slug = f"{_slug}-{counter}"
            counter += 1

        return unique_slug
	
    @classmethod
    def exists_slug(cls, slug):
        existing_slug = cls.query.filter_by(slug=slug).first()
        return existing_slug