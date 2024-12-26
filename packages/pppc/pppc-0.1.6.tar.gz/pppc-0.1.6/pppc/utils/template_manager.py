"""Template management utilities"""

from typing import Dict, Any
from jinja2 import Environment, BaseLoader
from ..templates import (
    MAIN_CLASS_TEMPLATE,
    EVENT_HANDLER_TEMPLATE,
    COMMAND_HANDLER_TEMPLATE
)

class TemplateManager:
    """Manages Java code templates"""
    
    def __init__(self):
        self.env = Environment(loader=BaseLoader())
        
    def render_main_class(self, context: Dict[str, Any]) -> str:
        """Render main plugin class template"""
        template = self.env.from_string(MAIN_CLASS_TEMPLATE)
        return template.render(**context)
        
    def render_event_handler(self, context: Dict[str, Any]) -> str:
        """Render event handler template"""
        template = self.env.from_string(EVENT_HANDLER_TEMPLATE)
        return template.render(**context)
        
    def render_command_handler(self, context: Dict[str, Any]) -> str:
        """Render command handler template"""
        template = self.env.from_string(COMMAND_HANDLER_TEMPLATE)
        return template.render(**context)