"""
OTP Generator - TOTP/HOTP secret generation.
"""

import secrets
import base64
from .base import BaseGenerator, GeneratorResult


class OtpGenerator(BaseGenerator):
    """Generate TOTP/HOTP compatible secrets."""
    
    @property
    def generator_type(self) -> str:
        return "otp"
    
    def generate(
        self,
        digits: int = 6,
        period: int = 30,
        algorithm: str = "SHA1"
    ) -> GeneratorResult:
        """
        Generate an OTP secret.
        
        Args:
            digits: OTP code length (6 or 8)
            period: TOTP time period in seconds
            algorithm: Hash algorithm (SHA1, SHA256, SHA512)
            
        Returns:
            GeneratorResult with OTP secret
        """
        if digits not in [6, 8]:
            raise ValueError("Digits must be 6 or 8")
        if period < 15 or period > 120:
            raise ValueError("Period must be between 15 and 120 seconds")
        if algorithm not in ["SHA1", "SHA256", "SHA512"]:
            raise ValueError("Algorithm must be SHA1, SHA256, or SHA512")
        
        # Generate 20 bytes (160 bits) for SHA1, more for others
        byte_lengths = {"SHA1": 20, "SHA256": 32, "SHA512": 64}
        byte_length = byte_lengths[algorithm]
        
        secret_bytes = secrets.token_bytes(byte_length)
        
        # Base32 encode for compatibility with authenticator apps
        secret = base64.b32encode(secret_bytes).decode('ascii').rstrip('=')
        
        # Generate otpauth URI for QR codes
        # Format: otpauth://totp/PassForge:user@example.com?secret=XXX&issuer=PassForge
        otpauth_uri = (
            f"otpauth://totp/PassForge:user@example.com"
            f"?secret={secret}"
            f"&issuer=PassForge"
            f"&algorithm={algorithm}"
            f"&digits={digits}"
            f"&period={period}"
        )
        
        entropy_bits = byte_length * 8.0
        
        parameters = {
            "digits": digits,
            "period": period,
            "algorithm": algorithm,
            "secret": secret,
            "otpauth_uri": otpauth_uri,
            "pool_size": 2 ** (byte_length * 8)
        }
        
        return GeneratorResult(
            password=secret,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
