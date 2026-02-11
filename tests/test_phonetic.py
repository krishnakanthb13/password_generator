"""
Unit tests for PhoneticGenerator.
"""

import unittest
from src.generators.phonetic import PhoneticGenerator

class TestPhoneticGenerator(unittest.TestCase):
    """Tests for PhoneticGenerator."""
    
    def setUp(self):
        self.generator = PhoneticGenerator()
    
    def test_basic_conversion(self):
        """Test basic character to phonetic conversion."""
        result = self.generator.generate(text="abc")
        self.assertEqual(result.password, "Alpha Bravo Charlie")
        
    def test_case_insensitivity(self):
        """Test that input case doesn't affect output standard."""
        result = self.generator.generate(text="AbC")
        self.assertEqual(result.password, "Alpha Bravo Charlie")
        
    def test_numbers_conversion(self):
        """Test number conversion."""
        result = self.generator.generate(text="123")
        self.assertEqual(result.password, "One Two Three")
        
    def test_mixed_content(self):
        """Test mixed content including unmapped characters."""
        # '!' is not in the map, should remain as is
        result = self.generator.generate(text="a1!")
        self.assertEqual(result.password, "Alpha One !")
        
    def test_random_generation(self):
        """Test random sequence generation when no text provided."""
        length = 5
        result = self.generator.generate(length=length)
        # Should result in 5 words
        words = result.password.split()
        self.assertEqual(len(words), length)
        # Check entropy is calculated
        self.assertGreater(result.entropy_bits, 0)

if __name__ == '__main__':
    unittest.main()
