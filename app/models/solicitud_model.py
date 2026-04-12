from pydantic import BaseModel
from typing import Optional
from datetime import date

class Solicitud(BaseModel):
    id_solicitud: int = None
    id_estudiante: int
    id_tipo_solicitud: int
    fecha_creacion: Optional[date] = None
    descripcion: str
    id_estado: int