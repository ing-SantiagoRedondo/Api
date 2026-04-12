from pydantic import BaseModel
from datetime import datetime

class DocumentoGenerado(BaseModel):
    id_documento: int = None
    id_solicitud: int
    nombre_documento: str
    fecha_generacion: datetime
