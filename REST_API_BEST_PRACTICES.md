# REST API Best Practices - Category Endpoints

## 🎯 **Problema a Resolver**

Necesitas endpoints que manejen:
- `GET /categories?is_active=true` - Listar categorías con filtro
- `GET /categories/1` - Obtener categoría específica por ID

## 🏆 **3 Enfoques Implementados**

### **ENFOQUE 1: ViewSet con DRF Router (⭐ RECOMENDADO)**

```python
# Endpoint: /categories-rest/
class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = IncidentCategorySerializer
    lookup_field = 'id_category'
```

**URLs generadas automáticamente:**
- `GET /categories-rest/` - Lista categorías
- `GET /categories-rest/?is_active=true` - Filtra categorías
- `GET /categories-rest/{id}/` - Obtiene categoría específica

**✅ Ventajas:**
- Sigue convenciones REST automáticamente
- Manejo automático de errores 404
- Paginación automática (si se configura)
- Menos código para mantener
- Documentación automática con Swagger

---

### **ENFOQUE 2: APIView Única con Lógica Manual**

```python
# Endpoints: /categories-api/ y /categories-api/{id}/
class CategoryAPIView(APIView):
    def get(self, request, category_id=None):
        if category_id is not None:
            # Lógica para item específico
        else:
            # Lógica para lista
```

**URLs manuales:**
- `GET /categories-api/` - Lista categorías
- `GET /categories-api/?is_active=true` - Filtra categorías
- `GET /categories-api/{id}/` - Obtiene categoría específica

**✅ Ventajas:**
- Control total sobre la lógica
- Respuestas personalizadas
- Fácil de entender

**❌ Desventajas:**
- Más código para mantener
- Manejo manual de errores

---

### **ENFOQUE 3: Vistas Separadas (Tradicional)**

```python
# Diferentes vistas para diferentes operaciones
path("categories/", CategoryListView.as_view())
path("categories/<int:id>/", CategoryDetailView.as_view())
```

**✅ Ventajas:**
- Separación clara de responsabilidades
- Fácil testing individual

**❌ Desventajas:**
- Más vistas para mantener
- Duplicación de código

---

## 🚀 **Ejemplos de Uso**

### **ENFOQUE 1: ViewSet (Recomendado)**

```bash
# Listar todas las categorías activas
GET /categories-rest/

# Filtrar categorías por estado
GET /categories-rest/?is_active=true
GET /categories-rest/?is_active=false

# Obtener categoría específica
GET /categories-rest/1/
GET /categories-rest/5/
```

**Respuestas:**

```json
// GET /categories-rest/
{
    "message": "Active categories (default)",
    "content": [
        {
            "id_category": 1,
            "description": "Traffic Accident",
            "is_active": true
        },
        {
            "id_category": 2,
            "description": "Broken Traffic Light",
            "is_active": true
        }
    ],
    "count": 2
}

// GET /categories-rest/1/
{
    "message": "Category with ID 1",
    "content": {
        "id_category": 1,
        "description": "Traffic Accident",
        "is_active": true
    }
}

// GET /categories-rest/999/ (Not Found)
{
    "error": "Category with ID 999 not found",
    "message": "Category not found"
}
```

---

## 🔧 **Configuración de URLs**

```python
# urls.py
from rest_framework.routers import DefaultRouter

# ENFOQUE 1: Router automático
router = DefaultRouter()
router.register(r'categories-rest', views.CategoryViewSet, basename='categories-rest')

urlpatterns = [
    # ViewSet (automático)
    path("", include(router.urls)),
    
    # APIView manual
    path("categories-api/", views.CategoryAPIView.as_view()),
    path("categories-api/<int:category_id>/", views.CategoryAPIView.as_view()),
]
```

---

## 🎨 **Personalización de Respuestas**

### **ViewSet con Respuestas Personalizadas**

```python
class CategoryViewSet(ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Custom message',
            'content': serializer.data,
            'count': len(serializer.data),
            'timestamp': timezone.now()
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'message': f"Category {instance.id_category}",
            'content': serializer.data,
            'related_incidents_count': instance.incident_set.count()
        })
```

---

## 🔍 **Filtrado Avanzado**

### **Múltiples Filtros**

```python
def get_queryset(self):
    queryset = IncidentCategory.objects.all()
    
    # Filtro por activo/inactivo
    if 'is_active' in self.request.GET:
        is_active = get_boolean_query_param(self.request, 'is_active')
        queryset = queryset.filter(is_active=is_active)
    
    # Filtro por descripción (búsqueda)
    search = self.request.GET.get('search')
    if search:
        queryset = queryset.filter(description__icontains=search)
    
    # Ordenamiento
    ordering = self.request.GET.get('ordering', 'description')
    queryset = queryset.order_by(ordering)
    
    return queryset
```

**Ejemplos:**
```bash
GET /categories-rest/?is_active=true&search=traffic&ordering=-description
GET /categories-rest/?search=accident
GET /categories-rest/?ordering=id_category
```

---

## 📊 **Comparación de Enfoques**

| Aspecto | ViewSet | APIView Manual | Vistas Separadas |
|---------|---------|----------------|------------------|
| **Código** | Menos | Medio | Más |
| **Flexibilidad** | Media | Alta | Alta |
| **Convenciones REST** | ✅ Automático | ⚠️ Manual | ⚠️ Manual |
| **Manejo de Errores** | ✅ Automático | ❌ Manual | ❌ Manual |
| **Documentación** | ✅ Automático | ⚠️ Manual | ⚠️ Manual |
| **Testing** | ✅ Fácil | ⚠️ Medio | ✅ Fácil |
| **Mantenimiento** | ✅ Bajo | ⚠️ Medio | ❌ Alto |

---

## 🏅 **Recomendación Final**

### **Para APIs nuevas: ENFOQUE 1 (ViewSet)**
- Menos código
- Convenciones REST automáticas
- Fácil mantenimiento
- Documentación automática

### **Para APIs existentes: ENFOQUE 2 (APIView)**
- Control total
- Migración gradual
- Respuestas personalizadas

### **Para casos específicos: ENFOQUE 3 (Separadas)**
- Lógica muy diferente entre list/detail
- Permisos diferentes por operación

---

## 🧪 **Testing Examples**

```bash
# Test all approaches
curl "http://localhost:8000/categories-rest/"
curl "http://localhost:8000/categories-rest/1/"
curl "http://localhost:8000/categories-rest/?is_active=false"

curl "http://localhost:8000/categories-api/"  
curl "http://localhost:8000/categories-api/1/"
curl "http://localhost:8000/categories-api/?is_active=true"
```

¡El **ENFOQUE 1 (ViewSet)** es el más recomendado para la mayoría de casos de uso!
