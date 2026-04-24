import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.notificacion_model import Notificacion
from fastapi.encoders import jsonable_encoder


class NotificacionController:
        
    def create_notificacion(self, notificacion: Notificacion):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO notificacion (id_usuario, mensaje, fecha_envio, leida) VALUES (%s, %s, %s, %s)",
                (
                    notificacion.id_usuario,
                    notificacion.mensaje,
                    notificacion.fecha_envio,
                    notificacion.leida
                )
            )

            conn.commit()
            return {"resultado": "Notificacion creada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()
        

    def get_notificacion(self, notificacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM notificacion WHERE id_notificacion = %s",
                (notificacion_id,)
            )

            result = cursor.fetchone()

            if result:
                content = {
                    'id_notificacion': result[0],
                    'id_usuario': result[1],
                    'mensaje': result[2],
                    'fecha_envio': result[3],
                    'leida': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Notificacion not found")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()
       

    def get_notificaciones(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM notificacion")

            result = cursor.fetchall()
            payload = []

            for data in result:
                content = {
                    'id_notificacion': data[0],
                    'id_usuario': data[1],
                    'mensaje': data[2],
                    'fecha_envio': data[3],
                    'leida': data[4]
                }
                payload.append(content)

            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="Notificacion not found")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_notificaciones_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM notificacion WHERE id_usuario = %s ORDER BY fecha_envio DESC",
                (usuario_id,)
            )

            result = cursor.fetchall()
            payload = []

            for data in result:
                payload.append({
                    'id_notificacion': data[0],
                    'id_usuario': data[1],
                    'mensaje': data[2],
                    'fecha_envio': data[3],
                    'leida': data[4]
                })

            return {"resultado": jsonable_encoder(payload)}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def marcar_leida(self, notificacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE notificacion SET leida=TRUE WHERE id_notificacion=%s",
                (notificacion_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Notificacion not found")

            return {"mensaje": "Notificacion marcada como leida"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()


    def update_notificacion(self, notificacion_id: int, mensaje: str, leida: bool):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE notificacion SET mensaje=%s, leida=%s WHERE id_notificacion=%s",
                (mensaje, leida, notificacion_id)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Notificacion not found")

            return {"mensaje": f"Notificacion {notificacion_id} actualizada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()


    def delete_notificacion(self, notificacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM notificacion WHERE id_notificacion=%s",
                (notificacion_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Notificacion not found")

            return {"mensaje": f"Notificacion {notificacion_id} eliminada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()