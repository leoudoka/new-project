# app/services/portfolio/routes.py
from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from api.services.portfolio.portfolio_service import PortfolioService
from api.schemas import PortfolioSchema, PatchPortfolioSchema
from api.services.auth.auth_service import token_auth
from api.decorators import paginated_response

portfolio_service = PortfolioService()
portfolio = Blueprint('portfolio', __name__)
portfolio_schema = PortfolioSchema()
patch_portfolio_schema = PatchPortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)

@portfolio.route('/', methods=['POST'])
@body(portfolio_schema, location='form', media_type='multipart/form-data')
@response(portfolio_schema, 201)
@other_responses({404: 'User ID not found'})
def create_portfolio(args):
    """Register or Patch portfolio"""
    return portfolio_service.create_portfolio(args)


@portfolio.route('/', methods=['PATCH'])
@body(patch_portfolio_schema)
@response(patch_portfolio_schema)
@other_responses({404: 'User ID not found'})
def patch_new_portfolio(args):
    """Patch newly registered portfolio"""
    return portfolio_service.patch_new_portfolio(args)


@portfolio.route('/', methods=['GET'])
# @authenticate(token_auth)
@paginated_response(portfolios_schema)
def get_portfolios():
    """Retrieve all portfolios"""
    return portfolio_service.get_portfolios()


@portfolio.route('/me', methods=['GET'])
@authenticate(token_auth)
@response(portfolio_schema)
@other_responses({404: 'Portfolio not found'})
def get_portfolio_by_id_or_404():
    """Retrieve a portfolio by id"""
    user = token_auth.current_user()
    user_id = user.id
    return portfolio_service.get_portfolio_by_user_id_or_404(user_id)
