from pydantic import BaseModel
from typing import Optional


class Facultad(BaseModel):
    id_facultad: int = None
    nombre_facultad: str