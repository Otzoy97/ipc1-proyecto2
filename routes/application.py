from flask import Blueprint, Response, jsonify, request
from models.models import Application, Category
from flask_jwt_extended import jwt_required, get_jwt_identity

apps = Blueprint('apps', __name__)

# @apps.route('/apps/upload', methods=['GET', 'POST'])
# @jwt_required
# def upload_apps():
#     if request.method == 'POST':
#         ## verifica que se haya subido un archivo
#         if 'file' in request.files:
#             file = request.files['file']
#             ## verifica que no sea un archivo vacío
#             if file.filename != '':

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
