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
            conn.close()
            return {"resultado": "Solicitud creada"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_solicitud(self, solicitud_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM solicitud WHERE id_solicitud = %s", (solicitud_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_solicitud':int(result[0]),
                    'id_estudiante':int(result[1]),
                    'id_tipo_solicitud':int(result[2]),
                    'fecha_creacion':result[3],
                    'descripcion':result[4],
                    'id_estado':result[5],


            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="Solicitud not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
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
            content = {} 
            for data in result:
                content={
                    'id_solicitud':data[0],
                    'id_estudiante':data[1],
                    'id_tipo_solicitud':data[2],
                    'fecha_creacion':data[3],
                    'descripcion':data[4],
                    'id_estado':data[5]

                }
                payload.append(content)
                content = {}
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

    def update_solicitud(self, solicitud_id: int, estudiante_id: int, tipo_solicitud_id:int ,fecha_creacion: Optional[date],  descripcion: str, id_estado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE solicitud SET id_estudiante=%s, id_tipo_solicitud=%s, fecha_creacion=%s,  descripcion=%s, id_estado=%s WHERE id_solicitud=%s",
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
       

##user_controller = UserController()