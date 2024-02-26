#!/usr/bin/python3
"""the __init__ file containing imports and the app_views
    bllueprint to be used in other views"""
from flask import Blueprint


# the app_views varaible whih will be used in other modules in views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# importing all the functions and routes in views folder
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
