"""
Clipboard Module - Secure clipboard handling with auto-wipe timeout.
"""

import subprocess
import sys
import os
from typing import Optional

# Try to import pyperclip
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


class ClipboardManager:
    """Manages clipboard operations with security features."""
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if clipboard functionality is available."""
        return PYPERCLIP_AVAILABLE
    
    @classmethod
    def copy(cls, text: str, timeout: int = 0) -> bool:
        """
        Copy text to clipboard with optional auto-wipe timeout.
        
        Args:
            text: The text to copy to clipboard.
            timeout: Seconds before auto-wipe (0 = no timeout).
            
        Returns:
            True if successful, False otherwise.
        """
        if not PYPERCLIP_AVAILABLE:
            return False
            
        try:
            # Copy to clipboard
            pyperclip.copy(text)
            
            # Set up auto-wipe if timeout > 0
            if timeout > 0:
                cls._spawn_wiper(text, timeout)
                    
            return True
            
        except Exception:
            return False
    
    @classmethod
    def _spawn_wiper(cls, original_text: str, timeout: int) -> None:
        """
        Spawn a detached subprocess to wipe clipboard after timeout.
        
        This process survives after the main script exits.
        """
        # Python code to run in subprocess
        wiper_code = f'''
import time
import sys
try:
    import pyperclip
except ImportError:
    sys.exit(0)

time.sleep({timeout})

try:
    current = pyperclip.paste()
    original = {repr(original_text)}
    if current == original:
        pyperclip.copy("")
except:
    pass
'''
        
        try:
            # Use CREATE_NO_WINDOW on Windows to hide the subprocess
            if sys.platform == 'win32':
                # Windows: use CREATE_NO_WINDOW flag
                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen(
                    [sys.executable, '-c', wiper_code],
                    creationflags=CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
            else:
                # Unix: use start_new_session to detach
                subprocess.Popen(
                    [sys.executable, '-c', wiper_code],
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
        except Exception:
            pass
    
    @classmethod
    def clear(cls) -> bool:
        """Immediately clear the clipboard."""
        if not PYPERCLIP_AVAILABLE:
            return False
            
        try:
            pyperclip.copy("")
            return True
        except Exception:
            return False


# Default timeout in seconds (can be overridden via config)
DEFAULT_CLIPBOARD_TIMEOUT = 30

