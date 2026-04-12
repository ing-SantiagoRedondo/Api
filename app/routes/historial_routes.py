from fastapi import APIRouter, HTTPException
from controllers.historial_controller import *
from models.historial_model import Historial

router = APIRouter()

nuevo_historial = Historial_Controller()


@router.post("/create_historial")
async def create_historial(historial_data: Historial):
    rpta = nuevo_historial.create_historial(historial_data)
    return rpta


@router.get("/get_historial/{historial_id}", response_model=Historial)
async def get_historial(historial_id: int):
    rpta = nuevo_historial.get_historial(historial_id)
    return rpta


@router.get("/get_historiales/")
async def get_historiales():
    rpta = nuevo_historial.get_historiales()
    return rpta


@router.put("/update_historial/{historial_id}")
async def update_historial(historial_id: int, historial_data: Historial):
    rpta = nuevo_historial.update_historial(
        historial_id=historial_id,
        estado_anterior=historial_data.estado_anterior,
        estado_nuevo=historial_data.estado_nuevo
    )
    return rpta


@router.delete("/delete_historial/{historial_id}")
async def delete_historial(historial_id: int):
    rpta = nuevo_historial.delete_historial(historial_id)
    return rpta