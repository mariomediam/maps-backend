from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decimal import Decimal


class IncidentCategory(models.Model):
    """Incident category: traffic accidents, broken traffic light, damaged pavement, etc."""
    # Primary Key: IdCategory -> id_category (column name in DB)
    id_category = models.AutoField(primary_key=True, db_column='id_category')
    description = models.CharField(
        max_length=200, 
        null=False, 
        blank=False, 
        verbose_name="Description",
        db_column='description'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        db_column='is_active'
    )
    
    class Meta:
        verbose_name = "Incident Category"
        verbose_name_plural = "Incident Categories"
        db_table = "incident_category"
    
    def __str__(self):
        return self.description


class IncidentClosureType(models.Model):
    """Incident closure type: Solved, referred to another office, False information, etc."""
    # Primary Key: IdClosureType -> id_closure_type (column name in DB)
    id_closure_type = models.AutoField(primary_key=True, db_column='id_closure_type')
    description = models.CharField(
        max_length=200, 
        null=False, 
        blank=False, 
        verbose_name="Description",
        db_column='description'
    )
    
    class Meta:
        verbose_name = "Incident Closure Type"
        verbose_name_plural = "Incident Closure Types"
        db_table = "incident_closure_type"
    
    def __str__(self):
        return self.description


class IncidentPriority(models.Model):
    """Incident priority: High, Medium, Low"""
    # Primary Key: IdPriority -> id_priority (column name in DB)
    id_priority = models.AutoField(primary_key=True, db_column='id_priority')
    description = models.CharField(
        max_length=100, 
        null=False, 
        blank=False, 
        verbose_name="Description",
        db_column='description'
    )
    
    class Meta:
        verbose_name = "Incident Priority"
        verbose_name_plural = "Incident Priorities"
        db_table = "incident_priority"
    
    def __str__(self):
        return self.description


class Incident(models.Model):
    """Main model for registering road incidents"""
    
    USER_TYPE_CHOICES = [
        ('1', 'Inspector'),
        ('2', 'Citizen'),
    ]
    
    # Primary Key: IdIncident -> id_incident (column name in DB)
    id_incident = models.AutoField(primary_key=True, db_column='id_incident')
    
    # Required fields
    registration_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Registration Date",
        db_column='registration_date'
    )
    category = models.ForeignKey(
        IncidentCategory, 
        on_delete=models.PROTECT, 
        null=False, 
        verbose_name="Category",
        db_column='id_category'
    )
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        null=False, 
        verbose_name="Latitude",
        db_column='latitude'
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        null=False, 
        verbose_name="Longitude",
        db_column='longitude'
    )
    summary = models.TextField(
        null=False, 
        blank=False, 
        verbose_name="Incident Summary",
        db_column='summary'
    )
    reference = models.CharField(
        max_length=500, 
        null=False, 
        blank=True, 
        verbose_name="Reference",
        help_text="Example: Corner of Av. Junín with Av. Sánchez Cerro",
        db_column='reference'
    )
    show_on_map = models.BooleanField(
        default=False, 
        verbose_name="Show on Map",
        help_text="If the incident will be visible to other citizens",
        db_column='show_on_map'
    )
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        null=False, 
        verbose_name="User Type",
        db_column='user_type'
    )
    is_closed = models.BooleanField(
        default=False, 
        verbose_name="Incident Closed",
        db_column='is_closed'
    )
    
    # Fields for inspectors
    inspector = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Inspector",
        help_text="Inspector user who registered the incident",
        db_column='inspector_id'
    )
    
    # Fields for citizens
    citizen_name = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Citizen Name",
        db_column='citizen_name'
    )
    citizen_lastname = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Citizen Lastname",
        db_column='citizen_lastname'
    )
    citizen_phone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        verbose_name="Citizen Phone",        
        db_column='citizen_phone'
    )
    citizen_email = models.EmailField(
        null=True, 
        blank=True, 
        verbose_name="Citizen Email",
        db_column='citizen_email'
    )
    
    # Optional management fields
    priority = models.ForeignKey(
        IncidentPriority, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Priority",
        db_column='id_priority'
    )
    derivation_document = models.CharField(
        max_length=8, 
        null=True, 
        blank=True,
        verbose_name="Derivation Document",
        help_text="Document code with which the incident was referred",
        db_column='derivation_document'
    )
    
    # Closure fields
    closure_type = models.ForeignKey(
        IncidentClosureType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Closure Type",
        db_column='id_closure_type'
    )
    closure_description = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Closure Description",
        db_column='closure_description'
    )
    closure_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Closure Date",
        db_column='closure_date'
    )
    closure_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='closed_incidents',
        verbose_name="Closure User",
        db_column='closure_user_id'
    )
    
    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        db_table = "incident"
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"Incident #{self.id_incident} - {self.category.description} - {self.registration_date.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        """Override save to set show_on_map based on user type"""
        if self.user_type == '1':  # Inspector
            self.show_on_map = True
        elif self.user_type == '2':  # Citizen
            self.show_on_map = False
        super().save(*args, **kwargs)
    
    @property
    def coordinates(self):
        """Returns coordinates as tuple (latitude, longitude)"""
        return (float(self.latitude), float(self.longitude))
    
    @property
    def citizen_full_name(self):
        """Returns citizen's full name if applicable"""
        if self.user_type == '2' and self.citizen_name:  # Citizen
            return f"{self.citizen_name} {self.citizen_lastname or ''}".strip()
        return None


class Photography(models.Model):
    """Photographs associated with an incident"""
    # Primary Key: IdPhotography -> id_photography (column name in DB)
    id_photography = models.AutoField(primary_key=True, db_column='id_photography')
    incident = models.ForeignKey(
        Incident, 
        on_delete=models.CASCADE, 
        related_name='photographs',
        verbose_name="Incident",
        db_column='id_incident'
    )
    name = models.CharField(
        max_length=200, 
        null=False, 
        blank=False,
        verbose_name="Name",
        db_column='name',
        default='photo'
    )
    content_type = models.CharField(
        max_length=200, 
        null=False, 
        blank=True,
        verbose_name="Content Type",
        db_column='content_type',
        default=''
    )
    file_size = models.BigIntegerField(
        help_text="File size in bytes",
        null=True,  # Permitir null temporalmente
        blank=True,
        default=0
    )
    r2_key = models.CharField(
        max_length=500,
        help_text="Unique key in R2 bucket",
        null=True,  # Permitir null temporalmente
        blank=True
    )
    
    upload_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Upload Date",
        db_column='upload_date'
    )
    
    class Meta:
        verbose_name = "Photography"
        verbose_name_plural = "Photographs"
        db_table = "photography"
        ordering = ['upload_date']
    
    def __str__(self):
        return f"Photo #{self.id_photography} - Incident #{self.incident.id_incident}"


class Attachment(models.Model):
    """Files attached to an incident (only for system users and inspectors)"""
    # Primary Key: IdAttachment -> id_attachment (column name in DB)
    id_attachment = models.AutoField(primary_key=True, db_column='id_attachment')
    incident = models.ForeignKey(
        Incident, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name="Incident",
        db_column='id_incident'
    )
    description = models.CharField(
        max_length=300, 
        null=False, 
        blank=True,
        verbose_name="File Description",
        help_text="Description of the file content",
        db_column='description'
    )
    url = models.URLField(
        max_length=500, 
        null=False, 
        blank=False,
        verbose_name="File URL",
        help_text="URL from where the file can be downloaded",
        db_column='url'
    )
    upload_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Upload Date",
        db_column='upload_date'
    )
    upload_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Upload User",
        db_column='upload_user_id'
    )
    
    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
        db_table = "attachment"
        ordering = ['upload_date']
    
    def __str__(self):
        return f"Attachment #{self.id_attachment} - {self.description or 'No description'} - Incident #{self.incident.id_incident}"


class IncidentState(models.Model):
    """Incident state: Presentado, En proceso, Resuelto, etc."""
    # Primary Key: IdCategory -> id_category (column name in DB)
    id_state = models.AutoField(primary_key=True, db_column='id_state')
    description = models.CharField(
        max_length=200, 
        null=False, 
        blank=False, 
        verbose_name="Description",
        db_column='description'
    )
    
    class Meta:
        verbose_name = "Incident State"
        verbose_name_plural = "Incident States"
        db_table = "incident_state"
    
    def __str__(self):
        return self.description
