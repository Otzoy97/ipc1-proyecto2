from flask import Blueprint, Response, request, jsonify
from mongoengine.errors import NotUniqueError
from errors.errors import DuplicatedUser
from models.user import User

users = Blueprint('users', __name__)

## Signup
@users.route('/users/signup', methods=['POST'])
def sign_up():
    try:
        body = request.get_json()
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 200
    except NotUniqueError:
        raise DuplicatedUser('El usuario ya existe', status_code=400)

## Login
@users.route('/users/login', methods=['POST'])
def log_in():
    pass

@users.errorhandler(DuplicatedUser)
def handle_not_unique_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


