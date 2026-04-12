from fastapi import APIRouter, HTTPException
from controllers.programa_controller import *
from models.programa_model import Programa

router = APIRouter()

nuevo_programa = ProgramaController()


@router.post("/create_programa")
async def create_programa(programa: Programa):
    return nuevo_programa.create_programa(programa)


@router.get("/get_programa/{programa_id}", response_model=Programa)
async def get_programa(programa_id: int):
    return nuevo_programa.get_programa(programa_id)


@router.get("/get_programa/")
async def get_programas():
    return nuevo_programa.get_programas()


@router.put("/update_programa/{programa_id}")
async def update_programa(programa_id: int, programa: Programa):
    return nuevo_programa.update_programa(
        programa_id,
        programa.nombre_programa,
        programa.id_facultad
    )


@router.delete("/delete_programa/{programa_id}")
async def delete_programa(programa_id: int):
    return nuevo_programa.delete_programa(programa_id)