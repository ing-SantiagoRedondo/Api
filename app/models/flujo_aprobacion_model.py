from pydantic import BaseModel
from typing import Optional


class FlujoAprobacion(BaseModel):
    id_flujo: int = None
    id_tipo_solicitud: int
    orden_etapa: int
    id_rol_responsable: int
    nombre_etapa: str