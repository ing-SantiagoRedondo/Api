import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.facultad_model import Facultad
from fastapi.encoders import jsonable_encoder

class FacultadController:
        
    def create_facultad(self, facultad: Facultad):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO facultad (nombre_facultad) VALUES (%s)", (facultad.nombre_facultad,))
            conn.commit()
            conn.close()
            return {"resultado": "Facultad creada"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_facultad(self, facultad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facultad WHERE id_facultad = %s", (facultad_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_facultad':int(result[0]),
                    'nombre_facultad':result[1]

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
       
    def get_facultades(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facultad")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_facultad':data[0],
                    'nombre_facultad':data[1]

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="FAcultad not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_facultad(self, facultad_id: int, nombre_facultad: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE facultad SET nombre_facultad=%s WHERE id_facultad=%s",
                       (nombre_facultad,  facultad_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Facultad not found")
        
            return {"mensaje": f"Facultad {facultad_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_facultad(self, facultad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM facultad WHERE id_facultad=%s", (facultad_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Facultad not found")
        
            return {"mensaje": f"Facultad {facultad_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()    
       

##user_controller = UserController()