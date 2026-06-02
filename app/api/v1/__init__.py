from fastapi import APIRouter

from .routers.clientes import router as clientes_router
from .routers.produtos import router as produtos_router
from .routers.usuarios import router as usuarios_router
from .auth import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(usuarios_router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
api_router.include_router(produtos_router, prefix="/produtos", tags=["Produtos"])
