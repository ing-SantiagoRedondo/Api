import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.solicitud_model import Solicitud
from fastapi.encoders import jsonable_encoder
from typing import Optional
from datetime import date

class SolicitudController:

    def create_solicitud(self, solicitud: Solicitud):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_creacion = solicitud.fecha_creacion or date.today()
            cursor.execute("INSERT INTO solicitud (id_estudiante, id_tipo_solicitud, fecha_creacion, descripcion, id_estado) VALUES (%s, %s, %s, %s, %s)", (solicitud.id_estudiante, solicitud.id_tipo_solicitud, fecha_creacion, solicitud.descripcion, solicitud.id_estado,))
            conn.commit()
            return {"resultado": "Solicitud creada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_solicitud(self, solicitud_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM solicitud WHERE id_solicitud = %s", (solicitud_id,))
            result = cursor.fetchone()
            content = {
                'id_solicitud': int(result[0]),
                'id_estudiante': int(result[1]),
                'id_tipo_solicitud': int(result[2]),
                'fecha_creacion': result[3],
                'descripcion': result[4],
                'id_estado': result[5],
            }
            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Solicitud not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_solicitudes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM solicitud")
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id_solicitud': data[0],
                    'id_estudiante': data[1],
                    'id_tipo_solicitud': data[2],
                    'fecha_creacion': data[3],
                    'descripcion': data[4],
                    'id_estado': data[5]
                })
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="solicitud not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_reporte(self, id_tipo_solicitud, id_estado, id_programa):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    s.id_solicitud,
                    u.nombre AS estudiante,
                    p.nombre_programa AS programa,
                    f.nombre_facultad AS facultad,
                    ts.nombre_tipo AS tipo_solicitud,
                    e.nombre_estado AS estado,
                    s.fecha_creacion
                FROM solicitud s
                JOIN estudiante est ON s.id_estudiante = est.id_estudiante
                JOIN usuario u ON est.id_usuario = u.id_usuario
                JOIN programa p ON est.id_programa = p.id_programa
                JOIN facultad f ON p.id_facultad = f.id_facultad
                JOIN tipo_solicitud ts ON s.id_tipo_solicitud = ts.id_tipo_solicitud
                JOIN estado e ON s.id_estado = e.id_estado
                WHERE 1=1
            """

            params = []

            if id_tipo_solicitud:
                query += " AND s.id_tipo_solicitud = %s"
                params.append(id_tipo_solicitud)

            if id_estado:
                query += " AND s.id_estado = %s"
                params.append(id_estado)

            if id_programa:
                query += " AND est.id_programa = %s"
                params.append(id_programa)

            query += " ORDER BY s.fecha_creacion DESC"

            cursor.execute(query, params)
            result = cursor.fetchall()

            payload = []
            for data in result:
                payload.append({
                    'id_solicitud': data[0],
                    'estudiante': data[1],
                    'programa': data[2],
                    'facultad': data[3],
                    'tipo_solicitud': data[4],
                    'estado': data[5],
                    'fecha_creacion': str(data[6])
                })

            return {"resultado": jsonable_encoder(payload)}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_solicitud(self, solicitud_id: int, estudiante_id: int, tipo_solicitud_id: int, fecha_creacion: Optional[date], descripcion: str, id_estado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE solicitud SET id_estudiante=%s, id_tipo_solicitud=%s, fecha_creacion=%s, descripcion=%s, id_estado=%s WHERE id_solicitud=%s",
                       (estudiante_id, tipo_solicitud_id, fecha_creacion, descripcion, id_estado, solicitud_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="solicitud not found")
            return {"mensaje": f"solicitud {solicitud_id} actualizada exitosamente"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_solicitud(self, solicitud_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM solicitud WHERE id_solicitud=%s", (solicitud_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="solicitud not found")
            return {"mensaje": f"solicitud {solicitud_id} eliminado exitosamente"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()