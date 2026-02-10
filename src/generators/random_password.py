"""
Random Password Generator - Core alphanumeric + symbols password generation.
"""

import secrets
import math
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
        min_symbols: int = 0,
        balanced: bool = False,
        custom_seed: Optional[str] = None
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
            balanced: Enable balanced ratio (60% letters, 20% digits, 20% symbols)
            
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
        
        def pick_from_pool(source_charset):
            available = self.filter_charset(source_charset)
            available = "".join(c for c in available if c not in exclude_chars)
            
            if not available:
                raise ValueError("No available characters after filtering exclude_chars")
                
            if no_repeats:
                # Filter out already used characters
                remaining_available = [c for c in available if c not in password_chars]
                if not remaining_available:
                    raise ValueError("Pool exhausted for unique character requirement")
                char = secrets.choice(remaining_available)
            else:
                char = secrets.choice(available)
            return char

        # Add required characters first
        if min_uppercase > 0:
            for _ in range(min_uppercase):
                password_chars.append(pick_from_pool(self.UPPERCASE))
        
        if min_lowercase > 0:
            for _ in range(min_lowercase):
                password_chars.append(pick_from_pool(self.LOWERCASE))
        
        if min_digits > 0:
            for _ in range(min_digits):
                password_chars.append(pick_from_pool(self.DIGITS))
        
        if min_symbols > 0:
            for _ in range(min_symbols):
                password_chars.append(pick_from_pool(self.SYMBOLS))
        
        # Fill remaining length
        remaining = length - len(password_chars)
        
        if remaining > 0:
            if balanced and not no_repeats:
                # Balanced Mode (Ratio-based filling)
                # 60% Letters, 20% Digits, 20% Symbols
                letter_pool = ""
                if uppercase: letter_pool += self.UPPERCASE
                if lowercase: letter_pool += self.LOWERCASE
                letter_pool = self.filter_charset(letter_pool)
                letter_pool = "".join(c for c in letter_pool if c not in exclude_chars)
                
                digit_pool = self.filter_charset(self.DIGITS)
                digit_pool = "".join(c for c in digit_pool if c not in exclude_chars)
                
                symbol_pool = self.filter_charset(self.SYMBOLS)
                symbol_pool = "".join(c for c in symbol_pool if c not in exclude_chars)

                for _ in range(remaining):
                    # Randomly choose which pool based on weights
                    # Weighting: 60 Letter, 20 Digit, 20 Symbol
                    # Adjust if some pools are empty
                    weights = []
                    pools = []
                    if letter_pool: 
                        pools.append(letter_pool)
                        weights.append(60)
                    if digit_pool: 
                        pools.append(digit_pool)
                        weights.append(20)
                    if symbol_pool: 
                        pools.append(symbol_pool)
                        weights.append(20)
                    
                    if not pools:
                        # Fallback to general charset if specific pools are empty
                        password_chars.append(secrets.choice(charset))
                        continue

                    # Redistribute weights if some pools are missing
                    # If symbols are missing, give 10 to letters and 10 to digits
                    # If digits are missing, give 10 to letters and 10 to symbols
                    if len(pools) < 3:
                        total_missing_weight = 100 - sum(weights)
                        if letter_pool:
                            # Letters take the lion's share of missing weights
                            idx = [i for i, p in enumerate(pools) if p == letter_pool][0]
                            weights[idx] += total_missing_weight
                        else:
                            # Divide equally among remaining
                            extra = total_missing_weight // len(weights)
                            for i in range(len(weights)):
                                weights[i] += extra

                    # Manual weighted choice (secrets.choice doesn't support weights directly)
                    total_weight = sum(weights)
                    r = secrets.randbelow(total_weight)
                    upto = 0
                    for pool, weight in zip(pools, weights):
                        if upto + weight > r:
                            password_chars.append(secrets.choice(pool))
                            break
                        upto += weight
            elif no_repeats:
                # Use proper unique selection - remove used chars and sample
                available = [c for c in charset if c not in password_chars]
                # Sample unique characters one by one
                for _ in range(remaining):
                    if available:
                        idx = secrets.randbelow(len(available))
                        chosen = available.pop(idx)
                        password_chars.append(chosen)
                    else:
                        raise ValueError("Pool exhausted for unique remaining characters")
            else:
                # Allow repeats (standard mode)
                password_chars.extend(
                    secrets.choice(charset) for _ in range(remaining)
                )
        
        # Shuffle to randomize position of required chars
        shuffled = list(password_chars)
        
        if custom_seed:
            # PARANOID MODE: Use custom seed for an extra shuffle layer
            import random
            rng = random.Random(custom_seed)
            rng.shuffle(shuffled)
        else:
            # Standard secure shuffle using secrets
            for i in range(len(shuffled) - 1, 0, -1):
                j = secrets.randbelow(i + 1)
                shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        
        password = "".join(shuffled)
        
        # Calculate entropy
        pool_size = len(charset)
        if no_repeats:
            # For sampling without replacement, the number of possibilities is
            # permutations P(pool_size, length) = pool_size! / (pool_size - length)!
            # entropy = log2(P(pool_size, length))
            # We use lgamma for stable computation of log2(n!): log2(n!) = lgamma(n+1) / log(2)
            entropy_bits = (math.lgamma(pool_size + 1) - math.lgamma(pool_size - length + 1)) / math.log(2)
        else:
            # Standard entropy for sampling with replacement
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
            "balanced": balanced,
            "pool_size": pool_size,
            "easy_read": self.easy_read,
            "easy_say": self.easy_say,
            "paranoid": custom_seed is not None
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
