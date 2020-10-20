from flask import Flask
from database.db import initilize_db
from routes.index import init_routes
from config.config import MONGO_URI

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': MONGO_URI
}

initilize_db(app)
init_routes(app)

app.run()