from app.extensions import db  # Se importa la instancia de la base de datos desde el módulo principal del proyecto


# --- MODELO DE USUARIOS ---
class UsuariosModel(db.Model):
    # Nombre asignado a la tabla dentro de la base de datos
    __tablename__ = 'usuarios'

    # Definición de columnas y sus características
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de cada usuario
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)  # Nombre de usuario (no puede repetirse)
    password = db.Column(db.String(100), nullable=False)  # Contraseña cifrada o en texto (según la implementación)

    # Relación con la tabla de roles (cada usuario pertenece a un rol)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Clave foránea que conecta con la tabla 'roles'
    rol = db.relationship('RolModel', back_populates='usuarios')  # Relación bidireccional con el modelo de Rol

    def to_dict(self):
        """Convierte el objeto Usuario en un diccionario para facilitar su conversión a JSON."""
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'password': self.password
        }


# --- MODELO DE ROLES ---
class RolModel(db.Model):
    # Nombre asignado a la tabla dentro de la base de datos
    __tablename__ = 'roles'

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Identificador único del rol
    nombre_rol = db.Column(db.String(50), nullable=False, unique=True)  # Nombre del rol (por ejemplo: “admin”, “usuario”)

    # Relación con la tabla de usuarios (un rol puede tener varios usuarios)
    usuarios = db.relationship('UsuariosModel', back_populates='rol', lazy=True)

    def to_dict(self):
        """Convierte el objeto Rol en un diccionario para facilitar su representación JSON."""
        return {
            'id': self.id,
            'nombre_rol': self.nombre_rol
        }
