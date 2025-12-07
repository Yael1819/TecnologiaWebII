from flask import Flask
from dotenv import load_dotenv

# Cargar variables que esten en env lo antes posible
load_dotenv()

from app.routes.usuarios_routes import usuarios_bp
from app.routes.roles_routes import roles_bp
from app.routes.auth_routes import auth_bp
from app.routes.vacantes_routes import vacantes_bp
from app.extensions import db, jwt
from config import Config
from app.models.UsuariosModel import UsuariosModel, RolModel
from app.models.VacanteModel import VacanteModel  # Importar el modelo de vacantes

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app) 
    
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            
            # Crear roles por defecto si no existen
            roles_por_defecto = ['reclutador', 'postulante']
            for nombre_rol in roles_por_defecto:
                if not RolModel.query.filter_by(nombre_rol=nombre_rol).first():
                    nuevo_rol = RolModel(nombre_rol=nombre_rol)
                    db.session.add(nuevo_rol)
            
            db.session.commit()
            print("Roles por defecto creados exitosamente")
            
        except Exception as e:
            print('Advertencia: no se pudieron crear/actualizar las tablas:', e)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(vacantes_bp, url_prefix='/vacantes')
    
    return app