from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.database import SessionLocal
from app.schemas.paciente import PacienteCreate, PacienteResponse
from app.services import paciente as service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pacientes", response_model=PacienteResponse)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    try:
        # Llamada al servicio para registrar el paciente
        paciente = service.registrar_paciente(db, paciente)

        # Convertir a modelo Pydantic
        paciente_creado = PacienteResponse.model_validate(paciente)

        # Convertir a JSON serializable
        paciente_response_json = jsonable_encoder(paciente_creado)

        return JSONResponse(
            content={
                "message": "Paciente creado correctamente",
                "response": paciente_response_json
            },
            status_code=status.HTTP_201_CREATED
        )
    
    # Manejar el error de integridad, específicamente el de duplicados
    except IntegrityError as e:
        
        db.rollback()  # Es importante para deshacer los cambios y liberar la sesión

        return JSONResponse(
            content={
                "message": f"El documento {paciente.documento} ya está registrado. Por favor, verifique el documento."
            },
            status_code=status.HTTP_400_BAD_REQUEST  # Código de estado para solicitud incorrecta
        )

@router.get("/pacientes", response_model=list[PacienteResponse])
def obtener_pacientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    # Llamada al servicio para listar los 10 primeros pacientes
    pacientes = service.listar_pacientes(db, skip=skip, limit=limit)

    # Convertir a JSON serializable
    pacientes_response = jsonable_encoder(pacientes)

    return JSONResponse(
        content={
            "message": "Lista de los primeros 10 pacientes obtenida correctamente",
            "response": pacientes_response
        },
        status_code=status.HTTP_200_OK
    )

@router.get("/pacientes/{documento}", response_model=PacienteResponse)
def obtener_paciente(documento: int, db: Session = Depends(get_db)):
    
    # Llamada al servicio para obtener un paciente por documento
    paciente = service.obtener_paciente(db, documento=documento)

    # Verificar si el paciente fue encontrado
    if paciente is None:
        return JSONResponse(
            content={
                "message": f"El paciente con el documento {documento} no fue encontrado. Por favor, verifique el documento."
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Convertir a modelo Pydantic
    paciente_response = PacienteResponse.model_validate(paciente)

    # Convertir a JSON serializable
    paciente_response_json = jsonable_encoder(paciente_response)

    return JSONResponse(
        content={
            "message": "Paciente obtenido correctamente",
            "response": paciente_response_json
        },
        status_code=status.HTTP_200_OK
    )

@router.delete("/pacientes/{documento}", response_model=PacienteResponse)
def eliminar_paciente(documento: int, db: Session = Depends(get_db)):

    # Llamada al servicio para eliminar un paciente por documento
    paciente = service.eliminar_paciente(db, documento=documento)

    # Verificar si el paciente fue eliminado anteriormente
    if paciente is None:
        return JSONResponse(
            content={
                "message": f"El paciente con el documento {documento} que desea eliminar no fue encontrado. Por favor, verifique el documento."
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Convertir a modelo Pydantic
    paciente_reposonse = PacienteResponse.model_validate(paciente)

    # Convertir a JSON serializable
    paciente_response_json = jsonable_encoder(paciente_reposonse)

    return JSONResponse(
        content={
            "message": f"El paciente con el documento {documento} fue eliminado correctamente.",
            "response": paciente_response_json
        },
        status_code=status.HTTP_200_OK
    )
