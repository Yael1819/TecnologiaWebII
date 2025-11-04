from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.service.VacanteService import VacanteService

vacantes_bp = Blueprint('vacantes', __name__)

# --- RUTAS PARA RECLUTADORES ---

@vacantes_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear_vacante():
    """Crear nueva vacante - Solo reclutadores"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'reclutador':
        return jsonify({'error': 'Solo los reclutadores pueden crear vacantes'}), 403
    
    data = request.get_json() or {}
    
    respuesta = VacanteService.crear_vacante(
        nombre_vacante=data.get('nombre_vacante'),
        descripcion=data.get('descripcion'),
        detalles=data.get('detalles'),
        usuario_creador_id=int(get_jwt_identity())
    )
    
    return respuesta

@vacantes_bp.route('/mis-vacantes', methods=['GET'])
@jwt_required()
def obtener_mis_vacantes():
    """Obtener vacantes creadas por el reclutador actual"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'reclutador':
        return jsonify({'error': 'Solo los reclutadores pueden ver sus vacantes'}), 403
    
    usuario_id = int(get_jwt_identity())
    vacantes = VacanteService.obtener_vacantes_reclutador(usuario_id)
    
    return jsonify(vacantes), 200

@vacantes_bp.route('/<int:vacante_id>', methods=['PUT'])
@jwt_required()
def actualizar_vacante(vacante_id):
    """Actualizar vacante - Solo el creador"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'reclutador':
        return jsonify({'error': 'Solo los reclutadores pueden editar vacantes'}), 403
    
    data = request.get_json() or {}
    usuario_id = int(get_jwt_identity())
    
    respuesta = VacanteService.actualizar_vacante(vacante_id, data, usuario_id)
    return respuesta

@vacantes_bp.route('/asignar/<int:vacante_id>', methods=['POST'])
@jwt_required()
def asignar_postulante(vacante_id):
    """Asignar postulante a vacante - Solo el creador"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'reclutador':
        return jsonify({'error': 'Solo los reclutadores pueden asignar vacantes'}), 403
    
    data = request.get_json() or {}
    usuario_postulado_id = data.get('usuario_postulado_id')
    usuario_reclutador_id = int(get_jwt_identity())
    
    if not usuario_postulado_id:
        return jsonify({'error': 'Se requiere usuario_postulado_id'}), 400
    
    respuesta = VacanteService.asignar_postulante(vacante_id, usuario_postulado_id, usuario_reclutador_id)
    return respuesta

# --- RUTAS PARA POSTULANTES ---

@vacantes_bp.route('/disponibles', methods=['GET'])
@jwt_required()
def obtener_vacantes_disponibles():
    """Obtener todas las vacantes disponibles"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'postulante':
        return jsonify({'error': 'Solo los postulantes pueden ver vacantes disponibles'}), 403
    
    vacantes = VacanteService.obtener_vacantes_disponibles()
    return jsonify(vacantes), 200

@vacantes_bp.route('/ultimas-tres', methods=['GET'])
@jwt_required()
def obtener_ultimas_tres():
    """Obtener las últimas 3 vacantes disponibles"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'postulante':
        return jsonify({'error': 'Solo los postulantes pueden ver las últimas vacantes'}), 403
    
    vacantes = VacanteService.obtener_ultimas_tres_vacantes()
    return jsonify(vacantes), 200

@vacantes_bp.route('/detalle/<int:vacante_id>', methods=['GET'])
@jwt_required()
def obtener_detalle_vacante(vacante_id):
    """Obtener detalles de una vacante específica"""
    claims = get_jwt()
    rol = claims.get('rol')
    
    if rol != 'postulante':
        return jsonify({'error': 'Solo los postulantes pueden ver detalles de vacantes'}), 403
    
    detalle = VacanteService.obtener_detalle_vacante(vacante_id)
    return jsonify(detalle), 200