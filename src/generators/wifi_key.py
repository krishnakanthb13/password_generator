"""
WiFi Key Generator - WPA2/WPA3 compatible keys.
"""

import secrets
from .base import BaseGenerator, GeneratorResult


class WifiKeyGenerator(BaseGenerator):
    """Generate WiFi/WPA compatible keys (8-63 characters)."""
    
    @property
    def generator_type(self) -> str:
        return "wifi"
    
    def generate(
        self,
        length: int = 16,
        simple: bool = False
    ) -> GeneratorResult:
        """
        Generate a WiFi/WPA key.
        
        Args:
            length: Key length (8-63, default: 16)
            simple: Use only alphanumeric (no symbols)
            
        Returns:
            GeneratorResult with WiFi key
        """
        if length < 8:
            raise ValueError("WiFi key must be at least 8 characters")
        if length > 63:
            raise ValueError("WiFi key must be at most 63 characters")
        
        if simple:
            charset = self.LOWERCASE + self.UPPERCASE + self.DIGITS
        else:
            # WPA allows printable ASCII (32-126) but we use a safer subset
            charset = self.LOWERCASE + self.UPPERCASE + self.DIGITS + "!@#$%&*-_=+"
        
        # Apply easy_read filter if set
        charset = self.filter_charset(charset)
        
        key = "".join(secrets.choice(charset) for _ in range(length))
        
        pool_size = len(charset)
        entropy_bits = self.calculate_entropy(pool_size, length)
        
        parameters = {
            "length": length,
            "simple": simple,
            "pool_size": pool_size,
            "wpa_compatible": True
        }
        
        return GeneratorResult(
            password=key,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
