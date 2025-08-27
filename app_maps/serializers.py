from rest_framework import serializers
from .models import (
    IncidentCategory, 
    IncidentClosureType, 
    IncidentPriority, 
    IncidentState,
    Incident, 
    Photography, 
    Attachment
)


class IncidentCategorySerializer(serializers.ModelSerializer):
    """Serializer for IncidentCategory model"""
    class Meta:
        model = IncidentCategory
        fields = ['id_category', 'description', 'is_active']


class IncidentClosureTypeSerializer(serializers.ModelSerializer):
    """Serializer for IncidentClosureType model"""
    class Meta:
        model = IncidentClosureType
        fields = ['id_closure_type', 'description']


class IncidentPrioritySerializer(serializers.ModelSerializer):
    """Serializer for IncidentPriority model"""
    class Meta:
        model = IncidentPriority
        fields = ['id_priority', 'description']


class IncidentStateSerializer(serializers.ModelSerializer):
    """Serializer for IncidentState model"""
    class Meta:
        model = IncidentState
        fields = ['id_state', 'description']


class PhotographySerializer(serializers.ModelSerializer):
    """Serializer for Photography model"""
    class Meta:
        model = Photography
        fields = ['id_photography', 'name', 'content_type', 'file_size', 'r2_key', 'upload_date']


class AttachmentSerializer(serializers.ModelSerializer):
    """Serializer for Attachment model"""
    class Meta:
        model = Attachment
        fields = ['id_attachment', 'incident', 'description', 'url', 'upload_date', 'upload_user']


class IncidentSerializer(serializers.ModelSerializer):
    """Serializer for Incident model"""
    category_name = serializers.CharField(source='category.description', read_only=True)
    priority_name = serializers.CharField(source='priority.description', read_only=True)
    closure_type_name = serializers.CharField(source='closure_type.description', read_only=True)
    inspector_username = serializers.CharField(source='inspector.username', read_only=True)
    closure_user_username = serializers.CharField(source='closure_user.username', read_only=True)
    
    # Incluir fotografías relacionadas
    photographs = PhotographySerializer(many=True, read_only=True)
    
    class Meta:
        model = Incident
        fields = [
            'id_incident', 'registration_date', 'category', 'category_name',
            'latitude', 'longitude', 'summary', 'reference', 'show_on_map',
            'user_type', 'is_closed', 'inspector', 'inspector_username',
            'citizen_name', 'citizen_lastname', 'citizen_phone', 'citizen_email',
            'priority', 'priority_name', 'derivation_document',
            'closure_type', 'closure_type_name', 'closure_description',
            'closure_date', 'closure_user', 'closure_user_username',
            'photographs'  # Añadir el campo de fotografías
        ]


class IncidentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating incidents (with validation)"""
    class Meta:
        model = Incident
        fields = [
            'category', 'latitude', 'longitude', 'summary', 'reference',
            'user_type', 'inspector', 'citizen_name', 'citizen_lastname',
            'citizen_phone', 'citizen_email', 'priority'
        ]
        
    def validate(self, data):
        """Custom validation for incident creation"""
        user_type = data.get('user_type')
        
        if user_type == '1':  # Inspector
            if not data.get('inspector'):
                raise serializers.ValidationError("Inspector field is required when user_type is Inspector")
        elif user_type == '2':  # Citizen
            if not data.get('citizen_name'):
                raise serializers.ValidationError("Citizen name is required when user_type is Citizen")
        
        return data
