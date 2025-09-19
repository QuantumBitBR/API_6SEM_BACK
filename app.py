from os import environ
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from controllers.tickets_controller import tickets_ns
from controllers.indexer_controller import indexes_ns
from controllers.auth_controller import auth_ns
from controllers.user_controller import user_ns
from config.extensions import db, ma

app = Flask(__name__)
api = Api(app, version="1.0", title="Help.AI!", description="Help.AI!")
CORS(app)

api.add_namespace(tickets_ns, '/tickets')
api.add_namespace(indexes_ns, "/index")
api.add_namespace(user_ns, "/user")
api.add_namespace(auth_ns, "/auth")
# Database config
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)