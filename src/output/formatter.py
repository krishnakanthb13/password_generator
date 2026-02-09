"""
Output Formatter - Color-coded and JSON output formatting.
"""

from typing import Any, Dict
from colorama import Fore, Style


def colorize_password(password: str, no_color: bool = False) -> str:
    """
    Apply color coding to password characters.
    
    - Uppercase: Cyan
    - Lowercase: Blue
    - Digits: Green
    - Symbols: Magenta
    
    Args:
        password: Password to colorize
        no_color: Disable colors
        
    Returns:
        Colorized password string
    """
    if no_color:
        return password
    
    colored = []
    for char in password:
        if char.isalpha():
            if char.isupper():
                colored.append(f"{Style.BRIGHT}{Fore.CYAN}{char}{Style.RESET_ALL}")
            else:
                # Use LIGHTBLUE_EX or Style.BRIGHT + Fore.BLUE for better visibility on dark backgrounds
                colored.append(f"{Style.BRIGHT}{Fore.BLUE}{char}{Style.RESET_ALL}")
        elif char.isdigit():
            colored.append(f"{Style.BRIGHT}{Fore.GREEN}{char}{Style.RESET_ALL}")
        elif char in " \n\t-_":
            colored.append(char)
        else:
            colored.append(f"{Style.BRIGHT}{Fore.MAGENTA}{char}{Style.RESET_ALL}")
    
    return "".join(colored)


def format_result(result: Any, show_entropy: bool = False) -> str:
    """
    Format a generator result for display.
    
    Args:
        result: GeneratorResult object
        show_entropy: Include entropy information
        
    Returns:
        Formatted string
    """
    lines = [colorize_password(result.password)]
    
    if show_entropy:
        from ..security.entropy import EntropyCalculator
        
        strength = EntropyCalculator.get_strength_label(result.entropy_bits)
        crack_time = EntropyCalculator.get_crack_time_estimate(result.entropy_bits)
        
        lines.append("")
        lines.append(f"{Style.BRIGHT}{Fore.YELLOW}Entropy:{Style.RESET_ALL} {result.entropy_bits:.2f} bits")
        lines.append(f"{Style.BRIGHT}{Fore.YELLOW}Strength:{Style.RESET_ALL} {strength}")
        lines.append(f"{Style.BRIGHT}{Fore.YELLOW}Crack Time:{Style.RESET_ALL} {crack_time}")
    
    return "\n".join(lines)


def format_batch_results(results: list, numbered: bool = True) -> str:
    """
    Format multiple results for display.
    
    Args:
        results: List of GeneratorResult objects
        numbered: Add numbers to each result
        
    Returns:
        Formatted string
    """
    lines = []
    
    for i, result in enumerate(results, 1):
        password = colorize_password(result.password)
        if numbered:
            lines.append(f"{Style.BRIGHT}{Fore.YELLOW}{i:2}.{Style.RESET_ALL} {password}")
        else:
            lines.append(password)
    
    return "\n".join(lines)
