from os import environ
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from controllers.tickets_controller import tickets_ns
from controllers.auth_controller import auth_ns
from controllers.user_controller import users_ns
from config.extensions import db, ma, cache
from controllers.companies_controller import companies_ns
from controllers.privacy_policy_controller import privacy_policy_ns
from controllers.user_controller import users_ns
from flask_caching import Cache
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app, version="1.0", title="Help.AI!", description="Help.AI!")
CORS(app)

api.add_namespace(tickets_ns, '/tickets')
api.add_namespace(users_ns, "/user")
api.add_namespace(auth_ns, "/auth")
# Database config
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""CONFIGURAÇÃO REDIS"""
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 10


db.init_app(app)
ma.init_app(app)
cache.init_app(app)

api.add_namespace(companies_ns, '/companies')
api.add_namespace(privacy_policy_ns, '/privacy')
api.add_namespace(users_ns, '/users-tickets')


if __name__ == "__main__":
    app.run(debug=True)