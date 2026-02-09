"""
Strength Checker Module - Pattern-based password strength analysis using zxcvbn.
"""

from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass

# Try to import zxcvbn
try:
    from zxcvbn import zxcvbn
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False


@dataclass
class StrengthResult:
    """Result of password strength analysis."""
    score: int  # 0-4 (0=weak, 4=very strong)
    crack_time_display: str  # Human-readable crack time
    crack_time_seconds: float  # Raw crack time
    feedback_warning: str  # Main warning message
    feedback_suggestions: List[str]  # Improvement suggestions
    patterns_found: List[str]  # Detected weak patterns
    guesses: float  # Number of guesses needed
    guesses_log10: float  # Log10 of guesses


def is_available() -> bool:
    """Check if zxcvbn is available."""
    return ZXCVBN_AVAILABLE


def check_strength(password: str, user_inputs: Optional[List[str]] = None) -> Optional[StrengthResult]:
    """
    Analyze password strength using zxcvbn pattern matching.
    
    Args:
        password: The password to analyze.
        user_inputs: Optional list of user-specific words to penalize
                     (e.g., username, email, site name).
                     
    Returns:
        StrengthResult object or None if zxcvbn is unavailable.
    """
    if not ZXCVBN_AVAILABLE:
        return None
        
    try:
        result = zxcvbn(password, user_inputs or [])
        
        # Extract patterns found
        patterns = []
        for match in result.get('sequence', []):
            pattern_type = match.get('pattern', 'unknown')
            token = match.get('token', '')
            
            if pattern_type == 'dictionary':
                dict_name = match.get('dictionary_name', 'dictionary')
                patterns.append(f"Dictionary word '{token}' ({dict_name})")
            elif pattern_type == 'sequence':
                patterns.append(f"Sequence '{token}'")
            elif pattern_type == 'repeat':
                patterns.append(f"Repeated pattern '{token}'")
            elif pattern_type == 'regex':
                patterns.append(f"Common pattern '{token}'")
            elif pattern_type == 'date':
                patterns.append(f"Date pattern '{token}'")
            elif pattern_type == 'spatial':
                patterns.append(f"Keyboard pattern '{token}'")
        
        # Get crack time (offline, slow hashing scenario)
        crack_times = result.get('crack_times_display', {})
        crack_seconds = result.get('crack_times_seconds', {})
        
        return StrengthResult(
            score=result.get('score', 0),
            crack_time_display=crack_times.get('offline_slow_hashing_1e4_per_second', 'unknown'),
            crack_time_seconds=crack_seconds.get('offline_slow_hashing_1e4_per_second', 0),
            feedback_warning=result.get('feedback', {}).get('warning', ''),
            feedback_suggestions=result.get('feedback', {}).get('suggestions', []),
            patterns_found=patterns,
            guesses=result.get('guesses', 0),
            guesses_log10=result.get('guesses_log10', 0)
        )
        
    except Exception:
        return None


def get_strength_label(score: int) -> Tuple[str, str]:
    """
    Convert zxcvbn score to label and color code.
    
    Args:
        score: 0-4 score from zxcvbn.
        
    Returns:
        Tuple of (label, ansi_color_code).
    """
    labels = {
        0: ("Very Weak", "\033[91m"),   # Red
        1: ("Weak", "\033[91m"),         # Red
        2: ("Fair", "\033[93m"),         # Yellow
        3: ("Strong", "\033[92m"),       # Green
        4: ("Very Strong", "\033[92m"),  # Green
    }
    return labels.get(score, ("Unknown", "\033[0m"))


def format_strength_report(result: StrengthResult, no_color: bool = False) -> str:
    """
    Format a strength analysis report for display.
    
    Args:
        result: StrengthResult from check_strength().
        no_color: If True, omit ANSI color codes.
        
    Returns:
        Formatted string report.
    """
    label, color = get_strength_label(result.score)
    reset = "\033[0m"
    
    if no_color:
        color = ""
        reset = ""
    
    lines = [
        "+--------------------------------------------------+",
        "|              Pattern Analysis (zxcvbn)           |",
        "+--------------------------------------------------+",
        f"| Score:                          {color}{label:>14}{reset} |",
        f"| Crack Time:            {result.crack_time_display:>23} |",
        f"| Guesses (log10):                   {result.guesses_log10:>11.2f} |",
    ]
    
    if result.feedback_warning:
        warning = result.feedback_warning[:40]
        lines.append(f"| Warning: {warning:<37} |")
    
    if result.patterns_found:
        lines.append("|                                                  |")
        lines.append("| Patterns Detected:                               |")
        for pattern in result.patterns_found[:3]:  # Limit to 3
            pattern_short = pattern[:44]
            lines.append(f"|   - {pattern_short:<43} |")
    
    if result.feedback_suggestions:
        lines.append("|                                                  |")
        lines.append("| Suggestions:                                     |")
        for suggestion in result.feedback_suggestions[:2]:  # Limit to 2
            suggestion_short = suggestion[:44]
            lines.append(f"|   - {suggestion_short:<43} |")
    
    lines.append("+--------------------------------------------------+")
    
    return "\n".join(lines)
