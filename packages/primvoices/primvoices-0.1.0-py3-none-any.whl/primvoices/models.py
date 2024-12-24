from datetime import datetime
from typing import Optional, TypeVar, Generic, Literal
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar('T')

class BaseModelCamel(BaseModel):
    """Base model with camelCase to snake_case conversion."""
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True,
        from_attributes=True
    )

class APIResponse(BaseModelCamel, Generic[T]):
    """Generic API response wrapper."""
    data: T

class ErrorResponse(Exception):
    """Error response from the API."""
    def __init__(self, error: str, status: int):
        self.error = error
        self.status = status
        super().__init__(error)

class VoiceResponse(BaseModelCamel):
    """Response model for a voice."""
    id: str
    user_id: str
    name: str
    sample_url: str
    preview_url: str
    verified: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class VoiceCreateParams(BaseModelCamel):
    """Parameters for creating a voice.
    
    The verified field must be explicitly set to True by the user to acknowledge they have
    permission to use this voice for generation purposes.
    """
    name: str
    sample_url: str
    verified: bool

    def model_post_init(self, _):
        """Validate that verified is True."""
        if not self.verified:
            raise ValueError(
                "You must explicitly verify that you have permission to use this voice by setting verified=True. "
                "By setting verified=True, you acknowledge that you have the necessary rights and permissions "
                "to use this voice for generation purposes, and that you accept responsibility for any misuse."
            )

class GenerationResponse(BaseModelCamel):
    """Response model for a generation."""
    id: str
    user_id: str
    voice_id: str
    text: str
    source_url: str
    notes: str
    audio_url: str
    quality: str
    cost: float
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class GenerationCreateParams(BaseModelCamel):
    """Parameters for creating a generation."""
    voice_id: str
    text: Optional[str] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None
    quality: Literal['low', 'medium', 'high', 'voice']

class PublicVoiceResponse(BaseModelCamel):
    """Response model for a public voice."""
    id: str
    name: str
    sample_url: str
    preview_url: str
    verified: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class PaginationParams(BaseModelCamel):
    """Parameters for pagination."""
    limit: Optional[int] = None
    offset: Optional[int] = None
