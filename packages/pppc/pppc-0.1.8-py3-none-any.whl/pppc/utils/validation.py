"""Utility functions for validation"""

from typing import Any, Dict, List
from ..exceptions import ValidationError

def validate_plugin_config(config: Dict[str, Any]) -> None:
    """
    Validate plugin configuration
    
    Args:
        config: Plugin configuration dictionary
        
    Raises:
        ValidationError: If configuration is invalid
    """
    required_fields = ['name', 'version']
    for field in required_fields:
        if field not in config:
            raise ValidationError(f"Missing required field: {field}")
            
    if not isinstance(config.get('commands', {}), dict):
        raise ValidationError("Commands must be a dictionary")
        
    if not isinstance(config.get('event_handlers', {}), dict):
        raise ValidationError("Event handlers must be a dictionary")