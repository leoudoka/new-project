# app/services/country/country_service.py
from flask import abort

from api import db
from api.models import Country, State
from .i_country_service import ICountry


class CountryService(ICountry):
    def get_country_by_id_or_404(self, id):
        return db.session.get(Country, id) or abort(404)
    
    def get_state_by_id_or_404(self, id):
        return db.session.get(State, id) or abort(404)
    
    def get_countries(self):
        return Country.query \
                .order_by(Country.name.asc())
    
    def get_states(self):
        return State.query \
                .order_by(State.id.asc())
    
    def get_states_by_country_id(self, country_id):
        return State.query \
                .filter_by(country_id=country_id) \
                .order_by(State.name.asc())\
                .all()
    
    def get_given_column_name(self, model, column_name, value):
        if hasattr(model, column_name):
            column_name = getattr(model, column_name)
            return db.session.scalar(model.query.filter_by(column_name=value))
        abort(404)
    
    def get_country_by_given_column_name(self, column_name, value):
        return self.get_given_column_name(Country, column_name, value)
    
    def get_state_by_given_column_name(self, column_name, value):
        return self.get_given_column_name(State, column_name, value)