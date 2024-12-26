"""
PPPC (PythonPaperPluginCompiler) - Create Minecraft Paper plugins using Python
"""

from .core import Plugin, Event
from .compiler import compile_plugin
from .decorators import event_handler, command
from .version import SUPPORTED_VERSIONS, DEFAULT_VERSION

__version__ = "0.1.0"
__all__ = ['Plugin', 'Event', 'compile_plugin', 'event_handler', 'command', 
           'SUPPORTED_VERSIONS', 'DEFAULT_VERSION']