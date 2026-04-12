from fastapi import FastAPI
from routes.usuario_routes import router as usuario_router
from routes.tipo_solicitud_routes import router as tipo_solicitud_router
from routes.solicitud_routes import router as solicitud_router
from routes.historial_routes import router as historial_router
from routes.notificacion_routes import router as notificacion_router
from routes.flujo_aprobacion_routes import router as flujo_aprobacion_router
from routes.rol_routes import router as rol_router
from routes.estado_routes import router as estado_router
from routes.facultad_routes import router as facultad_router
from routes.programa_routes import router as programa_router
from routes.aprobacion_routes import router as aprobacion_router
from routes.documento_generado_routes import router as documento_generado_router
from routes.estudiante_routes import router as estudiante_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}

app.include_router(usuario_router)
app.include_router(tipo_solicitud_router)
app.include_router(solicitud_router)
app.include_router(historial_router)
app.include_router(notificacion_router)
app.include_router(flujo_aprobacion_router)
app.include_router(rol_router)
app.include_router(estado_router)
app.include_router(facultad_router)
app.include_router(programa_router)
app.include_router(aprobacion_router)
app.include_router(documento_generado_router)
app.include_router(estudiante_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)