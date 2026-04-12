from fastapi import APIRouter, HTTPException
from controllers.documento_generado_controller import *
from models.documento_generado_model import DocumentoGenerado

router = APIRouter()

nuevo_documento_generado = DocumentoGeneradoController()


@router.post("/create_documento_generado")
async def create_documento_generado(documento_generado: DocumentoGenerado):
    rpta = nuevo_documento_generado.create_documento_generado(documento_generado)
    return rpta


@router.get("/get_documento_generado/{id_documento}",response_model=DocumentoGenerado)
async def get_documento_generado(id_documento: int):
    rpta = nuevo_documento_generado.get_documento_generado(id_documento)
    return rpta


@router.get("/get_documentos_generados/")
async def get_documentos_generados():
    rpta = nuevo_documento_generado.get_documentos_generados()
    return rpta


@router.put("/update_documento_generado/{id_documento}")
async def update_documento_generado(id_documento: int, documento_generado: DocumentoGenerado):
    rpta = nuevo_documento_generado.update_documento_generado(
        documento_generado_id=id_documento,
        id_solicitud=documento_generado.id_solicitud,
        nombre_documento=documento_generado.nombre_documento,
        fecha_generacion=documento_generado.fecha_generacion

    )
    return rpta


@router.delete("/delete_documento_generado/{id_documento}")
async def delete_documento_generado(id_documento: int):
    rpta = nuevo_documento_generado.delete_documento_generado(id_documento)
    return rpta