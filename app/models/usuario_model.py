from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario: int = None
    nombre: str
    correo: str
    contraseña: str
    id_rol: int
    estado: str