import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.programa_model import Programa
from fastapi.encoders import jsonable_encoder


class ProgramaController:

    def create_programa(self, programa: Programa):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO programa (nombre_programa, id_facultad) VALUES (%s, %s)",
                (programa.nombre_programa, programa.id_facultad)
            )

            conn.commit()
            return {"resultado": "programa creado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear programa")

        finally:
            conn.close()


    def get_programa(self, programa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM programa WHERE id_programa = %s",
                (programa_id,)
            )

            result = cursor.fetchone()

            if result:
                content = {
                    "id_programa": result[0],
                    "nombre_programa": result[1],
                    "id_facultad": result[2]
                }

                return jsonable_encoder(content)

            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado")

        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()


    def get_programas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM programa")
            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_programa": data[0],
                    "nombre_programa": data[1],
                    "id_facultad": data[2]
                }

                payload.append(content)

            return {"resultado": jsonable_encoder(payload)}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()


    def update_programa(self, programa_id: int, nombre_programa: str, id_facultad: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE programa SET nombre_programa=%s, id_facultad=%s WHERE id_programa=%s",
                (nombre_programa, id_facultad, programa_id)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Programa no encontrado")

            return {"mensaje": f"Programa {programa_id} actualizado exitosamente"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()


    def delete_programa(self, programa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM programa WHERE id_programa=%s",
                (programa_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Programa no encontrado")

            return {"mensaje": f"Programa {programa_id} eliminado exitosamente"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            conn.close()