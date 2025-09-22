# models/user.py
from config.extensions import db, ma

# -------------------------
# Modelo do usuário
# -------------------------
class User(db.Model):
    __tablename__ = 'user_authentication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, name, password, role, email):
        self.name = name
        self.password = password
        self.role = role
        self.email = email

# -------------------------
# Schemas com Marshmallow
# -------------------------
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True   # permite criar objetos User diretamente
        sqla_session = db.session

# instâncias de schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
