"""
Python SDK for the ClickUp API
"""

from pyclickupy.client import ClickUpClient
from pyclickupy.exceptions import ClickupClientError

__version__ = "0.1.1"

def hello() -> str:
    return f"Hello from pyclickupy! v{__version__} :)"

__all__ = ['ClickUpClient', 'ClickupClientError']
