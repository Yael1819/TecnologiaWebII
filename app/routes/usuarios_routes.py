# En este archivo iran las rutas o EndPoints que tengan que ver con el CRUD de usuarios.

from flask import Blueprint, jsonify, request
from app.data import usuarios
from app.service.UsuarioService import UsuarioService

# Se crea el Blueprint
usuarios_bp = Blueprint('usuarios', __name__)

# Listar usuarios
@usuarios_bp.route('/', methods=['GET'])
def obtener_todos():
    usuarios = UsuarioService.obtener_usuarios()
    
    # Verificar si hay usuarios, si no hay, retornar un mensaje adecuado.
    if not usuarios:
        return jsonify({'mensaje': 'No hay usuarios registrados'}), 404
    
    return jsonify(usuarios)

# Crear usuarios
@usuarios_bp.route('/crear', methods=['POST'])
def crear_usuario():
    nuevo = request.get_json() or {}
    
    respuesta = UsuarioService.crear_usuario(
        nombre_usuario = nuevo.get('nombre_usuario'),
        password = nuevo.get('password'),
        rol_id = nuevo.get('rol_id')
    )
    return respuesta

# Buscar un usuario por id
@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario_por_id(usuario_id):
    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            return jsonify(usuario)
    return jsonify({'error': 'Usuario no encontrado'}), 404

# Actualizar informacion de un usuario
@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    # Obtener_usuario_por_id devuelve JSON; buscamos el objeto en la lista
    usuario_obj = next((u for u in usuarios if u['id'] == usuario_id), None)
    if usuario_obj is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    datos_actualizados = request.get_json() or {}

    if not datos_actualizados.get('nombre') or not datos_actualizados.get('password'):
        return jsonify({'error': 'Faltan campo obligatorios'}), 400

    usuario_obj.update(datos_actualizados)

    return jsonify({'Mensaje': 'Usuario actualizado exitosamente', 'Usuario': usuario_obj})