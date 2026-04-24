from fastapi import APIRouter, HTTPException
from controllers.solicitud_controller import *
from controllers.notificacion_controller import NotificacionController
from models.solicitud_model import Solicitud
from models.notificacion_model import Notificacion
from datetime import datetime
from typing import Optional
from fastapi import Query

router = APIRouter()

nuevo_solicitud = SolicitudController()
notificacion_ctrl = NotificacionController()


@router.post("/create_solicitud")
async def create_solicitud(solicitud: Solicitud):
    return nuevo_solicitud.create_solicitud(solicitud)

@router.get("/get_solicitud/{solicitud_id}", response_model=Solicitud)
async def get_solicitud(solicitud_id: int):
    return nuevo_solicitud.get_solicitud(solicitud_id)

@router.get("/get_solicitudes/")
async def get_solicitudes():
    return nuevo_solicitud.get_solicitudes()

@router.get("/get_reporte/")
async def get_reporte(
    id_tipo_solicitud: Optional[int] = Query(None),
    id_estado: Optional[int] = Query(None),
    id_programa: Optional[int] = Query(None)
):
    return nuevo_solicitud.get_reporte(id_tipo_solicitud, id_estado, id_programa)

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

    if solicitud.id_estado == 6:
        notificacion_ctrl.create_notificacion(Notificacion(
            id_usuario=solicitud.id_estudiante,
            mensaje=f"✅ Tu solicitud #{solicitud_id} ha sido APROBADA.",
            fecha_envio=datetime.now(),
            leida=False
        ))

    elif solicitud.id_estado == 7:
        notificacion_ctrl.create_notificacion(Notificacion(
            id_usuario=solicitud.id_estudiante,
            mensaje=f"❌ Tu solicitud #{solicitud_id} ha sido RECHAZADA.",
            fecha_envio=datetime.now(),
            leida=False
        ))

    return rpta

@router.delete("/delete_solicitud/{solicitud_id}")
async def delete_solicitud(solicitud_id: int):
    return nuevo_solicitud.delete_solicitud(solicitud_id)