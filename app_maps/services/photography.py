from app_maps.models import Photography
from app_maps.serializers import PhotographySerializer

class PhotographyService:
    
    def add_photography(self, **kwargs):
        id_incident = kwargs.get('id_incident')
        name = kwargs.get('name')
        content_type = kwargs.get('content_type')
        file_size = kwargs.get('file_size')
        r2_key = kwargs.get('r2_key')

        photography = Photography.objects.create(
            incident_id=id_incident,
            name=name,
            content_type=content_type,
            file_size=file_size,
            r2_key=r2_key
        )
        return {
        'id_photography': photography.id_photography,
        'incident': photography.incident_id,
        'name': photography.name,
        'content_type': photography.content_type,
        'file_size': photography.file_size,
        'r2_key': photography.r2_key,
        'upload_date': photography.upload_date
        }
    
    
    def get_photography(self, incident_id: int):
        pass

    def delete_photography(self, incident_id: int):
        pass