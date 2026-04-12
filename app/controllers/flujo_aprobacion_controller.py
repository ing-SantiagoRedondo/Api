import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.flujo_aprobacion_model import FlujoAprobacion
from fastapi.encoders import jsonable_encoder


class FlujoAprobacionController:

    def create_flujo_aprobacion(self, flujo_aprobacion: FlujoAprobacion):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO flujo_aprobacion
                (id_tipo_solicitud, orden_etapa, id_rol_responsable, nombre_etapa)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    flujo_aprobacion.id_tipo_solicitud,
                    flujo_aprobacion.orden_etapa,
                    flujo_aprobacion.id_rol_responsable,
                    flujo_aprobacion.nombre_etapa
                )
            )

            conn.commit()
            cursor.close()

            return {"mensaje": "Flujo de aprobación creado correctamente"}

        except psycopg2.Error as err:
            print(err)
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail="Error en la base de datos")

        finally:
            if conn:
                conn.close()


    def get_flujo_aprobacion(self, flujo_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM flujo_aprobacion WHERE id_flujo = %s",
                (flujo_id,)
            )

            result = cursor.fetchone()

            if result:

                content = {
                    "id_flujo": result[0],
                    "id_tipo_solicitud": result[1],
                    "orden_etapa": result[2],
                    "id_rol_responsable": result[3],
                    "nombre_etapa": result[4]
                }

                return jsonable_encoder(content)

            else:
                raise HTTPException(status_code=404, detail="Flujo de aprobación no encontrado")

        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error en la base de datos")

        finally:
            if conn:
                conn.close()


    def get_flujos_aprobacion(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM flujo_aprobacion")

            result = cursor.fetchall()
            payload = []

            for data in result:

                content = {
                    "id_flujo": data[0],
                    "id_tipo_solicitud": data[1],
                    "orden_etapa": data[2],
                    "id_rol_responsable": data[3],
                    "nombre_etapa": data[4]
                }

                payload.append(content)

            return {"resultado": jsonable_encoder(payload)}

        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error en la base de datos")

        finally:
            if conn:
                conn.close()


    def update_flujo_aprobacion(self, flujo_id: int, id_tipo_solicitud: int, orden_etapa: int, id_rol_responsable: int, nombre_etapa: str):

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE flujo_aprobacion
                SET id_tipo_solicitud=%s,
                    orden_etapa=%s,
                    id_rol_responsable=%s,
                    nombre_etapa=%s
                WHERE id_flujo=%s
                """,
                (id_tipo_solicitud, orden_etapa, id_rol_responsable, nombre_etapa, flujo_id)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Flujo de aprobación no encontrado")

            cursor.close()

            return {"mensaje": f"Flujo de aprobación {flujo_id} actualizado correctamente"}

        except psycopg2.Error as err:
            print(err)
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail="Error en la base de datos")

        finally:
            if conn:
                conn.close()


    def delete_flujo_aprobacion(self, flujo_id: int):

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM flujo_aprobacion WHERE id_flujo = %s",
                (flujo_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Flujo de aprobación no encontrado")

            cursor.close()

            return {"mensaje": f"Flujo de aprobación {flujo_id} eliminado correctamente"}

        except psycopg2.Error as err:
            print(err)
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail="Error en la base de datos")

        finally:
            if conn:
                conn.close()