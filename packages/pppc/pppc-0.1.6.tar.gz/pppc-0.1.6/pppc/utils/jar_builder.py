"""Utility functions for JAR file building"""

import os
import shutil
import tempfile
from typing import Dict, Any
from .java_generator import generate_main_class

class JarBuilder:
    """Handles building of the plugin JAR file"""
    
    def __init__(self, plugin_config: Dict[str, Any], output_dir: str):
        self.config = plugin_config
        self.output_dir = output_dir
        self.temp_dir = tempfile.mkdtemp()
        
    def build(self) -> str:
        """
        Build the plugin JAR file
        
        Returns:
            str: Path to the built JAR file
        """
        try:
            self._create_structure()
            self._generate_java_files()
            self._create_plugin_yml()
            return self._create_jar()
        finally:
            shutil.rmtree(self.temp_dir)
            
    def _create_structure(self) -> None:
        """Create temporary directory structure"""
        os.makedirs(os.path.join(self.temp_dir, "src"))
        os.makedirs(os.path.join(self.temp_dir, "resources"))
        
    def _generate_java_files(self) -> None:
        """Generate Java source files"""
        main_class = generate_main_class(self.config)
        package_path = os.path.join(self.temp_dir, "src", 
                                  self.config['name'].lower())
        os.makedirs(package_path)
        
        with open(os.path.join(package_path, f"{self.config['name']}Plugin.java"), 'w') as f:
            f.write(main_class)
            
    def _create_plugin_yml(self) -> None:
        """Create plugin.yml file"""
        # Implementation for creating plugin.yml
        pass
        
    def _create_jar(self) -> str:
        """Create the final JAR file"""
        # Implementation for creating JAR
        jar_name = f"{self.config['name'].lower()}-{self.config['version']}.jar"
        return os.path.join(self.output_dir, jar_name)