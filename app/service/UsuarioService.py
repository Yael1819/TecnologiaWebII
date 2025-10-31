# Archivo creado con el fin de implementar la logica de negocio para usuarios.
from app.models.UsuariosModel import UsuariosModel
from flask import jsonify
from app.extensions import db

class UsuarioService:

    @staticmethod
    def obtener_usuarios():
        usuarios = UsuariosModel.query.all()
        # Devolver lista serializable (dict) en lugar de objetos SQLAlchemy
        return [u.to_dict() for u in usuarios]
    
    @staticmethod
    def crear_usuario(nombre_usuario, password, rol_id):

        if not nombre_usuario or not password:
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        if UsuariosModel.query.filter_by(nombre_usuario=nombre_usuario).first():
            return jsonify({'error': 'El nombre de usuario ya existe'}), 400

        nuevo_usuario = UsuariosModel(
            nombre_usuario=nombre_usuario,
            password=password,
            rol_id=rol_id
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return jsonify({'mensaje': 'Usuario creado exitosamente', 'usuario': nuevo_usuario.to_dict()}), 201
        except Exception as e:
            # Si hay un error al commitear, hacer rollback para dejar la sesión limpia
            try:
                db.session.rollback()
            except Exception:
                pass
            # Devolver detalle mínimo para depuración (no exponer en producción)
            return jsonify({'error': 'Error al guardar el usuario en la base de datos', 'detalle': str(e)}), 500
    
    # Buscar usuario por id
    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        usuario = UsuariosModel.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return usuario.to_dict()
    
    