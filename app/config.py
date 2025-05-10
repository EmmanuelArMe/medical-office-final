import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '12345'),
    'database': os.getenv('DB_NAME', 'medical_office'),
    'port': int(os.getenv('DB_PORT', 3306))
}

API_PORT = int(os.getenv('API_PORT', 5000))
DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 3600))  # segundos

DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_CONFIG['user']}:"
    f"{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:"
    f"{DATABASE_CONFIG['port']}/"
    f"{DATABASE_CONFIG['database']}"
)