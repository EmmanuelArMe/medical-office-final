from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.utils.encryption_setting import encrypt

# Cargar configuración de encriptación
fernet = encrypt()

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    especialidad_id = Column(Integer, ForeignKey("especialidades.id"))
    email = Column(String(100))
    _telefono = Column("telefono", String(512), nullable=True)
    _email = Column("email", String(512), nullable=True)
    documento = Column(String(25), unique=True, nullable=False)

    especialidad = relationship("Especialidad", back_populates="medicos")
    citas = relationship("Cita", back_populates="medico")
    horarios = relationship("HorarioMedico", back_populates="medico")
    
    # Propiedad para manejar la encriptación de telefono
    @property
    def telefono(self):
        try:
            if self._telefono:
                return fernet.decrypt(self._telefono.encode()).decode()
            return None
        except Exception as e:
            print(f"Error al desencriptar teléfono: {e}")
            return "[ERROR DE DESENCRIPTACIÓN]"
    
    @telefono.setter
    def telefono(self, value):
        if value:
            self._telefono = fernet.encrypt(str(value).encode()).decode()
        else:
            self._telefono = None
    
    # Propiedad para manejar la encriptación de email
    @property
    def email(self):
        try:
            if self._email:
                return fernet.decrypt(self._email.encode()).decode()
            return None
        except Exception as e:
            print(f"Error al desencriptar email: {e}")
            return "[ERROR DE DESENCRIPTACIÓN]"
    
    @email.setter
    def email(self, value):
        if value:
            self._email = fernet.encrypt(str(value).encode()).decode()
        else:
            self._email = None