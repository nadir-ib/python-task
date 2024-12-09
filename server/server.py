from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from app.resources.vehicle_api import VehicleAPI

app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)

# Register the resource
api.add_resource(VehicleAPI, '/upload')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
