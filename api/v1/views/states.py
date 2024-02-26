#!/usr/bin/python3
"""gets all the state objects from the db and
    returns them in a get request"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False,
                 methods=['GET'])
def state():
    """retrieves a list of all state objects from the db"""
    state_objs = storage.all(State).values()
    state_list = [obj.to_dict() for obj in state_objs]
    return jsonify(state_list), 200


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def state_id(state_id):
    """gets a state object based on the id"""
    state_object = None
    state_objs = storage.all(State).values()
    for obj in state_objs:
        if obj.id == state_id:
            state_object = obj
            break
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict()), 200


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete(state_id):
    """method that deletes a state object from the db"""
    obj_key = 'State.{}'.format(state_id)
    obj = storage.all(State).get(obj_key)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}))


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def post():
    """adds a new state object to the states objects list"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if request.get_json().get('name') is None:
        abort(400, 'Missing name')
    obj = State()
    for key, value in request.get_json().items():
        setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict())), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def put(state_id):
    """updates a given states based on the id with new data"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    obj_key = 'State.{}'.format(state_id)
    obj = storage.all(State).get(obj_key)
    if obj is None:
        abort(404)
    ignore_key = ['id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore_key:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict())), 200
