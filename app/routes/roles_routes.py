from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.UsuariosModel import RolModel
from app.service.RolService import RolService

# Se crea un "Blueprint" para modularizar las rutas relacionadas con los roles.
# Esto permite mantener una estructura ordenada en la aplicación Flask.
roles_bp = Blueprint('roles', __name__)

# -----------------------------------------------------------
# RUTA: Obtener todos los roles registrados en la base de datos
# -----------------------------------------------------------
@roles_bp.route('/', methods=['GET'])
def obtener_roles():
    """
    Endpoint que devuelve la lista completa de roles registrados.
    Llama al servicio RolService para realizar la consulta.
    """

    # Llamada al servicio encargado de obtener los registros desde la base de datos
    roles = RolService.obtener_roles()

    # Se convierte cada objeto Rol en un diccionario JSON.
    # Además, para cada rol se agregan los nombres de usuarios asociados (relación uno a muchos).
    roles_json = [
        {
            'id': rol.id,
            'nombre_rol': rol.nombre_rol,
            'usuarios': [u.nombre_usuario for u in rol.usuarios]  # Lista de usuarios vinculados al rol
        }
        for rol in roles
    ]

    # Retorna la respuesta en formato JSON con código HTTP 200 (OK)
    return jsonify(roles_json), 200


# -----------------------------------------------------------
# RUTA: Crear un nuevo rol
# -----------------------------------------------------------
@roles_bp.route('/crear', methods=['POST'])
def crear_rol():
    """
    Endpoint que permite registrar un nuevo rol en la base de datos.
    Espera un JSON con el campo 'nombre_rol'.
    """

    # Se obtiene el cuerpo de la solicitud en formato JSON.
    # Si no se envía ningún dato, se usa un diccionario vacío por defecto.
    nuevo = request.get_json() or {}

    # Se llama al servicio encargado de validar y guardar el nuevo rol.
    respuesta = RolService.crear_rol(
        nombre_rol=nuevo.get('nombre_rol')
    )

    # Devuelve la respuesta generada por el servicio (puede ser éxito o error).
    return respuesta
