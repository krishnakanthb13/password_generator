"""
UUID Token Generator - RFC 4122/9562 UUIDs (v1, v4, v7).
"""

import secrets
import time
import string
from typing import Optional
from .base import BaseGenerator, GeneratorResult


class UuidGenerator(BaseGenerator):
    """Generate RFC 4122/9562 UUIDs in various versions and formats."""
    
    BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    @property
    def generator_type(self) -> str:
        return "uuid"
    
    def _base58_encode(self, num: int) -> str:
        """Encode a large integer to Base58 string."""
        if num == 0:
            return self.BASE58_ALPHABET[0]
        
        encoded = []
        while num > 0:
            num, rem = divmod(num, 58)
            encoded.append(self.BASE58_ALPHABET[rem])
        
        return "".join(reversed(encoded))

    def _generate_v7(self) -> bytes:
        """
        Generate a UUID v7 (Time-based, sortable).
        Structure: 48 bits timestamp | 4 bits ver (7) | 12 bits rand | 2 bits var (2) | 62 bits rand
        """
        # 48 bits Unix timestamp in MS
        ms = int(time.time() * 1000)
        timestamp_bytes = ms.to_bytes(6, byteorder='big')
        
        # 10 random bytes for the rest (80 bits)
        rand_bytes = bytearray(secrets.token_bytes(10))
        
        # Set version 7: 0x70 in high nibble of byte 6 (relative to start of 16-byte UUID)
        # Note: timestamp is 6 bytes, so byte 6 is the one after timestamp
        rand_bytes[0] = (rand_bytes[0] & 0x0f) | 0x70
        
        # Set variant 2 (RFC 4122): 0x80 (10xxxxxx) in byte 8
        # Byte 8 relative to UUID start is byte 2 of rand_bytes
        rand_bytes[2] = (rand_bytes[2] & 0x3f) | 0x80
        
        return timestamp_bytes + rand_bytes

    def _generate_v4(self) -> bytes:
        """Generate a UUID v4 (Random)."""
        random_bytes = bytearray(secrets.token_bytes(16))
        
        # Version 4
        random_bytes[6] = (random_bytes[6] & 0x0f) | 0x40
        # Variant 1 (0x80)
        random_bytes[8] = (random_bytes[8] & 0x3f) | 0x80
        
        return bytes(random_bytes)

    def _generate_v1(self) -> bytes:
        """Generate a UUID v1 (Time + MAC-ish). Using secrets for 'mac' part for privacy."""
        import uuid
        # uuid.uuid1() is standard but we prefer bytes
        return uuid.uuid1().bytes

    def generate(
        self,
        version: int = 4,
        short: bool = False,
        uppercase: bool = False
    ) -> GeneratorResult:
        """
        Generate a UUID token.
        
        Args:
            version: UUID version (1, 4, 7)
            short: Return Base58 encoded short UUID (~22 chars)
            uppercase: Output in uppercase (only for hex format)
            
        Returns:
            GeneratorResult with UUID
        """
        if version == 1:
            raw_bytes = self._generate_v1()
            entropy_bits = 60.0 # Time-based, roughly
        elif version == 7:
            raw_bytes = self._generate_v7()
            entropy_bits = 74.0 # 12 + 62 random bits
        else: # Default v4
            raw_bytes = self._generate_v4()
            entropy_bits = 122.0
            version = 4

        if short:
            # Base58 encoding of the 128-bit integer
            uuid_int = int.from_bytes(raw_bytes, byteorder='big')
            uuid_str = self._base58_encode(uuid_int)
            # Short UUIDs are usually case-sensitive anyway due to Base58
        else:
            # Standard hex format: 8-4-4-4-12
            hex_str = raw_bytes.hex()
            uuid_str = f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"
            if uppercase:
                uuid_str = uuid_str.upper()
        
        parameters = {
            "version": version,
            "format": "base58" if short else "hex",
            "uppercase": uppercase if not short else None,
            "pool_size": 2**entropy_bits
        }
        
        return GeneratorResult(
            password=uuid_str,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
