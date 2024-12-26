"""Custom exceptions for PPPC"""

class PPPCError(Exception):
    """Base exception for PPPC"""
    pass

class ValidationError(PPPCError):
    """Raised when validation fails"""
    pass

class CompilationError(PPPCError):
    """Raised when compilation fails"""
    pass

class VersionError(PPPCError):
    """Raised when version is not supported"""
    pass