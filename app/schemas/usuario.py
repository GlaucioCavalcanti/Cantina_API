from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr
    nome_completo: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id: int

    class Config:
        from_attributes = True