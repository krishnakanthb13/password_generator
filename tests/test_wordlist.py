"""Fail-before probe: missing --wordlist must not silently fall back."""

import unittest

from src.generators.passphrase import PassphraseGenerator


class TestMissingWordlist(unittest.TestCase):

    def setUp(self):
        self.generator = PassphraseGenerator()

    def test_missing_wordlist_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.generator.load_wordlist("/nonexistent-dir-xyz/words.txt")

    def test_default_wordlist_still_loads(self):
        words = self.generator.load_wordlist()
        self.assertTrue(len(words) > 0)


if __name__ == "__main__":
    unittest.main()
