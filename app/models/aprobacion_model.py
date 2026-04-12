from pydantic import BaseModel
from datetime import datetime

class Aprobacion(BaseModel):
    id_aprobacion: int = None
    id_solicitud: int
    id_usuario: int
    comentario: str
    fecha: datetime
    id_estado: int