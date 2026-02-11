"""
Unit tests for PassForge password generators.
"""

import unittest
import re
from src.generators.random_password import RandomPasswordGenerator
from src.generators.passphrase import PassphraseGenerator
from src.generators.leetspeak import LeetspeakGenerator
from src.generators.pin import PinGenerator
from src.generators.pronounceable import PronounceableGenerator
from src.generators.uuid_token import UuidGenerator
from src.generators.base64_secret import Base64SecretGenerator
from src.generators.jwt_secret import JwtSecretGenerator
from src.generators.wifi_key import WifiKeyGenerator
from src.generators.license_key import LicenseKeyGenerator
from src.generators.recovery_codes import RecoveryCodesGenerator
from src.generators.otp import OtpGenerator
from src.generators.pattern import PatternGenerator
from src.security.entropy import EntropyCalculator


class TestRandomPasswordGenerator(unittest.TestCase):
    """Tests for RandomPasswordGenerator."""
    
    def setUp(self):
        self.generator = RandomPasswordGenerator()
    
    def test_default_length(self):
        """Test default password length is 16."""
        result = self.generator.generate()
        self.assertEqual(len(result.password), 16)
    
    def test_custom_length(self):
        """Test custom password length."""
        result = self.generator.generate(length=24)
        self.assertEqual(len(result.password), 24)

    def test_extreme_lengths(self):
        """Test extreme password length constraints (Min: 4, Max: 1024)."""
        # Minimum
        res_min = self.generator.generate(length=4)
        self.assertEqual(len(res_min.password), 4)

        # Middle
        res_mid = self.generator.generate(length=512)
        self.assertEqual(len(res_mid.password), 512)

        # Maximum
        res_max = self.generator.generate(length=1024)
        self.assertEqual(len(res_max.password), 1024)

    def test_invalid_lengths(self):
        """Test that invalid lengths raise ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(length=3)
        with self.assertRaises(ValueError):
            self.generator.generate(length=1025)
    
    def test_no_uppercase(self):
        """Test excluding uppercase letters."""
        result = self.generator.generate(uppercase=False)
        self.assertFalse(any(c.isupper() for c in result.password))
    
    def test_no_lowercase(self):
        """Test excluding lowercase letters."""
        result = self.generator.generate(lowercase=False)
        self.assertFalse(any(c.islower() for c in result.password))
    
    def test_no_digits(self):
        """Test excluding digits."""
        result = self.generator.generate(digits=False)
        self.assertFalse(any(c.isdigit() for c in result.password))
    
    def test_no_symbols(self):
        """Test excluding symbols."""
        result = self.generator.generate(symbols=False)
        self.assertTrue(result.password.isalnum())
    
    def test_minimum_requirements(self):
        """Test minimum character requirements."""
        result = self.generator.generate(
            length=20,
            min_uppercase=3,
            min_lowercase=3,
            min_digits=3,
            min_symbols=3
        )
        self.assertGreaterEqual(sum(1 for c in result.password if c.isupper()), 3)
        self.assertGreaterEqual(sum(1 for c in result.password if c.islower()), 3)
        self.assertGreaterEqual(sum(1 for c in result.password if c.isdigit()), 3)
    
    def test_no_repeats(self):
        """Test no repeated characters."""
        result = self.generator.generate(length=20, no_repeats=True)
        self.assertEqual(len(result.password), len(set(result.password)))
    
    def test_entropy_positive(self):
        """Test entropy is calculated and positive."""
        result = self.generator.generate()
        self.assertGreater(result.entropy_bits, 0)
    
    def test_easy_read_mode(self):
        """Test easy-read mode excludes ambiguous characters."""
        gen = RandomPasswordGenerator(easy_read=True)
        result = gen.generate(length=50)
        ambiguous = '0O1lI'
        self.assertFalse(any(c in ambiguous for c in result.password))


class TestPassphraseGenerator(unittest.TestCase):
    """Tests for PassphraseGenerator."""
    
    def setUp(self):
        self.generator = PassphraseGenerator()
    
    def test_default_word_count(self):
        """Test default 4 words."""
        result = self.generator.generate()
        words = result.password.split('-')
        self.assertEqual(len(words), 4)
    
    def test_custom_word_count(self):
        """Test custom word count."""
        result = self.generator.generate(word_count=6)
        words = result.password.split('-')
        self.assertEqual(len(words), 6)

    def test_extreme_word_counts(self):
        """Test extreme word count constraints (Min: 2, Max: 64)."""
        # Minimum
        res_min = self.generator.generate(word_count=2)
        self.assertEqual(len(res_min.password.split('-')), 2)

        # Middle
        res_mid = self.generator.generate(word_count=33)
        self.assertEqual(len(res_mid.password.split('-')), 33)

        # Maximum
        res_max = self.generator.generate(word_count=64)
        self.assertEqual(len(res_max.password.split('-')), 64)
    
    def test_custom_separator(self):
        """Test custom separator."""
        result = self.generator.generate(separator='_')
        self.assertIn('_', result.password)
    
    def test_capitalize(self):
        """Test word capitalization."""
        result = self.generator.generate(capitalize=True)
        words = result.password.split('-')
        self.assertTrue(all(w[0].isupper() for w in words))
    
    def test_entropy_positive(self):
        """Test entropy is positive."""
        result = self.generator.generate()
        self.assertGreater(result.entropy_bits, 0)


class TestLeetspeakGenerator(unittest.TestCase):
    """Tests for LeetspeakGenerator."""
    
    def setUp(self):
        self.generator = LeetspeakGenerator()
    
    def test_contains_substitutions(self):
        """Test that leetspeak substitutions are applied."""
        result = self.generator.generate(word_count=5)
        # Should contain at least one numeric substitution
        self.assertTrue(any(c.isdigit() for c in result.password))
    
    def test_separator(self):
        """Test separator is applied."""
        result = self.generator.generate(separator='_')
        self.assertIn('_', result.password)


class TestPinGenerator(unittest.TestCase):
    """Tests for PinGenerator."""
    
    def setUp(self):
        self.generator = PinGenerator()
    
    def test_default_length(self):
        """Test default PIN length is 6."""
        result = self.generator.generate()
        self.assertEqual(len(result.password), 6)
    
    def test_numeric_only(self):
        """Test PIN contains only digits."""
        result = self.generator.generate()
        self.assertTrue(result.password.isdigit())
    
    def test_custom_length(self):
        """Test custom PIN length."""
        result = self.generator.generate(length=8)
        self.assertEqual(len(result.password), 8)

    def test_extreme_lengths(self):
        """Test extreme PIN length constraints (Min: 4, Max: 64)."""
        # Minimum
        res_min = self.generator.generate(length=4)
        self.assertEqual(len(res_min.password), 4)

        # Middle
        res_mid = self.generator.generate(length=34)
        self.assertEqual(len(res_mid.password), 34)

        # Maximum
        res_max = self.generator.generate(length=64)
        self.assertEqual(len(res_max.password), 64)


class TestPronounceableGenerator(unittest.TestCase):
    """Tests for PronounceableGenerator."""
    
    def setUp(self):
        self.generator = PronounceableGenerator()
    
    def test_default_length(self):
        """Test approximate default length."""
        result = self.generator.generate()
        self.assertGreaterEqual(len(result.password), 10)
    
    def test_contains_only_letters(self):
        """Test pronounceable passwords are alphabetic."""
        result = self.generator.generate()
        self.assertTrue(result.password.isalpha())

    def test_extreme_lengths(self):
        """Test extreme pronounceable length constraints (Min: 4, Max: 128)."""
        # Minimum
        res_min = self.generator.generate(length=4)
        self.assertEqual(len(res_min.password), 4)

        # Middle
        res_mid = self.generator.generate(length=64)
        self.assertEqual(len(res_mid.password), 64)

        # Maximum
        res_max = self.generator.generate(length=128)
        self.assertEqual(len(res_max.password), 128)


class TestUuidGenerator(unittest.TestCase):
    """Tests for UuidGenerator."""
    
    def setUp(self):
        self.generator = UuidGenerator()
    
    def test_uuid_format(self):
        """Test UUID follows standard format."""
        result = self.generator.generate()
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        self.assertTrue(re.match(uuid_pattern, result.password.lower()))
    
    def test_uppercase_option(self):
        """Test uppercase output."""
        result = self.generator.generate(uppercase=True)
        self.assertTrue(result.password.replace('-', '').isupper())


class TestBase64SecretGenerator(unittest.TestCase):
    """Tests for Base64SecretGenerator."""
    
    def setUp(self):
        self.generator = Base64SecretGenerator()
    
    def test_output_length(self):
        """Test output length is appropriate for byte count."""
        result = self.generator.generate(byte_length=32)
        # Base64 encoding expands by ~4/3, minus padding
        self.assertGreater(len(result.password), 32)

    def test_extreme_byte_counts(self):
        """Test extreme byte count constraints (Min: 8, Max: 1024)."""
        # Minimum
        res_min = self.generator.generate(byte_length=8)
        self.assertGreaterEqual(len(res_min.password), 8)

        # Middle
        res_mid = self.generator.generate(byte_length=512)
        self.assertGreaterEqual(len(res_mid.password), 512)

        # Maximum
        res_max = self.generator.generate(byte_length=1024)
        self.assertGreaterEqual(len(res_max.password), 1024)
    
    def test_entropy(self):
        """Test entropy matches byte count."""
        result = self.generator.generate(byte_length=32)
        self.assertEqual(result.entropy_bits, 256.0)


class TestJwtSecretGenerator(unittest.TestCase):
    """Tests for JwtSecretGenerator."""
    
    def setUp(self):
        self.generator = JwtSecretGenerator()
    
    def test_256_bit_secret(self):
        """Test 256-bit secret."""
        result = self.generator.generate(bits=256)
        self.assertEqual(result.entropy_bits, 256.0)
        self.assertEqual(result.parameters['algorithm'], 'HS256')
    
    def test_512_bit_secret(self):
        """Test 512-bit secret."""
        result = self.generator.generate(bits=512)
        self.assertEqual(result.entropy_bits, 512.0)
        self.assertEqual(result.parameters['algorithm'], 'HS512')


class TestWifiKeyGenerator(unittest.TestCase):
    """Tests for WifiKeyGenerator."""
    
    def setUp(self):
        self.generator = WifiKeyGenerator()
    
    def test_minimum_length(self):
        """Test minimum WPA length of 8."""
        result = self.generator.generate(length=8)
        self.assertEqual(len(result.password), 8)
    
    def test_simple_mode(self):
        """Test simple mode is alphanumeric only."""
        result = self.generator.generate(simple=True)
        self.assertTrue(result.password.isalnum())


class TestLicenseKeyGenerator(unittest.TestCase):
    """Tests for LicenseKeyGenerator."""
    
    def setUp(self):
        self.generator = LicenseKeyGenerator()
    
    def test_default_format(self):
        """Test default 4x4 format."""
        result = self.generator.generate()
        segments = result.password.split('-')
        self.assertEqual(len(segments), 4)
        self.assertTrue(all(len(s) == 4 for s in segments))

    def test_extreme_configurations(self):
        """Test extreme license key configurations."""
        # Minimum (2x2)
        res_min = self.generator.generate(segments=2, segment_length=2)
        segs_min = res_min.password.split('-')
        self.assertEqual(len(segs_min), 2)
        self.assertTrue(all(len(s) == 2 for s in segs_min))

        # Middle (33x17)
        res_mid = self.generator.generate(segments=33, segment_length=17)
        segs_mid = res_mid.password.split('-')
        self.assertEqual(len(segs_mid), 33)
        self.assertTrue(all(len(s) == 17 for s in segs_mid))

        # Maximum (64x32)
        res_max = self.generator.generate(segments=64, segment_length=32)
        segs_max = res_max.password.split('-')
        self.assertEqual(len(segs_max), 64)
        self.assertTrue(all(len(s) == 32 for s in segs_max))
    
    def test_uppercase_output(self):
        """Test output is uppercase."""
        result = self.generator.generate()
        self.assertTrue(result.password.replace('-', '').isupper())


class TestRecoveryCodesGenerator(unittest.TestCase):
    """Tests for RecoveryCodesGenerator."""
    
    def setUp(self):
        self.generator = RecoveryCodesGenerator()
    
    def test_default_count(self):
        """Test default 10 codes."""
        result = self.generator.generate()
        self.assertEqual(len(result.parameters['codes']), 10)

    def test_extreme_counts(self):
        """Test extreme recovery code counts (Min: 5, Max: 100)."""
        # Minimum
        res_min = self.generator.generate(count=5)
        self.assertEqual(len(res_min.parameters['codes']), 5)

        # Middle
        res_mid = self.generator.generate(count=52)
        self.assertEqual(len(res_mid.parameters['codes']), 52)

        # Maximum
        res_max = self.generator.generate(count=100)
        self.assertEqual(len(res_max.parameters['codes']), 100)
    
    def test_word_based_codes(self):
        """Test word-based recovery codes."""
        result = self.generator.generate(use_words=True)
        codes = result.parameters['codes']
        self.assertTrue(all('-' in code for code in codes))


class TestOtpGenerator(unittest.TestCase):
    """Tests for OtpGenerator."""
    
    def setUp(self):
        self.generator = OtpGenerator()
    
    def test_code_format(self):
        """Test password is a numeric code of correct length."""
        result = self.generator.generate(digits=6)
        self.assertTrue(result.password.isdigit())
        self.assertEqual(len(result.password), 6)
        
        result8 = self.generator.generate(digits=8)
        self.assertEqual(len(result8.password), 8)
    
    def test_secret_base32(self):
        """Test secret in parameters is base32 encoded."""
        result = self.generator.generate()
        secret = result.parameters['secret']
        # Base32 characters: A-Z and 2-7
        self.assertTrue(all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567' for c in secret))
    
    def test_otpauth_uri(self):
        """Test otpauth URI is generated."""
        result = self.generator.generate()
        self.assertIn('otpauth://totp/', result.parameters['otpauth_uri'])


class TestPatternGenerator(unittest.TestCase):
    """Tests for PatternGenerator."""
    
    def setUp(self):
        self.generator = PatternGenerator()
    
    def test_path_length(self):
        """Test path has correct length."""
        result = self.generator.generate(path_length=6)
        self.assertEqual(len(result.parameters['path']), 6)
    
    def test_no_duplicate_points(self):
        """Test path has no duplicate points."""
        result = self.generator.generate()
        path = result.parameters['path']
        self.assertEqual(len(path), len(set(path)))


class TestEntropyCalculator(unittest.TestCase):
    """Tests for EntropyCalculator."""
    
    def test_entropy_from_pool(self):
        """Test entropy calculation from pool size."""
        # 26 lowercase, 8 chars = 8 * log2(26) = ~37.6 bits
        entropy = EntropyCalculator.calculate_from_pool(26, 8)
        self.assertAlmostEqual(entropy, 37.6, delta=0.1)
    
    def test_strength_labels(self):
        """Test strength label thresholds."""
        self.assertIn('Weak', EntropyCalculator.get_strength_label(30))
        self.assertIn('Reasonable', EntropyCalculator.get_strength_label(50))
        self.assertIn('Strong', EntropyCalculator.get_strength_label(70))
        self.assertIn('Excellent', EntropyCalculator.get_strength_label(150))
    
    def test_crack_time_estimate(self):
        """Test crack time estimation."""
        # Very low entropy should be instant
        time_str = EntropyCalculator.get_crack_time_estimate(10)
        self.assertTrue('second' in time_str.lower() or 'instant' in time_str.lower())
        
        # High entropy should be long
        time_str = EntropyCalculator.get_crack_time_estimate(128)
        self.assertTrue('year' in time_str.lower() or 'billion' in time_str.lower())


if __name__ == '__main__':
    unittest.main()
