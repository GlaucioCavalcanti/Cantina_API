from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Em desenvolvimento, init_db() cria as tabelas se não existirem.
    # Em produção, prefira rodar 'alembic upgrade head' antes de iniciar.
    if settings.ENVIRONMENT != "production":
        init_db()
    yield


app = FastAPI(
    title="Cantina Interativa API",
    description=("Serviço REST modular para gerenciar clientes e produtos.\n\n"
        "**Links do Projeto:**\n"
        "* 🖥️ [Meu GitHub](https://github.com/GlaucioCavalcanti)\n"
        "* 📄 [Meu Portfólio](https://portfolioglauciocavalcanti.vercel.app/)"
    ),
    version="0.1.0",
    lifespan=lifespan,
    contact={
        "name": "Glaucio Luiz Cavalcanti",
        "url": "https://wa.me/81987989303",  # Adicionado https://
        "email": "glaucio_de_libra@hotmail.com",
    },
)

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]
if not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"], summary="Verificar saúde da API")
def health_check() -> dict:
    return {"status": "ok", "message": "Cantina API está rodando"}


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "cantina_api.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["cantina_api"],
    )
