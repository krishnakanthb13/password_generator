"""
JWT Secret Generator - High-entropy secrets for JWT signing.
"""

import secrets
import base64
from .base import BaseGenerator, GeneratorResult


class JwtSecretGenerator(BaseGenerator):
    """Generate secrets suitable for JWT signing (HS256, HS384, HS512)."""
    
    @property
    def generator_type(self) -> str:
        return "jwt"
    
    def generate(
        self,
        bits: int = 256,
        output_hex: bool = False
    ) -> GeneratorResult:
        """
        Generate a JWT signing secret.
        
        Args:
            bits: Secret size in bits (256, 384, or 512)
            output_hex: Output as hex instead of base64
            
        Returns:
            GeneratorResult with JWT secret
        """
        if bits not in [256, 384, 512]:
            raise ValueError("Bits must be 256, 384, or 512")
        
        byte_length = bits // 8
        random_bytes = secrets.token_bytes(byte_length)
        
        if output_hex:
            secret = random_bytes.hex()
        else:
            secret = base64.urlsafe_b64encode(random_bytes).decode('ascii').rstrip('=')
        
        # Map to algorithm names
        algorithm = {256: "HS256", 384: "HS384", 512: "HS512"}[bits]
        
        parameters = {
            "bits": bits,
            "bytes": byte_length,
            "algorithm": algorithm,
            "output_format": "hex" if output_hex else "base64",
            "pool_size": 2 ** bits
        }
        
        return GeneratorResult(
            password=secret,
            entropy_bits=float(bits),
            generator_type=self.generator_type,
            parameters=parameters
        )
