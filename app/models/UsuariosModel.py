from app.extensions import db

# --- MODELO DE USUARIOS ---
class UsuariosModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
    # Relación con la tabla de roles
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    rol = db.relationship('RolModel', back_populates='usuarios')

    # Relaciones con el modelo de Vacantes - CORREGIDO
    vacantes_creadas = db.relationship('VacanteModel', 
                                     foreign_keys='VacanteModel.usuario_creador_id', 
                                     backref='creador', 
                                     lazy=True)
    
    vacantes_postuladas = db.relationship('VacanteModel', 
                                        foreign_keys='VacanteModel.usuario_postulado_id', 
                                        backref='postulante', 
                                        lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'password': self.password,
            'rol_id': self.rol_id,
            'nombre_rol': self.rol.nombre_rol if self.rol else None
        }


# --- MODELO DE ROLES ---
class RolModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), nullable=False, unique=True)

    # Relación con la tabla de usuarios
    usuarios = db.relationship('UsuariosModel', back_populates='rol', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_rol': self.nombre_rol
        }