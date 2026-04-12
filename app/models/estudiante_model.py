from pydantic import BaseModel

class Estudiante(BaseModel):
    id_estudiante: int = None
    id_usuario: int
    codigo_estudiantil: str
    semestre: int
    estado_academico: str
    tipo_documento: str
    numero_documento: int
    id_programa: int