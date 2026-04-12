from fastapi import APIRouter, HTTPException
from controllers.estado_controller import *
from models.estado_model import Estado

router = APIRouter()

nuevo_estado = EstadoController()


@router.post("/create_estado")
async def create_rol(estado: Estado):
    rpta = nuevo_estado.create_estado(estado)
    return rpta


@router.get("/get_estado/{estado_id}",response_model=Estado)
async def get_estado(estado_id: int):
    rpta = nuevo_estado.get_estado(estado_id)
    return rpta

@router.get("/get_estados/")
async def get_estados():
    rpta = nuevo_estado.get_estados()
    return rpta

@router.put("/update_estado/{estado_id}")
async def update_estado(estado_id: int, estado: Estado):
    rpta = nuevo_estado.update_estado(
        estado_id=estado_id,
        nombre_estado=estado.nombre_estado,
        descripcion=estado.descripcion

    )
    return rpta

@router.delete("/delete_estado/{estado_id}")
async def delete_estado(estado_id: int):
    rpta = nuevo_estado.delete_estado(estado_id)
    return rpta