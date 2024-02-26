#!/usr/bin/python3
"""contains all the routes for the places review"""
from flask import request, abort, jsonify
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def reviews_get(place_id):
    """gets all the reviews of a place"""
    from models.place import Place
    key = 'Place.{}'.format(place_id)
    place_obj = storage.all(Place).get(key)
    if place_obj is None:
        abort(404)
    review_list = [review_obj.to_dict() for review_obj in place_obj.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def review_get(review_id):
    """gets a specific review based on the id"""
    key = 'Review.{}'.format(review_id)
    review_obj = storage.all(Review).get(key)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def review_delete(review_id):
    """deletes a review based on the review id"""
    key = 'Review.{}'.format(review_id)
    review_obj = storage.all(Review).get(key)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def review_post(place_id):
    """creates a new review on a given place using the place id"""
    from models.place import Place
    from models.user import User
    place_key = 'Place.{}'.format(place_id)
    place_obj = storage.all(Place).get(place_key)
    if place_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if request.get_json().get('user_id') is None:
        abort(400, 'Missing user_id')
    user_key = 'User.{}'.format(request.get_json().get("user_id"))
    user_obj = storage.all(User).get(user_key)
    if user_obj is None:
        abort(404)
    if request.get_json().get('text') is None:
        abort(400, 'Missing text')
    new_review = Review()
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_review, key, value)
    new_review.place_id = place_id
    new_review.save()
    return (jsonify(new_review.to_dict())), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def review_put(review_id):
    """updates a given review based on its id"""
    key = 'Review.{}'.format(review_id)
    review_obj = storage.all(Review).get(key)
    if review_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore_list = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in request.get_json().items():
        if key not in ignore_list:
            setattr(review_obj, key, value)
    review_obj.save()
    return (jsonify(review_obj.to_dict())), 200
