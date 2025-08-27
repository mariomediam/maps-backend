from django.contrib.auth.models import User
from app_maps.models import Incident, Photography

from app_maps.serializers import IncidentSerializer, PhotographySerializer
from app_maps.services.cloudflare import CloudflareService
from app_maps.services.photography import PhotographyService

from django.core.files.uploadedfile import UploadedFile
import tempfile

class IncidentService:
    def __init__(self):
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
    
    def get_incident_by_id(self, id: int):
        incident = Incident.objects.get(id=id)
        serializer = IncidentSerializer(incident)
        return serializer.data
    
    def get_all_incidents(self):
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
        return serializer.data
    
    def add_incident(self, **kwargs):

        try:
        
            category_id = kwargs.get('category_id')
            latitude = kwargs.get('latitude')
            longitude = kwargs.get('longitude')
            summary = kwargs.get('summary')
            reference = kwargs.get('reference')
            login = kwargs.get('login')
            files = kwargs.get('files')

            inspector = None
            citizen_name = None
            citizen_lastname = None
            citizen_phone = None
            citizen_email = None


            if login:
                show_on_map = True
                inspector = User.objects.get(username=kwargs.get('login'))
                user_type = 'inspector'
            else:
                show_on_map = False
                citizen_name = kwargs.get('citizen_name')
                citizen_lastname = kwargs.get('citizen_lastname')
                citizen_phone = kwargs.get('citizen_phone')
                citizen_email = kwargs.get('citizen_email')
                user_type = 'citizen'        

            incident = Incident.objects.create(
                user_type=user_type,
                category_id=category_id,
                latitude=latitude,
                longitude=longitude,
                summary=summary,
                reference=reference,
                show_on_map=show_on_map,            
                inspector=inspector,
                citizen_name=citizen_name,
                citizen_lastname=citizen_lastname,
                citizen_phone=citizen_phone,
                citizen_email=citizen_email,
            )

            for file in files:
                self.add_photography(incident.id_incident, file)

            serializer = IncidentSerializer(incident)
            return serializer.data
        
        except Exception as e:
            if incident:
                incident.delete()
            raise Exception(e)


        
    def add_photography(self, id_incident: int, file: UploadedFile):
        

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file.seek(0)

            upload_file_service = CloudflareService()
            response_upload = upload_file_service.upload_file(temp_file.name, id_incident, file.content_type)
            success = response_upload.get('success', False)
            r2_key = response_upload.get('r2_key', None)
            error = response_upload.get('error', 'Error subiendo el archivo')
            
            if not success:                
                raise Exception(error)                
            
            photography_service = PhotographyService()

            info_photography = {
                'id_incident': id_incident,
                'name': file.name,
                'content_type': file.content_type,
                'file_size': file.size,
                'r2_key': r2_key
            }
            photography_service.add_photography(**info_photography)
                    
         
