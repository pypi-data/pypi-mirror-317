"""Decorators for event handling and commands"""

from functools import wraps
from typing import Callable, Any

def event_handler(event_name: str) -> Callable:
    """Decorator for event handlers"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)
        wrapper._event_name = event_name
        return wrapper
    return decorator

def command(name: str, description: str = "") -> Callable:
    """Decorator for command handlers"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)
        wrapper._command_name = name
        wrapper._command_description = description
        return wrapper
    return decorator