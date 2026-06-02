from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import deps
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.services.usuarios_service import create_user

router = APIRouter()


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(deps.get_db)):
    return create_user(db, usuario_in)