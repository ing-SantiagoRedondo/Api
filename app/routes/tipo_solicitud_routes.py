from fastapi import APIRouter, HTTPException
from controllers.tipo_solicitud_controller import *
from models.tipo_solicitud_model import Tipo_Solicitud

router = APIRouter()

nuevo_tipo_solicitud = Tipo_SolicitudController()


@router.post("/create_tipo_solicitud")
async def create_tipo_solicitud(tipo_solicitud: Tipo_Solicitud):
    rpta = nuevo_tipo_solicitud.create_tipo_solicitud(tipo_solicitud)
    return rpta


@router.get("/get_tipo_solicitud/{tipo_solicitud_id}",response_model=Tipo_Solicitud)
async def get_tipo_solicitud(tipo_solicitud_id: int):
    rpta = nuevo_tipo_solicitud.get_tipo_solicitud(tipo_solicitud_id)
    return rpta

@router.get("/get_tipos_solicitud/")
async def get_tipos_solicitud():
    rpta = nuevo_tipo_solicitud.get_tipos_solicitud()
    return rpta

@router.put("/update_tipo_solicitud/{tipo_solicitud_id}")
async def update_tipo_solicitud(tipo_solicitud_id: int, tipo_solicitud: Tipo_Solicitud):
    rpta = nuevo_tipo_solicitud.update_tipo_solicitud(
        tipo_solicitud_id=tipo_solicitud_id,
        nombre_tipo=tipo_solicitud.nombre_tipo,
        descripcion=tipo_solicitud.descripcion,
    )
    return rpta

@router.delete("/delete_tipo_solicitud/{tipo_solicitud_id}")
async def delete_tipo_solicitud(tipo_solicitud_id: int):
    rpta = nuevo_tipo_solicitud.delete_tipo_solicitud(tipo_solicitud_id)
    return rpta