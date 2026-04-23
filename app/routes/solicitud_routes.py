from fastapi import APIRouter, HTTPException
from controllers.solicitud_controller import *
from controllers.estudiante_controller import EstudianteController
from controllers.usuario_controller import UsuarioController
from models.solicitud_model import Solicitud
from config.email_config import enviar_correo

router = APIRouter()

nuevo_solicitud = SolicitudController()
estudiante_ctrl = EstudianteController()
usuario_ctrl = UsuarioController()


@router.post("/create_solicitud")
async def create_solicitud(solicitud: Solicitud):
    rpta = nuevo_solicitud.create_solicitud(solicitud)
    return rpta


@router.get("/get_solicitud/{solicitud_id}", response_model=Solicitud)
async def get_solicitud(solicitud_id: int):
    rpta = nuevo_solicitud.get_solicitud(solicitud_id)
    return rpta


@router.get("/get_solicitudes/")
async def get_solicitudes():
    rpta = nuevo_solicitud.get_solicitudes()
    return rpta


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

    if solicitud.id_estado in [6, 7]:
        try:
            estudiante = estudiante_ctrl.get_estudiante(solicitud.id_estudiante)
            usuario = usuario_ctrl.get_usuario(estudiante["id_usuario"])
            correo_estudiante = usuario["correo"]
            nombre_estudiante = usuario["nombre"]

            if solicitud.id_estado == 6:
                await enviar_correo(
                    destinatario=correo_estudiante,
                    asunto="✅ Solicitud Aprobada",
                    cuerpo=f"""
                    <div style="font-family:Arial; padding:20px; color:#333;">
                        <h2 style="color:#002E59;">Sistema de Solicitudes Académicas</h2>
                        <p>Hola <strong>{nombre_estudiante}</strong>,</p>
                        <p>Tu solicitud <strong>#{solicitud_id}</strong> ha sido <strong style="color:green;">APROBADA</strong>.</p>
                        <p>Ingresa al sistema para ver los detalles.</p>
                        <hr>
                        <small>Este es un correo automático, no responder.</small>
                    </div>
                    """
                )

            elif solicitud.id_estado == 7:
                await enviar_correo(
                    destinatario=correo_estudiante,
                    asunto="❌ Solicitud Rechazada",
                    cuerpo=f"""
                    <div style="font-family:Arial; padding:20px; color:#333;">
                        <h2 style="color:#002E59;">Sistema de Solicitudes Académicas</h2>
                        <p>Hola <strong>{nombre_estudiante}</strong>,</p>
                        <p>Tu solicitud <strong>#{solicitud_id}</strong> ha sido <strong style="color:red;">RECHAZADA</strong>.</p>
                        <p>Ingresa al sistema para ver los detalles o generar una nueva solicitud.</p>
                        <hr>
                        <small>Este es un correo automático, no responder.</small>
                    </div>
                    """
                )

        except Exception as e:
            print(f"Error enviando correo: {e}")

    return rpta


@router.delete("/delete_solicitud/{solicitud_id}")
async def delete_solicitud(solicitud_id: int):
    rpta = nuevo_solicitud.delete_solicitud(solicitud_id)
    return rpta