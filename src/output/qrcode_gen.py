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
        qr = qrcode.QRCode()
        qr.add_data(data)
        qr.make()
        
        # Use StringIO to capture the output of print_ascii
        import io
        f = io.StringIO()
        qr.print_ascii(out=f)
        return f.getvalue()
        
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
