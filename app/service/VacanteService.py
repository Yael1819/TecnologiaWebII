from app.models.VacanteModel import VacanteModel
from app.models.UsuariosModel import UsuariosModel
from flask import jsonify
from app.extensions import db
from datetime import datetime
from flask_jwt_extended import get_jwt

class VacanteService:

    @staticmethod
    def crear_vacante(nombre_vacante, descripcion, detalles, usuario_creador_id):
        """Crea una nueva vacante - Solo para reclutadores"""
        try:
            # Validar campos obligatorios
            if not all([nombre_vacante, descripcion, detalles, usuario_creador_id]):
                return jsonify({'error': 'Faltan campos obligatorios'}), 400
            
            # Verificar que el usuario creador existe
            usuario_creador = UsuariosModel.query.get(usuario_creador_id)
            if not usuario_creador:
                return jsonify({'error': 'Usuario creador no encontrado'}), 404
            
            nueva_vacante = VacanteModel(
                nombre_vacante=nombre_vacante,
                descripcion=descripcion,
                detalles=detalles,
                usuario_creador_id=usuario_creador_id,
                estado='Disponible'
            )
            
            db.session.add(nueva_vacante)
            db.session.commit()
            
            return jsonify({
                'mensaje': 'Vacante creada exitosamente',
                'vacante': nueva_vacante.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error al crear vacante', 'detalle': str(e)}), 500

    @staticmethod
    def obtener_vacantes_reclutador(usuario_id):
        """Obtiene las vacantes creadas por un reclutador"""
        try:
            vacantes = VacanteModel.query.filter_by(usuario_creador_id=usuario_id).all()
            return [vacante.to_dict() for vacante in vacantes]
        except Exception as e:
            return jsonify({'error': 'Error al obtener vacantes', 'detalle': str(e)}), 500

    @staticmethod
    def obtener_vacantes_disponibles():
        """Obtiene todas las vacantes disponibles - Para postulantes"""
        try:
            vacantes = VacanteModel.query.filter_by(estado='Disponible').all()
            return [vacante.to_dict() for vacante in vacantes]
        except Exception as e:
            return jsonify({'error': 'Error al obtener vacantes disponibles', 'detalle': str(e)}), 500

    @staticmethod
    def obtener_ultimas_tres_vacantes():
        """Obtiene las últimas 3 vacantes disponibles"""
        try:
            vacantes = VacanteModel.query.filter_by(estado='Disponible')\
                .order_by(VacanteModel.fecha_publicacion.desc())\
                .limit(3).all()
            return [vacante.to_dict() for vacante in vacantes]
        except Exception as e:
            return jsonify({'error': 'Error al obtener últimas vacantes', 'detalle': str(e)}), 500

    @staticmethod
    def actualizar_vacante(vacante_id, datos_actualizados, usuario_id):
        """Actualiza una vacante - Solo el creador puede actualizar"""
        try:
            vacante = VacanteModel.query.get(vacante_id)
            if not vacante:
                return jsonify({'error': 'Vacante no encontrada'}), 404
            
            # Verificar que el usuario es el creador
            if vacante.usuario_creador_id != usuario_id:
                return jsonify({'error': 'No tienes permisos para editar esta vacante'}), 403
            
            # Actualizar campos permitidos
            if 'nombre_vacante' in datos_actualizados:
                vacante.nombre_vacante = datos_actualizados['nombre_vacante']
            if 'descripcion' in datos_actualizados:
                vacante.descripcion = datos_actualizados['descripcion']
            if 'detalles' in datos_actualizados:
                vacante.detalles = datos_actualizados['detalles']
            
            vacante.fecha_edicion = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'mensaje': 'Vacante actualizada exitosamente',
                'vacante': vacante.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error al actualizar vacante', 'detalle': str(e)}), 500

    @staticmethod
    def asignar_postulante(vacante_id, usuario_postulado_id, usuario_reclutador_id):
        """Asigna un postulante a una vacante - Solo el creador puede asignar"""
        try:
            vacante = VacanteModel.query.get(vacante_id)
            if not vacante:
                return jsonify({'error': 'Vacante no encontrada'}), 404
            
            # Verificar que el usuario es el creador
            if vacante.usuario_creador_id != usuario_reclutador_id:
                return jsonify({'error': 'No tienes permisos para asignar esta vacante'}), 403
            
            # Verificar que el usuario postulado existe
            usuario_postulado = UsuariosModel.query.get(usuario_postulado_id)
            if not usuario_postulado:
                return jsonify({'error': 'Usuario postulado no encontrado'}), 404
            
            vacante.usuario_postulado_id = usuario_postulado_id
            vacante.estado = 'Ocupada'
            vacante.fecha_edicion = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'mensaje': 'Vacante asignada exitosamente',
                'vacante': vacante.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error al asignar vacante', 'detalle': str(e)}), 500

    @staticmethod
    def obtener_detalle_vacante(vacante_id):
        """Obtiene los detalles completos de una vacante"""
        try:
            vacante = VacanteModel.query.get(vacante_id)
            if not vacante:
                return jsonify({'error': 'Vacante no encontrada'}), 404
            
            return vacante.to_dict()
            
        except Exception as e:
            return jsonify({'error': 'Error al obtener detalle de vacante', 'detalle': str(e)}), 500