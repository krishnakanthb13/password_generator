"""
Phonetic Generator - NATO phonetic alphabet conversion for passwords.
"""

from typing import Dict
from .base import BaseGenerator, GeneratorResult

NATO_MAP: Dict[str, str] = {
    'a': 'Alpha', 'b': 'Bravo', 'c': 'Charlie', 'd': 'Delta', 'e': 'Echo',
    'f': 'Foxtrot', 'g': 'Golf', 'h': 'Hotel', 'i': 'India', 'j': 'Juliett',
    'k': 'Kilo', 'l': 'Lima', 'm': 'Mike', 'n': 'November', 'o': 'Oscar',
    'p': 'Papa', 'q': 'Quebec', 'r': 'Romeo', 's': 'Sierra', 't': 'Tango',
    'u': 'Uniform', 'v': 'Victor', 'w': 'Whiskey', 'x': 'X-ray', 'y': 'Yankee',
    'z': 'Zulu',
    '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
    '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine',
}

class PhoneticGenerator(BaseGenerator):
    """Convert a password or generate a random phonetic sequence."""
    
    @property
    def generator_type(self) -> str:
        return "phonetic"
    
    def to_phonetic(self, text: str) -> str:
        """Convert a string to NATO phonetic alphabet."""
        result = []
        for char in text.lower():
            if char in NATO_MAP:
                result.append(NATO_MAP[char])
            else:
                result.append(char)
        return " ".join(result)
    
    def generate(
        self,
        text: str = "",
        length: int = 8
    ) -> GeneratorResult:
        """
        Generate a phonetic sequence.
        
        Args:
            text: Text to convert (if empty, generates a random sequence)
            length: Length of random sequence if 'text' is empty
            
        Returns:
            GeneratorResult with phonetic representation
        """
        if length < 4:
            raise ValueError("Sequence length must be at least 4")
        if length > 128:
            raise ValueError("Sequence length must be at most 128")
        import secrets
        import string
        
        is_generated = False
        if not text:
            is_generated = True
            # Generate random alphanumeric string first
            chars = string.ascii_lowercase + string.digits
            text = "".join(secrets.choice(chars) for _ in range(length))
            original = text
        else:
            original = text
            
        phonetic_text = self.to_phonetic(text)
        
        # Entropy is based on the original string length
        # Assuming only alphanumeric for random generation
        pool_size = 36 # 26 letters + 10 digits
        import math
        entropy_bits = length * math.log2(pool_size) if is_generated else 0
        
        parameters = {
            "original": original,
            "length": len(original),
        }
        
        return GeneratorResult(
            password=phonetic_text,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
