#!/usr/bin/python3
"""module that contains all the routes related to users which gets
    data about a user"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
def users_get():
    """returns a list of all the users in storage db"""
    from models.user import User
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def user_get(user_id):
    """gets a user from storage based on the users id"""
    from models.user import User
    key = 'User.{}'.format(user_id)
    user_obj = storage.all(User).get(key)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def user_delete(user_id):
    """deletes a given user based on the id part of the url"""
    from models.user import User
    key = 'User.{}'.format(user_id)
    user_obj = storage.all(User).get(key)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def user_post():
    """adds a new user to storage making sure all constraints met"""
    from models.user import User
    if not request.get_json():
        abort(400, 'Not a JSON')
    if request.get_json().get('email') is None:
        abort(400, 'Missing email')
    if request.get_json().get('password') is None:
        abort(400, 'Missing password')
    new_user = User()
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_user, key, value)
    new_user.save()
    return (jsonify(new_user.to_dict())), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def user_put(user_id):
    """updates a given user based on the id of the url part"""
    from models.user import User
    key = 'User.{}'.format(user_id)
    user_obj = storage.all(User).get(key)
    if user_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user_obj, key, value)
    user_obj.save()
    return (jsonify(user_obj.to_dict())), 200
