from flask import Blueprint, Response, jsonify, request
from models.models import Application, Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist

apps = Blueprint('apps', __name__)

@apps.route('/apps/upload', methods=['POST'])
def upload():
    body = request.get_json()
    errores = False
    try:
        # itera la carga y recupera los datos de la aplicación
        # y la categoría
        for app in body:
            try:
                # busca la categoría por nombre
                category = Category.objects.get(name=app.get('name'))
            except DoesNotExist:
                # si no existe se salta ese objeto
                errores = True
                continue
            # si la categoría existe almacena la aplicación
            app = Application(
                title = app.get("title"),
                url = app.get("url"),
                cat = category,
                downloads = app.get("downloads"),
                des = app.get("des"),
                price = app.get("price"),
                likes = app.get("likes")
            ).save()
            # actualiza la categoría
            category.update(push__apps=app)
        # al terminar envía el resultado de la operación
        return {'message': 'Carga recibida ' + 'con errores' if errores else 'sin errores'}, 200
    except Exception as e:
        return {'message': 'Ocurrió un error'}, 400

@apps.route('/apps/update', methods=['PUT'])
def update():
    body = request.get_json()
    try:
        Application.objects.get(id=body.get('id')).update(**body)
        return {'message': 'Aplicación actualizada'}, 200
    except Exception:
        return {'message': 'No se pudo actualizar la aplicación'}, 400

@apps.route('/apps/create', methods=['POST'])
def create():
    body = request.get_json()
    try:
        category = Category.objects.get(id=body.get('cat'))
        app = Application(**body).save()
        category.update(push__apps=app)
        return {'message': 'Aplicación creada'}, 200
    except Exception:
        return {'message': 'No se pudo crear la aplicación'}, 400

@apps.route('/apps/delete', methods=['DELETE'])
def delete():
    body = request.get_json()
    try:
        Application(id = body.get('id')).delete()
        return {'message': 'Aplicción eliminada'}, 200
    except Exception:
        return {'message': 'No se pudo eliminar la aplicación'}, 400
