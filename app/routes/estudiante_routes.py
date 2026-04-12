from fastapi import APIRouter, HTTPException
from controllers.estudiante_controller import *
from models.estudiante_model import Estudiante

router = APIRouter()

nuevo_estudiante = EstudianteController()


@router.post("/create_estudiante")
async def create_estudiante(estudiante: Estudiante):
    rpta = nuevo_estudiante.create_estudiante(estudiante)
    return rpta


@router.get("/get_estudiante/{estudiante_id}", response_model=Estudiante)
async def get_estudiante(estudiante_id: int):
    rpta = nuevo_estudiante.get_estudiante(estudiante_id)
    return rpta


@router.get("/get_estudiantes/")
async def get_estudiantes():
    rpta = nuevo_estudiante.get_estudiantes()
    return rpta


@router.put("/update_estudiante/{estudiante_id}")
async def update_estudiante(estudiante_id: int, estudiante: Estudiante):
    rpta = nuevo_estudiante.update_estudiante(
        estudiante_id=estudiante_id,
        id_usuario=estudiante.id_usuario,
        codigo_estudiantil=estudiante.codigo_estudiantil,
        semestre=estudiante.semestre,
        estado_academico=estudiante.estado_academico,
        tipo_documento=estudiante.tipo_documento,
        numero_documento=estudiante.numero_documento,
        id_programa=estudiante.id_programa
    )
    return rpta


@router.delete("/delete_estudiante/{estudiante_id}")
async def delete_estudiante(estudiante_id: int):
    rpta = nuevo_estudiante.delete_estudiante(estudiante_id)
    return rpta