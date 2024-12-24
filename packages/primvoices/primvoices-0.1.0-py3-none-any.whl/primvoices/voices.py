from typing import Optional, List

import requests

from .models import (
    APIResponse,
    VoiceResponse,
    VoiceCreateParams,
    PublicVoiceResponse,
    PaginationParams,
    ErrorResponse,
)

class VoicesAPI:
    """Client for the Voices API endpoints."""

    def __init__(self, client: requests.Session, base_url: str):
        """Initialize the voices API client.
        
        Args:
            client: The requests session to use
            base_url: The base URL for the API
        """
        self.client = client
        self.base_url = base_url

    def list(self, params: Optional[PaginationParams] = None) -> APIResponse[List[VoiceResponse]]:
        """List all voices for the authenticated user.
        
        Args:
            params: Optional pagination parameters
            
        Returns:
            List of voices and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.get(f"{self.base_url}/v1/voices", params=params.model_dump(by_alias=True) if params else None)
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[List[VoiceResponse]](data=response.json()["data"])

    def retrieve(self, voice_id: str) -> APIResponse[VoiceResponse]:
        """Get a specific voice by ID.
        
        Args:
            voice_id: The ID of the voice to retrieve
            
        Returns:
            The voice details and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.get(f"{self.base_url}/v1/voices/{voice_id}")
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[VoiceResponse](data=response.json()["data"])

    def create(self, params: VoiceCreateParams) -> APIResponse[VoiceResponse]:
        """Create a new voice.
        
        Args:
            params: The voice creation parameters
            
        Returns:
            The created voice and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.post(f"{self.base_url}/v1/voices", json=params.model_dump(by_alias=True))
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[VoiceResponse](data=response.json()["data"])

    def delete(self, voice_id: str) -> APIResponse[None]:
        """Delete a voice.
        
        Args:
            voice_id: The ID of the voice to delete
            
        Returns:
            Response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.delete(f"{self.base_url}/v1/voices/{voice_id}")
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[None](data=None)

    def list_public(self, params: Optional[PaginationParams] = None) -> APIResponse[List[PublicVoiceResponse]]:
        """List all public voices.
        
        Args:
            params: Optional pagination parameters
            
        Returns:
            List of public voices and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.get(f"{self.base_url}/v1/publicVoices", params=params.model_dump(by_alias=True) if params else None)
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[List[PublicVoiceResponse]](data=response.json()["data"])

    def retrieve_public(self, voice_id: str) -> APIResponse[PublicVoiceResponse]:
        """Get a specific public voice by ID.
        
        Args:
            voice_id: The ID of the public voice to retrieve
            
        Returns:
            The public voice details and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.get(f"{self.base_url}/v1/publicVoices/{voice_id}")
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[PublicVoiceResponse](data=response.json()["data"])
