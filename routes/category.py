from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.models import Category, User
from mongoengine.errors import DoesNotExist, NotUniqueError

cats = Blueprint('cats', __name__)

## Crea un nueva categoría con un nombre único
@cats.route('/cats/add', methods=['POST'])
# @jwt_required
def add():
    # admin_id = get_jwt_identity()
    # user = User.objects.get(id=admin_id)
    # if (user.type_ != 1):
    #     return {'message': 'El usuario no es admin'}, 401
    try:
        body = request.get_json()
        Category(**body).save()
        return {'message': 'Categoría creada'}, 200
    except NotUniqueError:
        return {"message": "La categoría ya existe"}, 400

## Elimina una categoría
@cats.route('/cats/delete', methods=['DELETE'])
# @jwt_required
def delete_():
    # admin_id = get_jwt_identity()
    # user = User.objects.get(id=admin_id)
    # if (user.type_ != 1):
    #     return {'message': 'El usuario no es admin'}, 401
    try:
        body = request.get_json()
        Category.objects.get(id=body.get('id')).delete()
        return {'message': 'Categoría eliminada'}, 200
    except DoesNotExist:
        return {'message': 'Categoría no existe'}, 400
    except Exception:
        return {'message': 'No se pudo eliminar la categoría'}, 400

## Recupera todas las categorías
@cats.route('/cats/list', methods=['GET'])
# @jwt_required
def list():
    # admin_id = get_jwt_identity()
    # user = User.objects.get(id=admin_id)
    # if (user.type_ != 1):
    #     return {'message': 'El usuario no es admin'}, 401
    try:
        categories = []
        for c in Category.objects.all():
            categories.append({'id_': str(c.id), 'nombre': c.name})
        return {'payload': categories}, 200
    except Exception:
        return {'message': 'No se pudo recuperar las categorías'}, 400

## Actualiza el nombre de una categoría
@cats.route('/cats/update', methods=['PUT'])
# @jwt_required
def update():
    # admin_id = get_jwt_identity()
    # user = User.objects.get(id=admin_id)
    # if (user.type_ != 1):
    #     return {'message': 'El usuario no es admin'}, 401
    body = request.get_json()
    try: 
        Category.objects.get(id=body.get('id')).update(name=body.get('name'))
        return {'message': 'Categoría actualizada'}, 200
    except NotUniqueError:
        return {'message': 'La categoría ya existe'}, 400
    except DoesNotExist:
        return {'message': 'La categoria no existe'}, 401
        