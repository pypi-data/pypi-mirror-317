"""Utility functions for Java code generation"""

import os
from typing import Dict, Any
from ..templates import (
    MAIN_CLASS_TEMPLATE,
    EVENT_HANDLER_TEMPLATE,
    COMMAND_HANDLER_TEMPLATE
)

def generate_main_class(plugin_config: Dict[str, Any]) -> str:
    """Generate the main plugin Java class"""
    return MAIN_CLASS_TEMPLATE.format(
        package_name=plugin_config['name'].lower(),
        class_name=f"{plugin_config['name']}Plugin",
        startup_code=generate_startup_code(plugin_config),
        shutdown_code=generate_shutdown_code(plugin_config)
    )

def generate_startup_code(plugin_config: Dict[str, Any]) -> str:
    """Generate plugin startup code"""
    code = []
    if plugin_config.get('commands'):
        code.append("// Register commands")
        for cmd_name in plugin_config['commands']:
            code.append(f"this.getCommand(\"{cmd_name}\").setExecutor(this);")
    return "\n        ".join(code)

def generate_shutdown_code(plugin_config: Dict[str, Any]) -> str:
    """Generate plugin shutdown code"""
    return "getLogger().info(\"Plugin disabled\");"