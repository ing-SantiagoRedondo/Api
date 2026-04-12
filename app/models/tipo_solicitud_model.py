from pydantic import BaseModel

class Tipo_Solicitud(BaseModel):
    id_tipo_solicitud: int = None
    nombre_tipo: str
    descripcion: str