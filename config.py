# -----------------------------------------------------------
# Archivo: config.py
# Descripción:
#   Define la configuración global de la aplicación Flask,
#   incluyendo la conexión a la base de datos, parámetros de depuración
#   y la configuración de los tokens JWT para autenticación.
# -----------------------------------------------------------
import os
from dotenv import load_dotenv
from datetime import timedelta

# Esto permite mantener contraseñas, llaves secretas y configuraciones sensibles
# fuera del código fuente. Flask leerá los valores mediante os.getenv().
load_dotenv()


class Config:

    #  Configuración general 
    DEBUG = True  # Habilita el modo de depuración
    PORT = 5000   # Puerto por defecto en el que correrá la aplicación Flask

    #  Configuración de la base de datos 
    # Se obtienen los valores desde las variables de entorno definidas en .env.
    # Si alguna variable no está definida, se usa el valor por defecto.
    DB_USER = os.getenv('DB_USER', 'yael')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Yael123!')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'vacantes_db')

    # Cadena de conexión para SQLAlchemy usando el conector PyMySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    #  Configuración de seguridad 
    # Clave secreta utilizada para firmar y verificar los tokens JWT.
    # Debe cambiarse en producción por una clave más compleja y segura.
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Tiempo de expiración para el token de acceso.
    # Define cuánto dura la sesión activa del usuario antes de tener que renovarla.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # Tiempo de expiración del token de refresco.
    # Permite generar un nuevo token de acceso sin volver a iniciar sesión.
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
