from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from app_maps.utils import get_boolean_query_param
from app_maps.models import IncidentCategory
from app_maps.serializers import IncidentCategorySerializer

from app_maps.services.states import StateService
from app_maps.services.categories import CategoryService
from app_maps.services.incident import IncidentService

def index(request):
    return HttpResponse("Conexión exitosa")



class CategoryView(APIView):    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Get categories with optional filtering by is_active parameter.        
        """
        try:
            category_service = CategoryService()
            
            # Check if is_active parameter is provided
            if 'is_active' in request.GET:
                # Parse the is_active parameter using our robust utility                
                is_active = get_boolean_query_param(request, 'is_active', default=True)
                categories = category_service.get_category_by_active(is_active)
                
                message = f"Categories filtered by is_active={is_active}"
            else:
                # No filter provided, return only active categories (default behavior)
                categories = category_service.get_all_categories()
                message = "All categories"
            
            return Response(data={
                'message': message,
                'content': categories,              
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
                        return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve categories"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CategoryDetailView(APIView):
    """
    View for specific category
    """
    permission_classes = [AllowAny]
    
    def get(self, request, category_id):
        """
        Handle specific category request
        """
        try:
            category_service = CategoryService()
            category = category_service.get_category_by_id(category_id)
            return Response({
                'message': f"Category with ID {category_id}",
                'content': category
            })
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve category"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class StateView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:

            state_service = StateService()
            states = state_service.get_all_states()
            return Response({
                'message': "All states",
                'content': states
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve states"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class IncidentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            incident_service = IncidentService()
            data = request.data.dict()        
            files = request.FILES.getlist('files', [])
            login = request.user.username
            data['files'] = files
            data['login'] = login
            incident = incident_service.add_incident(**data)
            return Response({
                'message': "Incident added successfully",
                'content': incident
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to add incident"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)