#!/usr/bin/python3
"""the module that contains the different routes to get city objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def state_cities(state_id):
    """gets the cities from a given state"""
    from models.state import State
    key = 'State.{}'.format(state_id)
    state_obj = storage.all(State).get(key)
    if state_obj is None:
        abort(404)
    cities_list = []
    for obj in state_obj.cities:
        cities_list.append(obj.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def cities(city_id):
    """retrieves a city object based on the id"""
    key = 'City.{}'.format(city_id)
    city_obj = storage.all(City).get(key)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def city_delete(city_id):
    """deletes a city object from storage"""
    key = 'City.{}'.format(city_id)
    city_obj = storage.all(City).get(key)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def city_post(state_id):
    """adds a new city object with a given state_id"""
    from models.state import State
    key = 'State.{}'.format(state_id)
    state_obj = storage.all(State).get(key)
    if state_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if request.get_json().get('name') is None:
        abort(400, 'Missing name')
    new_obj = City()
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_obj, key, value)
    new_obj.state_id = state_id
    new_obj.save()
    return (jsonify(new_obj.to_dict())), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def city_put(city_id):
    """updates a given city objec based on the city id"""
    key = 'City.{}'.format(city_id)
    city_obj = storage.all(City).get(key)
    if city_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)
    city_obj.save()
    return (jsonify(city_obj.to_dict())), 200
