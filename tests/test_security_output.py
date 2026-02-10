"""
Unit tests for security and output modules (Clipboard, QR Code, Strength Checker).
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import time
import io

# Add src to path
sys.path.append('src')

from src.output.clipboard import ClipboardManager
from src.output.qrcode_gen import generate_terminal_qr
from src.security.strength_checker import check_strength, StrengthResult


class TestClipboardManager(unittest.TestCase):
    
    @patch('src.output.clipboard.PYPERCLIP_AVAILABLE', True)
    @patch('pyperclip.copy')
    @patch('src.output.clipboard.ClipboardManager._spawn_wiper')
    def test_copy_success(self, mock_spawn, mock_copy):
        """Test successful copy to clipboard."""
        result = ClipboardManager.copy("secret123")
        self.assertTrue(result)
        mock_copy.assert_called_with("secret123")
        mock_spawn.assert_not_called()  # No timeout by default

    @patch('src.output.clipboard.PYPERCLIP_AVAILABLE', True)
    @patch('pyperclip.copy')
    @patch('src.output.clipboard.ClipboardManager._spawn_wiper')
    def test_copy_with_timeout(self, mock_spawn, mock_copy):
        """Test copy with timeout spawns wiper."""
        result = ClipboardManager.copy("secret123", timeout=5)
        self.assertTrue(result)
        mock_copy.assert_called_with("secret123")
        mock_spawn.assert_called_with("secret123", 5)

    @patch('src.output.clipboard.PYPERCLIP_AVAILABLE', False)
    def test_unavailable(self):
        """Test behavior when pyperclip is missing."""
        result = ClipboardManager.copy("secret123")
        self.assertFalse(result)


class TestQRCodeGenerator(unittest.TestCase):
    
    @patch('src.output.qrcode_gen.QRCODE_AVAILABLE', True)
    @patch('qrcode.QRCode')
    def test_generate_terminal_qr(self, mock_qr_cls):
        """Test QR code generation logic."""
        # Setup mock matrix
        mock_qr = MagicMock()
        mock_qr_cls.return_value = mock_qr
        
        # 3x3 matrix:
        # 1 0 1
        # 0 1 0
        # 1 1 1
        mock_qr.get_matrix.return_value = [
            [True, False, True],
            [False, True, False],
            [True, True, True]
        ]
        
        output = generate_terminal_qr("test_data")
        
        # Verify calls
        mock_qr.add_data.assert_called_with("test_data")
        mock_qr.make.assert_called_with(fit=True)
        
        # Verify output format (using \u2588\u2588 for Black/True and spaces for White/False)
        expected_lines = [
            "\u2588\u2588  \u2588\u2588",
            "  \u2588\u2588  ",
            "\u2588\u2588\u2588\u2588\u2588\u2588"
        ]
        self.assertEqual(output, "\n".join(expected_lines))

    @patch('src.output.qrcode_gen.QRCODE_AVAILABLE', False)
    def test_qr_unavailable(self):
        """Test behavior when qrcode is missing."""
        output = generate_terminal_qr("test")
        self.assertIsNone(output)


class TestStrengthChecker(unittest.TestCase):
    
    @patch('src.security.strength_checker.ZXCVBN_AVAILABLE', True)
    @patch('src.security.strength_checker.zxcvbn')
    def test_check_strength(self, mock_zxcvbn):
        """Test strength checker wrapper."""
        # Mock zxcvbn return
        mock_zxcvbn.return_value = {
            'score': 3,
            'crack_times_display': {'offline_slow_hashing_1e4_per_second': 'centuries'},
            'crack_times_seconds': {'offline_slow_hashing_1e4_per_second': 1000000},
            'feedback': {'warning': '', 'suggestions': ['Use more words']},
            'sequence': [],
            'guesses': 1000,
            'guesses_log10': 3.0
        }
        
        result = check_strength("correcthorsebatterystaple")
        
        self.assertIsInstance(result, StrengthResult)
        self.assertEqual(result.score, 3)
        self.assertEqual(result.crack_time_display, 'centuries')
        self.assertEqual(result.feedback_suggestions, ['Use more words'])

    @patch('src.security.strength_checker.ZXCVBN_AVAILABLE', False)
    def test_checker_unavailable(self):
        """Test behavior when zxcvbn is missing."""
        result = check_strength("password")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
