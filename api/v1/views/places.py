#!/usr/bin/python3
""" module contains routes to places"""
from flask import abort, jsonify, request
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def places_get(city_id):
    """gets a list of places linked to a given city"""
    from models.city import City
    key = 'City.{}'.format(city_id)
    city_obj = storage.all(City).get(key)
    if city_obj is None:
        abort(404)
    places_objs = city_obj.places
    places_list = [place_obj.to_dict() for place_obj in places_objs]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def place_get(place_id):
    """gets a place object based on the place id"""
    key = 'Place.{}'.format(place_id)
    place_obj = storage.all(Place).get(key)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """deletes a place from storage based on the place id"""
    key = 'Place.{}'.format(place_id)
    place_obj = storage.all(Place).get(key)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def place_post(city_id):
    """adds a new place with a given city id"""
    from models.city import City
    from models.user import User
    key = 'City.{}'.format(city_id)
    city_obj = storage.all(City).get(key)
    if city_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if request.get_json().get('user_id') is None:
        abort(400, 'Missing user_id')
    user_key = 'User.{}'.format(request.get_json().get("user_id"))
    user_obj = storage.all(User).get(user_key)
    if user_obj is None:
        abort(404)
    if request.get_json().get('name') is None:
        abort(400, 'Missing name')
    new_place = Place()
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_place, key, value)
    new_place.city_id = city_id
    new_place.save()
    return (jsonify(new_place.to_dict())), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def place_put(place_id):
    """updates a given place with new data based on the place id"""
    key = 'Place.{}'.format(place_id)
    place_obj = storage.all(Place).get(key)
    if place_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore_list = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in request.get_json().items():
        if key not in ignore_list:
            setattr(place_obj, key, value)
    place_obj.save()
    return (jsonify(place_obj.to_dict())), 200
