"""
Random Password Generator - Core alphanumeric + symbols password generation.
"""

import secrets
from typing import Optional, Set
from .base import BaseGenerator, GeneratorResult


class RandomPasswordGenerator(BaseGenerator):
    """
    Generate cryptographically secure random passwords.
    
    Supports configurable:
    - Length (default: 16)
    - Character sets (uppercase, lowercase, digits, symbols)
    - Custom include/exclude characters
    - Repetition control
    """
    
    @property
    def generator_type(self) -> str:
        return "random"
    
    def generate(
        self,
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        digits: bool = True,
        symbols: bool = True,
        include_chars: str = "",
        exclude_chars: str = "",
        no_repeats: bool = False,
        min_uppercase: int = 0,
        min_lowercase: int = 0,
        min_digits: int = 0,
        min_symbols: int = 0
    ) -> GeneratorResult:
        """
        Generate a random password.
        
        Args:
            length: Password length (default: 16)
            uppercase: Include uppercase letters
            lowercase: Include lowercase letters
            digits: Include digits
            symbols: Include symbols
            include_chars: Additional characters to include
            exclude_chars: Characters to exclude
            no_repeats: Prevent character repetition
            min_uppercase: Minimum uppercase characters required
            min_lowercase: Minimum lowercase characters required
            min_digits: Minimum digits required
            min_symbols: Minimum symbols required
            
        Returns:
            GeneratorResult with password and metadata
        """
        # Build character pool
        charset = ""
        
        if uppercase:
            charset += self.UPPERCASE
        if lowercase:
            charset += self.LOWERCASE
        if digits:
            charset += self.DIGITS
        if symbols:
            charset += self.SYMBOLS
        
        # Add custom characters
        charset += include_chars
        
        # Remove excluded characters
        charset = "".join(c for c in charset if c not in exclude_chars)
        
        # Apply easy_read/easy_say filters
        charset = self.filter_charset(charset)
        
        # Remove duplicates while preserving order
        charset = "".join(dict.fromkeys(charset))
        
        if not charset:
            raise ValueError("No characters available in the pool after filtering")
        
        if no_repeats and length > len(charset):
            raise ValueError(
                f"Cannot generate {length} unique characters from pool of {len(charset)}"
            )
        
        # Validate minimum requirements
        total_min = min_uppercase + min_lowercase + min_digits + min_symbols
        if total_min > length:
            raise ValueError(
                f"Minimum requirements ({total_min}) exceed password length ({length})"
            )
        
        # Generate password with minimum requirements
        password_chars = []
        
        # Add required characters first
        if min_uppercase > 0:
            available = self.filter_charset(self.UPPERCASE)
            available = "".join(c for c in available if c not in exclude_chars)
            password_chars.extend(secrets.choice(available) for _ in range(min_uppercase))
        
        if min_lowercase > 0:
            available = self.filter_charset(self.LOWERCASE)
            available = "".join(c for c in available if c not in exclude_chars)
            password_chars.extend(secrets.choice(available) for _ in range(min_lowercase))
        
        if min_digits > 0:
            available = self.filter_charset(self.DIGITS)
            available = "".join(c for c in available if c not in exclude_chars)
            password_chars.extend(secrets.choice(available) for _ in range(min_digits))
        
        if min_symbols > 0:
            available = self.filter_charset(self.SYMBOLS)
            available = "".join(c for c in available if c not in exclude_chars)
            password_chars.extend(secrets.choice(available) for _ in range(min_symbols))
        
        # Fill remaining length
        remaining = length - len(password_chars)
        
        if no_repeats:
            # Remove already used characters
            available = [c for c in charset if c not in password_chars]
            password_chars.extend(
                secrets.choice(available) for _ in range(remaining)
            )
        else:
            # Allow repeats
            password_chars.extend(
                secrets.choice(charset) for _ in range(remaining)
            )
        
        # Shuffle to randomize position of required chars
        shuffled = list(password_chars)
        for i in range(len(shuffled) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        
        password = "".join(shuffled)
        
        # Calculate entropy
        pool_size = len(charset)
        entropy_bits = self.calculate_entropy(pool_size, length)
        
        # Store parameters for logging
        parameters = {
            "length": length,
            "uppercase": uppercase,
            "lowercase": lowercase,
            "digits": digits,
            "symbols": symbols,
            "include_chars": include_chars if include_chars else None,
            "exclude_chars": exclude_chars if exclude_chars else None,
            "no_repeats": no_repeats,
            "min_uppercase": min_uppercase,
            "min_lowercase": min_lowercase,
            "min_digits": min_digits,
            "min_symbols": min_symbols,
            "pool_size": pool_size,
            "easy_read": self.easy_read,
            "easy_say": self.easy_say
        }
        
        return GeneratorResult(
            password=password,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
    
    def generate_batch(
        self,
        count: int = 5,
        **kwargs
    ) -> list[GeneratorResult]:
        """
        Generate multiple passwords with the same settings.
        
        Args:
            count: Number of passwords to generate
            **kwargs: Arguments passed to generate()
            
        Returns:
            List of GeneratorResult objects
        """
        return [self.generate(**kwargs) for _ in range(count)]
