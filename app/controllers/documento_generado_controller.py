import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.documento_generado_model import DocumentoGenerado
from fastapi.encoders import jsonable_encoder

class DocumentoGeneradoController:
        
    def create_documento_generado(self, documento_generado: DocumentoGenerado):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO documento_generado (id_solicitud,nombre_documento,fecha_generacion) VALUES ( %s, %s, %s )", (documento_generado.id_solicitud, documento_generado.nombre_documento, documento_generado.fecha_generacion))
            conn.commit()
            conn.close()
            return {"resultado": "Documento creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
        

    def get_documento_generado(self, documento_generado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documento_generado WHERE id_documento = %s", (documento_generado_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_documento':int(result[0]),
                    'id_solicitud':int(result[1]),
                    'nombre_documento':result[2],
                    'fecha_generacion':result[3]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Documento not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
       
    def get_documentos_generados(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documento_generado")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_documento':data[0],
                    'id_solicitud':data[1],
                    'nombre_documento':data[2],
                    'fecha_generacion':data[3]

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Documento not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_documento_generado(self, documento_generado_id: int, id_solicitud: int, nombre_documento: str, fecha_generacion: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE documento_generado SET id_solicitud=%s, nombre_documento=%s, fecha_generacion=%s WHERE id_documento=%s",
                       (id_solicitud, nombre_documento, fecha_generacion, documento_generado_id))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        
            return {"mensaje": f"Documento {documento_generado_id} actualizado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
    
    def delete_documento_generado(self, documento_generado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM documento_generado WHERE id_documento=%s", (documento_generado_id,))
            conn.commit()
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Documento not found")
        
            return {"mensaje": f"Documento {documento_generado_id} eliminado exitosamente"}
    
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()    

##user_controller = UserController()