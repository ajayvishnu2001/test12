from flask import Flask
from flask_cors import CORS
from report import pand_rep
from forecast import pycaret
from mongodb2 import mongo2

app = Flask(__name__)
CORS(app)

app.register_blueprint(pand_rep)
app.register_blueprint(pycaret)
app.register_blueprint(mongo2)

if __name__ == "__main__":
    app.run()
