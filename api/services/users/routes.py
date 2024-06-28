# app/services/users/routes.py
from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.services.users.user_service import UserService
from api.schemas import UserSchema, UpdateUserSchema, UserDetailsSchema, RecruiterSchema
from api.services.auth.auth_service import token_auth
from api.decorators import paginated_response

user_service = UserService()
users = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)

user_details_schema = UserDetailsSchema()
recruiter_schema = RecruiterSchema()

@token_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()

@users.route('/', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
def create_user(args):
    """Register a new user"""
    return user_service.create_user(args)


@users.route('/', methods=['GET'])
@authenticate(token_auth)
@paginated_response(users_schema)
def get_users():
    """Retrieve all users"""
    return user_service.get_users()


@users.route('/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get_user_by_id_or_404():
    """Retrieve a user by id"""
    user = token_auth.current_user()
    user_id = user.id
    return user_service.get_user_by_id_or_404(user_id)


@users.route('/username/<username>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get_by_username(username):
    """Retrieve a user by username"""
    return user_service.get_user_by_given_column_name(username=username)


@users.route('/talent', methods=['PUT', 'PATCH'])
@body(user_details_schema)
@response(user_details_schema, 201)
def update_new_talent(args):
    """Update newly registered talent"""
    return user_service.update_user_details(args)


@users.route('/recruiter', methods=['PUT', 'PATCH'])
@body(user_details_schema)
@response(user_details_schema, 201)
def update_new_recruiter(args):
    """Update newly registered recruiters"""
    return user_service.update_user_details(args)


@users.route('/recruiter/details', methods=['PATCH'])
@body(recruiter_schema, location='form', media_type='multipart/form-data')
@response(recruiter_schema, 201)
def update_recruiter_details(args):
    """Update newly registered recruiters"""
    return user_service.update_recruiter_details(args)


@users.route('/', methods=['PUT', 'PATCH'])
@authenticate(token_auth)
@body(update_user_schema)
@response(update_user_schema, 201)
def update_user(args):
    """Update existing user"""
    user = token_auth.current_user()
    args['id'] = user.id
    return user_service.update_user(args)
