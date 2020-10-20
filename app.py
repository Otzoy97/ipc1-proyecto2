from flask import Flask
from flask_cors import CORS
from database.db import initilize_db
from routes.index import init_routes
from config.config import MONGO_URI

app = Flask(__name__)
CORS(app)

app.config['MONGODB_SETTINGS'] = {
    'host': MONGO_URI
}

initilize_db(app)
init_routes(app)

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)