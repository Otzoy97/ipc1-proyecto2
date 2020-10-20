from flask import Blueprint, Response, request
from mongoengine.errors import NotUniqueError
from models.user import User

users = Blueprint('users', __name__)

## Crear usuario 
@users.route('/users', methods=['POST'])
def add_user():
    try:
        body = request.get_json()
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 200
    except NotUniqueError:
        raise NotUniqueError('El usuario ya existe', status_code=400)

