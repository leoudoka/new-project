# app/services/portfolio/portfolio_service.py
import os

from flask import abort, request
import cloudinary
import cloudinary.uploader

from api import db
from api.models import Portfolio
from .i_portfolio_service import IPortfolio


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

class PortfolioService(IPortfolio):
    def get_portfolio_by_id_or_404(self, id):
        return db.session.get(Portfolio, id) or abort(404)
    
    def get_portfolios(self):
        return Portfolio.query \
                .order_by(Portfolio.id.desc())
    
    def get_portfolio_by_given_column_name(self, column_name, value):
        if hasattr(Portfolio, column_name):
            column_name = getattr(Portfolio, column_name)
            return db.session.scalar(Portfolio.query.filter_by(column_name=value))
        abort(404)
    
    def create_portfolio(self, args: dict):
        try:
            resume_to_upload = request.files.get('resume')
            photo_to_upload = request.files.get('photo')
            if resume_to_upload:
                uploaded_resume = cloudinary.uploader.upload(resume_to_upload, folder='resume')
                args['resume_attachment'] = uploaded_resume["secure_url"]
                del args["resume"]
            elif photo_to_upload:
                uploaded_photo = cloudinary.uploader.upload(photo_to_upload, folder='profile')
                args['photo_attachment'] = uploaded_photo["secure_url"]
                del args["photo"]
            portfolio_data = Portfolio(**args)
            db.session.add(portfolio_data)
            db.session.commit()
            return portfolio_data
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_portfolio(self, args: dict):
        try:
            if args.get('id'):
                portfolio_to_update = self.get_portfolio_by_id_or_404(args.get('id'))
                if portfolio_to_update:
                    portfolio_to_update.update(args)
                    db.session.commit()
                    return portfolio_to_update

        except Exception as e:
            db.session.rollback()
            raise e

    def delete_portfolio(self, id: int)-> dict:
        portfolio_to_delete = self.get_portfolio_by_id_or_404(id)

        db.session.delete(portfolio_to_delete)
        db.session.commit()
        return {}, 204