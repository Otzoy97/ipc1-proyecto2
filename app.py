from flask import Flask
from database.db import initilize_db
from routes.index import init_routes

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/usac-store'
}

initilize_db(app)
init_routes(app)

app.run()