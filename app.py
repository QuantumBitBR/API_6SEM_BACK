from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from controllers.tickets_controller import tickets_ns
from controllers.companies_controller import companies_ns
from controllers.privacy_policy_controller import privacy_policy_ns
from controllers.user_controller import users_ns

app = Flask(__name__)
api = Api(app, version="1.0", title="Help.AI!", description="Help.AI!")
CORS(app)

api.add_namespace(tickets_ns, '/tickets')
api.add_namespace(companies_ns, '/companies')
api.add_namespace(privacy_policy_ns, '/privacy')
api.add_namespace(users_ns, '/users-tickets')

if __name__ == "__main__":
    app.run(debug=True)