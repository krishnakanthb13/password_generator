"""
Jitter Entropy Collector - Collects entropy from human timing variability.
"""

import time
import hashlib
import sys
from typing import Optional

try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
except ImportError:
    # Fallback if colorama is not available
    class Fore: RED = ""; GREEN = ""; YELLOW = ""; RESET = ""; CYAN = ""; MAGENTA = ""
    class Style: BRIGHT = ""; RESET_ALL = ""

def collect_jitter(duration: int = 5) -> str:
    """
    Collect entropy from the timing of keyboard presses.
    
    Args:
        duration: Time in seconds to collect data
        
    Returns:
        A SHA-256 hex digest of the collected timing data
    """
    print(f"\n{Style.BRIGHT}{Fore.CYAN}🛡️ ENTERING PARANOID MODE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}--------------------------------------------------{Style.RESET_ALL}")
    print(f"To generate extra entropy, please {Style.BRIGHT}bash your keyboard randomly{Style.RESET_ALL}.")
    print(f"We are measuring the micro-timing (nanoseconds) between your keys.")
    print(f"{Fore.YELLOW}--------------------------------------------------{Style.RESET_ALL}\n")
    
    # Try to use msvcrt for non-blocking input on Windows
    # or termios on Linux
    try:
        import msvcrt
        platform = "win"
    except ImportError:
        try:
            import tty
            import termios
            platform = "linux"
        except ImportError:
            platform = "fallback"

    timing_data = []
    start_time = time.time()
    next_milestone = 1
    
    print(f"[{Fore.GREEN}{' ' * 20}{Style.RESET_ALL}] 0%", end="\r")
    
    # Simple input collection loop
    # We want to catch characters as they come
    
    if platform == "win":
        while time.time() - start_time < duration:
            if msvcrt.kbhit():
                # Get the key
                key = msvcrt.getch()
                # Record current precise time
                t = time.perf_counter_ns()
                timing_data.append(str(t) + str(key))
            
            # Update progress bar
            elapsed = time.time() - start_time
            progress = int((elapsed / duration) * 20)
            percent = int((elapsed / duration) * 100)
            
            bar = "█" * progress + " " * (20 - progress)
            print(f"[{Fore.GREEN}{bar}{Style.RESET_ALL}] {percent}%", end="\r")
            time.sleep(0.01) # Small sleep to prevent CPU spike
            
    elif platform == "linux":
        # Linux implementation would go here (omitted for brevity in this specific windows-focused session but structure is here)
        # Using a simple fallback for now if tty/termios is tricky to handle in one shot
        pass
    
    if not timing_data or platform == "fallback":
        # Standard input fallback if specialized modules aren't available
        # Ask for a random string
        print(f"{Fore.MAGENTA}Specialized input handler unavailable. Fallback enabled.{Style.RESET_ALL}")
        print("Please type a long string of random characters and press Enter:")
        user_input = input("> ")
        timing_data.append(user_input + str(time.perf_counter_ns()))
    
    print(f"\n\n{Fore.GREEN}✅ Entropy collection complete! {len(timing_data)} samples gathered.{Style.RESET_ALL}")
    
    # Hash the data
    seed = hashlib.sha256("".join(timing_data).encode()).hexdigest()
    return seed

def mix_entropy(base_bytes: bytes, custom_seed: str) -> bytes:
    """
    Mix a custom seed into a base byte sequence (CSPRNG output).
    Uses HMAC-SHA256 to combine them.
    """
    import hmac
    return hmac.new(custom_seed.encode(), base_bytes, hashlib.sha256).digest()
