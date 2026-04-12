from fastapi import APIRouter, HTTPException
from controllers.aprobacion_controller import *
from models.aprobacion_model import Aprobacion

router = APIRouter()

nuevo_aprobacion = AprobacionController()


@router.post("/create_aprobacion")
async def create_aprobacion(aprobacion: Aprobacion):
    rpta = nuevo_aprobacion.create_aprobacion(aprobacion)
    return rpta


@router.get("/get_aprobacion/{aprobacion_id}", response_model=Aprobacion)
async def get_aprobacion(aprobacion_id: int):
    rpta = nuevo_aprobacion.get_aprobacion(aprobacion_id)
    return rpta


@router.get("/get_aprobaciones/")
async def get_aprobaciones():
    rpta = nuevo_aprobacion.get_aprobaciones()
    return rpta


@router.put("/update_aprobacion/{aprobacion_id}")
async def update_aprobacion(aprobacion_id: int, aprobacion: Aprobacion):
    rpta = nuevo_aprobacion.update_aprobacion(
        aprobacion_id=aprobacion_id,
        id_solicitud=aprobacion.id_solicitud,
        id_usuario=aprobacion.id_usuario,
        comentario=aprobacion.comentario,
        fecha=aprobacion.fecha,
        id_estado=aprobacion.id_estado
    )
    return rpta


@router.delete("/delete_aprobacion/{aprobacion_id}")
async def delete_aprobacion(aprobacion_id: int):
    rpta = nuevo_aprobacion.delete_aprobacion(aprobacion_id)
    return rpta