from errors.user import DuplicatedUser, UserNotExist
from flask import Blueprint, Response, jsonify, request
from models.models import User
from mongoengine.errors import DoesNotExist, NotUniqueError
import datetime
from flask_jwt_extended.utils import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

users = Blueprint('users', __name__)

# Signup - cliente
@users.route('/users/client/signup', methods=['POST'])
def normal_sign_up():
    try:
        body = request.get_json()
        User(**body, type_ = 0).save()
        return {'message': 'Usuario creado'}, 200
    except NotUniqueError:
        raise DuplicatedUser('El usuario ya existe', status_code=400)

# Signup - admin
@users.route('/users/admin/signup', methods=['POST'])
@jwt_required
def admin_sign_up():
    """Crea un nuevo usuario administrador. Solo un usuario admin
    puede crear otro usuario admin"""
    admin_id = get_jwt_identity()
    user = User.objects.get(id=admin_id)
    if user.type_ == 1:
        try:
            body = request.get_json()
            User(**body, type_ = 1).save()
            return {'message': 'Usuario admin creado'}, 200
        except NotUniqueError:
            raise DuplicatedUser('El usuario ya existe', status_code=400)
    else:
        return {'message': 'El usuario no es admin'}, 401


# Login
@users.route('/users/login', methods=['POST'])
def log_in():
    try:
        body = request.get_json()
        user = User.objects.get(usr=body.get('usr'), pwd=body.get('pwd'))
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
    except DoesNotExist:
        raise UserNotExist('Usuario o contraseña inválido', status_code=401)

# Recuperar contraseña
@users.route('/users/recoverpwd', methods=['POST'])
def recover_pwd():
    try:
        body = request.get_json()
        user = User.objects.get(usr=body.get('usr'))
        return {'pwd': str(user.pwd)}, 200
    except DoesNotExist:
        raise UserNotExist('Usuario no existe', status_code=401)

# Actualizar usuario
@users.route('/users/update', methods=['PUT'])
@jwt_required
def update():
    try:
        user_id = get_jwt_identity()
        body = request.get_json()
        User.objects.get(id=user_id).update(**body)
        return {'message': 'Usuario actualizado'}, 200
    except NotUniqueError:
        raise DuplicatedUser('El usuario ya existe', status_code=400)

# Recupera todos los usuarios
@users.route('/users/admin/list', methods=['GET'])
# @jwt_required
def list():
    """Recupera la información de todos los usuarios"""
    # admin_id = get_jwt_identity()
    # user = User.objects.get(id=admin_id)
    # if user.type_ != 1:
    #     return {'message': 'El usuario no es admin'}, 401
    try:
        #users = User.objects.all()
        users = []
        for u in User.objects.all():
            users.append({"nombre": u.name, "apellido": u.surname,
                            "usuario": u.usr, "rol": "Cliente" if u.type_ == 0 else "Admin"})
        return {"payload": users}, 200
    except Exception:
        return {'message': 'No se pudo recuperar los usuario'}, 400
        
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
