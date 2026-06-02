from pydantic import BaseModel, EmailStr
from typing import Optional


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None


class ClienteRead(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True
