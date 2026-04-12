import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.usuario_model import Usuario
from fastapi.encoders import jsonable_encoder

class UsuarioController:
        
    def create_usuario(self, usuario: Usuario):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuario (nombre,correo,contraseña,id_rol,estado) VALUES (%s, %s, %s, %s, %s )", (usuario.nombre, usuario.correo, usuario.contraseña, usuario.id_rol,usuario.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Usuario creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_usuario':int(result[0]),
                    'nombre':result[1],
                    'correo':result[2],
                    'contraseña':result[3],
                    'id_rol':int(result[4]),
                    'estado':result[5]
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
       
    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_usuario':data[0],
                    'nombre':data[1],
                    'contraseña':data[2],
                    'id_rol':data[3],
                    'estado':data[4]

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

    def update_usuario(self, usuario_id: int, nombre: str, correo: str, contraseña: str, id_rol: int, estado: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuario SET nombre=%s, correo=%s, contraseña=%s, id_rol=%s, estado=%s WHERE id_usuario=%s",
                       (nombre, correo, contraseña, id_rol, estado, usuario_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        
            return {"mensaje": f"Usuario {usuario_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE id_usuario=%s", (usuario_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        
            return {"mensaje": f"Usuario {usuario_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()    
       

##user_controller = UserController()