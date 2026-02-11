"""
Pronounceable Password Generator - Easy to speak and remember passwords.
"""

import secrets
from .base import BaseGenerator, GeneratorResult


# Syllable components for pronounceable passwords
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
VOWELS = "aeiou"

# Common syllable patterns
SYLLABLE_PATTERNS = [
    "cv",   # consonant-vowel (ba, de, fi)
    "cvc",  # consonant-vowel-consonant (bat, den, fir)
    "vc",   # vowel-consonant (at, en, ir)
]


class PronounceableGenerator(BaseGenerator):
    """Generate pronounceable, easy-to-say passwords."""
    
    @property
    def generator_type(self) -> str:
        return "pronounceable"
    
    def generate_syllable(self) -> str:
        """Generate a single pronounceable syllable."""
        pattern = secrets.choice(SYLLABLE_PATTERNS)
        syllable = []
        
        for char in pattern:
            if char == 'c':
                syllable.append(secrets.choice(CONSONANTS))
            else:  # char == 'v'
                syllable.append(secrets.choice(VOWELS))
        
        return "".join(syllable)
    
    def generate(
        self,
        length: int = 12,
        capitalize_first: bool = True,
        add_number: bool = False
    ) -> GeneratorResult:
        """
        Generate a pronounceable password.
        
        Args:
            length: Approximate target length (default: 12)
            capitalize_first: Capitalize the first letter
            add_number: Add a random digit at the end
            
        Returns:
            GeneratorResult with pronounceable password
        """
        if length < 4:
            raise ValueError("Length must be at least 4")
        if length > 128:
            raise ValueError("Length must be at most 128")
        
        password = []
        
        # Generate syllables until we reach target length
        while len("".join(password)) < length:
            syllable = self.generate_syllable()
            password.append(syllable)
        
        result = "".join(password)
        
        # Trim to exact length
        result = result[:length]
        
        if capitalize_first:
            result = result.capitalize()
        
        if add_number:
            result = result[:-1] + secrets.choice("0123456789")
        
        # Calculate entropy
        # Average syllable has ~2.5 characters, pool size depends on pattern
        # Conservative estimate: 21 consonants * 5 vowels per syllable
        avg_syllable_entropy = 21 * 5  # ~105 combinations per syllable
        num_syllables = len(password)
        entropy_bits = self.calculate_entropy(avg_syllable_entropy, num_syllables)
        
        parameters = {
            "length": len(result),
            "target_length": length,
            "capitalize_first": capitalize_first,
            "add_number": add_number,
            "syllables": password,
            "pool_size": avg_syllable_entropy
        }
        
        return GeneratorResult(
            password=result,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
