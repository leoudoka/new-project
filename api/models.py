from datetime import datetime, timedelta
from hashlib import md5
import secrets, enum
from time import time
from typing import Optional

from flask import current_app, url_for
import jwt
from alchemical import Model
import sqlalchemy as sa
from sqlalchemy import orm as so
from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Token(Model):
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
        db.session.execute(Token.delete().where(
            Token.refresh_expiration < yesterday))

    @staticmethod
    def from_jwt(access_token_jwt):
        access_token = None
        try:
            access_token = jwt.decode(access_token_jwt,
                                      current_app.config['SECRET_KEY'],
                                      algorithms=['HS256'])['token']
            return db.session.scalar(Token.select().filter_by(
                access_token=access_token))
        except jwt.PyJWTError:
            pass


class User(Updateable, Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    middle_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, nullable=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    gender: so.Mapped[Optional[enum.Enum]] = so.mapped_column(
        'gender', sa.Enum('male', 'female', 'not-specified'), 
        default='not-specified')
    dob: so.Mapped[Optional[datetime.date]] = so.mapped_column(sa.Date, index=True, nullable=True)
    mobile_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(15))
    password_harsh: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    email_verified_at: so.Mapped[datetime] = so.mapped_column(nullable=True)
    last_seen: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    tokens: so.WriteOnlyMapped['Token'] = so.relationship(back_populates='user')
    address: so.WriteOnlyMapped['Address'] = so.relationship(back_populates='user')
    attachments: so.WriteOnlyMapped['Attachment'] = so.relationship(back_populates='user')
    jobs: so.WriteOnlyMapped['Job'] = so.relationship(back_populates='user')
    applicant: so.WriteOnlyMapped['JobApplicant'] = so.relationship(back_populates='user')

    def __repr__(self):  # pragma: no cover
        return '<User {}>'.format(self.username)

    @property
    def url(self):
        return url_for('users.get', id=self.id)

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
    

class Address(Updateable, Model):
    __tablename__ = 'addresses'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    city_id: so.Mapped[int]
    country_id: so.Mapped[int]
    postal_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    user: so.Mapped[User] = so.relationship(back_populates='address')

    def __repr__(self):  # pragma: no cover
        return '<Address {}>'.format(self.address)
    
class Attachment(Updateable, Model):
    __tablename__ = 'attachments'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    path: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    entity_id: so.Mapped[int]
    entity_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    user: so.Mapped[User] = so.relationship(back_populates='attachments')

    def __repr__(self):  # pragma: no cover
        return '<Attachment {}>'.format(self.path)
    

class JobContractType(Updateable, Model):
    __tablename__ = 'job_contract_types'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contract_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)


    def __repr__(self):  # pragma: no cover
        return '<Job Contract Type {}>'.format(self.contract_type)
    
class JobWorkType(Updateable, Model):
    __tablename__ = 'job_work_types'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    work_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)


    def __repr__(self):  # pragma: no cover
        return '<Job Work Type {}>'.format(self.work_type)
    
class JobExperienceType(Updateable, Model):
    __tablename__ = 'job_experience_types'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    experience_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)


    def __repr__(self):  # pragma: no cover
        return '<Job Experience Type {}>'.format(self.experience_type)
    
class JobCategory(Updateable, Model):
    __tablename__ = 'job_categories'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)


    def __repr__(self):  # pragma: no cover
        return '<Job Category {}>'.format(self.name)
    

class JobIndustry(Updateable, Model):
    __tablename__ = 'job_industries'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)


    def __repr__(self):  # pragma: no cover
        return '<Job Industries {}>'.format(self.name)
    
class Job(Updateable, Model):
    __tablename__ = 'jobs'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True, unique=True)
    summary: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    job_category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobCategory.id))
    job_industry_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobIndustry.id))
    job_experience_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobExperienceType.id))
    job_contract_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(JobContractType.id))
    featured: so.Mapped[bool] = so.mapped_column(default=False)
    status: so.Mapped[Optional[enum.Enum]] = so.mapped_column(
        sa.Enum('open', 'paused', 'closed'), 
        default='open')
    employer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('employer.id'), index=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    employer: so.Mapped['Employer'] = so.relationship(back_populates='jobs')
    user: so.Mapped[User] = so.relationship(back_populates='jobs')

class Employer(Updateable, Model):
    __tablename__ = 'employers'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True)
    slug: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), index=True, unique=True)
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, index=True)
    country_id: so.Mapped[int]
    state_id: so.Mapped[int]
    address_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Address.id), index=True)
    attachment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Attachment.id), index=True)
    is_approved: so.Mapped[bool] = so.mapped_column(default=False)
    status: so.Mapped[bool] = so.mapped_column(default=False)
    approved_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    applicant: so.Mapped['JobApplicant'] = so.relationship(back_populates='employer')
    user: so.Mapped['User'] = so.relationship(back_populates='employer')

class JobApplicant(Updateable, Model):
    __tablename__ = 'job_applicants'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    job_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Job.id))
    employer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Employer.id))
    cover_letter_attachment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Attachment.id))
    cv_attachment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Attachment.id))
    status: so.Mapped[Optional[enum.Enum]] = so.mapped_column(
        sa.Enum('accepted', 'pending', 'rejected'), 
        default='pending')
    is_approved: so.Mapped[bool] = so.mapped_column(default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    vetted_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    approved_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    employer: so.Mapped['Employer'] = so.relationship(back_populates='applicant')
    user: so.Mapped['User'] = so.relationship(back_populates='applicant')