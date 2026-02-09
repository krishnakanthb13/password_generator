"""
Base Generator - Abstract base class for all password generators.
All generators must implement the generate() method.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
import math


@dataclass
class GeneratorResult:
    """Result object returned by all generators."""
    password: str
    entropy_bits: float
    generator_type: str
    parameters: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        return {
            "password": self.password,
            "entropy_bits": round(self.entropy_bits, 2),
            "generator_type": self.generator_type,
            "parameters": self.parameters
        }


class BaseGenerator(ABC):
    """Abstract base class for all password generators."""
    
    # Character sets for common use
    LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS = "0123456789"
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
    
    # Ambiguous characters (for --easy-read mode)
    AMBIGUOUS = "0O1lI|"
    
    # Hard to pronounce (for --easy-say mode)
    HARD_TO_SAY = "0O1lI|!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
    
    def __init__(self, easy_read: bool = False, easy_say: bool = False):
        """
        Initialize base generator with global modifiers.
        
        Args:
            easy_read: Remove ambiguous characters (0/O, 1/l/I)
            easy_say: Only pronounceable characters
        """
        self.easy_read = easy_read
        self.easy_say = easy_say
    
    @property
    @abstractmethod
    def generator_type(self) -> str:
        """Return the type name of this generator."""
        pass
    
    @abstractmethod
    def generate(self, **kwargs) -> GeneratorResult:
        """
        Generate a password/secret.
        
        Returns:
            GeneratorResult with password and metadata
        """
        pass
    
    def filter_charset(self, charset: str) -> str:
        """Apply easy_read and easy_say filters to a character set."""
        if self.easy_say:
            charset = "".join(c for c in charset if c not in self.HARD_TO_SAY)
        elif self.easy_read:
            charset = "".join(c for c in charset if c not in self.AMBIGUOUS)
        return charset
    
    @staticmethod
    def calculate_entropy(pool_size: int, length: int) -> float:
        """
        Calculate entropy in bits.
        
        Formula: entropy = length * log2(pool_size)
        
        Args:
            pool_size: Number of possible characters
            length: Length of the password
            
        Returns:
            Entropy in bits
        """
        if pool_size <= 0 or length <= 0:
            return 0.0
        return length * math.log2(pool_size)
    
    @staticmethod
    def get_strength_label(entropy_bits: float) -> str:
        """
        Get human-readable strength label based on entropy.
        
        Based on NIST guidelines and common security practices.
        """
        if entropy_bits < 28:
            return "Very Weak"
        elif entropy_bits < 36:
            return "Weak"
        elif entropy_bits < 60:
            return "Reasonable"
        elif entropy_bits < 80:
            return "Strong"
        elif entropy_bits < 128:
            return "Very Strong"
        else:
            return "Excellent"
