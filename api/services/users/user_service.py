from flask import abort

from api import db
from api.models import User as UserModel
from .i_user_service import IUser

class User(IUser):
    def get_user_by_id_or_404(self, id):
        return db.session.get(UserModel, id) or abort(404)