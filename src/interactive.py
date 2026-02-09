"""
Interactive Menu - Menu-driven interface for PassForge.
"""

import sys
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama
init()


class InteractiveMenu:
    """Interactive menu-driven interface for PassForge."""
    
    MENU_OPTIONS = [
        ("1", "Random Password", "random"),
        ("2", "Passphrase", "phrase"),
        ("3", "Leetspeak Passphrase", "leet"),
        ("4", "PIN", "pin"),
        ("5", "Pronounceable Password", "pronounce"),
        ("6", "UUID Token", "uuid"),
        ("7", "Base64 Secret", "base64"),
        ("8", "JWT Secret", "jwt"),
        ("9", "WiFi/WPA Key", "wifi"),
        ("10", "License Key", "license"),
        ("11", "Recovery Codes", "recovery"),
        ("12", "OTP Secret", "otp"),
        ("13", "Pattern Password", "pattern"),
        ("14", "View History", "history"),
        ("0", "Exit", "exit"),
    ]
    
    def __init__(self):
        self.running = True
    
    def print_menu(self):
        """Print the main menu."""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.YELLOW}  Choose a generator:{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
        
        for key, name, _ in self.MENU_OPTIONS:
            if key == "0":
                print(f"{Style.BRIGHT}{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            print(f"  {Style.BRIGHT}{Fore.GREEN}[{key:>2}]{Style.RESET_ALL} {name}")
        
        print(f"{Style.BRIGHT}{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
    
    def get_input(self, prompt: str, default: Optional[str] = None) -> str:
        """Get user input with optional default."""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        
        value = input(f"{Style.BRIGHT}{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip()
        return value if value else (default or "")
    
    def get_int(self, prompt: str, default: int, min_val: int = 1, max_val: int = 100) -> int:
        """Get integer input with validation."""
        while True:
            value = self.get_input(prompt, str(default))
            try:
                num = int(value)
                if min_val <= num <= max_val:
                    return num
                print(f"{Style.BRIGHT}{Fore.RED}Please enter a number between {min_val} and {max_val}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Style.BRIGHT}{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
    
    def get_bool(self, prompt: str, default: bool = False) -> bool:
        """Get yes/no input."""
        default_str = "Y/n" if default else "y/N"
        value = self.get_input(f"{prompt} ({default_str})", "").lower()
        if value in ["y", "yes"]:
            return True
        elif value in ["n", "no"]:
            return False
        return default
    
    def print_result(self, result, show_entropy: bool = True):
        """Print a generator result."""
        from .output.formatter import colorize_password
        from .security.entropy import EntropyCalculator
        
        print(f"\n{Style.BRIGHT}{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.WHITE}Generated:{Style.RESET_ALL}")
        print(f"\n{colorize_password(result.password)}\n")
        
        if show_entropy:
            strength = EntropyCalculator.get_strength_label(result.entropy_bits)
            crack_time = EntropyCalculator.get_crack_time_estimate(result.entropy_bits)
            print(f"{Style.BRIGHT}{Fore.YELLOW}Entropy:{Style.RESET_ALL} {result.entropy_bits:.2f} bits")
            print(f"{Style.BRIGHT}{Fore.YELLOW}Strength:{Style.RESET_ALL} {strength}")
            print(f"{Style.BRIGHT}{Fore.YELLOW}Crack Time:{Style.RESET_ALL} {crack_time}")
        
        print(f"{Style.BRIGHT}{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
    
    def handle_random(self):
        """Handle random password generation."""
        from .generators.random_password import RandomPasswordGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Random Password ==={Style.RESET_ALL}")
        
        length = self.get_int("Length", 16, 4, 128)
        uppercase = self.get_bool("Include uppercase", True)
        lowercase = self.get_bool("Include lowercase", True)
        digits = self.get_bool("Include digits", True)
        symbols = self.get_bool("Include symbols", True)
        easy_read = self.get_bool("Easy to read (no ambiguous chars)", False)
        count = self.get_int("How many to generate", 1, 1, 10)
        
        generator = RandomPasswordGenerator(easy_read=easy_read)
        
        for i in range(count):
            result = generator.generate(
                length=length,
                uppercase=uppercase,
                lowercase=lowercase,
                digits=digits,
                symbols=symbols
            )
            self.print_result(result)
    
    def handle_phrase(self):
        """Handle passphrase generation."""
        from .generators.passphrase import PassphraseGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Passphrase ==={Style.RESET_ALL}")
        
        words = self.get_int("Number of words", 4, 2, 12)
        separator = self.get_input("Separator", "-")
        capitalize = self.get_bool("Capitalize words", False)
        count = self.get_int("How many to generate", 1, 1, 10)
        
        generator = PassphraseGenerator()
        
        for i in range(count):
            result = generator.generate(
                word_count=words,
                separator=separator,
                capitalize=capitalize
            )
            self.print_result(result)
    
    def handle_leet(self):
        """Handle leetspeak passphrase generation."""
        from .generators.leetspeak import LeetspeakGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Leetspeak Passphrase ==={Style.RESET_ALL}")
        
        words = self.get_int("Number of words", 3, 2, 8)
        print("Separator options: - _ . ,")
        separator = self.get_input("Separator", "-")
        if separator not in ["-", "_", ".", ","]:
            separator = "-"
        count = self.get_int("How many to generate", 1, 1, 10)
        
        generator = LeetspeakGenerator()
        
        for i in range(count):
            result = generator.generate(
                word_count=words,
                separator=separator
            )
            self.print_result(result)
    
    def handle_pin(self):
        """Handle PIN generation."""
        from .generators.pin import PinGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== PIN ==={Style.RESET_ALL}")
        
        length = self.get_int("PIN length", 6, 4, 20)
        count = self.get_int("How many to generate", 1, 1, 10)
        
        generator = PinGenerator()
        
        for i in range(count):
            result = generator.generate(length=length)
            self.print_result(result)
    
    def handle_pronounce(self):
        """Handle pronounceable password generation."""
        from .generators.pronounceable import PronounceableGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Pronounceable Password ==={Style.RESET_ALL}")
        
        length = self.get_int("Length", 12, 4, 32)
        count = self.get_int("How many to generate", 1, 1, 10)
        
        generator = PronounceableGenerator()
        
        for i in range(count):
            result = generator.generate(length=length)
            self.print_result(result)
    
    def handle_uuid(self):
        """Handle UUID generation."""
        from .generators.uuid_token import UuidGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== UUID Token ==={Style.RESET_ALL}")
        
        uppercase = self.get_bool("Uppercase", False)
        count = self.get_int("How many to generate", 1, 1, 10)
        
        generator = UuidGenerator()
        
        for i in range(count):
            result = generator.generate(uppercase=uppercase)
            self.print_result(result)
    
    def handle_base64(self):
        """Handle base64 secret generation."""
        from .generators.base64_secret import Base64SecretGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Base64 Secret ==={Style.RESET_ALL}")
        
        bytes_len = self.get_int("Bytes length", 32, 8, 128)
        url_safe = self.get_bool("URL-safe encoding", True)
        
        generator = Base64SecretGenerator()
        result = generator.generate(byte_length=bytes_len, url_safe=url_safe)
        self.print_result(result)
    
    def handle_jwt(self):
        """Handle JWT secret generation."""
        from .generators.jwt_secret import JwtSecretGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== JWT Secret ==={Style.RESET_ALL}")
        print("Bit sizes: 256 (HS256), 384 (HS384), 512 (HS512)")
        
        bits = self.get_int("Bits", 256, 256, 512)
        if bits not in [256, 384, 512]:
            bits = 256
        output_hex = self.get_bool("Output as hex", False)
        
        generator = JwtSecretGenerator()
        result = generator.generate(bits=bits, output_hex=output_hex)
        self.print_result(result)
    
    def handle_wifi(self):
        """Handle WiFi key generation."""
        from .generators.wifi_key import WifiKeyGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== WiFi/WPA Key ==={Style.RESET_ALL}")
        
        length = self.get_int("Length", 16, 8, 63)
        simple = self.get_bool("Simple (alphanumeric only)", False)
        
        generator = WifiKeyGenerator()
        result = generator.generate(length=length, simple=simple)
        self.print_result(result)
    
    def handle_license(self):
        """Handle license key generation."""
        from .generators.license_key import LicenseKeyGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== License Key ==={Style.RESET_ALL}")
        
        segments = self.get_int("Number of segments", 4, 2, 8)
        segment_len = self.get_int("Characters per segment", 4, 3, 6)
        
        generator = LicenseKeyGenerator()
        result = generator.generate(segments=segments, segment_length=segment_len)
        self.print_result(result)
    
    def handle_recovery(self):
        """Handle recovery codes generation."""
        from .generators.recovery_codes import RecoveryCodesGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Recovery Codes ==={Style.RESET_ALL}")
        
        count = self.get_int("Number of codes", 10, 5, 20)
        use_words = self.get_bool("Use word-based codes", False)
        
        generator = RecoveryCodesGenerator()
        result = generator.generate(count=count, use_words=use_words)
        
        print(f"\n{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Recovery Codes:{Style.RESET_ALL}\n")
        for i, code in enumerate(result.parameters['codes'], 1):
            print(f"  {Fore.YELLOW}{i:2}.{Style.RESET_ALL} {code}")
        print(f"\n  {Fore.YELLOW}Entropy per code:{Style.RESET_ALL} {result.entropy_bits:.2f} bits")
        print(f"{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
    
    def handle_otp(self):
        """Handle OTP secret generation."""
        from .generators.otp import OtpGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== OTP Secret ==={Style.RESET_ALL}")
        
        print("Digits: 6 or 8")
        digits = self.get_int("Digits", 6, 6, 8)
        if digits not in [6, 8]:
            digits = 6
        period = self.get_int("Time period (seconds)", 30, 15, 120)
        
        generator = OtpGenerator()
        result = generator.generate(digits=digits, period=period)
        
        print(f"\n{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}OTP Secret:{Style.RESET_ALL}")
        print(f"\n  {Fore.CYAN}{result.password}{Style.RESET_ALL}\n")
        print(f"  {Fore.YELLOW}OTPAuth URI:{Style.RESET_ALL}")
        print(f"  {result.parameters['otpauth_uri']}")
        print(f"\n  {Fore.YELLOW}Entropy:{Style.RESET_ALL} {result.entropy_bits:.2f} bits")
        print(f"{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
    
    def handle_pattern(self):
        """Handle pattern generation."""
        from .generators.pattern import PatternGenerator
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Pattern Password ==={Style.RESET_ALL}")
        
        print("Grid sizes: 3 (3x3), 4 (4x4), 5 (5x5)")
        grid = self.get_int("Grid size", 3, 3, 5)
        if grid not in [3, 4, 5]:
            grid = 3
        max_path = grid * grid
        path_len = self.get_int(f"Path length (4-{max_path})", 5, 4, max_path)
        
        generator = PatternGenerator()
        result = generator.generate(grid_size=grid, path_length=path_len)
        
        print(f"\n{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Pattern:{Style.RESET_ALL} {result.password}\n")
        print(result.parameters['visual_grid'])
        print(f"\n  {Fore.YELLOW}Entropy:{Style.RESET_ALL} {result.entropy_bits:.2f} bits")
        print(f"{Fore.GREEN}{'─' * 50}{Style.RESET_ALL}")
    
    def handle_history(self):
        """Handle history viewing."""
        from .output.logger import PasswordLogger
        from .output.formatter import colorize_password
        
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Password History ==={Style.RESET_ALL}")
        
        logger = PasswordLogger()
        limit = self.get_int("Show last N entries", 10, 1, 100)
        
        entries = logger.get_history(limit=limit)
        
        if not entries:
            print(f"\n{Fore.YELLOW}No history entries found.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}{'─' * 70}{Style.RESET_ALL}")
        for entry in entries:
            ts = entry['timestamp'][:19].replace('T', ' ')
            gen_type = entry['generator_type']
            password = colorize_password(entry['password'][:30])
            if len(entry['password']) > 30:
                password += "..."
            print(f"{Fore.CYAN}{ts}{Style.RESET_ALL} | {gen_type:12} | {password}")
        print(f"{Fore.GREEN}{'─' * 70}{Style.RESET_ALL}")
    
    def run(self):
        """Run the interactive menu loop."""
        handlers = {
            "random": self.handle_random,
            "phrase": self.handle_phrase,
            "leet": self.handle_leet,
            "pin": self.handle_pin,
            "pronounce": self.handle_pronounce,
            "uuid": self.handle_uuid,
            "base64": self.handle_base64,
            "jwt": self.handle_jwt,
            "wifi": self.handle_wifi,
            "license": self.handle_license,
            "recovery": self.handle_recovery,
            "otp": self.handle_otp,
            "pattern": self.handle_pattern,
            "history": self.handle_history,
        }
        
        while self.running:
            self.print_menu()
            choice = input(f"\n{Fore.GREEN}Enter choice: {Style.RESET_ALL}").strip()
            
            # Find the handler
            handler = None
            for key, name, cmd in self.MENU_OPTIONS:
                if choice == key:
                    if cmd == "exit":
                        print(f"\n{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}\n")
                        self.running = False
                    else:
                        handler = handlers.get(cmd)
                    break
            
            if handler:
                try:
                    handler()
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Cancelled.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
            elif self.running and choice:
                print(f"\n{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
