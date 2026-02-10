"""
Entropy Calculator - Calculate and display password entropy.
"""

import math
from typing import Optional
from ..generators.base import BaseGenerator


class EntropyCalculator:
    """Calculate password entropy and strength metrics."""
    
    
    # Strength thresholds (in bits)
    THRESHOLDS = {
        "very_weak": 28,
        "weak": 36,
        "reasonable": 60,
        "strong": 80,
        "very_strong": 128
    }
    
    # Extended pool for unknown printable characters
    ASCII_EXTENDED_POOL = 95
    
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
        has_lower = False
        has_upper = False
        has_digit = False
        has_symbol = False
        others = 0
        
        # Single-pass analysis for improved efficiency
        for char in password:
            if char in BaseGenerator.LOWERCASE:
                has_lower = True
            elif char in BaseGenerator.UPPERCASE:
                has_upper = True
            elif char in BaseGenerator.DIGITS:
                has_digit = True
            elif char in BaseGenerator.SYMBOLS:
                has_symbol = True
            else:
                others += 1
        
        if has_lower:
            pool_size += len(BaseGenerator.LOWERCASE)
        if has_upper:
            pool_size += len(BaseGenerator.UPPERCASE)
        if has_digit:
            pool_size += len(BaseGenerator.DIGITS)
        if has_symbol:
            pool_size += len(BaseGenerator.SYMBOLS)
        
        if others > 0:
            # If characters outside standard pools are used, 
            # assume at least the full printable ASCII range (95)
            # but don't double count if we already calculated more.
            pool_size = max(pool_size, EntropyCalculator.ASCII_EXTENDED_POOL)
            
        entropy = EntropyCalculator.calculate_from_pool(pool_size, len(password))
        return entropy, pool_size
    
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
        pool_size: Optional[int] = None,
        colorized_password: Optional[str] = None
    ) -> str:
        """
        Generate a formatted entropy report.
        """
        strength = EntropyCalculator.get_strength_label(entropy_bits)
        crack_time = EntropyCalculator.get_crack_time_estimate(entropy_bits)
        
        # Calculate report width
        width = 50
        
        display_password = colorized_password if colorized_password else password
        
        lines = [
            "",
            display_password,
            "",
            f"+{'-' * width}+",
            f"| {'Entropy Report':^{width-2}} |",
            f"+{'-' * width}+",
            f"| Length:        {len(password):>{width-18}} |",
            f"| Entropy:       {entropy_bits:>{width-22}.2f} bits |",
            f"| Strength:      {strength:>{width-18}} |",
            f"| Crack Time:    {crack_time:>{width-18}} |",
        ]
        
        if pool_size:
            lines.append(f"| Pool Size:     {pool_size:>{width-18}} |")
        
        lines.append(f"+{'-' * width}+")
        
        return "\n".join(lines)
