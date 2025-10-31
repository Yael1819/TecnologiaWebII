from app.models.UsuariosModel import RolModel
from flask import jsonify
from app.extensions import db


class RolService:

    @staticmethod
    def obtener_roles():
        roles = RolModel.query.all()
        return roles

    @staticmethod
    def crear_rol(nombre_rol):

        if not nombre_rol:
            return jsonify({'error': 'Faltan campos '}), 400

        # Verificar existencia en RolModel (no en UsuariosModel)
        if RolModel.query.filter_by(nombre_rol=nombre_rol).first():
            return jsonify({'error': 'El nombre del Rol ya es existente'}), 400

        nuevo_rol = RolModel(
            nombre_rol=nombre_rol
        )

        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify({'mensaje': 'Rol ha sido creado exitosamente', 'Rol': nuevo_rol.to_dict()}), 201