"""Java compilation utilities"""

import os
import subprocess
import tempfile
from typing import List, Optional
from ..exceptions import CompilationError

class JavaCompiler:
    """Handles Java source compilation"""
    
    def __init__(self, src_dir: str, classpath: Optional[List[str]] = None):
        self.src_dir = src_dir
        self.classpath = classpath or []
        
        # Add Java version check
        if not self._check_java_installation():
            raise CompilationError(
                "Java Development Kit (JDK) not found. Please install JDK and ensure 'javac' is in your PATH."
            )

    def _check_java_installation(self) -> bool:
        """Check if Java compiler is available"""
        try:
            subprocess.run(['javac', '-version'], 
                          capture_output=True, 
                          check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def compile(self, output_dir: str, source_version: str = "1.8") -> None:
        """
        Compile Java source files using javac
        
        Args:
            output_dir: Directory for compiled classes
            source_version: Java source version (default: 1.8)
            
        Raises:
            CompilationError: If compilation fails
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Create a temporary file listing all Java sources
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                sources = []
                for root, _, files in os.walk(self.src_dir):
                    for file in files:
                        if file.endswith(".java"):
                            sources.append(os.path.join(root, file))
                if not sources:
                    raise CompilationError("No Java source files found")
                f.write('\n'.join(sources))
                sources_file = f.name

            # Prepare javac command with additional options
            cmd = [
                'javac',
                '-d', output_dir,
                '-source', source_version,
                '-target', source_version,
                '-encoding', 'UTF-8',
                '-Xlint:deprecation',
                '-Xlint:unchecked'
            ]
            
            # Add classpath if specified
            if self.classpath:
                cmd.extend(['-cp', os.pathsep.join(self.classpath)])
            
            # Add source files from the list
            cmd.extend(['@' + sources_file])
            
            # Run javac
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            # Clean up sources file
            os.unlink(sources_file)
            
            # Check for compilation errors
            if result.returncode != 0:
                raise CompilationError(
                    f"Compilation failed:\n{result.stderr}"
                )
                
        except Exception as e:
            raise CompilationError(f"Failed to compile Java files: {str(e)}")