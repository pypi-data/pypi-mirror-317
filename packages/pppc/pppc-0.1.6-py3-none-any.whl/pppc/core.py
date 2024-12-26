"""Core functionality for PPPC"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class Event:
    """Base class for Minecraft events"""
    name: str
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Plugin:
    """Main plugin class"""
    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    api_version: str = "1.21.3"
    commands: Dict[str, Any] = field(default_factory=dict)
    event_handlers: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        from .version import validate_version
        if not validate_version(self.api_version):
            raise ValueError(f"Unsupported API version: {self.api_version}")

    def register_command(self, name: str, handler: Any, description: str = ""):
        """Register a command handler"""
        self.commands[name] = {
            "handler": handler,
            "description": description
        }

    def register_event_handler(self, event_name: str, handler: Any):
        """Register an event handler"""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)