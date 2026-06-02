from sqlalchemy import Column, Float, Integer, String
from ..core.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(String(500), nullable=False)
    preco = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Produto(id={self.id}, nome={self.nome}, preco={self.preco})>"
