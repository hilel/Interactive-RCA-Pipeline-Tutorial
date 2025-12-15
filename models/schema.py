"""
Schema definitions for Project Stressed.
Defines the Pydantic models that enforce strict typing.
"""

from pydantic import BaseModel, Field
from typing import Optional


class StructuredLogEvent(BaseModel):
    """
    This Pydantic model defines the 'Destination' for our parser.
    It enforces strict typing. If the parser finds an order_id, it MUST be an int.
    """
    timestamp: str          # We keep as string for simplicity in demo, usually DateTime
    event_name: str         # The most critical field: "UseCase_X" or "Screen_Y"
    order_id: Optional[int] # Optional because some system logs might not have an ID
    severity: str           # INFO, WARN, ERROR
    details: Optional[str]  # Catch-all for extra text
