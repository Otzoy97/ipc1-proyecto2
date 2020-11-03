from errors.user import DuplicatedUser, UserNotExist
from flask import Blueprint, Response, jsonify, request
from models.user import User
from mongoengine.errors import DoesNotExist, NotUniqueError
import datetime
from flask_jwt_extended.utils import create_access_token

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
    try:
        body = request.get_json()
        user = User.objects.get(usr=body.get('usr'), pwd=body.get('pwd'))
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
    except DoesNotExist:
        raise UserNotExist('Usuario o contraseña inválido', status_code=401)

## Recuperar contraseña
@users.route('/users/recoverpwd', methods=['POST'])
def recover_pwd():
    try:
        body = request.get_json()
        user = User.objects.get(usr=body.get('usr'))
        return {'pwd': str(user.pwd)}, 200
    except DoesNotExist:
        raise UserNotExist('Usuario no existe', status_code=401)

@users.errorhandler(DuplicatedUser)
def handle_not_unique_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@users.errorhandler(UserNotExist)
def handle_not_exist_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
