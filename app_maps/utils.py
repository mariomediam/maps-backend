"""
Utility functions for the app_maps application
"""

def parse_boolean_param(value):
    """
    Parse a string parameter to boolean value in a flexible way.
    
    Args:
        value: String value from URL parameter
        
    Returns:
        bool or None: True, False, or None if invalid
        
    Examples:
        parse_boolean_param('true') -> True
        parse_boolean_param('True') -> True
        parse_boolean_param('TRUE') -> True
        parse_boolean_param('1') -> True
        parse_boolean_param('yes') -> True
        
        parse_boolean_param('false') -> False
        parse_boolean_param('False') -> False
        parse_boolean_param('FALSE') -> False
        parse_boolean_param('0') -> False
        parse_boolean_param('no') -> False
        
        parse_boolean_param('invalid') -> None
        parse_boolean_param(None) -> None
    """
    if value is None:
        return None
    
    # Convert to string and normalize
    str_value = str(value).lower().strip()
    
    # True values
    if str_value in ['true', '1', 'yes', 'on', 'active']:
        return True
    
    # False values
    if str_value in ['false', '0', 'no', 'off', 'inactive']:
        return False
    
    # Invalid value
    return None


def get_boolean_query_param(request, param_name, default=None):
    """
    Get a boolean parameter from request query parameters.
    
    Args:
        request: Django request object
        param_name: Name of the query parameter
        default: Default value if parameter is not provided or invalid
        
    Returns:
        bool or default value
        
    Examples:
        # URL: /categories/?is_active=true
        get_boolean_query_param(request, 'is_active') -> True
        
        # URL: /categories/?is_active=false
        get_boolean_query_param(request, 'is_active') -> False
        
        # URL: /categories/
        get_boolean_query_param(request, 'is_active', True) -> True
        
        # URL: /categories/?is_active=invalid
        get_boolean_query_param(request, 'is_active', True) -> True
    """
    param_value = request.GET.get(param_name)
    parsed_value = parse_boolean_param(param_value)
    
    # If parsing failed, return default
    if parsed_value is None:
        return default
    
    return parsed_value


def validate_required_boolean_param(request, param_name):
    """
    Validate and get a required boolean parameter.
    
    Args:
        request: Django request object
        param_name: Name of the query parameter
        
    Returns:
        tuple: (bool_value, error_message)
        
    Examples:
        # URL: /categories/?is_active=true
        validate_required_boolean_param(request, 'is_active') -> (True, None)
        
        # URL: /categories/?is_active=invalid
        validate_required_boolean_param(request, 'is_active') -> (None, "Invalid boolean value for 'is_active'")
        
        # URL: /categories/
        validate_required_boolean_param(request, 'is_active') -> (None, "Parameter 'is_active' is required")
    """
    param_value = request.GET.get(param_name)
    
    if param_value is None:
        return None, f"Parameter '{param_name}' is required"
    
    parsed_value = parse_boolean_param(param_value)
    
    if parsed_value is None:
        return None, f"Invalid boolean value for '{param_name}'. Use: true/false, 1/0, yes/no"
    
    return parsed_value, None
