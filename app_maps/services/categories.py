from app_maps.models import IncidentCategory
from app_maps.serializers import IncidentCategorySerializer

class CategoryService:
    def __init__(self):
        categories = IncidentCategory.objects.all()
        serializer = IncidentCategorySerializer(categories, many=True)
        
    
    def get_category_by_id(self, id: int):
        category = IncidentCategory.objects.get(id_category=id)
        serializer = IncidentCategorySerializer(category)
        return serializer.data
    
    def get_category_by_active(self, is_active: bool):
        """Get by ctive categories"""
        categories = IncidentCategory.objects.filter(is_active=is_active)
        serializer = IncidentCategorySerializer(categories, many=True)
        return serializer.data
    
    def get_all_categories(self):
        """Get all categories"""
        categories = IncidentCategory.objects.all()
        serializer = IncidentCategorySerializer(categories, many=True)
        return serializer.data
    