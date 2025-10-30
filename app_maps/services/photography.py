from app_maps.models import Photography
from app_maps.serializers import PhotographySerializer
from app_maps.services.cloudflare import CloudflareService

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
    
    
    def get_photography_url(self, id_photography: int):
        photography = Photography.objects.get(id_photography=id_photography)
        cloudflare_service = CloudflareService()
        url = cloudflare_service.get_file_url(photography.r2_key)
        return url
    
    def get_photography_by_id(self, id_photography: int):
        photography = Photography.objects.get(id_photography=id_photography)
        serializer = PhotographySerializer(photography)
        return serializer.data

    def  get_blob_photography_by_id(self, id_photography: int):
        photography = Photography.objects.get(id_photography=id_photography)
        cloudflare_service = CloudflareService()
        blob = cloudflare_service.get_blob(photography.r2_key)
        print("blob", blob)
        return blob

    def delete_photography_by_id(self, id_photography: int):
        photography = Photography.objects.get(id_photography=id_photography)
        cloudflare_service = CloudflareService()
        cloudflare_service.delete_file(photography.r2_key)
        photography.delete()
        return True
        

