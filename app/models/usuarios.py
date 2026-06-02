from sqlalchemy import Column, Integer, String, Boolean
from ..core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nome_completo = Column(String)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)