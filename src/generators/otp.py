"""
OTP Generator - TOTP/HOTP secret generation.
"""

import secrets
import base64
import hmac
import hashlib
import time
import struct
from .base import BaseGenerator, GeneratorResult


class OtpGenerator(BaseGenerator):
    """Generate TOTP/HOTP compatible secrets."""
    
    @property
    def generator_type(self) -> str:
        return "otp"
    
    def _generate_totp_code(
        self,
        secret_bytes: bytes,
        digits: int,
        period: int,
        algorithm: str
    ) -> str:
        """
        Generate the current TOTP code from secret bytes.
        
        Args:
            secret_bytes: The raw secret bytes
            digits: Number of digits (6 or 8)
            period: Time period in seconds
            algorithm: Hash algorithm
            
        Returns:
            Current OTP code as a string
        """
        # Calculate counter (number of periods since Unix epoch)
        counter = int(time.time() / period)
        
        # Pack counter into 8 bytes (big-endian)
        msg = struct.pack(">Q", counter)
        
        # Select hash algorithm
        hash_map = {
            "SHA1": hashlib.sha1,
            "SHA256": hashlib.sha256,
            "SHA512": hashlib.sha512
        }
        hash_func = hash_map.get(algorithm, hashlib.sha1)
        
        # Calculate HMAC
        hmac_hash = hmac.new(secret_bytes, msg, hash_func).digest()
        
        # Dynamic truncation
        # The last nibble of the hash is the offset
        offset = hmac_hash[-1] & 0x0F
        # Extract 4 bytes starting at offset
        truncated_hash = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7FFFFFFF
        
        # Convert to digits
        code = truncated_hash % (10 ** digits)
        
        # Pad with leading zeros
        return str(code).zfill(digits)

    def generate(
        self,
        digits: int = 6,
        period: int = 30,
        algorithm: str = "SHA1"
    ) -> GeneratorResult:
        """
        Generate an OTP secret and current code.
        
        Args:
            digits: OTP code length (6 or 8)
            period: TOTP time period in seconds
            algorithm: Hash algorithm (SHA1, SHA256, SHA512)
            
        Returns:
            GeneratorResult with current OTP code and secret metadata
        """
        if digits not in [6, 8]:
            raise ValueError("Digits must be 6 or 8")
        if period < 15 or period > 120:
            raise ValueError("Period must be between 15 and 120 seconds")
        if algorithm not in ["SHA1", "SHA256", "SHA512"]:
            raise ValueError("Algorithm must be SHA1, SHA256, or SHA512")
        
        # Generate raw bytes
        byte_lengths = {"SHA1": 20, "SHA256": 32, "SHA512": 64}
        byte_length = byte_lengths[algorithm]
        secret_bytes = secrets.token_bytes(byte_length)
        
        # Base32 encode the secret for authenticator apps
        secret_b32 = base64.b32encode(secret_bytes).decode('ascii').rstrip('=')
        
        # Generate the current TOTP code
        current_code = self._generate_totp_code(
            secret_bytes, digits, period, algorithm
        )
        
        # Generate otpauth URI for QR codes
        otpauth_uri = (
            f"otpauth://totp/PassForge:user@example.com"
            f"?secret={secret_b32}"
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
            "secret": secret_b32,
            "otpauth_uri": otpauth_uri,
            "pool_size": 2 ** (byte_length * 8)
        }
        
        return GeneratorResult(
            password=current_code,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
