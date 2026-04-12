import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.rol_model import Rol
from fastapi.encoders import jsonable_encoder

class RolController:
        
    def create_rol(self, rol: Rol):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO rol (nombre_rol, descripcion) VALUES (%s, %s)", (rol.nombre_rol, rol.descripcion))
            conn.commit()
            conn.close()
            return {"resultado": "Rol creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rol WHERE id_rol = %s", (rol_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_rol':int(result[0]),
                    'nombre_rol':result[1],
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
                raise HTTPException(status_code=404, detail="Rol not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rol")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_rol':data[0],
                    'nombre_rol':data[1],
                    'descripcion':data[2]

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Rol not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_rol(self, rol_id: int, nombre_rol: str, descripcion: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE rol SET nombre_rol=%s, descripcion=%s WHERE id_rol=%s",
                       (nombre_rol, descripcion, rol_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol not found")
        
            return {"mensaje": f"Rol {rol_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rol WHERE id_rol=%s", (rol_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol not found")
        
            return {"mensaje": f"Rol {rol_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()    
       

##user_controller = UserController()