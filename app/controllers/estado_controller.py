import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.estado_model import Estado 
from fastapi.encoders import jsonable_encoder

class EstadoController:
        
    def create_estado(self, estado: Estado):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO estado (nombre_estado, descripcion) VALUES (%s, %s)", (estado.nombre_estado , estado.descripcion))
            conn.commit()
            conn.close()
            return {"resultado": "Estado creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_estado(self, estado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estado WHERE id_estado = %s", (estado_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_estado':int(result[0]),
                    'nombre_estado':result[1],
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
                raise HTTPException(status_code=404, detail="Estado not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_estados(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estado")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_estado':data[0],
                    'nombre_estado':data[1],
                    'descripcion':data[2]

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Estado not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_estado(self, estado_id: int, nombre_estado: str, descripcion: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE estado SET nombre_estado=%s, descripcion=%s WHERE id_estado=%s",
                       (nombre_estado, descripcion, estado_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estado not found")
        
            return {"mensaje": f"Estado {estado_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_estado(self, estado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estado WHERE id_estado=%s", (estado_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estado not found")
        
            return {"mensaje": f"Estado {estado_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()    
       

##user_controller = UserController()