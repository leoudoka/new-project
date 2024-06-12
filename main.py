import os
from api import create_app

config_class = os.environ.get('CONFIGURATION_SETUP')
app = create_app(config_class)
