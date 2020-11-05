from flask import Blueprint, Response, jsonify, request
from models.models import Application, Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist

apps = Blueprint('apps', __name__)

@apps.route('/apps/upload', methods=['POST'])
def upload():
    """Crea aplicaciones utilizando la información de un json
    que se presupone se construyó al leer un archivo csv"""
    body = request.get_json()
    errores = False
    try:
        # itera la carga y recupera los datos de la aplicación
        # y la categoría
        for app in body:
            try:
                # busca la categoría por nombre
                category = Category.objects.get(name=app.get('cat'))
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
                likes = app.get("likes"),
                auth = True
            ).save()
            # actualiza la categoría
            category.update(push__apps=app)
        # al terminar envía el resultado de la operación
        return {'message': 'Carga recibida ' + 'con errores' if errores else 'sin errores'}, 200
    except Exception as e:
        return {'message': 'Ocurrió un error'}, 400
    
@apps.route('/apps/by_cat', methods = ['GET'])
def by_cat():
    """Recupera las aplicaciones por id de categoria"""
    body = request.get_json()
    try:
        cat_ = Category.objects.get(id = body.get('id'))
        apps = []
        for c in Application.objects(cat = cat_, auth = True):
            apps.append({
                "id" : str(c.id),
                "title": c.title,
                "url": c.url,
                "cat": {
                    "id" : str(c.cat.id),
                    "name": c.cat.name
                    },
                "downloads": c.downloads,
                "des": c.des,
                "price": float(c.price),
                "likes": c.likes
            })
        return {'payload': apps}, 200
    except DoesNotExist:
        return {'message': 'No hubo coincidencias'}, 204
    except Exception:
        return {'message': 'No se pudo recuperar las aplicaciones'}, 400

@apps.route('/apps/list_auth', methods = ['GET'])
def list_auth():
    """Devuelve una lista de todas las aplicaciones del sistema
    que ya han sido autorizadas por un administrador"""
    try:
        applications = []
        for c in Application.objects(auth = True):
            applications.append({
                "id" : str(c.id),
                "title": c.title,
                "url": c.url,
                "cat": {
                    "id" : str(c.cat.id),
                    "name": c.cat.name
                    },
                "downloads": c.downloads,
                "des": c.des,
                "price": float(c.price),
                "likes": c.likes
            })
        return {'payload': applications}, 200
    except Exception as e:
        print(e)
        return {'message': 'No se pudo recuperar las aplicaciones'}, 400

@apps.route('/apps/list_all', methods = ['GET'])
def list_all():
    """Devuelve una lista de todas las aplicaciones del sistema"""
    try:
        applications = []
        for c in Application.objects.all():
            applications.append({
                "id" : str(c.id),
                "title": c.title,
                "url": c.url,
                "cat": {
                    "id" : str(c.cat.id),
                    "name": c.cat.name
                    },
                "downloads": c.downloads,
                "des": c.des,
                "price": float(c.price),
                "likes": c.likes,
                "auth": c.auth
            })
        return {'payload': applications}, 200
    except Exception as e:
        return {'message': 'No se pudo recuperar las aplicaciones'}, 400

@apps.route('/apps/get_by_name', methods = ['GET'])
def get_by_name():
    """Recuperar aplicacion por coincidencia en title"""
    body = request.get_json()
    try:
        apps = []
        for c in Application.objects(title__contains=body.get('title'), auth = True):
            apps.append({
                "id" : str(c.id),
                "title": c.title,
                "url": c.url,
                "cat": {
                    "id" : str(c.cat.id),
                    "name": c.cat.name
                    },
                "downloads": c.downloads,
                "des": c.des,
                "price": float(c.price),
                "likes": c.likes,
            })
        return {'payload': apps}, 200
    except DoesNotExist:
        return {'message': 'No hay coincidencias'}, 204
    except Exception:
        return {'message': 'No se pudo recuperar información'}, 400

@apps.route('/apps/create', methods=['POST'])
def create():
    """Crea una aplicación. La categoría de la aplicación debe ser 
    pasada por id, no por nombre"""
    body = request.get_json()
    try:
        category = Category.objects.get(id=body.get('cat'))
        app = Application(**body, auth=False).save()
        category.update(push__apps=app)
        return {'message': 'Aplicación creada'}, 200
    except Exception:
        return {'message': 'No se pudo crear la aplicación'}, 400

@apps.route('/apps/delete', methods=['DELETE'])
def delete():
    """Elimina una aplicación utilizando el id"""
    body = request.get_json()
    try:
        Application(id = body.get('id')).delete()
        return {'message': 'Aplicción eliminada'}, 200
    except Exception:
        return {'message': 'No se pudo eliminar la aplicación'}, 400

@apps.route('/apps/update', methods=['PUT'])
def update():
    """Actualiza una aplicación"""
    body = request.get_json()
    try:
        Application.objects.get(id=body.get('id')).update(**body)
        return {'message': 'Aplicación actualizada'}, 200
    except Exception:
        return {'message': 'No se pudo actualizar la aplicación'}, 400