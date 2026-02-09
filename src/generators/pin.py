"""
PIN Generator - Numeric PIN generation.
"""

import secrets
from .base import BaseGenerator, GeneratorResult


class PinGenerator(BaseGenerator):
    """Generate numeric PINs."""
    
    @property
    def generator_type(self) -> str:
        return "pin"
    
    def generate(
        self,
        length: int = 6
    ) -> GeneratorResult:
        """
        Generate a numeric PIN.
        
        Args:
            length: PIN length (default: 6)
            
        Returns:
            GeneratorResult with PIN and metadata
        """
        if length < 4:
            raise ValueError("PIN length must be at least 4")
        if length > 20:
            raise ValueError("PIN length must be at most 20")
        
        pin = "".join(secrets.choice(self.DIGITS) for _ in range(length))
        
        entropy_bits = self.calculate_entropy(10, length)
        
        parameters = {
            "length": length,
            "pool_size": 10
        }
        
        return GeneratorResult(
            password=pin,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
