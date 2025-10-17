from app_maps.models import IncidentClosureType
from app_maps.serializers import IncidentClosureTypeSerializer

class ClosureTypeService:
    
    def get_closure_type_by_id(self, id: int):
        closure_type = IncidentClosureType.objects.get(id=id)
        serializer = IncidentClosureTypeSerializer(closure_type)
        return serializer.data
    
    def get_all_closure_types(self):
        closure_types = IncidentClosureType.objects.all()
        serializer = IncidentClosureTypeSerializer(closure_types, many=True)
        return serializer.data