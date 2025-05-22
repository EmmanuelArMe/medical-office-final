from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Removed SessionLocal import as get_db will provide the session
from app.db.database import get_db # Import the centralized get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.token import Token
from app.services import usuario as service
from app.utils import auth as auth_utils
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
    "/usuarios",
    response_model=UsuarioResponse,
    summary="Crear usuario",
    description="Crea un nuevo usuario en el sistema."
)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = service.crear_usuario(db, usuario)
    return JSONResponse(
        content={"message": "Usuario creado correctamente", "response": jsonable_encoder(nuevo_usuario)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por ID",
    description="Obtiene un usuario por su ID."
)
def obtener_usuario_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(auth_utils.get_current_user)):
    usuario = service.obtener_usuario_por_id(db, id)
    return JSONResponse(
        content={"message": "Usuario obtenido correctamente", "response": jsonable_encoder(usuario)},
        status_code=status.HTTP_200_OK
    )

@router.get(
    "/usuarios",
    response_model=list[UsuarioResponse],
    summary="Obtener lista de usuarios",
    description="Obtiene una lista de todos los usuarios paginada."
)
def obtener_usuarios(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(auth_utils.get_current_user)):
    usuarios = service.obtener_usuarios(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de usuarios obtenida correctamente", "response": jsonable_encoder(usuarios)},
        status_code=status.HTTP_200_OK
    )

@router.put(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario",
    description="Actualiza un usuario por su ID."
)
def actualizar_usuario(id: int, usuario: UsuarioCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(auth_utils.get_current_user)):
    usuario_actualizado = service.actualizar_usuario(db, id, usuario)
    return JSONResponse(
        content={"message": "Usuario actualizado correctamente", "response": jsonable_encoder(usuario_actualizado)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Eliminar usuario",
    description="Elimina un usuario por su ID."
)
def eliminar_usuario(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(auth_utils.get_current_user)):
    usuario = service.eliminar_usuario(db, id)
    return JSONResponse(
        content={"message": "Usuario eliminado correctamente", "response": jsonable_encoder(usuario)},
        status_code=status.HTTP_200_OK
    )

@router.get(
    "/usuarios/rol/{id}",
    response_model=list[UsuarioResponse],
    summary="Obtener usuarios por rol",
    description="Obtiene una lista de usuarios por su rol."
)   
def obtener_usuarios_por_rol(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(auth_utils.get_current_user)):
    usuarios = service.obtener_usuario_por_rol(db, id)
    return JSONResponse(
        content={"message": "Lista de usuarios por rol obtenida correctamente", "response": jsonable_encoder(usuarios)},
        status_code=status.HTTP_200_OK
    )

@router.post("/login", response_model=Token, summary="Iniciar sesión", description="Inicia sesión para obtener un token de acceso.")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Note: 'verificar_password' and 'obtener_usuario_por_nombre_de_usuario' are called via 'service.'
    user = service.obtener_usuario_por_nombre_de_usuario(db, username=form_data.username)
    if not user or not service.verificar_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_utils.create_access_token(
        data={"sub": user.username} # Using username as subject
    )
    return {"access_token": access_token, "token_type": "bearer"}