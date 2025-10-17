from app_maps.models import IncidentPriority
from app_maps.serializers import IncidentPrioritySerializer

class PriorityService:    
    def get_priority_by_id(self, id: int):
        priority = IncidentPriority.objects.get(id_priority=id)
        serializer = IncidentPrioritySerializer(priority)
        return serializer.data
    
    def get_all_priorities(self):
        priorities = IncidentPriority.objects.all().order_by('id_priority')
        serializer = IncidentPrioritySerializer(priorities, many=True)
        return serializer.data