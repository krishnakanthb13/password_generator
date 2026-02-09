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
    D -->|...| H[Other Generators]
    E & F & G & H --> I[GeneratorResult]
    I --> J[Formatter (JSON/Color)]
    I --> K[Logger (JSON Lines)]
```

## 2. File Structure

| Directory | Purpose | Key Files |
| :--- | :--- | :--- |
| `src/generators/` | Core logic for each password type. | `base.py`, `random_password.py`, `otp.py` |
| `src/security/` | Entropy calculation and pattern analysis. | `entropy.py`, `strength_checker.py` |
| `src/output/` | Presentation logic and secure utilities. | `formatter.py`, `logger.py`, `clipboard.py`, `qrcode_gen.py` |
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
*   `License Key System`: Supports dynamic **AXB formatting** (A segments of B character length).

### Entropy Calculator (`src/security/entropy.py`)
Provides the `EntropyCalculator` class with static methods:
*   `calculate_from_pool(pool_size, length)`: Returns bits based on pool size.
*   `calculate_from_password(password)`: Estimates entropy based on password composition (upper bound).
*   `get_strength_label(bits)`: Maps bits to labels (Weak, Reasonable, Strong, Excellent).
*   `get_crack_time_estimate(bits)`: Returns human-readable brute-force time estimates.

### Output Formatting (`src/output/formatter.py`)
Handles colorization using `colorama`.
*   **Colors**: Digits (GREEN), Uppercase (CYAN), Lowercase (BLUE), Symbols (MAGENTA).
*   **Modes**: 
    *   Standard: Colorized string to stdout.
    *   JSON (`--json`): Pure JSON object with metadata.
    *   No-Color (`--no-color`): Plain text output.

### Logging (`src/output/logger.py`)
Writes history to `~/.passforge/pass_history.log` in JSON Lines format.
*   `entropy_bits`
*   `parameters` (length, options used)
*   **Automatic Logging**: To ensure no secret is lost, the platform launchers and interactive menu now enable history logging by default.

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
    *   `qrcode` (Optional): QR code generation for OTPs.
    *   `zxcvbn` (Optional): Password strength analysis.
    *   `Pillow` (Optional): Required by `qrcode` (for images).
*   **Dev/Test**:
    *   `pytest`: Test runner.
    *   `pytest-cov`: Coverage reporting.
    *   `pyinstaller`: Building standalone executables.
