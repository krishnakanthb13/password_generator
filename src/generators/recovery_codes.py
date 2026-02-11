"""
Recovery Codes Generator - 2FA backup recovery codes.
"""

import secrets
from typing import List
from .base import BaseGenerator, GeneratorResult
from .passphrase import DEFAULT_WORDLIST


class RecoveryCodesGenerator(BaseGenerator):
    """Generate 2FA recovery/backup codes."""
    
    @property
    def generator_type(self) -> str:
        return "recovery"
    
    def generate_numeric_code(self, digits: int = 8) -> str:
        """Generate a numeric recovery code."""
        return "".join(secrets.choice(self.DIGITS) for _ in range(digits))
    
    def generate_word_code(self, words: int = 3) -> str:
        """Generate a word-based recovery code."""
        short_words = [w for w in DEFAULT_WORDLIST if len(w) <= 6]
        selected = [secrets.choice(short_words) for _ in range(words)]
        return "-".join(selected)
    
    def generate(
        self,
        count: int = 10,
        use_words: bool = False,
            digits: int = 8,
            words_per_code: int = 3
        ) -> GeneratorResult:
        """
        Generate a set of recovery codes.
        
        Args:
            count: Number of codes (default: 10)
            use_words: Use word-based codes instead of numeric
            digits: Digits per numeric code (4-32, default: 8)
            words_per_code: Words per word-based code (2-12, default: 3)
            
        Returns:
            GeneratorResult with recovery codes
        """
        if count < 5:
            raise ValueError("Must generate at least 5 codes")
        if count > 100:
            raise ValueError("Must generate at most 100 codes")
        
        if not use_words:
            if digits < 4 or digits > 32:
                raise ValueError("Digits per code must be between 4 and 32")
        else:
            if words_per_code < 2 or words_per_code > 12:
                raise ValueError("Words per code must be between 2 and 12")
        
        codes: List[str] = []
        
        for _ in range(count):
            if use_words:
                code = self.generate_word_code(words_per_code)
            else:
                code = self.generate_numeric_code(digits)
            codes.append(code)
        
        # Format as newline-separated list
        password = "\n".join(codes)
        
        # Calculate entropy per code
        if use_words:
            short_words = [w for w in DEFAULT_WORDLIST if len(w) <= 6]
            pool_size = len(short_words)
            entropy_per_code = self.calculate_entropy(pool_size, words_per_code)
        else:
            entropy_per_code = self.calculate_entropy(10, digits)
        
        parameters = {
            "count": count,
            "use_words": use_words,
            "entropy_per_code": round(entropy_per_code, 2),
            "codes": codes,
            "pool_size": len(short_words) if use_words else 10
        }
        
        return GeneratorResult(
            password=password,
            entropy_bits=entropy_per_code,  # Per individual code
            generator_type=self.generator_type,
            parameters=parameters
        )
