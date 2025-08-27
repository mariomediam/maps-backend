from app_maps.models import IncidentState
from app_maps.serializers import IncidentStateSerializer

class StateService:
    def __init__(self):
        states = IncidentState.objects.all()
        serializer = IncidentStateSerializer(states, many=True)
    
    def get_state_by_id(self, id: int):
        state = IncidentState.objects.get(id=id)
        serializer = IncidentStateSerializer(state)
        return serializer.data
    
    def get_all_states(self):
        states = IncidentState.objects.all()
        serializer = IncidentStateSerializer(states, many=True)
        return serializer.data
    
    