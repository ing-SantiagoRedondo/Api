from pydantic import BaseModel

class Rol(BaseModel):
    id_rol: int = None
    nombre_rol: str
    descripcion: str