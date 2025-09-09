from flask import Flask
from flask_restx import Api
from controllers.tickets_by_company_controller import tickets_ns


app = Flask(__name__)
api = Api(app, version="1.0", title="Help.AI!", description="Help.AI!")

api.add_namespace(tickets_ns, '/tickets')

if __name__ == "__main__":
    app.run(debug=True)