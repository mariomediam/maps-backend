import boto3
from django.conf import settings
import os
from datetime import datetime
from typing import Dict, Any, Optional

class CloudflareService:
    
    def __init__(self):
        """
        Inicializa el cliente S3 para Cloudflare R2
        """
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name='auto'
        )
        self.bucket_name = settings.R2_BUCKET_NAME

    def upload_file(self, file_path: str, id_incident: str, content_type: str) -> Dict[str, Any]:
        """
        Sube un archivo a Cloudflare R2 y retorna la key del archivo.
        
        Args:
            file_path (str): Ruta del archivo local a subir
            id_incident (str): ID de incidencia para organizar en carpetas
            content_type (str): Tipo de contenido del archivo
            
        Returns:
            Dict[str, Any]: Diccionario con la key del archivo en R2
        """
        try:
            # Generar un nombre único para el archivo            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')            
            file_extension = os.path.splitext(file_path)[1]            
            r2_key = f"incidents/{id_incident}/{timestamp}{file_extension}"                

            # Subir el archivo
            with open(file_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    r2_key,
                    ExtraArgs={'ContentType': content_type}
                )   

            return {
                'r2_key': r2_key,
                'success': True
            }
            
        except Exception as e:
            return {
                'r2_key': None,
                'success': False,
                'error': str(e)
            }

    def delete_file(self, r2_key: str) -> Dict[str, Any]:
        """
        Elimina un archivo de Cloudflare R2.
        
        Args:
            r2_key (str): Key del archivo en R2 a eliminar
            
        Returns:
            Dict[str, Any]: Resultado de la operación
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=r2_key
            )
            
            return {
                'success': True,
                'message': f'Archivo {r2_key} eliminado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_file_url(self, r2_key: str, expiration: int = 300) -> Optional[str]:
        """
        Genera una URL temporal para acceder al archivo.
        
        Args:
            r2_key (str): Key del archivo en R2
            expiration (int): Tiempo de expiración en segundos (default: 1 minuto)
            
        Returns:
            Optional[str]: URL temporal del archivo o None si hay error
        """
        try:


            print("***** 1 ******")
            print(self.bucket_name)
            print(r2_key)
            print(expiration)
            print("***** 2 ******")
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': r2_key},
                ExpiresIn=expiration
            )


            #  url = s3_client.generate_presigned_url(
            #     'get_object',
            #     Params={
            #         'Bucket': settings.R2_BUCKET_NAME,
            #         'Key': attachment.r2_key
            #     },
            #     ExpiresIn=60  # 1 minuto en segundos
            # )
            return url
            
        except Exception as e:
            print(f"Error generando URL: {str(e)}")
            return None

    def file_exists(self, r2_key: str) -> bool:
        """
        Verifica si un archivo existe en R2.
        
        Args:
            r2_key (str): Key del archivo en R2
            
        Returns:
            bool: True si el archivo existe, False en caso contrario
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=r2_key)
            return True
        except:
            return False