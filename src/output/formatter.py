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


def prompt_interactive_actions(result: Any, clipboard_timeout: int = 30) -> None:
    """
    Prompt user for post-generation actions (Copy, QR Code).
    
    Args:
        result: GeneratorResult object
        clipboard_timeout: Seconds before clipboard is cleared
    """
    from .clipboard import ClipboardManager
    from .qrcode_gen import is_available as qr_available, generate_terminal_qr
    
    prompt = f"\n{Style.BRIGHT}> Press [C]opy"
    if qr_available():
        prompt += ", [Q]R Code"
    prompt += f", or Enter to return... {Style.RESET_ALL}"
    
    try:
        choice = input(prompt).strip().lower()
        
        if choice in ['c', 'q']:
            if ClipboardManager.is_available():
                if ClipboardManager.copy(result.password, timeout=clipboard_timeout):
                    print(f"{Fore.GREEN}✓ Secret copied to clipboard!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ Failed to copy to clipboard{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Clipboard module not available{Style.RESET_ALL}")
                
        if choice == 'q':
            if qr_available():
                qr_output = generate_terminal_qr(result.password)
                if qr_output:
                    print(f"\n{Fore.CYAN}Scan with any QR reader:{Style.RESET_ALL}")
                    print(qr_output)
                    input(f"\nPress Enter to return... ")
            else:
                print(f"{Fore.YELLOW}QR generation requires 'qrcode' package{Style.RESET_ALL}")
        elif choice == 'c':
            input(f"\nPress Enter to return... ")
            
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Fore.YELLOW}Action cancelled.{Style.RESET_ALL}")
