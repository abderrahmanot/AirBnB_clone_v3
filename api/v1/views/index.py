#!/usr/bin/python3
"""the file that contains the blueprints to be used in the app
    the ones for status and count"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


# the function that handles the status route /status
@app_views.route('/status', strict_slashes=False,
                 methods=['GET'])
def status():
    """returns the status of the server in json format
        like {status: OK}"""
    dict = {}
    dict['status'] = 'OK'
    return jsonify(dict), 200


# the function that handles the api/v1/stats route
@app_views.route('/stats', strict_slashes=False,
                 methods=['GET'])
def count():
    """returns the count of the classes in models in json format
        the returned value is a list of dictionaries"""
    from models.amenity import Amenity
    from models.base_model import BaseModel
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    models_dict = {'amenities': Amenity, 'cities': City, 'places': Place,
                   'reviews': Review, 'states': State, 'users': User}
    res_dict = {}
    for key, value in models_dict.items():
        res_dict[key] = storage.count(value)
    return jsonify(res_dict)
