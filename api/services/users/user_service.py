# app/services/users/user_service.py
import os

from flask import abort, jsonify, request
import cloudinary
import cloudinary.uploader

from api import db
from api.models import User, Token, Address, Recruiter
from .i_user_service import IUser

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

class UserService(IUser):
    def get_user_by_id_or_404(self, id):
        return db.session.get(User, id) or abort(404)
    
    def get_users(self):
        return User.query \
                .order_by(User.id.desc())
    
    def get_user_by_given_column_name(self, column_name, value):
        if hasattr(User, column_name):
            column_name = getattr(User, column_name)
            return db.session.scalar(User.query.filter_by(column_name=value))
        abort(404)
    
    def create_user(self, args: dict):
        try:
            user_data = User(**args)
            db.session.add(user_data)
            db.session.commit()
            return user_data
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_user_details(self, args: dict):
        try:
            if args.get('id'):
                user_id = args.get('id')
                user_to_update = self.get_user_by_id_or_404(user_id)
                if args.get('country_id') or args.get('state_id'):
                    try:
                        user_address_data_exists = db.session.scalar(Address.query
                                 .filter(Address.user_id == user_id))
                        if user_address_data_exists:
                            user_address_data = user_address_data_exists
                        else:
                            user_address_data = Address()
                            user_address_data.user_id = user_id

                        if args.get('country_id'):
                            user_address_data.country_id = args.get('country_id')
                            del args['country_id']
                        if args.get('state_id'):
                            user_address_data.state_id = args.get('state_id')
                            del args['state_id']
                        db.session.add(user_address_data)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                if user_id and args.get('org_id'):
                    try:
                        recruiter_organization_data_exists = db.session.scalar(Recruiter.query
                                    .filter(Recruiter.user_id == user_id))
                        if recruiter_organization_data_exists:
                            recruiter_organization_data = recruiter_organization_data_exists
                        else:
                            recruiter_organization_data = Recruiter()
                            recruiter_organization_data.user_id = user_id

                        recruiter_organization_data.org_id = args.get('org_id')
                        del args['org_id']

                        db.session.add(recruiter_organization_data)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                if user_to_update:
                    user_to_update.update(args)
                    db.session.commit()
                    return user_to_update
            return jsonify({"error": "User ID not provided/found"}), 404
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_recruiter_details(self, args: dict):
        try:
            user_id = args.get('user_id')
            if user_id:
                try:
                    recruiter_organization_data = db.session.scalar(Recruiter.query
                                .filter(Recruiter.user_id == user_id))
                    recruiter_organization_data.user_id = user_id

                    if args.get('org_id'):
                        recruiter_organization_data.org_id = args.get('org_id')
                        del args['org_id']
                    scope_to_upload = request.files.get('scope_attachment')
                    if scope_to_upload:
                        uploaded_scope = cloudinary.uploader.upload(scope_to_upload, folder='scope')
                        recruiter_organization_data.scope = uploaded_scope["secure_url"]
                    if args.get('work_preference'):
                        recruiter_organization_data.work_preference = args.get('work_preference')
                    if args.get('contract_type'):
                        recruiter_organization_data.contract_type = args.get('contract_type')

                    db.session.add(recruiter_organization_data)
                    db.session.commit()

                    return recruiter_organization_data
                except Exception as e:
                    db.session.rollback()
            return jsonify({"error": "User ID not provided/found"}), 404
        except Exception as e:
            db.session.rollback()
            raise e
        

    def update_user(self, args: dict):
        try:
            user_id = args.get('id')
            if user_id:
                user_to_update = self.get_user_by_id_or_404(user_id)
                if user_to_update:
                    user_to_update.update(args)
                    db.session.commit()
                    return user_to_update
            return jsonify({"error": "User ID not provided/found"}), 404
        except Exception as e:
            db.session.rollback()
            raise e


    def delete_user(self, id: int)-> dict:
        user_to_delete = self.get_user_by_id_or_404(id)

        db.session.delete(user_to_delete)
        db.session.commit()
        return {}, 204