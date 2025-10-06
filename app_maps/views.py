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
from app_maps.services.photography import PhotographyService

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
    """
    Vista para manejar incidentes con autenticación diferencial:
    - GET: No requiere autenticación (ciudadanos pueden consultar)
    - POST: Requiere autenticación (solo usuarios autenticados pueden crear)
    """
    
    def get_permissions(self):
        """
        Retorna los permisos requeridos según el método HTTP
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:  # POST, PUT, PATCH, DELETE
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
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
        
    def get(self, request):
        """
        Obtiene incidentes con filtros opcionales via query parameters.
        No requiere autenticación - acceso público para ciudadanos.
        """
        try:
            incident_service = IncidentService()
            # Usar query_params para GET requests (buena práctica REST)
            filters = dict(request.query_params.items())
            print("***** se ejecuto el get de incidentes ****** con los filtros: ", filters)
            incidents = incident_service.get_incidents_by_filters(**filters)
            return Response({
                'message': "Incidents retrieved successfully",
                'content': incidents
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve incidents"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class PhotographyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_photography):
        try:
            print("***** se ejecuto el get de fotografia ****** con el id: ", id_photography)
            photography_service = PhotographyService()            
            photography = photography_service.get_photography_by_id(id_photography)            
            url = photography_service.get_photography_url(id_photography)            
            photography['url'] = url            
            
            return Response({
                'message': "Photography URL retrieved successfully",
                'content': photography
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve photography URL"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PhotographyMiniatureView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_incident):
        try:
            incident_service = IncidentService()
            url = incident_service.get_photography_miniature_url(id_incident)
            return Response({
                'message': "Photography miniature URL retrieved successfully",
                'content': url
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve photography miniature URL"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncidentDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_incident):
        try:
            incident_service = IncidentService()
            incident = incident_service.get_incident_by_id(id_incident)
            return Response({
                'message': "Incident retrieved successfully",
                'content': incident
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Internal server error: {str(e)}",
                "message": "Failed to retrieve incident"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)