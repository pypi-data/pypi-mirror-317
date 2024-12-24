from typing import Optional, List, Callable

import requests

from .models import (
    APIResponse,
    GenerationResponse,
    GenerationCreateParams,
    PaginationParams,
    ErrorResponse,
)

class GenerationsAPI:
    """Client for the Generations API endpoints."""

    def __init__(self, client: requests.Session, base_url: str):
        """Initialize the generations API client.
        
        Args:
            client: The requests session to use
            base_url: The base URL for the API
        """
        self.client = client
        self.base_url = base_url

    def _validate_params(self, params: GenerationCreateParams) -> None:
        """Validate generation parameters.
        
        Args:
            params: The parameters to validate
            
        Raises:
            ErrorResponse: If the parameters are invalid
        """
        if not params.quality:
            raise ErrorResponse(error="quality is required", status=400)
        if not params.voice_id:
            raise ErrorResponse(error="voice_id is required", status=400)
        if params.quality in ['low', 'medium', 'high'] and not params.text:
            raise ErrorResponse(error=f"text is required for quality {params.quality}", status=400)
        if params.quality == 'voice' and not params.source_url:
            raise ErrorResponse(error="source_url is required for voice quality", status=400)

    def list(self, params: Optional[PaginationParams] = None) -> APIResponse[List[GenerationResponse]]:
        """List all generations for the authenticated user.
        
        Args:
            params: Optional pagination parameters
            
        Returns:
            List of generations and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.get(f"{self.base_url}/v1/generations", params=params.model_dump(by_alias=True) if params else None)
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[List[GenerationResponse]](data=response.json()["data"])

    def retrieve(self, generation_id: str) -> APIResponse[GenerationResponse]:
        """Get a specific generation by ID.
        
        Args:
            generation_id: The ID of the generation to retrieve
            
        Returns:
            The generation details and response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.get(f"{self.base_url}/v1/generations/{generation_id}")
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[GenerationResponse](data=response.json()["data"])

    def create(self, params: GenerationCreateParams) -> APIResponse[GenerationResponse]:
        """Create a new generation.
        
        Args:
            params: The generation creation parameters
            
        Returns:
            The created generation and response metadata
            
        Raises:
            ErrorResponse: If the API request fails or parameters are invalid
        """
        self._validate_params(params)
        response = self.client.post(f"{self.base_url}/v1/generations", json=params.model_dump(by_alias=True))
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[GenerationResponse](data=response.json()["data"])

    def delete(self, generation_id: str) -> APIResponse[None]:
        """Delete a generation.
        
        Args:
            generation_id: The ID of the generation to delete
            
        Returns:
            Response metadata
            
        Raises:
            ErrorResponse: If the API request fails
        """
        response = self.client.delete(f"{self.base_url}/v1/generations/{generation_id}")
        if not response.ok:
            raise ErrorResponse(**response.json())
        return APIResponse[None](data=None) 
