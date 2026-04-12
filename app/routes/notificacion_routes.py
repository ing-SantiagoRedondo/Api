from fastapi import APIRouter, HTTPException
from controllers.notificacion_controller import *
from models.notificacion_model import Notificacion

router = APIRouter()

nueva_notificacion = NotificacionController()


@router.post("/create_notificacion")
async def create_notificacion(notificacion: Notificacion):
    rpta = nueva_notificacion.create_notificacion(notificacion)
    return rpta


@router.get("/get_notificacion/{notificacion_id}", response_model=Notificacion)
async def get_notificacion(notificacion_id: int):
    rpta = nueva_notificacion.get_notificacion(notificacion_id)
    return rpta


@router.get("/get_notificaciones/")
async def get_notificaciones():
    rpta = nueva_notificacion.get_notificaciones()
    return rpta


@router.put("/update_notificacion/{notificacion_id}")
async def update_notificacion(notificacion_id: int, notificacion: Notificacion):
    rpta = nueva_notificacion.update_notificacion(
        notificacion_id=notificacion_id,
        mensaje=notificacion.mensaje,
        leida=notificacion.leida,
    )
    return rpta


@router.delete("/delete_notificacion/{notificacion_id}")
async def delete_notificacion(notificacion_id: int):
    rpta = nueva_notificacion.delete_notificacion(notificacion_id)
    return rpta