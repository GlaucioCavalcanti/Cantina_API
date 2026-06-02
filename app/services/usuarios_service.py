from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..core import security
from ..models.usuarios import Usuario
from ..schemas.usuario import UsuarioCreate


def create_user(db: Session, usuario_in: UsuarioCreate) -> Usuario:
    # Verifica se o email já existe
    user_exists = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado."
        )

    novo_usuario = Usuario(
        email=usuario_in.email,
        hashed_password=security.get_password_hash(usuario_in.password),
        nome_completo=usuario_in.nome_completo,
        is_active=usuario_in.is_active
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar usuário: {str(e)}")


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user
