"""
License Key Generator - Software license keys with optional checksums.
Format: XXXX-XXXX-XXXX-XXXX
"""

import secrets
from .base import BaseGenerator, GeneratorResult


class LicenseKeyGenerator(BaseGenerator):
    """Generate software license keys in standard format."""
    
    # License keys typically use these characters (avoiding ambiguous ones)
    LICENSE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    
    @property
    def generator_type(self) -> str:
        return "license"
    
    def calculate_checksum(self, key_without_checksum: str) -> str:
        """Calculate a simple checksum character for validation."""
        total = sum(ord(c) for c in key_without_checksum if c.isalnum())
        index = total % len(self.LICENSE_CHARS)
        return self.LICENSE_CHARS[index]
    
    def generate(
        self,
        segments: int = 4,
        segment_length: int = 4,
        add_checksum: bool = False
    ) -> GeneratorResult:
        """
        Generate a license key.
        
        Args:
            segments: Number of segments (default: 4)
            segment_length: Characters per segment (default: 4)
            add_checksum: Add checksum character at end
            
        Returns:
            GeneratorResult with license key
        """
        if segments < 2:
            raise ValueError("Must have at least 2 segments")
        if segments > 8:
            raise ValueError("Must have at most 8 segments")
        if segment_length < 3:
            raise ValueError("Segment length must be at least 3")
        if segment_length > 6:
            raise ValueError("Segment length must be at most 6")
        
        # Generate segments
        key_segments = []
        for _ in range(segments):
            segment = "".join(
                secrets.choice(self.LICENSE_CHARS) 
                for _ in range(segment_length)
            )
            key_segments.append(segment)
        
        key = "-".join(key_segments)
        
        if add_checksum:
            checksum = self.calculate_checksum(key)
            key = f"{key}-{checksum}"
        
        # Calculate entropy
        total_chars = segments * segment_length
        pool_size = len(self.LICENSE_CHARS)
        entropy_bits = self.calculate_entropy(pool_size, total_chars)
        
        parameters = {
            "segments": segments,
            "segment_length": segment_length,
            "total_chars": total_chars,
            "add_checksum": add_checksum,
            "pool_size": pool_size
        }
        
        return GeneratorResult(
            password=key,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
