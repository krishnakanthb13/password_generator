"""
Leetspeak Passphrase Generator - Word-based with character substitution.
Example: C0nju64t3d-Int3r8r3d-dAmm1t5
"""

import secrets
from typing import Dict
from .base import BaseGenerator, GeneratorResult
from .passphrase import DEFAULT_WORDLIST


# Leetspeak substitution map
LEET_MAP: Dict[str, str] = {
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7',
    'b': '8', 'B': '8',
    'g': '6', 'G': '6',
}


class LeetspeakGenerator(BaseGenerator):
    """Generate leetspeak passphrases with character substitution."""
    
    @property
    def generator_type(self) -> str:
        return "leetspeak"
    
    def to_leetspeak(self, word: str) -> str:
        """Convert a word to leetspeak with partial substitution."""
        result = []
        for char in word:
            # Only substitute with a 50% probability for better readability
            if char in LEET_MAP and secrets.randbelow(100) < 50:
                result.append(LEET_MAP[char])
            else:
                result.append(char)
        return "".join(result)
    
    def generate(
        self,
        word_count: int = 3,
        separator: str = "-",
        capitalize: bool = True
    ) -> GeneratorResult:
        """
        Generate a leetspeak passphrase.
        
        Args:
            word_count: Number of words (default: 3)
            separator: Word separator (- _ . ,)
            capitalize: Capitalize words before leetspeak conversion
            
        Returns:
            GeneratorResult with leetspeak passphrase
        """
        if word_count < 2:
            raise ValueError("Word count must be at least 2")
        if word_count > 64:
            raise ValueError("Word count must be at most 64")
        if separator not in ["-", "_", ".", ","]:
            raise ValueError("Separator must be one of: - _ . ,")
        
        # Filter longer words for better readability
        wordlist = [w for w in DEFAULT_WORDLIST if 5 <= len(w) <= 10]
        
        # Select random words
        words = [secrets.choice(wordlist) for _ in range(word_count)]
        
        # Capitalize if requested
        if capitalize:
            words = [w.capitalize() for w in words]
        
        # Convert to leetspeak
        leet_words = [self.to_leetspeak(w) for w in words]
        
        passphrase = separator.join(leet_words)
        
        # Entropy calculation (still based on wordlist size)
        pool_size = len(wordlist)
        entropy_bits = self.calculate_entropy(pool_size, word_count)
        
        parameters = {
            "word_count": word_count,
            "separator": separator,
            "capitalize": capitalize,
            "pool_size": pool_size,
            "original_words": words
        }
        
        return GeneratorResult(
            password=passphrase,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
