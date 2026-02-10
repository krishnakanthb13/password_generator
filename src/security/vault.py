"""
Vault Module - Handles encryption for secure history storage.
"""

import os
import base64
import logging
from pathlib import Path
from typing import Optional

# Setup logger
logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet, InvalidToken
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
        """Initialize or load the Fernet encryption instance with restrictive permissions."""
        if not self.key_file.exists():
            # Generate a new unique key for this PC
            key = Fernet.generate_key()
            
            # Create file with restrictive permissions (0600 - Owner read/write only)
            # This is handled atomically via os.open
            try:
                fd = os.open(self.key_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(fd, 'wb') as f:
                    f.write(key)
            except Exception as e:
                logger.error(f"Failed to create secure key file: {e}")
                return
        else:
            # Check existing permissions and try to fix if too permissive
            try:
                current_mode = self.key_file.stat().st_mode
                if current_mode & 0o077: # Group/Others have any permissions
                    self.key_file.chmod(0o600)
            except Exception:
                pass
            
            try:
                with open(self.key_file, 'rb') as f:
                    key = f.read()
            except Exception as e:
                logger.error(f"Failed to read key file: {e}")
                return
        
        try:
            self._fernet = Fernet(key)
        except Exception as e:
            logger.error(f"Failed to initialize Fernet with key: {e}")
            self._fernet = None

    @property
    def is_active(self) -> bool:
        """Check if encryption is available and initialized."""
        return CRYPTOGRAPHY_AVAILABLE and self._fernet is not None

    def encrypt(self, text: str, strict: bool = False) -> str:
        """
        Encrypt a string. 
        Falling back to plaintext by default unless strict=True.
        """
        if not self.is_active or not text:
            if strict and text:
                raise RuntimeError("Vault is not active, cannot encrypt strictly")
            return text
            
        try:
            encrypted = self._fernet.encrypt(text.encode('utf-8'))
            return encrypted.decode('ascii')
        except (InvalidToken, Exception) as e:
            logger.warning(f"Encryption failed: {e}")
            if strict:
                raise
            return text

    def decrypt(self, encrypted_text: str, strict: bool = False) -> str:
        """
        Decrypt a base64 encoded string.
        Falling back to input text by default unless strict=True.
        """
        if not self.is_active or not encrypted_text:
            if strict and encrypted_text:
                raise RuntimeError("Vault is not active, cannot decrypt strictly")
            return encrypted_text
            
        try:
            decrypted = self._fernet.decrypt(encrypted_text.encode('ascii'))
            return decrypted.decode('utf-8')
        except (InvalidToken, Exception) as e:
            logger.warning(f"Decryption failed: {e}")
            if strict:
                raise
            # If decryption fails (e.g. wrong key or plain text), return as is
            return encrypted_text
