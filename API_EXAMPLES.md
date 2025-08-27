# API Usage Examples - Category Endpoints

## 📋 Endpoints Overview

### 1. `/categories/` - Flexible Category Endpoint
- **Method**: GET
- **Description**: Returns categories with optional filtering
- **Default**: Returns only active categories
- **Parameter**: `is_active` (optional)

### 2. `/categories/filter/` - Strict Category Endpoint  
- **Method**: GET
- **Description**: Returns categories with required filtering
- **Parameter**: `is_active` (required)

---

## 🔧 Parameter Handling

### Accepted Boolean Values

| Input | Parsed Value | Description |
|-------|-------------|-------------|
| `true`, `True`, `TRUE` | `True` | Active categories |
| `false`, `False`, `FALSE` | `False` | Inactive categories |
| `1`, `yes`, `on`, `active` | `True` | Active categories |
| `0`, `no`, `off`, `inactive` | `False` | Inactive categories |

---

## 🌐 URL Examples

### Flexible Endpoint (`/categories/`)

```bash
# Get only active categories (default behavior)
GET /categories/
GET /categories/?is_active=true
GET /categories/?is_active=True  
GET /categories/?is_active=1
GET /categories/?is_active=yes
GET /categories/?is_active=on
GET /categories/?is_active=active

# Get only inactive categories
GET /categories/?is_active=false
GET /categories/?is_active=False
GET /categories/?is_active=FALSE
GET /categories/?is_active=0
GET /categories/?is_active=no
GET /categories/?is_active=off
GET /categories/?is_active=inactive

# Invalid values fallback to default (active=true)
GET /categories/?is_active=invalid
GET /categories/?is_active=maybe
```

### Strict Endpoint (`/categories/filter/`)

```bash
# Get only active categories
GET /categories/filter/?is_active=true
GET /categories/filter/?is_active=1
GET /categories/filter/?is_active=yes

# Get only inactive categories  
GET /categories/filter/?is_active=false
GET /categories/filter/?is_active=0
GET /categories/filter/?is_active=no

# These return 400 Bad Request
GET /categories/filter/                    # Missing parameter
GET /categories/filter/?is_active=invalid # Invalid value
```

---

## 📄 Response Examples

### Success Response (Active Categories)
```json
{
    "message": "Categories filtered by is_active=True",
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
    "count": 2,
    "filter_applied": true
}
```

### Success Response (Inactive Categories)
```json
{
    "message": "Categories filtered by is_active=False",
    "content": [
        {
            "id_category": 3,
            "description": "Deprecated Category",
            "is_active": false
        }
    ],
    "count": 1,
    "filter_applied": true
}
```

### Error Response (Strict Endpoint - Missing Parameter)
```json
{
    "error": "Parameter 'is_active' is required",
    "message": "Invalid or missing parameter",
    "accepted_values": [
        "true", "false", "True", "False", 
        "1", "0", "yes", "no", "on", "off", 
        "active", "inactive"
    ]
}
```

### Error Response (Strict Endpoint - Invalid Value)
```json
{
    "error": "Invalid boolean value for 'is_active'. Use: true/false, 1/0, yes/no",
    "message": "Invalid or missing parameter", 
    "accepted_values": [
        "true", "false", "True", "False",
        "1", "0", "yes", "no", "on", "off",
        "active", "inactive"
    ]
}
```

---

## 🎯 Best Practices

### 1. **Use Flexible Endpoint for General Use**
```javascript
// Frontend JavaScript example
const getCategories = async (activeOnly = true) => {
    const url = activeOnly 
        ? '/categories/?is_active=true'
        : '/categories/?is_active=false';
    
    const response = await fetch(url);
    return response.json();
};
```

### 2. **Use Strict Endpoint for Validated Forms**
```javascript
// Form validation example
const getCategoriesByStatus = async (isActive) => {
    if (isActive === undefined) {
        throw new Error('is_active parameter is required');
    }
    
    const url = `/categories/filter/?is_active=${isActive}`;
    const response = await fetch(url);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error);
    }
    
    return response.json();
};
```

### 3. **Handle Different Input Types**
```python
# Python client example
def get_categories(is_active=None):
    if is_active is None:
        url = "/categories/"
    else:
        # Convert boolean to string
        active_str = "true" if is_active else "false"
        url = f"/categories/?is_active={active_str}"
    
    response = requests.get(url)
    return response.json()

# Usage
get_categories()          # Default (active only)
get_categories(True)      # Active categories
get_categories(False)     # Inactive categories
```

---

## 🔍 Testing Commands

### cURL Examples
```bash
# Test flexible endpoint
curl "http://localhost:8000/categories/"
curl "http://localhost:8000/categories/?is_active=true"
curl "http://localhost:8000/categories/?is_active=false"
curl "http://localhost:8000/categories/?is_active=invalid"

# Test strict endpoint
curl "http://localhost:8000/categories/filter/?is_active=true"
curl "http://localhost:8000/categories/filter/?is_active=false" 
curl "http://localhost:8000/categories/filter/"  # Should return 400
curl "http://localhost:8000/categories/filter/?is_active=invalid"  # Should return 400
```

### HTTPie Examples
```bash
# Test flexible endpoint
http GET localhost:8000/categories/
http GET localhost:8000/categories/ is_active==true
http GET localhost:8000/categories/ is_active==false

# Test strict endpoint  
http GET localhost:8000/categories/filter/ is_active==true
http GET localhost:8000/categories/filter/ is_active==false
http GET localhost:8000/categories/filter/  # Should return 400
```
