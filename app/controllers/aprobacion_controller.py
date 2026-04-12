import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.aprobacion_model import Aprobacion
from fastapi.encoders import jsonable_encoder

class AprobacionController:
        
    def create_aprobacion(self, aprobacion: Aprobacion):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO aprobacion (id_solicitud, id_usuario, comentario, fecha, id_estado) VALUES (%s, %s, %s, %s, %s )", (aprobacion.id_solicitud, aprobacion.id_usuario, aprobacion.comentario, aprobacion.fecha,aprobacion.id_estado))
            conn.commit()
            conn.close()
            return {"resultado": "Aprobacion creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
        

    def get_aprobacion(self, aprobacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM aprobacion WHERE id_aprobacion = %s", (aprobacion_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_aprobacion':int(result[0]),
                    'id_solicitud':int (result[1]),
                    'id_usuario' :int (result[2]),
                    'comentario': result[3],
                    'fecha': result[4],
                    'id_estado' :int (result[5])
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
       
    def get_aprobaciones(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM aprobacion")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_aprobacion':data[0],
                    'id_solicitud':data[1],
                    'id_usuario':data[2],
                    'comentario':data[3],
                    'fecha' :data [4],
                    'id_estado' : data [5]

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_aprobacion(self, aprobacion_id: int, id_solicitud: int, id_usuario: int, comentario: str, fecha: str, id_estado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE aprobacion SET id_solicitud=%s, id_usuario=%s, comentario=%s, fecha=%s, id_estado=%s WHERE id_aprobacion=%s",
                       (id_solicitud, id_usuario, comentario, fecha, id_estado, aprobacion_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Aprobacion not found")
        
            return {"mensaje": f"Aprobacion {aprobacion_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_aprobacion(self, aprobacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM aprobacion WHERE id_aprobacion=%s", (aprobacion_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Aprobacion not found")
        
            return {"mensaje": f"Aprobacion {aprobacion_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()