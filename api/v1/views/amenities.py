#!/usr/bin/python3
"""module that contains all the routes to be used in the api
    for amenities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def amenities_get():
    """retrieves a list of all amenities in storage"""
    amenity_objs = storage.all(Amenity).values()
    amenity_list = [obj.to_dict() for obj in amenity_objs]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenity_get(amenity_id):
    """gets an amenity from storage based on the id"""
    key = 'Amenity.{}'.format(amenity_id)
    amenity_obj = storage.all(Amenity).get(key)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def amenity_delete(amenity_id):
    """ deletes an amenity based on the id"""
    key = 'Amenity.{}'.format(amenity_id)
    amenity_obj = storage.all(Amenity).get(key)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def amenity_post():
    """adds a new amenity obj"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if request.get_json().get('name') is None:
        abort(400, 'Missing name')
    new_obj = Amenity()
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_obj, key, value)
    new_obj.save()
    return (jsonify(new_obj.to_dict())), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def amenity_put(amenity_id):
    """updates an amenity object based on the amenity id"""
    key = 'Amenity.{}'.format(amenity_id)
    amenity_obj = storage.all(Amenity).get(key)
    if amenity_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return (jsonify(amenity_obj.to_dict())), 200
