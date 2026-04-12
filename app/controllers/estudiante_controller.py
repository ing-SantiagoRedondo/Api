import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.estudiante_model import Estudiante
from fastapi.encoders import jsonable_encoder

class EstudianteController:
        
    def create_estudiante(self, estudiante: Estudiante):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO estudiante (id_usuario, codigo_estudiantil, semestre, estado_academico, tipo_documento, numero_documento, id_programa) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    estudiante.id_usuario,
                    estudiante.codigo_estudiantil,
                    estudiante.semestre,
                    estudiante.estado_academico,
                    estudiante.tipo_documento,
                    estudiante.numero_documento,
                    estudiante.id_programa
                )
            )
            conn.commit()
            conn.close()
            return {"resultado": "Estudiante creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
        

    def get_estudiante(self, estudiante_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiante WHERE id_estudiante = %s", (estudiante_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content={
                'id_estudiante': int(result[0]),
                'id_usuario': int(result[1]),
                'codigo_estudiantil': result[2],
                'semestre': result[3],
                'estado_academico': result[4],
                'tipo_documento': result[5],
                'numero_documento': int(result[6]),
                'id_programa': int(result[7])
            }

            payload.append(content)
            json_data = jsonable_encoder(content)

            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Estudiante not found")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()


    def get_estudiantes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiante")
            result = cursor.fetchall()
            payload = []
            content = {}

            for data in result:
                content={
                    'id_estudiante': data[0],
                    'id_usuario': data[1],
                    'codigo_estudiantil': data[2],
                    'semestre': data[3],
                    'estado_academico': data[4],
                    'tipo_documento': data[5],
                    'numero_documento': data[6],
                    'id_programa': data[7]
                }

                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Estudiante not found")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()


    def update_estudiante(self, estudiante_id: int, id_usuario: int, codigo_estudiantil: str, semestre: int, estado_academico: str, tipo_documento: str, numero_documento: int, id_programa: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE estudiante SET id_usuario=%s, codigo_estudiantil=%s, semestre=%s, estado_academico=%s, tipo_documento=%s, numero_documento=%s, id_programa=%s WHERE id_estudiante=%s",
                (
                    id_usuario,
                    codigo_estudiantil,
                    semestre,
                    estado_academico,
                    tipo_documento,
                    numero_documento,
                    id_programa,
                    estudiante_id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estudiante not found")

            return {"mensaje": f"Estudiante {estudiante_id} actualizado exitosamente"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()


    def delete_estudiante(self, estudiante_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estudiante WHERE id_estudiante=%s", (estudiante_id,))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estudiante not found")

            return {"mensaje": f"Estudiante {estudiante_id} eliminado exitosamente"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()