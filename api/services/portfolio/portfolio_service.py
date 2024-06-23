# app/services/portfolio/portfolio_service.py
from flask import abort

from api import db
from api.models import Portfolio
from .i_portfolio_service import IPortfolio

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
            portfolio_data = Portfolio(**args)
            db.session.add(portfolio_data)
            db.session.commit()
            return portfolio_data
        except Exception as e:
            self.sqlalchemy.session.rollback()
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