# app/services/portfolio/routes.py
from apifairy.decorators import other_responses
from flask import Blueprint
from apifairy import  response

from api.services.country.country_service import CountryService
from api.schemas import CountrySchema, StateSchema
from api.decorators import paginated_response

country_service = CountryService()
country = Blueprint('country', __name__)
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
state_schema = StateSchema()
states_schema = StateSchema(many=True)

@country.route('/', methods=['GET'])
@response(countries_schema)
def get_portfolios():
    """Retrieve all countries"""
    return country_service.get_countries()


@country.route('/<int:id>', methods=['GET'])
@response(country_schema)
@other_responses({404: 'Country not found'})
def get_portfolio_by_id_or_404(id):
    """Retrieve a country by id"""
    return country_service.get_country_by_id_or_404(id)

@country.route('/states/', methods=['GET'])
@response(states_schema)
def get_states():
    """Retrieve all states"""
    return country_service.get_states()


@country.route('/states/<int:id>', methods=['GET'])
@response(state_schema)
@other_responses({404: 'State not found'})
def get_state_by_id_or_404(id):
    """Retrieve a state by id"""
    return country_service.get_state_by_id_or_404(id)
