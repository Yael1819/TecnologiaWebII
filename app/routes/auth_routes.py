from flask import Blueprint, jsonify, request
from app.models.UsuariosModel import UsuariosModel
from app.service.AuthUsuario import AuthUsuario
from flask_jwt_extended import create_access_token, create_refresh_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')

    auth_usuario = AuthUsuario.authenticate_user(
        nombre_usuario=nombre_usuario,
        password=password
    )
    
    if auth_usuario:
        nombre_rol = auth_usuario.rol.nombre_rol
        # Genera un access token
        access_token = create_access_token(
            identity=str(auth_usuario.id),
            # opcional pero necesario si queremos hacer validaciones en endpoints
            # o para establecer proteccion de rutas
            additional_claims={'rol': nombre_rol}
        )

        # Genera un refresh token
        refresh_token = create_refresh_token(identity=str(auth_usuario.id))

        return jsonify({
            'message': 'Login exitoso',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        })
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401