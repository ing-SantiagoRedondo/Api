from pydantic import BaseModel

class Programa(BaseModel):
    id_programa: int = None
    nombre_programa: str
    id_facultad: int