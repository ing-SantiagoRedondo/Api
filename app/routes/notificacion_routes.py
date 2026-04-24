from fastapi import APIRouter, HTTPException
from controllers.notificacion_controller import *
from models.notificacion_model import Notificacion

router = APIRouter()

nueva_notificacion = NotificacionController()


@router.post("/create_notificacion")
async def create_notificacion(notificacion: Notificacion):
    return nueva_notificacion.create_notificacion(notificacion)

@router.get("/get_notificacion/{notificacion_id}", response_model=Notificacion)
async def get_notificacion(notificacion_id: int):
    return nueva_notificacion.get_notificacion(notificacion_id)

@router.get("/get_notificaciones/")
async def get_notificaciones():
    return nueva_notificacion.get_notificaciones()

@router.get("/get_notificaciones_usuario/{usuario_id}")
async def get_notificaciones_usuario(usuario_id: int):
    return nueva_notificacion.get_notificaciones_usuario(usuario_id)

@router.put("/marcar_leida/{notificacion_id}")
async def marcar_leida(notificacion_id: int):
    return nueva_notificacion.marcar_leida(notificacion_id)

@router.put("/update_notificacion/{notificacion_id}")
async def update_notificacion(notificacion_id: int, notificacion: Notificacion):
    return nueva_notificacion.update_notificacion(
        notificacion_id=notificacion_id,
        mensaje=notificacion.mensaje,
        leida=notificacion.leida,
    )

@router.delete("/delete_notificacion/{notificacion_id}")
async def delete_notificacion(notificacion_id: int):
    return nueva_notificacion.delete_notificacion(notificacion_id)