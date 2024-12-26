"""Plugin compilation functionality"""

import os
from typing import Optional
from .core import Plugin
from .exceptions import CompilationError
from .utils.validation import validate_plugin_config
from .utils.jar_builder import JarBuilder

def compile_plugin(plugin: Plugin, output_dir: Optional[str] = None) -> str:
    """
    Compile the Python plugin into a Paper plugin JAR file
    
    Args:
        plugin: Plugin instance to compile
        output_dir: Optional directory for the output JAR file
        
    Returns:
        Path to the compiled JAR file
        
    Raises:
        CompilationError: If compilation fails
    """
    if output_dir is None:
        output_dir = os.getcwd()
        
    try:
        # Validate plugin configuration
        config = plugin.__dict__
        validate_plugin_config(config)
        
        # Build JAR file
        builder = JarBuilder(config, output_dir)
        jar_path = builder.build()
        
        return jar_path
    except Exception as e:
        raise CompilationError(f"Failed to compile plugin: {str(e)}")