# app/services/portfolio/routes.py
from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api import db
from api.services.portfolio.portfolio_service import PortfolioService
from api.schemas import PortfolioSchema, EmptySchema
from api.services.auth.auth_service import token_auth
from api.decorators import paginated_response

portfolio_service = PortfolioService()
portfolio = Blueprint('portfolio', __name__)
portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)
# update_portfolio_schema = UpdatePortfolioSchema(partial=True)


@portfolio.route('/', methods=['POST'])
@body(portfolio_schema, location='form', media_type='multipart/form-data')
@response(portfolio_schema, 201)
def create_portfolio(args):
    """Register a new portfolio"""
    return portfolio_service.create_portfolio(args)


@portfolio.route('/', methods=['GET'])
@authenticate(token_auth)
@paginated_response(portfolios_schema)
def get_portfolios():
    """Retrieve all portfolios"""
    return portfolio_service.get_portfolios()


@portfolio.route('/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(portfolio_schema)
@other_responses({404: 'Portfolio not found'})
def get_portfolio_by_id_or_404(id):
    """Retrieve a portfolio by id"""
    return portfolio_service.get_portfolio_by_id_or_404(id)
