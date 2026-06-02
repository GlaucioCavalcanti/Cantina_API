"""Pacote de schemas Pydantic para a Cantina API."""

from .cliente import ClienteCreate, ClienteRead, ClienteUpdate
from .produto import ProdutoCreate, ProdutoRead, ProdutoUpdate

__all__ = [
    "ClienteCreate",
    "ClienteRead",
    "ClienteUpdate",
    "ProdutoCreate",
    "ProdutoRead",
    "ProdutoUpdate",
]
