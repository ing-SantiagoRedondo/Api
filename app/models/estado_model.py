from pydantic import BaseModel
from typing import Optional


class Estado(BaseModel):
    id_estado: int = None
    nombre_estado: str
    descripcion: str