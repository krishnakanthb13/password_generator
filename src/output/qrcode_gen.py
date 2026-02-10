"""
QR Code Module - Generate QR codes for OTP secrets.
"""

from typing import Optional

# Try to import qrcode
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False


def is_available() -> bool:
    """Check if QR code functionality is available."""
    return QRCODE_AVAILABLE


def generate_terminal_qr(data: str, border: int = 1) -> Optional[str]:
    """
    Generate a QR code for terminal display using ASCII characters.
    
    Args:
        data: The data to encode (e.g., otpauth:// URI).
        border: Size of border around QR code.
        
    Returns:
        String representation of QR code for terminal, or None if unavailable.
    """
    if not QRCODE_AVAILABLE:
        return None
        
    try:
        qr = qrcode.QRCode(border=border)
        qr.add_data(data)
        qr.make(fit=True)
        
        matrix = qr.get_matrix()
        lines = []
        for row in matrix:
            # Use Unicode full block characters (█) for a "real" QR look.
            # We use two blocks per module to approximate a square shape in terminals.
            line = "".join("\u2588\u2588" if cell else "  " for cell in row)
            lines.append(line)
        
        return "\n".join(lines)
        
    except Exception:
        return None


def generate_qr_image(data: str, filename: str) -> bool:
    """
    Generate a QR code image file.
    
    Args:
        data: The data to encode.
        filename: Output file path (PNG format).
        
    Returns:
        True if successful, False otherwise.
    """
    if not QRCODE_AVAILABLE:
        return False
        
    try:
        # Check for Pillow
        try:
            from PIL import Image
        except ImportError:
            return False
            
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return True
        
    except Exception:
        return False
