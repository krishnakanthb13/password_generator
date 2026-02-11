"""
Base64 Secret Generator - URL-safe base64-encoded random secrets.
"""

import secrets
import base64
from .base import BaseGenerator, GeneratorResult


class Base64SecretGenerator(BaseGenerator):
    """Generate base64-encoded random secrets for APIs and configs."""
    
    @property
    def generator_type(self) -> str:
        return "base64"
    
    def generate(
        self,
        byte_length: int = 32,
        url_safe: bool = True
    ) -> GeneratorResult:
        """
        Generate a base64-encoded secret.
        
        Args:
            byte_length: Number of random bytes (default: 32)
            url_safe: Use URL-safe encoding (default: True)
            
        Returns:
            GeneratorResult with base64 secret
        """
        if byte_length < 8:
            raise ValueError("Byte length must be at least 8")
        if byte_length > 1024:
            raise ValueError("Byte length must be at most 1024")
        
        random_bytes = secrets.token_bytes(byte_length)
        
        if url_safe:
            # URL-safe base64 (replaces + with - and / with _)
            secret = base64.urlsafe_b64encode(random_bytes).decode('ascii').rstrip('=')
        else:
            secret = base64.b64encode(random_bytes).decode('ascii')
        
        # Entropy is simply byte_length * 8 bits
        entropy_bits = byte_length * 8.0
        
        parameters = {
            "byte_length": byte_length,
            "url_safe": url_safe,
            "pool_size": 2 ** (byte_length * 8)
        }
        
        return GeneratorResult(
            password=secret,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
