from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.UsuariosModel import RolModel
from app.service.RolService import RolService

roles_bp = Blueprint('roles', __name__)

# Obtener todos los roles
@roles_bp.route('/', methods=['GET'])
def obtener_roles():
    # Hacer querys desde instancia
    # query = db.session.query().filter() sirve para hacer consultas mas complejas
    # roles = RolModel.query.all() # Query en Python con Flask usando sqlalchemy. Esta es otra forma de hacerlo
    
    roles = RolService.obtener_roles() # Llamada al servicio para obtener roles.

    # Convertir los datos a un JSON
    roles_json = [ {
        'id': roles.id,
        'nombre_rol': roles.nombre_rol,
        'usuarios' : [u.nombre_usuario for u in roles.usuarios] # Iteración para obtener los nombres de usuario asociados a cada rol

    } for roles in roles
    ]
    
    # Devuelve los datos en formato JSON.
    return jsonify(roles_json), 200

# Crear un nuevo rol
@roles_bp.route('/crear', methods=['POST'])
def crear_rol():
    nuevo = request.get_json() or {}

    respuesta = RolService.crear_rol(
        nombre_rol=nuevo.get('nombre_rol'))
    return respuesta
    
    