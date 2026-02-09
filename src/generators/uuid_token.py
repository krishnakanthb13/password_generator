"""
UUID Token Generator - RFC 4122 v4 random UUIDs.
"""

import secrets
from .base import BaseGenerator, GeneratorResult


class UuidGenerator(BaseGenerator):
    """Generate RFC 4122 version 4 (random) UUIDs."""
    
    @property
    def generator_type(self) -> str:
        return "uuid"
    
    def generate(
        self,
        uppercase: bool = False
    ) -> GeneratorResult:
        """
        Generate a UUID v4 token.
        
        Args:
            uppercase: Output in uppercase
            
        Returns:
            GeneratorResult with UUID
        """
        # Generate 16 random bytes
        random_bytes = secrets.token_bytes(16)
        
        # Set version (4) and variant bits per RFC 4122
        random_list = list(random_bytes)
        random_list[6] = (random_list[6] & 0x0f) | 0x40  # Version 4
        random_list[8] = (random_list[8] & 0x3f) | 0x80  # Variant 1
        
        # Format as UUID string
        hex_str = bytes(random_list).hex()
        uuid_str = f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"
        
        if uppercase:
            uuid_str = uuid_str.upper()
        
        # UUID v4 entropy: 122 random bits (128 - 6 fixed version/variant bits)
        entropy_bits = 122.0
        
        parameters = {
            "version": 4,
            "uppercase": uppercase,
            "pool_size": 2**122
        }
        
        return GeneratorResult(
            password=uuid_str,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
