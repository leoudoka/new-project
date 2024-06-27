import os
from api import create_app

config_class = os.environ.get('CONFIGURATION_SETUP')
app = create_app(config_class)

# Runs the server
if __name__ == '__main__':
    # setup_log()
    app.config.from_object(os.getenv('CONFIGURATION_SETUP'))
    app.run(debug=True, host='0.0.0.0', port=app.config['PORT'])