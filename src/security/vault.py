"""
Vault Module - Handles encryption for secure history storage.
"""

import os
import base64
from pathlib import Path
from typing import Optional

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


class Vault:
    """Manages encryption keys and secure data transformation."""
    
    def __init__(self, vault_dir: Optional[Path] = None):
        """Initialize vault with a storage directory."""
        if vault_dir:
            self.vault_dir = vault_dir
        else:
            self.vault_dir = Path.home() / ".passforge"
            
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.key_file = self.vault_dir / ".vault.key"
        self._fernet = None
        
        if CRYPTOGRAPHY_AVAILABLE:
            self._init_fernet()

    def _init_fernet(self):
        """Initialize or load the Fernet encryption instance."""
        if not self.key_file.exists():
            # Generate a new unique key for this PC
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_file, 'rb') as f:
                key = f.read()
        
        try:
            self._fernet = Fernet(key)
        except Exception:
            # If key is corrupted, we might need to reset, 
            # but for now we'll just disable encryption to prevent crashes
            self._fernet = None

    @property
    def is_active(self) -> bool:
        """Check if encryption is available and initialized."""
        return CRYPTOGRAPHY_AVAILABLE and self._fernet is not None

    def encrypt(self, text: str) -> str:
        """Encrypt a string and return a base64 encoded result."""
        if not self.is_active or not text:
            return text
            
        try:
            encrypted = self._fernet.encrypt(text.encode('utf-8'))
            return encrypted.decode('ascii')
        except Exception:
            return text

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt a base64 encoded string."""
        if not self.is_active or not encrypted_text:
            return encrypted_text
            
        try:
            decrypted = self._fernet.decrypt(encrypted_text.encode('ascii'))
            return decrypted.decode('utf-8')
        except Exception:
            # If decryption fails (e.g. wrong key or plain text), return as is
            return encrypted_text
