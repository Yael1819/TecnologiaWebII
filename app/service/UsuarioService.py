# Archivo creado con el fin de implementar la logica de negocio para usuarios.
from app.models.UsuariosModel import UsuariosModel
from flask import jsonify
from app.extensions import db

class UsuarioService:

    @staticmethod
    def obtener_usuarios():
        """
        Obtener todos los usuarios de la base de datos
        """
        try:
            usuarios = UsuariosModel.query.all()
            # Devolver lista serializable (dict) en lugar de objetos SQLAlchemy
            return [u.to_dict() for u in usuarios]
        except Exception as e:
            return jsonify({'error': 'Error al obtener los usuarios', 'detalle': str(e)}), 500
    
    @staticmethod
    def crear_usuario(nombre_usuario, password, rol_id):
        """
        Crear un nuevo usuario en la base de datos
        """
        if not nombre_usuario or not password or not rol_id:
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        # Verificar si el nombre de usuario ya existe
        if UsuariosModel.query.filter_by(nombre_usuario=nombre_usuario).first():
            return jsonify({'error': 'El nombre de usuario ya existe'}), 400

        # Crear nuevo usuario
        nuevo_usuario = UsuariosModel(
            nombre_usuario=nombre_usuario,
            password=password,
            rol_id=rol_id
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return jsonify({
                'mensaje': 'Usuario creado exitosamente', 
                'usuario': nuevo_usuario.to_dict()
            }), 201
        except Exception as e:
            # Si hay un error al commitear, hacer rollback para dejar la sesión limpia
            db.session.rollback()
            return jsonify({
                'error': 'Error al guardar el usuario en la base de datos', 
                'detalle': str(e)
            }), 500
    
    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        """
        Buscar un usuario por su ID
        """
        try:
            usuario = UsuariosModel.query.get(usuario_id)
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            return jsonify(usuario.to_dict())
        except Exception as e:
            return jsonify({'error': 'Error al buscar el usuario', 'detalle': str(e)}), 500
    
    @staticmethod
    def actualizar_usuario(usuario_id, datos_actualizados):
        """
        Actualizar la información de un usuario existente
        """
        try:
            usuario = UsuariosModel.query.get(usuario_id)
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            # Verificar que al menos un campo fue proporcionado para actualizar
            campos_proporcionados = [field for field in ['nombre_usuario', 'password', 'rol_id'] if field in datos_actualizados]
            if not campos_proporcionados:
                return jsonify({'error': 'No se proporcionaron campos para actualizar'}), 400

            # Actualizar los campos proporcionados
            if 'nombre_usuario' in datos_actualizados:
                if not datos_actualizados['nombre_usuario']:
                    return jsonify({'error': 'El nombre de usuario no puede estar vacío'}), 400
                
                # Verificar que el nuevo nombre de usuario no exista (excluyendo el usuario actual)
                usuario_existente = UsuariosModel.query.filter(
                    UsuariosModel.nombre_usuario == datos_actualizados['nombre_usuario'],
                    UsuariosModel.id != usuario_id
                ).first()
                if usuario_existente:
                    return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400
                usuario.nombre_usuario = datos_actualizados['nombre_usuario']
            
            if 'password' in datos_actualizados:
                if not datos_actualizados['password']:
                    return jsonify({'error': 'La contraseña no puede estar vacía'}), 400
                usuario.password = datos_actualizados['password']
            
            if 'rol_id' in datos_actualizados:
                usuario.rol_id = datos_actualizados['rol_id']

            db.session.commit()
            return jsonify({
                'mensaje': 'Usuario actualizado exitosamente', 
                'usuario': usuario.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Error al actualizar el usuario', 
                'detalle': str(e)
            }), 500

    @staticmethod
    def eliminar_usuario(usuario_id):
        """
        Eliminar un usuario por su ID
        """
        try:
            usuario = UsuariosModel.query.get(usuario_id)
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'mensaje': 'Usuario eliminado exitosamente'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Error al eliminar el usuario', 
                'detalle': str(e)
            }), 500