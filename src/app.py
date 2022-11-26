"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person
import requests

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_people():
    people_response = requests.get("https://swapi.dev/api/people")
    results = people_response.json()["results"]
    new_results = []
    for i in results: 
        new_results.append(i["name"])

    new_height = []
    for i in results:
        new_height.append(i["height"])

    return jsonify(new_results, new_height), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    people_response = requests.get("https://swapi.dev/api/planets")
    results = people_response.json()["results"]
    new_results = []
    for i in results: 
        new_results.append(i["name"])

    new_climate = []
    for i in results:
        new_climate.append(i["climate"])

    return jsonify(new_results, new_climate), 200

@app.route("/species", methods=["GET"])
def handle_species():
    species_response = requests.get("https://swapi.dev/api/species")
    results = species_response.json()["results"]
    new_results = []
    for i in results:
        new_results.append(i["name"])
    
    new_language = []
    for i in results:
        new_language.append(i["language"])


    return jsonify(new_results, new_language), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
