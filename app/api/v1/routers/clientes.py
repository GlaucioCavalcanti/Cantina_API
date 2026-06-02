from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....models.cliente import Cliente
from ....schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from .. import deps
from ....models.usuarios import Usuario

router = APIRouter()


@router.get("/", response_model=list[ClienteRead], status_code=status.HTTP_200_OK)
def listar_clientes(db: Session = Depends(get_db), current_user: Usuario = Depends(deps.get_current_user)) -> list[Cliente]:
    return db.query(Cliente).all()


@router.post("/", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def criar_cliente(
    cliente: ClienteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> Cliente:
    novo_cliente = Cliente(nome=cliente.nome, email=cliente.email)
    db.add(novo_cliente)
    try:
        db.commit()
        db.refresh(novo_cliente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema.",
        )
    return novo_cliente


@router.get("/{cliente_id}", response_model=ClienteRead, status_code=status.HTTP_200_OK)
def buscar_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )
    return cliente


@router.put("/{cliente_id}", response_model=ClienteRead, status_code=status.HTTP_200_OK)
def atualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    if cliente_update.nome is not None:
        cliente.nome = cliente_update.nome
    if cliente_update.email is not None:
        cliente.email = cliente_update.email

    try:
        db.commit()
        db.refresh(cliente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado no sistema.",
        )
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> None:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )
    db.delete(cliente)
    db.commit()
    return None
