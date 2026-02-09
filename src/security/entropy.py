"""
Entropy Calculator - Calculate and display password entropy.
"""

import math
from typing import Optional


class EntropyCalculator:
    """Calculate password entropy and strength metrics."""
    
    # Common character set sizes
    LOWERCASE_SIZE = 26
    UPPERCASE_SIZE = 26
    DIGITS_SIZE = 10
    SYMBOLS_SIZE = 32  # Common printable symbols
    
    # Strength thresholds (in bits)
    THRESHOLDS = {
        "very_weak": 28,
        "weak": 36,
        "reasonable": 60,
        "strong": 80,
        "very_strong": 128
    }
    
    @staticmethod
    def calculate_from_pool(pool_size: int, length: int) -> float:
        """
        Calculate entropy from known pool size and length.
        
        Args:
            pool_size: Number of possible characters in the pool
            length: Length of the password
            
        Returns:
            Entropy in bits
        """
        if pool_size <= 0 or length <= 0:
            return 0.0
        return length * math.log2(pool_size)
    
    @staticmethod
    def calculate_from_password(password: str) -> float:
        """
        Estimate entropy from an existing password by analyzing its composition.
        
        Note: This is an upper-bound estimate assuming uniform random selection.
        Real-world passwords may have lower effective entropy due to patterns.
        
        Args:
            password: The password to analyze
            
        Returns:
            Estimated entropy in bits
        """
        if not password:
            return 0.0
        
        pool_size = 0
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        if has_lower:
            pool_size += EntropyCalculator.LOWERCASE_SIZE
        if has_upper:
            pool_size += EntropyCalculator.UPPERCASE_SIZE
        if has_digit:
            pool_size += EntropyCalculator.DIGITS_SIZE
        if has_symbol:
            pool_size += EntropyCalculator.SYMBOLS_SIZE
        
        return EntropyCalculator.calculate_from_pool(pool_size, len(password))
    
    @staticmethod
    def get_strength_label(entropy_bits: float) -> str:
        """
        Get human-readable strength label.
        
        Args:
            entropy_bits: Entropy in bits
            
        Returns:
            Strength label string
        """
        if entropy_bits < EntropyCalculator.THRESHOLDS["very_weak"]:
            return "Very Weak [!]"
        elif entropy_bits < EntropyCalculator.THRESHOLDS["weak"]:
            return "Weak [-]"
        elif entropy_bits < EntropyCalculator.THRESHOLDS["reasonable"]:
            return "Reasonable [~]"
        elif entropy_bits < EntropyCalculator.THRESHOLDS["strong"]:
            return "Strong [+]"
        elif entropy_bits < EntropyCalculator.THRESHOLDS["very_strong"]:
            return "Very Strong [++]"
        else:
            return "Excellent [***]"
    
    @staticmethod
    def get_crack_time_estimate(entropy_bits: float, guesses_per_second: int = 10_000_000_000) -> str:
        """
        Estimate time to crack via brute force.
        
        Args:
            entropy_bits: Password entropy in bits
            guesses_per_second: Assumed attack speed (default: 10 billion/sec for GPU)
            
        Returns:
            Human-readable time estimate
        """
        if entropy_bits <= 0:
            return "Instant"
        
        # Total combinations = 2^entropy
        combinations = 2 ** entropy_bits
        # Average attempts = half of total
        seconds = (combinations / 2) / guesses_per_second
        
        if seconds < 1:
            return "< 1 second"
        elif seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.0f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.0f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.0f} days"
        elif seconds < 31536000 * 100:
            return f"{seconds/31536000:.0f} years"
        elif seconds < 31536000 * 1000000:
            return f"{seconds/31536000/1000:.0f} thousand years"
        elif seconds < 31536000 * 1000000000:
            return f"{seconds/31536000/1000000:.0f} million years"
        else:
            return "Billions of years"
    
    @staticmethod
    def format_entropy_report(
        password: str,
        entropy_bits: float,
        pool_size: Optional[int] = None
    ) -> str:
        """
        Generate a formatted entropy report.
        
        Args:
            password: The generated password
            entropy_bits: Calculated entropy
            pool_size: Optional pool size used
            
        Returns:
            Formatted report string
        """
        strength = EntropyCalculator.get_strength_label(entropy_bits)
        crack_time = EntropyCalculator.get_crack_time_estimate(entropy_bits)
        
        lines = [
            f"+{'-' * 50}+",
            f"| {'Entropy Report':^48} |",
            f"+{'-' * 50}+",
            f"| Length:        {len(password):>32} |",
            f"| Entropy:       {entropy_bits:>28.2f} bits |",
            f"| Strength:      {strength:>32} |",
            f"| Crack Time:    {crack_time:>32} |",
        ]
        
        if pool_size:
            lines.append(f"| Pool Size:     {pool_size:>32} |")
        
        lines.append(f"+{'-' * 50}+")
        
        return "\n".join(lines)
