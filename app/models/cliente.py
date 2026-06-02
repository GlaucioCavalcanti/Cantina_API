from sqlalchemy import Column, Integer, String
from ..core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nome={self.nome}, email={self.email})>"
