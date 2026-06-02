from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....models.produto import Produto
from ....schemas.produto import ProdutoCreate, ProdutoRead, ProdutoUpdate
from .. import deps
from ....models.usuarios import Usuario

router = APIRouter()


@router.get("/", response_model=list[ProdutoRead], status_code=status.HTTP_200_OK)
def listar_produtos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> list[Produto]:
    return db.query(Produto).all()


@router.post("/", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> Produto:
    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@router.get("/{produto_id}", response_model=ProdutoRead, status_code=status.HTTP_200_OK)
def buscar_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> Produto:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )
    return produto


@router.put("/{produto_id}", response_model=ProdutoRead, status_code=status.HTTP_200_OK)
def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
) -> Produto:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    if produto_update.nome is not None:
        produto.nome = produto_update.nome
    if produto_update.descricao is not None:
        produto.descricao = produto_update.descricao
    if produto_update.preco is not None:
        produto.preco = produto_update.preco

    db.commit()
    db.refresh(produto)
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.check_admin) # Apenas Admin agora
) -> None:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )
    db.delete(produto)
    db.commit()
    return None
