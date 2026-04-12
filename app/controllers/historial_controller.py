import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.historial_model import Historial
from fastapi.encoders import jsonable_encoder


class Historial_Controller:
        
    def create_historial(self, historial: Historial):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO historial (id_solicitud, estado_anterior, estado_nuevo, fecha_cambio) VALUES (%s, %s, %s, %s)",
                (historial.id_solicitud, historial.estado_anterior, historial.estado_nuevo, historial.fecha_cambio)
            )

            conn.commit()
            conn.close()

            return {"resultado": "historial creado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()
        

    def get_historial(self, historial_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM historial WHERE id_historial = %s",
                (historial_id,)
            )

            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                'id_historial': int(result[0]),
                'id_solicitud': result[1],
                'estado_anterior': result[2],
                'estado_nuevo': result[3],
                'fecha_cambio': result[4]
            }

            payload.append(content)

            json_data = jsonable_encoder(content)

            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Historial not found")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()
       

    def get_historiales(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM historial")

            result = cursor.fetchall()
            payload = []
            content = {}

            for data in result:

                content = {
                    'id_historial': data[0],
                    'id_solicitud': data[1],
                    'estado_anterior': data[2],
                    'estado_nuevo': data[3],
                    'fecha_cambio': data[4]
                }

                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Historial not found")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_historial(self, historial_id: int, estado_anterior: str, estado_nuevo: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE historial SET estado_anterior=%s, estado_nuevo=%s WHERE id_historial=%s",
                (estado_anterior, estado_nuevo, historial_id)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Historial not found")

            return {"mensaje": f"Historial {historial_id} actualizado exitosamente"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()


    def delete_historial(self, historial_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM historial WHERE id_historial=%s",
                (historial_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Historial not found")

            return {"mensaje": f"Historial {historial_id} eliminado exitosamente"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()