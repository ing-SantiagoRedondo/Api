from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Historial(BaseModel):
    id_solicitud: int
    estado_anterior: Optional[str] = None
    estado_nuevo: str
    fecha_cambio: datetime