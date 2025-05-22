import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.config import SECRET_KEY, JWT_EXPIRATION
from app.db.database import get_db
from app.models.usuario import Usuario  # For type hinting and return type
from app.services import usuario as usuario_service # To call the service function


# Initialize CryptContext for password hashing (can be shared if already defined elsewhere)
# For now, let's keep it self-contained for auth utilities, or ensure it's accessible.
# If you have a central place for pwd_context, import it from there.
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTPBearer for extracting token from Authorization header
oauth2_scheme = HTTPBearer()

# Helper function to create access token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Helper function to verify and decode access token
def verify_access_token(token: str, credentials_exception: HTTPException) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=credentials_exception.status_code,
            detail="Token has expired",
            headers=credentials_exception.headers
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

# Dependency to get current user from token
async def get_current_user(
    token: HTTPAuthorizationCredentials = Security(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token.credentials, credentials_exception)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = usuario_service.obtener_usuario_por_nombre_de_usuario(db, username=username)
    if user is None:
        raise credentials_exception
    return user
