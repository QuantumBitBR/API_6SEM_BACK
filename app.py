from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from controllers.tickets_controller import tickets_ns
from config.db_connection import get_cursor

app = Flask(__name__)
api = Api(app, version="1.0", title="Help.AI!", description="Help.AI!")
CORS(app)

api.add_namespace(tickets_ns, '/tickets')

if __name__ == "__main__":
    app.run(debug=True)