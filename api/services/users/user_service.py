# app/services/users/user_service.py
from flask import abort

from api import db
from api.models import User
from .i_user_service import IUser

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
        
    def update_user(self, args: dict):
        try:
            if args.get('id'):
                user_to_update = self.get_user_by_id_or_404(args.get('id'))
                if args.get('country'):
                    del args['country']
                    del args['state']
                if user_to_update:
                    user_to_update.update(args)
                    db.session.commit()
                    return user_to_update

        except Exception as e:
            db.session.rollback()
            raise e

    def delete_user(self, id: int)-> dict:
        user_to_delete = self.get_user_by_id_or_404(id)

        db.session.delete(user_to_delete)
        db.session.commit()
        return {}, 204