# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_caching import Cache

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache()