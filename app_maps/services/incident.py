from django.contrib.auth.models import User
from app_maps.models import Incident, Photography, IncidentState

from app_maps.serializers import IncidentSerializer, PhotographySerializer, IncidentStateSerializer
from app_maps.services.cloudflare import CloudflareService
from app_maps.services.photography import PhotographyService
from app_maps.services.file_utils import FileUtils
from django.core.files.uploadedfile import UploadedFile
import tempfile

class IncidentService:
    def __init__(self):
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
    
    def get_incident_by_id(self, id: int):
       # Optimización: usar select_related y prefetch_related para evitar N+1 queries
        incident = Incident.objects.select_related(
            'category',
            'priority', 
            'closure_type',
            'inspector',
            'closure_user'
        ).prefetch_related('photographs').get(id_incident=id)
        incident_serializer = IncidentSerializer(incident)

        incident_serializer_data = incident_serializer.data

        incident_serializer_data = self.add_state_to_incident(incident_serializer_data, self.get_states_dict())

        return incident_serializer_data
    
    def get_all_incidents(self):
        # Optimización: usar select_related y prefetch_related para evitar N+1 queries
        incidents = Incident.objects.select_related(
            'category',
            'priority', 
            'closure_type',
            'inspector',
            'closure_user'
        ).prefetch_related('photographs')
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

            if len(files) > 0:
                self.add_photography_miniature(incident.id_incident, files[0])

            serializer = IncidentSerializer(incident)
            return serializer.data
        
        except Exception as e:
            if incident:
                incident.delete()
            raise Exception(e)


        
    def add_photography(self, id_incident: int, file: UploadedFile):
        
        # Optimizar la imagen antes de subirla
        file_utils = FileUtils()
        optimized_file = file_utils.optimize_image(file, max_width=1024, max_height=1024, quality=80)

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            for chunk in optimized_file.chunks():
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

    def add_photography_miniature(self, id_incident: int, file: UploadedFile):
         # Optimizar la imagen antes de subirla
        file_utils = FileUtils()
        optimized_file = file_utils.optimize_image(file, max_width=128, max_height=128, quality=80)

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            for chunk in optimized_file.chunks():
                temp_file.write(chunk)
            temp_file.seek(0)

            upload_file_service = CloudflareService()
            response_upload = upload_file_service.upload_file(temp_file.name, id_incident, file.content_type, name_key='miniature.jpg')
            success = response_upload.get('success', False)
            r2_key = response_upload.get('r2_key', None)
            error = response_upload.get('error', 'Error subiendo el archivo')
            
            if not success:                
                raise Exception(error)                

            return r2_key
            


    def get_incidents_by_filters(self, **kwargs):
        id_category = kwargs.get('id_category')
        id_state = kwargs.get('id_state')
        show_on_map = kwargs.get('show_on_map')
        text_search = kwargs.get('text_search')
        id_incident = kwargs.get('id_incident')
        
        registration_period = kwargs.get('registration_period')
        if registration_period:
            from_date = registration_period.get('from_date')
            to_date = registration_period.get('to_date')
        else:
            from_date = None
            to_date = None

        # Optimización: usar select_related y prefetch_related para evitar N+1 queries
        # select_related para relaciones ForeignKey, prefetch_related para OneToMany
        incidents = Incident.objects.select_related(
            'category',           # Para category.description
            'priority',           # Para priority.description  
            'closure_type',       # Para closure_type.description
            'inspector',          # Para inspector.username
            'closure_user'        # Para closure_user.username
        ).prefetch_related('photographs')  # Para fotografías (OneToMany)

        if id_incident:
            incidents = incidents.filter(id_incident=id_incident)

        if id_category:            
            incidents = incidents.filter(category_id=id_category)

        if id_state: 
            id_state = int(id_state)                        
            if id_state == 3:            
                incidents = incidents.filter(is_closed=True)
            elif id_state == 2:            
                incidents = incidents.filter(is_closed=False, priority__isnull=False)
            elif id_state == 1:            
                incidents = incidents.filter(is_closed=False, priority__isnull=True)
            
        if registration_period:
            incidents = incidents.filter(registration_date__range=(from_date, to_date))

        if show_on_map:
            incidents = incidents.filter(show_on_map=show_on_map)

        if text_search:
            incidents = incidents.filter(summary__icontains=text_search) | incidents.filter(reference__icontains=text_search) 

        serializer = IncidentSerializer(incidents, many=True)

        incidentes_serializer = serializer.data
        incidentes_serializer_with_state = []

        # Optimización: crear diccionario indexado de estados una sola vez
        states_dict = self.get_states_dict()

        # Optimización: usar list comprehension en lugar de loop + append
        incidentes_serializer_with_state = [
            self.add_state_to_incident(incident, states_dict) 
            for incident in incidentes_serializer
        ]

        return incidentes_serializer_with_state

    

    
    def get_all_states(self):
        states = IncidentState.objects.all()
        serializer = IncidentStateSerializer(states, many=True)
        return serializer.data
    
    def get_states_dict(self):
        """Optimización: retorna un diccionario indexado por id_state para búsquedas O(1)"""
        states_list = self.get_all_states()
        return {state['id_state']: state for state in states_list}

        
    def add_state_to_incident(self, incident_serializer: dict, states_dict: dict):
        """Optimizada: usa diccionario indexado para búsquedas O(1) en lugar de O(n)"""
        if not states_dict:
            states_dict = self.get_states_dict()

        # Determinar el id_state basado en la lógica del negocio
        if incident_serializer.get('is_closed') == True:
            state_id = 3  # Resuelto
        elif incident_serializer.get('priority') is not None:
            state_id = 2  # En proceso
        else:
            state_id = 1  # Presentado
        
        # Búsqueda optimizada O(1) usando diccionario
        state = states_dict.get(state_id)
        
        if state:
            incident_serializer['id_state'] = state['id_state']
            incident_serializer['description_state'] = state['description']
            incident_serializer['color_state'] = state.get('color', '#000000')
        else:
            # Estado por defecto si no se encuentra
            incident_serializer['id_state'] = 1
            incident_serializer['description_state'] = 'Estado desconocido'
            incident_serializer['color_state'] = '#000000'

        return incident_serializer
        

    
    def get_photography_miniature_url(self, id_incident: int):
        key = f"incidents/{id_incident}/miniature.jpg"
        cloudflare_service = CloudflareService()
        url = cloudflare_service.get_file_url(key)
        return url

    def update_incident_partial(self, id_incident: int, update_data: dict, user=None):
        """
        Actualiza campos específicos de un incidente.
        Solo permite actualizar campos en la lista blanca.
        
        Args:
            id_incident: ID del incidente a actualizar
            update_data: Diccionario con los campos a actualizar
            user: Usuario que realiza la actualización (opcional)
        
        Returns:
            Incidente serializado con los cambios aplicados
        
        Raises:
            ValueError: Si se intenta actualizar un campo no permitido
            Exception: Si el incidente no existe
        """
        # Lista blanca de campos permitidos para actualización parcial
        ALLOWED_FIELDS = {
            'show_on_map',      # Mostrar/ocultar en mapa
            'is_closed',        # Cerrar/abrir incidente
            'priority',         # Cambiar prioridad (id_priority)
            'derivation_document',  # Documento de derivación
            'closure_type',     # Tipo de cierre (id_closure_type)
            'closure_description',  # Descripción del cierre
        }
        
        try:
            # Verificar que el incidente existe
            incident = Incident.objects.get(id_incident=id_incident)
            
            # Validar que solo se actualicen campos permitidos
            invalid_fields = set(update_data.keys()) - ALLOWED_FIELDS
            if invalid_fields:
                raise ValueError(
                    f"Cannot update fields: {', '.join(invalid_fields)}. "
                    f"Allowed fields: {', '.join(ALLOWED_FIELDS)}"
                )
            
            # Actualizar cada campo proporcionado
            for field, value in update_data.items():
                if field == 'show_on_map':
                    incident.show_on_map = bool(value)
                
                elif field == 'is_closed':
                    incident.is_closed = bool(value)
                    # Si se está cerrando, registrar fecha y usuario
                    if incident.is_closed and not incident.closure_date:
                        from django.utils import timezone
                        incident.closure_date = timezone.now()
                        if user:
                            incident.closure_user = user
                
                elif field == 'priority':
                    # Puede ser None o un ID de prioridad
                    if value is None:
                        incident.priority = None
                    else:
                        incident.priority_id = int(value)
                
                elif field == 'derivation_document':
                    incident.derivation_document = value if value else None
                
                elif field == 'closure_type':
                    if value is None:
                        incident.closure_type = None
                    else:
                        incident.closure_type_id = int(value)
                
                elif field == 'closure_description':
                    incident.closure_description = value if value else None
            
            # Guardar cambios
            incident.save()
            
            # Retornar incidente actualizado serializado
            return self.get_incident_by_id(id_incident)
            
        except Incident.DoesNotExist:
            raise Exception(f"Incident with ID {id_incident} not found")