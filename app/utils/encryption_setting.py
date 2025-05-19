from cryptography.fernet import Fernet
import os
import base64

def encrypt() -> Fernet:
    # Cargar la clave de encriptación desde las variables de entorno
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

    if not ENCRYPTION_KEY:
        # Generar una nueva clave de encriptación si no existe
        ENCRYPTION_KEY = Fernet.generate_key().decode()
        
        # Guardar la clave en el archivo .env
        with open(".env", "a") as env_file:
            env_file.write(f"\nENCRYPTION_KEY={ENCRYPTION_KEY}")

    # Asegurarnos de que la clave esté codificada correctamente
    try:
        if not ENCRYPTION_KEY.endswith('='):
            # Podría ser una clave en otro formato, intentamos convertirla
            ENCRYPTION_KEY = base64.urlsafe_b64encode(ENCRYPTION_KEY.encode()).decode()
        
        # Crear el objeto Fernet con la clave de encriptación
        fernet = Fernet(ENCRYPTION_KEY.encode())
        
        # Verificar que la clave funciona
        test_data = fernet.encrypt(b"test")
        fernet.decrypt(test_data)
        
        return fernet
        
    except Exception as e:
        # Si hay un problema con la clave, generamos una nueva
        print(f"Error con la clave de encriptación: {e}")
        print("Generando nueva clave...")
        
        ENCRYPTION_KEY = Fernet.generate_key().decode()
        
        # Guardar la nueva clave en el archivo .env
        with open(".env", "a") as env_file:
            env_file.write(f"\nENCRYPTION_KEY_NEW={ENCRYPTION_KEY}")
        
        fernet = Fernet(ENCRYPTION_KEY.encode())
        print("Nueva clave generada. Actualiza las variables de entorno.")
        
        return fernet