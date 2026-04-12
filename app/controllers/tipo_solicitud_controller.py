import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.tipo_solicitud_model import Tipo_Solicitud
from fastapi.encoders import jsonable_encoder

class Tipo_SolicitudController:
        
    def create_tipo_solicitud(self, tipo_solicitud: Tipo_Solicitud):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tipo_solicitud (nombre_tipo,descripcion) VALUES (%s, %s)", (tipo_solicitud.nombre_tipo, tipo_solicitud.descripcion))
            conn.commit()
            conn.close()
            return {"resultado": "Tipo_solicitud creada"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_tipo_solicitud(self, tipo_solicitud_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo_solicitud WHERE id_tipo_solicitud = %s", (tipo_solicitud_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_tipo_solicitud':int(result[0]),
                    'nombre_tipo':result[1],
                    'descripcion':result[2]

            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_tipos_solicitud(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo_solicitud")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_tipo_solicitud':data[0],
                    'nombre_tipo':data[1],
                    'descripcion':data[2]

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Tipo_solicitud not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_tipo_solicitud(self, tipo_solicitud_id: int, nombre_tipo: str, descripcion: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tipo_solicitud SET nombre_tipo=%s, descripcion=%s WHERE id_tipo_solicitud=%s",
                       (nombre_tipo, descripcion, tipo_solicitud_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Tipo_solicitud not found")
        
            return {"mensaje": f"tipo_solicitud {tipo_solicitud_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_tipo_solicitud(self, tipo_solicitud_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tipo_solicitud WHERE id_tipo_solicitud=%s", (tipo_solicitud_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Tipo_solicitud not found")
        
            return {"mensaje": f"Tipo_solicitud {tipo_solicitud_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()    
       

##user_controller = UserController()