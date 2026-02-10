"""
CLI Module - Command-line interface with argparse and interactive menu.
"""

import argparse
import sys
from typing import Optional, List
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands."""
    
    parser = argparse.ArgumentParser(
        prog="passforge",
        description="PassForge - All-in-One Password Generator CLI",
        epilog="Examples:\n"
               "  passforge random -l 20 --symbols\n"
               "  passforge phrase -w 4\n"
               "  passforge pin -l 6\n"
               "  passforge --interactive",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global options
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Launch interactive menu mode"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "--clipboard", "-c",
        action="store_true",
        help="Copy password to clipboard"
    )
    
    parser.add_argument(
        "--clipboard-timeout",
        type=int,
        default=30,
        metavar="SECONDS",
        help="Auto-wipe clipboard after N seconds (default: 30, 0=disabled)"
    )
    
    parser.add_argument(
        "--show-entropy",
        action="store_true",
        help="Display entropy analysis"
    )
    
    parser.add_argument(
        "--check-strength",
        action="store_true",
        help="Run zxcvbn pattern analysis (requires zxcvbn package)"
    )
    
    # Global modifiers
    parser.add_argument(
        "--easy-read",
        action="store_true",
        help="Exclude ambiguous characters (0/O, 1/l/I)"
    )
    
    parser.add_argument(
        "--easy-say",
        action="store_true",
        help="Only pronounceable characters (no symbols)"
    )
    
    parser.add_argument(
        "--log",
        action="store_true",
        help="Log generated password to history"
    )
    
    parser.add_argument(
        "--confirm-copy",
        action="store_true",
        help="Ask to copy to clipboard after displaying"
    )
    
    parser.add_argument(
        "--preset",
        choices=["strong", "memorable", "dev", "pin", "web", "wifi", "key"],
        help="Use a predefined security profile"
    )
    
    # Subcommands for each generator
    subparsers = parser.add_subparsers(
        dest="command",
        title="generators",
        description="Available password generators"
    )
    
    # Random password generator
    random_parser = subparsers.add_parser(
        "random",
        help="Generate random character password",
        aliases=["r"]
    )
    random_parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Password length (default: 16)"
    )
    random_parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters"
    )
    random_parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters"
    )
    random_parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits"
    )
    random_parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols"
    )
    random_parser.add_argument(
        "--include",
        type=str,
        default="",
        help="Additional characters to include"
    )
    random_parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="Characters to exclude"
    )
    random_parser.add_argument(
        "--no-repeats",
        action="store_true",
        help="No repeated characters"
    )
    random_parser.add_argument(
        "--balanced",
        action="store_true",
        help="Use balanced ratio (60%% Letters, 20%% Digits, 20%% Symbols)"
    )
    random_parser.add_argument(
        "--min-upper",
        type=int,
        default=0,
        help="Minimum uppercase characters"
    )
    random_parser.add_argument(
        "--min-lower",
        type=int,
        default=0,
        help="Minimum lowercase characters"
    )
    random_parser.add_argument(
        "--min-digits",
        type=int,
        default=0,
        help="Minimum digit characters"
    )
    random_parser.add_argument(
        "--min-symbols",
        type=int,
        default=0,
        help="Minimum symbol characters"
    )
    random_parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate"
    )
    
    # Passphrase generator
    phrase_parser = subparsers.add_parser(
        "phrase",
        help="Generate word-based passphrase",
        aliases=["p"]
    )
    phrase_parser.add_argument(
        "-w", "--words",
        type=int,
        default=4,
        help="Number of words (default: 4)"
    )
    phrase_parser.add_argument(
        "-s", "--separator",
        type=str,
        default="-",
        help="Word separator (default: -)"
    )
    phrase_parser.add_argument(
        "--capitalize",
        action="store_true",
        help="Capitalize each word"
    )
    phrase_parser.add_argument(
        "--wordlist",
        type=str,
        help="Path to custom wordlist file"
    )
    phrase_parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of passphrases to generate"
    )
    
    # PIN generator
    pin_parser = subparsers.add_parser(
        "pin",
        help="Generate numeric PIN"
    )
    pin_parser.add_argument(
        "-l", "--length",
        type=int,
        default=6,
        help="PIN length (default: 6)"
    )
    pin_parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of PINs to generate"
    )
    
    # OTP generator
    otp_parser = subparsers.add_parser(
        "otp",
        help="Generate TOTP/HOTP secret"
    )
    otp_parser.add_argument(
        "--digits",
        type=int,
        default=6,
        choices=[6, 8],
        help="OTP digit length (default: 6)"
    )
    otp_parser.add_argument(
        "--period",
        type=int,
        default=30,
        help="TOTP time period in seconds (default: 30)"
    )
    otp_parser.add_argument(
        "--qr",
        action="store_true",
        help="Generate QR code for the secret"
    )
    
    # UUID generator
    uuid_parser = subparsers.add_parser(
        "uuid",
        help="Generate UUID token"
    )
    uuid_parser.add_argument(
        "--upper",
        action="store_true",
        help="Output in uppercase"
    )
    uuid_parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of UUIDs to generate"
    )
    
    # Pronounceable password
    pronounce_parser = subparsers.add_parser(
        "pronounce",
        help="Generate pronounceable password",
        aliases=["pr"]
    )
    pronounce_parser.add_argument(
        "-l", "--length",
        type=int,
        default=12,
        help="Password length (default: 12)"
    )
    pronounce_parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate"
    )
    
    # Leetspeak passphrase
    leet_parser = subparsers.add_parser(
        "leet",
        help="Generate leetspeak passphrase",
        aliases=["l"]
    )
    leet_parser.add_argument(
        "-w", "--words",
        type=int,
        default=3,
        help="Number of words (default: 3)"
    )
    leet_parser.add_argument(
        "-s", "--separator",
        type=str,
        default="-",
        choices=["-", "_", ".", ","],
        help="Word separator (default: -)"
    )
    leet_parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of passphrases to generate"
    )
    
    # Base64 secret
    b64_parser = subparsers.add_parser(
        "base64",
        help="Generate base64-encoded secret",
        aliases=["b64"]
    )
    b64_parser.add_argument(
        "-b", "--bytes",
        type=int,
        default=32,
        help="Number of random bytes (default: 32)"
    )
    b64_parser.add_argument(
        "--url-safe",
        action="store_true",
        help="Use URL-safe base64 encoding"
    )
    
    # JWT secret
    jwt_parser = subparsers.add_parser(
        "jwt",
        help="Generate JWT signing secret"
    )
    jwt_parser.add_argument(
        "--bits",
        type=int,
        default=256,
        choices=[256, 384, 512],
        help="Secret size in bits (default: 256)"
    )
    jwt_parser.add_argument(
        "--hex",
        action="store_true",
        help="Output as hex instead of base64"
    )
    
    # WiFi key
    wifi_parser = subparsers.add_parser(
        "wifi",
        help="Generate WiFi/WPA key"
    )
    wifi_parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Key length (8-63, default: 16)"
    )
    wifi_parser.add_argument(
        "--simple",
        action="store_true",
        help="Use only alphanumeric characters"
    )
    
    # License key
    license_parser = subparsers.add_parser(
        "license",
        help="Generate software license key"
    )
    license_parser.add_argument(
        "--segments",
        type=int,
        default=4,
        help="Number of segments (default: 4)"
    )
    license_parser.add_argument(
        "--segment-length",
        type=int,
        default=4,
        help="Characters per segment (default: 4)"
    )
    
    # Recovery codes
    recovery_parser = subparsers.add_parser(
        "recovery",
        help="Generate 2FA recovery codes"
    )
    recovery_parser.add_argument(
        "-n", "--count",
        type=int,
        default=10,
        help="Number of codes (default: 10)"
    )
    recovery_parser.add_argument(
        "--words",
        action="store_true",
        help="Use word-based codes instead of numeric"
    )
    
    # Pattern generator
    pattern_parser = subparsers.add_parser(
        "pattern",
        help="Generate pattern-style password"
    )
    pattern_parser.add_argument(
        "--grid",
        type=int,
        default=3,
        choices=[3, 4, 5],
        help="Grid size (3x3, 4x4, or 5x5)"
    )
    
    # Phonetic generator
    phonetic_parser = subparsers.add_parser(
        "phonetic",
        help="Generate NATO phonetic alphabet sequence",
        aliases=["ph"]
    )
    phonetic_parser.add_argument(
        "--text",
        type=str,
        help="Text to convert to phonetic"
    )
    phonetic_parser.add_argument(
        "-l", "--length",
        type=int,
        default=8,
        help="Length of random sequence if --text not provided (default: 8)"
    )

    # Analyze existing password
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze strength of an existing password",
        aliases=["check"]
    )
    analyze_parser.add_argument(
        "password",
        nargs="?",
        help="The password to analyze (will be prompted if not provided)"
    )
    
    # History viewer
    history_parser = subparsers.add_parser(
        "history",
        help="View password generation history",
        aliases=["h"]
    )
    history_parser.add_argument(
        "--last",
        type=int,
        default=10,
        help="Show last N entries"
    )
    history_parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Show all history entries (overrides --last)"
    )
    history_parser.add_argument(
        "--search",
        type=str,
        help="Search in history"
    )
    history_parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact passwords in terminal output"
    )
    history_parser.add_argument(
        "--export",
        type=str,
        help="Export history to file (JSON or CSV)"
    )
    history_parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Do not redact passwords in FILE export (Caution!)"
    )
    history_parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear history"
    )
    
    return parser


def colorize_password(password: str, no_color: bool = False) -> str:
    """
    Apply color coding to password characters.
    
    - Letters: Blue/Cyan
    - Digits: Green
    - Symbols: Red/Magenta
    """
    if no_color:
        return password
    
    colored = []
    for char in password:
        if char.isalpha():
            if char.isupper():
                colored.append(f"{Style.BRIGHT}{Fore.CYAN}{char}{Style.RESET_ALL}")
            else:
                colored.append(f"{Style.BRIGHT}{Fore.BLUE}{char}{Style.RESET_ALL}")
        elif char.isdigit():
            colored.append(f"{Style.BRIGHT}{Fore.GREEN}{char}{Style.RESET_ALL}")
        else:
            colored.append(f"{Style.BRIGHT}{Fore.MAGENTA}{char}{Style.RESET_ALL}")
    
    return "".join(colored)


def print_banner():
    """Print the PassForge banner."""
    banner = f"""
{Style.BRIGHT}{Fore.CYAN}+===========================================================+
|  {Fore.YELLOW}PassForge{Fore.CYAN} - All-in-One Password Generator              |
|     {Fore.WHITE}Generate. Secure. Manage.{Fore.CYAN}                            |
+===========================================================+{Style.RESET_ALL}
"""
    print(banner)


def run_interactive_menu():
    """Run the interactive menu-driven interface."""
    from .interactive import InteractiveMenu
    menu = InteractiveMenu()
    menu.run()


def main(args: Optional[List[str]] = None):
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    # No command, no interactive flag, and no preset = show help
    if not parsed.command and not parsed.interactive and not parsed.preset:
        print_banner()
        parser.print_help()
        return 0
    
    # Interactive mode
    if parsed.interactive:
        print_banner()
        run_interactive_menu()
        return 0
    
    # Handle generator commands
    from .command_handler import handle_command
    return handle_command(parsed)


if __name__ == "__main__":
    sys.exit(main())
