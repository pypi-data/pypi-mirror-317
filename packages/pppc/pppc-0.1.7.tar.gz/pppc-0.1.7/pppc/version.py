"""Version management for PPPC"""

DEFAULT_VERSION = "1.21.3"

SUPPORTED_VERSIONS = [
    "1.21.3",
    "1.20.4",
    "1.19.4",
    "1.18.2",
    "1.17.1",
    "1.16.5"
]

def validate_version(version: str) -> bool:
    """Validate if the specified version is supported"""
    return version in SUPPORTED_VERSIONS