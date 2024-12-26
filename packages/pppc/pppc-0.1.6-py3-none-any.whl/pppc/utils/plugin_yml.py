"""Utility functions for plugin.yml generation"""

import yaml
from typing import Dict, Any

def generate_plugin_yml(config: Dict[str, Any]) -> str:
    """
    Generate plugin.yml content
    
    Args:
        config: Plugin configuration dictionary
        
    Returns:
        str: YAML content for plugin.yml
    """
    plugin_yml = {
        "name": config["name"],
        "version": config["version"],
        "main": f"{config['name'].lower()}.{config['name']}Plugin",
        "api-version": config.get("api_version", "1.21.3")
    }
    
    if config.get("description"):
        plugin_yml["description"] = config["description"]
    if config.get("author"):
        plugin_yml["author"] = config["author"]
    if config.get("commands"):
        plugin_yml["commands"] = {
            name: {"description": cmd.get("description", "")}
            for name, cmd in config["commands"].items()
        }
        
    return yaml.dump(plugin_yml, sort_keys=False)