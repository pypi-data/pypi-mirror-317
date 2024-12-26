"""File management utilities"""

import os
import shutil
from typing import List

class FileManager:
    """Manages file operations during compilation"""
    
    @staticmethod
    def create_directory_structure(base_dir: str, directories: List[str]) -> None:
        """Create required directories"""
        for directory in directories:
            os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
            
    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Write content to file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    @staticmethod
    def copy_resources(src_dir: str, dest_dir: str) -> None:
        """Copy resource files"""
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)