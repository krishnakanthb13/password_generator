# PassForge Release Notes

This document tracks all notable changes to the **PassForge** project.

## [v1.0.0] - 2026-02-09

🚀 **Initial Production Release**

PassForge v1.0.0 marks the first stable release of the all-in-one password generator CLI. This release delivers a complete suite of 17 generation modes, robust security features, and cross-platform support.

### 🌟 Key Features
*   **17 Generation Modes**: Random, Passphrase, PIN, Leetspeak, UUID, Base64, JWT, WiFi, License Keys, Recovery Codes, OTP (TOTP/HOTP), Pattern, Pronounceable, Themed Phrases, NATO Phonetic, and more.
*   **Cryptographically Secure**: 100% reliance on Python's `secrets` module (CSPRNG). No weak PRNGs.
*   **Entropy Transparency**: Real-time Shannon entropy calculation and brute-force time estimation for every password.
*   **Cross-Platform Launchers**:
    *   `passforge_launch.bat` (Windows): Interactive menu with numbered selection.
    *   `passforge_launch.sh` (Linux/macOS): Full feature parity with Windows launcher.
*   **Interactive Menu**: A self-guiding "wizard" mode (`--interactive`) for users who prefer menus over CLI flags.

### 🚀 New Additions (since beta)
*   **Themed Passphrases**: Generate memorable phrases from themes like Animals, Sci-Fi, and Biology (e.g., `Tiger-Falcon-Shark-Wolf`).
*   **NATO Phonetic Generator**: Convert any text or password into the NATO phonetic alphabet for clear verbal communication (e.g., `Alfa-Bravo-Charlie`).
*   **QR Code Support**: Generate scannable ASCII QR codes in the terminal for OTP secrets (requires `qrcode` library).
*   **Secure Clipboard**: Auto-clearing clipboard integration with configurable timeout.
*   **History Logging**: Automatic, secure logging of generated credentials to `~/.passforge/pass_history.log`.

### 🛠️ Technical Improvements
*   **Standalone Builds**: Optimised PyInstaller build scripts that bundle all dependencies (including wordlists and config) into a single ~7MB executable.
*   **Zero-Indentation UI**: A clean, professional CLI output style designed for easy reading and piping.
*   **Configuration**: Support for YAML/JSON config files to persist user preferences.
*   **Code Quality**: 100% type-hinted Python codebase with comprehensive unit tests (`pytest`).

### 📚 Documentation
*   **Complete Guide**: Updated `README.md` with usage examples for all 17 modes.
*   **Architecture**: Added `CODE_DOCUMENTATION.md` detailing the modular plugin system.
*   **Philosophy**: published `DESIGN_PHILOSOPHY.md` outlining the security-first and human-centric design principles.
