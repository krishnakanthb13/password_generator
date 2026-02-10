"""
Unit tests for the Security Vault (Encryption).
"""

import unittest
import os
import shutil
from pathlib import Path
from src.security.vault import Vault, CRYPTOGRAPHY_AVAILABLE

class TestVault(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary vault directory."""
        self.test_dir = Path("tests/temp_vault")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.vault = Vault(self.test_dir)

    def tearDown(self):
        """Cleanup temporary vault directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    @unittest.skipUnless(CRYPTOGRAPHY_AVAILABLE, "Cryptography library not installed")
    def test_encryption_decryption(self):
        """Test that data can be encrypted and decrypted back to original."""
        original_text = "secret_password_123"
        
        # Encrypt
        encrypted = self.vault.encrypt(original_text, strict=True)
        self.assertNotEqual(original_text, encrypted)
        
        # Decrypt
        decrypted = self.vault.decrypt(encrypted, strict=True)
        self.assertEqual(original_text, decrypted)

    @unittest.skipUnless(CRYPTOGRAPHY_AVAILABLE, "Cryptography library not installed")
    def test_key_persistence(self):
        """Test that encryption key persists across vault instances."""
        original_text = "persist_me"
        encrypted = self.vault.encrypt(original_text)
        
        # New vault instance pointing to same dir
        new_vault = Vault(self.test_dir)
        decrypted = new_vault.decrypt(encrypted)
        
        self.assertEqual(original_text, decrypted)

    @unittest.skipUnless(CRYPTOGRAPHY_AVAILABLE, "Cryptography library not installed")
    def test_file_permissions(self):
        """Test that the key file is created with restrictive permissions (Unix/Linux focus)."""
        # On Windows, chmod behavior is limited, but we check if we can at least stat it
        key_file = self.test_dir / ".vault.key"
        self.assertTrue(key_file.exists())
        
        if os.name != 'nt':  # Only check detailed mode on Unix
            mode = key_file.stat().st_mode & 0o777
            self.assertEqual(mode, 0o600)

    @unittest.skipUnless(CRYPTOGRAPHY_AVAILABLE, "Cryptography library not installed")
    def test_decrypt_invalid_data(self):
        """Test decryption of non-encrypted or corrupted data returns original."""
        garbage = "not_encrypted_at_all"
        result = self.vault.decrypt(garbage)
        self.assertEqual(garbage, result)

if __name__ == '__main__':
    unittest.main()
