"""
Prim Voices API Python Client

A Python client for interacting with the Prim Voices API.
"""

import requests

from .voices import VoicesAPI
from .generations import GenerationsAPI
from .models import GenerationResponse, VoiceResponse

class Client:
    """Main client for the Prim Voices API."""

    def __init__(self, api_key: str):
        """Initialize the Prim Voices API client.
        
        Args:
            api_key: API key for the API client
        """
        self.api_key = api_key
        self.base_url = "https://api.primvoices.com"
        
        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        
        # Initialize API resources
        self.voices = VoicesAPI(self.session, self.base_url)
        self.generations = GenerationsAPI(self.session, self.base_url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the client session."""
        self.session.close() 
