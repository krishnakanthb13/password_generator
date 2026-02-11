# Code Documentation

This document provides a technical walkthrough of the **PassForge** codebase. It is intended for developers who wish to understand the inner workings, contribute new features, or integrate with the API.

## 1. High-Level Architecture

PassForge follows a modular architecture where the **Command Handler** (`command_handler.py`) orchestrates requests between the **CLI** (`cli.py`), **Generators** (`generators/`), and **Output** (`output/`) components.

```mermaid
graph TD
    A[main.py] --> B[cli.py (Argparse)]
    B --> C[command_handler.py]
    C --> D{Generator Type?}
    D -->|random| E[RandomPasswordGenerator]
    D -->|phrase| F[PassphraseGenerator]
    D -->|otp| G[OtpGenerator]
    D -->|phonetic| H[PhoneticGenerator]
    D -->|...| I[Other Generators]
    E & F & G & H & I --> J[GeneratorResult]
    J --> K[Formatter (JSON/Color)]
    J --> L[Logger (Encrypted JSONL)]
    L --> M[Vault (AES-128)]
```

## 2. File Structure

| Directory | Purpose | Key Files |
| :--- | :--- | :--- |
| `src/generators/` | Core logic for each password type. | `base.py`, `random_password.py`, `otp.py` |
| `src/security/` | Entropy, strength, and encryption. | `entropy.py`, `vault.py`, `jitter.py` |
| `src/output/` | Presentation and secure logging. | `formatter.py`, `logger.py` |
| `src/config/` | Configuration file parsing and presets. | `loader.py`, `presets.py` |
| `tests/` | Unit tests ensuring generator correctness. | `test_generators.py`, `test_security_output.py` |

## 3. Core Modules

### Generator System (`src/generators/`)
All generators inherit from `BaseGenerator` (`src/generators/base.py`).

**Interface:**
```python
class BaseGenerator(ABC):
    @property
    @abstractmethod
    def generator_type(self) -> str:
        """The identifier string (e.g., 'random', 'otp')."""
        pass

    @abstractmethod
    def generate(self, **kwargs) -> GeneratorResult:
        """The main generation logic."""
        pass
```

**Common Utilities:**
*   `calculate_entropy(pool_size, length)`: Computes Shannon entropy bits.
*   `filter_charset(charset)`: Removes ambiguous characters (`0`, `O`, `1`, `I`, `l`) if `easy_read` is set.
*   `to_leetspeak(word)`: Specialized logic for Leetspeak using a **50% substitution ratio** to balance security with human readability.
*   `Balanced Mode`: Implements weighted selection (60% letters, 20% digits, 20% symbols) to prevent "symbol crowding" in random passwords.
*   `License Key System`: Supports dynamic **AXB formatting** (A segments of B character length).
*   `Phonetic Conversion`: Maps characters to NATO standard (A -> Alpha) for clear verbal communication.
*   **OTP System**: Implements **RFC 6238 (TOTP)**.
    *   **Logic**: Uses `hmac` with configurable algorithms (SHA1/256/512) and `struct` to perform dynamic truncation of the hash into a 6 or 8-digit code.
    *   **Time Drift**: Defaults to a **30-second period**.
    1.  Secret is generated as cryptographically secure random bytes.
    2.  Bytes are Base32 encoded for app compatibility.
    3.  A `GeneratorResult` is returned with the **current code** as the primary password.

### Themed Passphrases (`src/generators/passphrase.py`)
Utilizes the `data/wordlists/` directory to offer themed generation.
*   **Scanning**: Use `os.listdir` to find `.txt` files.
*   **Selection**: Interactive menus (Python & Shell) present a **numbered list** for easy user selection.
*   **Execution**: Passes the full path to `PassphraseGenerator(wordlist_path=...)`.

### Entropy Calculator (`src/security/entropy.py`)
Provides the `EntropyCalculator` class with static methods:
*   `calculate_from_pool(pool_size, length)`: Returns bits based on pool size.
*   `calculate_from_password(password)`: Estimates entropy based on construction using a **single-pass analysis** for high performance. Returns a tuple of `(entropy_bits, pool_size)`.
*   `no_repeats logic`: Uses **Permutation-based entropy** ($P(n, k)$) via `math.lgamma` instead of standard $n^k$ power logic when character repetition is disabled.
*   `format_entropy_report()`: Generates a visual table in the CLI containing Length, Entropy, Pool Size, Strength, and Crack Time.
*   `get_strength_label(bits)`: Maps bits to labels (Weak, Reasonable, Strong, Excellent).
*   `get_crack_time_estimate(bits)`: Returns human-readable brute-force time estimates based on an assumed 10 billion guesses/sec.

### Jitter Entropy Collector (`src/security/jitter.py`)
Enables "Paranoid Mode" by collecting true user randomness.
*   **Logic**: Uses `msvcrt.kbhit()` (Windows) or `termios` (Linux) to capture **nanosecond-precision timestamps** of keystrokes.
*   **Mixing**: The collected timing data is hashed (SHA-256) and then **mixed** into the `secrets` output using HMAC-SHA256, ensuring the final result depends on both the OS CSPRNG and the physical user input.
*   **Use Case**: For users who want to guarantee entropy beyond what the OS kernel provides.

### Output Formatting (`src/output/formatter.py`)
Handles colorization using `colorama`.
*   **Colors**: Digits (GREEN), Uppercase (CYAN), Lowercase (BLUE), Symbols (MAGENTA).
*   **Modes**: 
    *   Standard: Colorized string to stdout.
    *   JSON (`--json`): Pure JSON object with metadata.
    *   No-Color (`--no-color`): Plain text output.

### Vault & Security (`src/security/vault.py`)
Handles local encryption of sensitive history data.
*   **Encryption**: Uses `cryptography.fernet` (AES-128 in CBC mode with HMAC signatures).
*   **Key Management**: Prioritizes `PASSFORGE_API_KEY` from `.env`. Fallbacks to legacy `.vault.key` in `~/.passforge/` for backward compatibility.
*   **File Permissions**: Enforces `0600` (Owner Read/Write) on key files atomically during creation.
*   **Error Handling**: Validates encryption tokens and logs warnings on failure without crashing.

### Logging (`src/output/logger.py`)
Writes history to `~/.passforge/pass_history.log` in JSON Lines format.
*   **Encrypted Secrets**: Passwords are automatically encrypted via the `Vault` before being written to disk.
*   **Redacted Export**: The `export_history` method redacts password values by default to prevent accidental data leaks.
*   **Automatic Logging**: Enabled by default in launchers and interactive mode.

### Preset System (`src/config/presets.py`)
Uses `apply_preset(args)` in `command_handler.py` to intercept and override command-line arguments with predefined values.
*   **Default Injection**: Ensures all necessary attributes exist on the `Namespace` object.
*   **Logic Inversion**: Handles flags where `True` in preset means `False` in CLI (e.g., `uppercase=True` maps to `no_uppercase=False`).

## 4. Execution Flow (Example: `passforge random -l 16`)

1.  **Entry**: `main.py` calls `cli.main()`.
2.  **Parse**: `argparse` parses `-l 16` (or `--preset strong`).
3.  **Route**: `command_handler.handle_command()`:
    *   Calls `apply_preset(args)` if `--preset` is present.
    *   Calls appropriate handler (e.g., `handle_random(args)`).
4.  **Instantiate**: `RandomPasswordGenerator(easy_read=False)` is created.
5.  **Generate**: `generator.generate(length=16, ...)` runs:
    *   Builds `charset` (upper+lower+digits+symbols).
    *   Uses `secrets.choice()` to pick 16 secure characters.
    *   Calculates entropy (~94 chars ^ 16).
    *   Returns `GeneratorResult`.
6.  **Output**: `command_handler.output_result()`:
    *   Calls `colorize_password()` to format the string.
    *   Prints to stdout with **strictly one blank line** for visual separation.
    *   (Optional) Logs to history if `--log` is present.
7.  **Loop**: In Interactive Mode, the system pauses with a "Press Enter" prompt to prevent screen-clearing before the user has viewed the result.

## 5. Adding a New Generator

1.  Create `src/generators/new_type.py`.
2.  Inherit from `BaseGenerator`.
3.  Implement `generator_type` and `generate()`.
4.  Add a handler function in `src/command_handler.py`.
5.  Register the subcommand in `src/cli.py`.
6.  Add unit tests in `tests/test_generators.py`.

## 6. Dependencies

*   **Runtime**:
    *   `colorama`: Cross-platform ANSI colors.
    *   `pyperclip` (Optional): Clipboard integration.
    *   `cryptography`: Secure history encryption (AES-128).
    *   `qrcode` (Optional): QR code generation for OTPs.
    *   `zxcvbn` (Optional): Password strength analysis.
    *   `Pillow` (Optional): Required by `qrcode` (for images).
*   **Dev/Test**:
    *   `pytest`: Test runner.
    *   `pytest-cov`: Coverage reporting.
    *   `pyinstaller`: Building standalone executables.

## 7. Installation & Usage (Release Artifacts)

PassForge is distributed in three formats: Standalone Executable, packaged ZIP/Tarball, and Source Code.

### A. Standalone Executable (`passforge_v1.0.14.exe` / `passforge_v1.0.14`)
A single-file binary containing the Python runtime and all dependencies.
*   **How to use**: Download and run with `-i` to enter Interactive Mode.
*   **Command Line**: Open a terminal in the folder and run `passforge_v1.0.14.exe random -l 20`.
*   **Pros**: Zero installation, fully portable (USB drive ready).

### B. ZIP / Tarball (`passforge_v1.0.14.zip`)
Examples: `.zip` (Windows), `.tar.gz` (Linux/macOS).
Contains the executable plus helper scripts, documentation, and wordlists.
1.  **Extract**: Right-click -> Extract All (or `unzip passforge_v1.0.14.zip`).
2.  **Run**:
    *   **Windows**: Double-click `passforge_launch.bat` for the full menu experience.
    *   **Linux/Mac**: Run `./passforge_launch.sh` in a terminal.
3.  **Why use this?**: The launchers provide a superior UX with auto-clearing screens, menus, and theme selection that the raw executable lacks by default.

### C. Source Code
For developers who want to modify the code.
1.  `git clone ...`
2.  `pip install -r requirements.txt`
3.  `python main.py --interactive`

## 🌐 PWA Architecture (Add-on)

The PassForge PWA is designed as a modular add-on that bridges the existing Python logic with a modern web interface.

### Components in `pwa/`
- **`server.py`**: A FastAPI-based backend that imports generators from `src/` and exposes them via a REST API. 
    *   **SecureStaticFiles**: 🛡️ Subclasses `StaticFiles` to block access to sensitive file extensions (`.py`, `.sh`, `.bat`, `.key`, `.log`).
- **`index.html`**: The main application shell using semantic HTML and Lucide icons.
- **`css/style.css`**: A premium design system with Glassmorphism and theme variables.
- **`js/app.js`**: Pure Vanilla Javascript handling state management and UI rendering.
    - **Defensive UI**: 🛡️ Wraps all `lucide` calls in safety checks and provides network-resilient feedback to prevent crashes if the application initializes offline.
- **`manifest.json` / `sw.js`**: Standard PWA manifests for an installable mobile/desktop experience.
    - **sw.js (v7+)**: Implements atomic precaching for core assets and individual caching for external scripts (Lucide, Google Fonts) to maximize offline resilience.

### API Endpoints
- `GET /api/generate`: Accepts parameters (type, length, etc.) and returns the generated secret along with entropy and a base64 QR code. Supports optional logging.
- `GET /api/history`: Retrieves encrypted history entries. Protected by `verify_api_key` dependency.
- `DELETE /api/history`: Clears local history logs. Protected by `verify_api_key` dependency.
- `POST /api/analyze`: Accepts a password in the request body and returns entropy metrics. Sets `No-Cache` security headers to protect sensitive data.

### Folder Isolation
All PWA-specific files are strictly contained within the `pwa/` directory and project root launchers to ensure zero impact on the core CLI functionality.
