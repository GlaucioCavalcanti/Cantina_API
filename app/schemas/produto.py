from pydantic import BaseModel
from typing import Optional


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None


class ProdutoRead(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float

    class Config:
        from_attributes = True
