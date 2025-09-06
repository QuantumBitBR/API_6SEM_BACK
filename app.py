from flask import Flask
from flask_restx import Api


app = Flask(__name__)
api = Api(app, version="1.0", title="Help.AI!", description="Help.AI!")

if __name__ == "__main__":
    app.run(debug=True)