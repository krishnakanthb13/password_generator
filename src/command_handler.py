"""
Command Handler - Routes CLI commands to appropriate generators.
"""

import json
import sys
from datetime import datetime
from typing import Any
from colorama import Fore, Style

from .generators.random_password import RandomPasswordGenerator
from .security.entropy import EntropyCalculator
from .output.formatter import colorize_password


def handle_command(args: Any) -> int:
    """
    Handle CLI commands and route to appropriate generators.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Apply preset if provided
        if hasattr(args, 'preset') and args.preset:
            args = apply_preset(args)
            
        if args.command in ["random", "r"]:
            return handle_random(args)
        elif args.command in ["phrase", "p"]:
            return handle_phrase(args)
        elif args.command == "pin":
            return handle_pin(args)
        elif args.command in ["pronounce", "pr"]:
            return handle_pronounce(args)
        elif args.command in ["leet", "l"]:
            return handle_leet(args)
        elif args.command == "uuid":
            return handle_uuid(args)
        elif args.command in ["base64", "b64"]:
            return handle_base64(args)
        elif args.command == "jwt":
            return handle_jwt(args)
        elif args.command == "wifi":
            return handle_wifi(args)
        elif args.command == "license":
            return handle_license(args)
        elif args.command == "recovery":
            return handle_recovery(args)
        elif args.command == "pattern":
            return handle_pattern(args)
        elif args.command == "otp":
            return handle_otp(args)
        elif args.command in ["phonetic", "ph"]:
            return handle_phonetic(args)
        elif args.command == "history":
            return handle_history(args)
        else:
            print(f"{Fore.RED}Unknown command: {args.command}{Style.RESET_ALL}")
            return 1
            
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


def apply_preset(args: Any) -> Any:
    """Apply preset profile settings to args."""
    from .config.presets import PRESETS
    
    preset_name = args.preset
    if preset_name not in PRESETS:
        return args
        
    preset_data = PRESETS[preset_name]
    
    # Set command if not already set
    if not args.command:
        args.command = preset_data.get("command")

    # Define all possible attributes and their default values
    # to avoid AttributeError when a preset is used without a subcommand
    defaults = {
        "length": 16,
        "no_uppercase": False,
        "no_lowercase": False,
        "no_digits": False,
        "no_symbols": False,
        "include": "",
        "exclude": "",
        "no_repeats": False,
        "min_upper": 0,
        "min_lower": 0,
        "min_digits": 0,
        "min_symbols": 0,
        "words": 4,
        "separator": "-",
        "capitalize": False,
        "wordlist": None,
        "bytes": 32,
        "url_safe": False,
        "bits": 256,
        "hex": False,
        "simple": False,
        "segments": 4,
        "segment_length": 4,
        "digits": 6,
        "period": 30,
        "qr": False,
        "upper": False,
        "grid": 3,
        "balanced": False,
        "count": 1
    }

    # Set defaults if attribute doesn't exist
    for attr, default_val in defaults.items():
        if not hasattr(args, attr):
            setattr(args, attr, default_val)
        
    # Map of preset keys to arg attributes
    mapping = {
        "length": "length",
        "words": "words",
        "uppercase": "no_uppercase", # Inverted logic in args: no_uppercase
        "lowercase": "no_lowercase",
        "digits": "no_digits",
        "symbols": "no_symbols",
        "min_uppercase": "min_upper",
        "min_lowercase": "min_lower",
        "min_digits": "min_digits",
        "min_symbols": "min_symbols",
        "no_repeats": "no_repeats",
        "simple": "simple",
        "segments": "segments",
        "segment_length": "segment_length",
        "capitalize": "capitalize",
        "bits": "bits",
        "bytes": "bytes"
    }
    
    for preset_key, arg_attr in mapping.items():
        if preset_key in preset_data:
            val = preset_data[preset_key]
            
            # Handle inverted flags
            if preset_key in ["uppercase", "lowercase", "digits", "symbols"]:
                setattr(args, arg_attr, not val)
            else:
                setattr(args, arg_attr, val)
                
    return args


def handle_random(args: Any) -> int:
    """Handle random password generation."""
    generator = RandomPasswordGenerator(
        easy_read=args.easy_read,
        easy_say=args.easy_say
    )
    
    count = getattr(args, 'count', 1)
    
    for i in range(count):
        result = generator.generate(
            length=args.length,
            uppercase=not args.no_uppercase,
            lowercase=not args.no_lowercase,
            digits=not args.no_digits,
            symbols=not args.no_symbols,
            include_chars=args.include,
            exclude_chars=args.exclude,
            no_repeats=args.no_repeats,
            min_uppercase=args.min_upper,
            min_lowercase=args.min_lower,
            min_digits=args.min_digits,
            min_symbols=args.min_symbols,
            balanced=args.balanced
        )
        
        output_result(result, args)
    
    return 0


def handle_phrase(args: Any) -> int:
    """Handle passphrase generation."""
    from .generators.passphrase import PassphraseGenerator
    
    generator = PassphraseGenerator(
        easy_read=args.easy_read,
        easy_say=args.easy_say
    )
    
    count = getattr(args, 'count', 1)
    wordlist_path = getattr(args, 'wordlist', None)
    
    for i in range(count):
        result = generator.generate(
            word_count=args.words,
            separator=args.separator,
            capitalize=args.capitalize,
            wordlist_path=wordlist_path
        )
        
        output_result(result, args)
    
    return 0


def handle_pin(args: Any) -> int:
    """Handle PIN generation."""
    from .generators.pin import PinGenerator
    
    generator = PinGenerator()
    count = getattr(args, 'count', 1)
    
    for i in range(count):
        result = generator.generate(length=args.length)
        output_result(result, args)
    
    return 0


def handle_pronounce(args: Any) -> int:
    """Handle pronounceable password generation."""
    from .generators.pronounceable import PronounceableGenerator
    
    generator = PronounceableGenerator()
    count = getattr(args, 'count', 1)
    
    for i in range(count):
        result = generator.generate(length=args.length)
        output_result(result, args)
    
    return 0


def handle_leet(args: Any) -> int:
    """Handle leetspeak passphrase generation."""
    from .generators.leetspeak import LeetspeakGenerator
    
    generator = LeetspeakGenerator()
    count = getattr(args, 'count', 1)
    
    for i in range(count):
        result = generator.generate(
            word_count=args.words,
            separator=args.separator
        )
        output_result(result, args)
    
    return 0


def handle_uuid(args: Any) -> int:
    """Handle UUID generation."""
    from .generators.uuid_token import UuidGenerator
    
    generator = UuidGenerator()
    count = getattr(args, 'count', 1)
    
    for i in range(count):
        result = generator.generate(uppercase=args.upper)
        output_result(result, args)
    
    return 0


def handle_base64(args: Any) -> int:
    """Handle base64 secret generation."""
    from .generators.base64_secret import Base64SecretGenerator
    
    generator = Base64SecretGenerator()
    url_safe = getattr(args, 'url_safe', False)
    
    result = generator.generate(
        byte_length=args.bytes,
        url_safe=url_safe
    )
    output_result(result, args)
    
    return 0


def handle_jwt(args: Any) -> int:
    """Handle JWT secret generation."""
    from .generators.jwt_secret import JwtSecretGenerator
    
    generator = JwtSecretGenerator()
    use_hex = getattr(args, 'hex', False)
    
    result = generator.generate(
        bits=args.bits,
        output_hex=use_hex
    )
    output_result(result, args)
    
    return 0


def handle_wifi(args: Any) -> int:
    """Handle WiFi key generation."""
    from .generators.wifi_key import WifiKeyGenerator
    
    generator = WifiKeyGenerator()
    simple = getattr(args, 'simple', False)
    
    result = generator.generate(
        length=args.length,
        simple=simple
    )
    output_result(result, args)
    
    return 0


def handle_license(args: Any) -> int:
    """Handle license key generation."""
    from .generators.license_key import LicenseKeyGenerator
    
    generator = LicenseKeyGenerator()
    
    result = generator.generate(
        segments=args.segments,
        segment_length=args.segment_length
    )
    output_result(result, args)
    
    return 0


def handle_recovery(args: Any) -> int:
    """Handle recovery codes generation."""
    from .generators.recovery_codes import RecoveryCodesGenerator
    
    generator = RecoveryCodesGenerator()
    use_words = getattr(args, 'words', False)
    
    result = generator.generate(
        count=args.count,
        use_words=use_words
    )
    output_result(result, args)
    
    return 0


def handle_pattern(args: Any) -> int:
    """Handle pattern generation."""
    from .generators.pattern import PatternGenerator
    
    generator = PatternGenerator()
    
    result = generator.generate(grid_size=args.grid)
    output_result(result, args)
    
    return 0


def handle_otp(args: Any) -> int:
    """Handle OTP secret generation."""
    from .generators.otp import OtpGenerator
    
    generator = OtpGenerator()
    generate_qr = getattr(args, 'qr', False)
    
    result = generator.generate(
        digits=args.digits,
        period=args.period
    )
    output_result(result, args)
    
    # Generate QR if requested
    if generate_qr:
        from .output.qrcode_gen import is_available, generate_terminal_qr
        
        otpauth_uri = result.parameters.get('otpauth_uri', '')
        
        if is_available() and otpauth_uri:
            qr_output = generate_terminal_qr(otpauth_uri)
            if qr_output:
                print()
                print(f"{Fore.CYAN}Scan this QR code with your authenticator app:{Style.RESET_ALL}")
                print(qr_output)
        else:
            print(f"{Fore.YELLOW}QR generation requires 'qrcode' package: pip install qrcode{Style.RESET_ALL}")
    
    return 0


def handle_phonetic(args: Any) -> int:
    """Handle phonetic alphabet generation."""
    from .generators.phonetic import PhoneticGenerator
    
    text = getattr(args, 'text', "")
    length = getattr(args, 'length', 8)
    
    generator = PhoneticGenerator()
    result = generator.generate(text=text, length=length)
    
    return output_result(result, args)


def handle_history(args: Any) -> int:
    """Handle history viewing."""
    from .output.logger import PasswordLogger
    
    logger = PasswordLogger()
    
    if args.clear:
        logger.clear_history()
        print(f"{Fore.GREEN}History cleared.{Style.RESET_ALL}")
        return 0
    
    search_term = getattr(args, 'search', None)
    show_all = getattr(args, 'all', False)
    limit = None if show_all else args.last
    
    entries = logger.get_history(
        limit=limit,
        search=search_term
    )
    
    if not entries:
        print(f"{Fore.YELLOW}No history entries found.{Style.RESET_ALL}")
        return 0
    
    print(f"\n{Fore.GREEN}{'-' * 70}{Style.RESET_ALL}")
    for entry in entries:
        ts = entry['timestamp'][:19].replace('T', ' ')
        gen_type = entry['generator_type']
        password = colorize_password(entry['password'])
        print(f"{Fore.CYAN}{ts}{Style.RESET_ALL} | {gen_type:12} | {password}")
    print(f"{Fore.GREEN}{'-' * 70}{Style.RESET_ALL}")
    
    return 0


def output_result(result: Any, args: Any) -> None:
    """Output the generator result based on args."""
    
    # JSON output
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
        return
    
    # Regular output with color
    no_color = getattr(args, 'no_color', False)
    password = colorize_password(result.password, no_color)
    
    # Entropy display
    if args.show_entropy:
        report = EntropyCalculator.format_entropy_report(
            result.password,
            result.entropy_bits,
            result.parameters.get('pool_size'),
            colorized_password=password
        )
        print(report)
    else:
        # Just print the password if entropy isn't shown
        print(f"\n{password}\n")
    
    # zxcvbn strength analysis
    check_strength = getattr(args, 'check_strength', False)
    if check_strength:
        from .security.strength_checker import check_strength as zxcvbn_check, format_strength_report, is_available
        if is_available():
            strength_result = zxcvbn_check(result.password)
            if strength_result:
                print(format_strength_report(strength_result, no_color))
        else:
            print(f"{Fore.YELLOW}Pattern analysis requires 'zxcvbn' package: pip install zxcvbn{Style.RESET_ALL}")
    
    # Clipboard with timeout
    if args.clipboard:
        from .output.clipboard import ClipboardManager, DEFAULT_CLIPBOARD_TIMEOUT
        
        if ClipboardManager.is_available():
            timeout = getattr(args, 'clipboard_timeout', DEFAULT_CLIPBOARD_TIMEOUT)
            if ClipboardManager.copy(result.password, timeout=timeout):
                if timeout > 0:
                    print(f"{Fore.GREEN}[OK] Copied to clipboard (auto-wipe in {timeout}s){Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[OK] Copied to clipboard{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[ERR] Failed to copy to clipboard{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Clipboard requires 'pyperclip' package: pip install pyperclip{Style.RESET_ALL}")
    
    # Logging
    if args.log:
        from .output.logger import PasswordLogger
        logger = PasswordLogger()
        logger.log(result)
        print(f"{Fore.GREEN}[OK] Logged to history{Style.RESET_ALL}")

    # Confirm Copy (Interactive Post-Generation Flow)
    if getattr(args, 'confirm_copy', False):
        from .output.clipboard import ClipboardManager, DEFAULT_CLIPBOARD_TIMEOUT
        from .output.qrcode_gen import is_available as qr_available, generate_terminal_qr
        
        prompt = f"\n{Style.BRIGHT}> Press [C]opy"
        if qr_available():
            prompt += ", [Q]R Code"
        prompt += f", or Enter to return... {Style.RESET_ALL}"
        
        choice = input(prompt).strip().lower()
        
        if choice in ['c', 'q']:
            if ClipboardManager.is_available():
                timeout = getattr(args, 'clipboard_timeout', DEFAULT_CLIPBOARD_TIMEOUT)
                if ClipboardManager.copy(result.password, timeout=timeout):
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

