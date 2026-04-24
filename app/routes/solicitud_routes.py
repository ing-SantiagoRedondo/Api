from fastapi import APIRouter, HTTPException, Query
from controllers.solicitud_controller import *
from models.solicitud_model import Solicitud
from typing import Optional

router = APIRouter()

nuevo_solicitud = SolicitudController()


@router.post("/create_solicitud")
async def create_solicitud(solicitud: Solicitud):
    rpta = nuevo_solicitud.create_solicitud(solicitud)
    return rpta


@router.get("/get_solicitud/{solicitud_id}", response_model=Solicitud)
async def get_solicitud(solicitud_id: int):
    rpta = nuevo_solicitud.get_solicitud(solicitud_id)
    return rpta


@router.get("/get_solicitudes/")
async def get_solicitudes():
    rpta = nuevo_solicitud.get_solicitudes()
    return rpta


@router.get("/get_reporte/")
async def get_reporte(
    id_tipo_solicitud: Optional[int] = Query(None),
    id_estado: Optional[int] = Query(None),
    id_programa: Optional[int] = Query(None)
):
    rpta = nuevo_solicitud.get_reporte(id_tipo_solicitud, id_estado, id_programa)
    return rpta


@router.put("/update_solicitud/{solicitud_id}")
async def update_solicitud(solicitud_id: int, solicitud: Solicitud):
    rpta = nuevo_solicitud.update_solicitud(
        solicitud_id=solicitud_id,
        estudiante_id=solicitud.id_estudiante,
        tipo_solicitud_id=solicitud.id_tipo_solicitud,
        fecha_creacion=solicitud.fecha_creacion,
        descripcion=solicitud.descripcion,
        id_estado=solicitud.id_estado
    )
    return rpta


@router.delete("/delete_solicitud/{solicitud_id}")
async def delete_solicitud(solicitud_id: int):
    rpta = nuevo_solicitud.delete_solicitud(solicitud_id)
    return rpta