from fastapi import HTTPException
from typing import Any

class InfrastructureException(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=500, detail=detail or "Infrastructure operation failed")

class ConfigurationException(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=400, detail=detail or "Invalid configuration")

class AnsibleException(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=500, detail=detail or "Ansible operation failed")