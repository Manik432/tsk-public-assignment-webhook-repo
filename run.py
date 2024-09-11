import configparser
import os
from app import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("test.ini")))

app = create_app()

if __name__ == '__main__': 
    app.config['MONGO_URI'] = config['TEST']['DB_URI']
    app.run(debug=True)
