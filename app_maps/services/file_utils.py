from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile
from PIL import Image
import io
import os

class FileUtils:
    def get_file_information(self, file: UploadedFile):

        file_size = file.size
        content_type = file.content_type
        file_name = file.name
        file_extension = file.name.split('.')[-1]

        return {
            'file_size': file_size,
            'content_type': content_type,
            'file_name': file_name,
            'file_extension': file_extension
        }

    def optimize_image(self, file: UploadedFile, max_width=1920, max_height=1920, quality=85):
        """
        Optimiza una imagen reduciendo su tamaño y comprimiéndola.
        Similar al comportamiento de WhatsApp al enviar fotos.
        
        Args:
            file: Archivo de imagen subido
            max_width: Ancho máximo de la imagen (default: 1920px)
            max_height: Alto máximo de la imagen (default: 1920px)
            quality: Calidad de compresión JPEG 0-100 (default: 85)
            
        Returns:
            InMemoryUploadedFile: Archivo optimizado en memoria
        """
        try:
            # Verificar que sea una imagen
            if not file.content_type.startswith('image/'):
                return file
            
            # Abrir la imagen con Pillow
            image = Image.open(file)
            
            # Obtener orientación EXIF si existe (para rotar automáticamente)
            try:
                from PIL import ImageOps
                image = ImageOps.exif_transpose(image)
            except:
                pass
            
            # Obtener dimensiones originales
            original_width, original_height = image.size
            
            # Calcular nuevas dimensiones manteniendo el aspect ratio
            if original_width > max_width or original_height > max_height:
                # Calcular la proporción de reducción
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                # Redimensionar usando LANCZOS para mejor calidad
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convertir RGBA a RGB si es necesario (para PNGs con transparencia)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Crear un fondo blanco
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                # Pegar la imagen sobre el fondo blanco
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Guardar la imagen optimizada en memoria
            output = io.BytesIO()
            
            # Siempre guardar como JPEG para mejor compresión
            image.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            # Obtener el nombre del archivo sin extensión y agregar .jpg
            original_name = os.path.splitext(file.name)[0]
            new_name = f"{original_name}.jpg"
            
            # Crear un nuevo archivo en memoria
            optimized_file = InMemoryUploadedFile(
                output,
                'ImageField',
                new_name,
                'image/jpeg',
                output.getbuffer().nbytes,
                None
            )
            
            return optimized_file
            
        except Exception as e:
            # Si hay algún error, devolver el archivo original
            print(f"Error optimizando imagen: {str(e)}")
            file.seek(0)
            return file
    
    