from fastapi import APIRouter, HTTPException
from controllers.flujo_aprobacion_controller import *
from models.flujo_aprobacion_model import FlujoAprobacion

router = APIRouter()

nuevo_flujo_aprobacion = FlujoAprobacionController()


@router.post("/create_flujo_aprobacion")
async def create_flujo_aprobacion(flujo: FlujoAprobacion):
    rpta = nuevo_flujo_aprobacion.create_flujo_aprobacion(flujo)
    return rpta


@router.get("/get_flujo_aprobacion/{flujo_id}", response_model=FlujoAprobacion)
async def get_flujo_aprobacion(flujo_id: int):
    rpta = nuevo_flujo_aprobacion.get_flujo_aprobacion(flujo_id)
    return rpta


@router.get("/get_flujos_aprobacion/")
async def get_flujos_aprobacion():
    rpta = nuevo_flujo_aprobacion.get_flujos_aprobacion()
    return rpta


@router.put("/update_flujo_aprobacion/{flujo_id}")
async def update_flujo_aprobacion(flujo_id: int, flujo: FlujoAprobacion):
    rpta = nuevo_flujo_aprobacion.update_flujo_aprobacion(
        flujo_id=flujo_id,
        id_tipo_solicitud=flujo.id_tipo_solicitud,
        orden_etapa=flujo.orden_etapa,
        id_rol_responsable=flujo.id_rol_responsable,
        nombre_etapa=flujo.nombre_etapa
    )
    return rpta


@router.delete("/delete_flujo_aprobacion/{flujo_id}")
async def delete_flujo_aprobacion(flujo_id: int):
    rpta = nuevo_flujo_aprobacion.delete_flujo_aprobacion(flujo_id)
    return rpta