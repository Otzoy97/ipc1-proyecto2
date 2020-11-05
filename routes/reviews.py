from flask import Blueprint, Response, jsonify, request
from models.models import Application, Review, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import DoesNotExist

reviews = Blueprint('reviews', __name__)


@reviews.route('/reviews/get_by_id', methods=['GET'])
def get_by_id():
    """Recupera todas las reseñas de una aplicación, utilizando
    el identificador de la aplicación"""
    body = request.get_json()
    try:
        app_ = Application.objects.get(id=body.get('id'), auth=True)
        ret_app = {
            "id": str(app_.id),
            "title": app_.title,
            "url": app_.url,
            "cat": {
                "id": str(app_.cat.id),
                "name": app_.cat.name
            },
            "downloads": app_.downloads,
            "des": app_.des,
            "price": float(app_.price),
            "likes": app_.likes
        }
        rev = []
        for r in Review.objects(app=app_):
            rev.append({
                'user': {
                    "name": r.user.name,
                    "surname": r.user.surname,
                    "usr": r.user.usr
                },
                'txt': r.txt,
                'rating': r.rating
            })
        return {'payload': {'app': ret_app, 'reviews': rev}}, 200
    except Exception:
        return {'message': 'No se encontraron coincidencias'}, 400


@reviews.route('/reviews/create', methods=['POST'])
@jwt_required
def create():
    """Agrega una nueva reseña a una aplicación, la aplicción
    se identifica utilizando el id, y el usuario con el token
    de sesión"""
    body = request.get_json()
    user_id = get_jwt_identity()
    try:
        # recupera el usuario
        user_ = User.objects.get(id=user_id)
        # recupera la aplicación
        app_ = Application.objects.get(id=body.get('app'))
        # crea la review
        review = Review(txt=body.get('txt'),
                        rating=body.get('rating'),
                        app=app_,
                        user=user_).save()
        # actualiza las reviews del usuario y de la aplicación
        user_.update(push__reviews=review)
        app_.update(push__reviews=review)
        return {'message': 'Reviews creada'}, 200
    except Exception:
        return {'message': 'No se pudo crear la review'}, 400
