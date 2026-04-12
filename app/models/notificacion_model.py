from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Notificacion(BaseModel):
    id_usuario: int
    mensaje: str
    fecha_envio: datetime
    leida: Optional[bool] = False