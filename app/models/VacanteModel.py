from app.extensions import db
from datetime import datetime

class VacanteModel(db.Model):
    __tablename__ = 'vacantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_vacante = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    detalles = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_edicion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = db.Column(db.String(20), default='Disponible')  # 'Disponible' u 'Ocupada'
    
    # Relaciones - CORREGIDO
    usuario_creador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario_postulado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    # Relaciones con UsuariosModel - SIN backref duplicado
    # Los backref ya están definidos en UsuariosModel
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_vacante': self.nombre_vacante,
            'descripcion': self.descripcion,
            'detalles': self.detalles,
            'fecha_publicacion': self.fecha_publicacion.isoformat() if self.fecha_publicacion else None,
            'fecha_edicion': self.fecha_edicion.isoformat() if self.fecha_edicion else None,
            'estado': self.estado,
            'usuario_creador_id': self.usuario_creador_id,
            'usuario_postulado_id': self.usuario_postulado_id,
            'usuario_creador': self.creador.nombre_usuario if self.creador else None,
            'usuario_postulado': self.postulante.nombre_usuario if self.postulante else None
        }