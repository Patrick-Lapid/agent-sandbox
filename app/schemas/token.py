from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema for decoding JWT."""
    sub: Optional[str] = None
