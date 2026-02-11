# PassForge Release Notes

This document tracks all notable changes to the **PassForge** project.

## [v1.2.0] - 2026-02-11

🚀 **The "Extreme Ranges & PWA Sync" Update**

This major update pushes PassForge into the "Extreme" category, expanding the operational limits of every generator and achieving 100% feature parity between the CLI and the PWA. We've also hardened the core math to handle passwords of astronomical size (1,024+ characters) without numeric overflow.

### 🚀 New Features (v1.1.7 - v1.1.21)
*   **Massive Length Support**: You can now generate passwords up to **1,024 characters** and Base64 secrets up to **1,024 bytes**.
*   **Pro-Level Passphrases**: Expanded word counts to **64 words** for both standard Passphrases and Leetspeak.
*   **Recovery Customization**: Full control over Recovery Code generation: up to **100 codes**, with **32 digits** or **12 words** per code.
*   **UUID Versatility**: Added support for UUID Versions **1, 4, and 7** and **Short (Base58)** formatting in both CLI and PWA.
*   **Enhanced PWA Controls**: The PWA now includes full controls for Recovery Code types and strict selection for JWT bit lengths (256/384/512).

### ⚡ Improvements & Security
*   **Entropy Overflow Protection**: Capped crack-time calculation at 512 bits to prevent numeric overflow crashes when generating extremely long (1,024-char) credentials.
*   **Full PWA Synchronization**: Every slider and range in the web interface now matches the new CLI "Extreme Limits."
*   **PWA API Hardening**: implemented restricted CORS and a secure localhost-only bootstrap for API key provisioning.
*   **Secure Static Hosting**: PWA server now strictly blocks access to all `.py`, `.sh`, `.bat`, `.key`, and hidden files.

### 🏗️ Infrastructure
*   Updated all build scripts (`passforge_build.bat/sh`) and launchers (`passforge_launch.bat/sh`) to **v1.2.0**.
*   Synchronized asset versioning across the PWA stack for seamless updates.

### 📚 Documentation
*   Updated `SECURITY.md` with the latest audit findings (V1.2.0).
*   Refreshed `CODE_DOCUMENTATION.md` and `DESIGN_PHILOSOPHY.md` to reflect the expanded operational ranges.

## [v1.1.6] - 2026-02-10

🚀 **the performance & paranoid security update**

This milestone release introduces "Paranoid Mode" for high-stakes entropy collection and a major overhaul of the PWA architecture for maximum performance and offline resilience. We've consolidated core logic and refined the UI to provide a snappier, more professional experience across all platforms.

### 🚀 New Features
*   **Paranoid Mode (v1.1.0)**: 🛡️ A new high-security generation mode that utilizes timing-based entropy collection (user-driven jitter) to supplement system CSPRNGs for ultra-high-stakes secrets.
*   **Service Worker v7+ (v1.1.4-v1.1.6)**: ⚡ fully registered and optimized Service Worker with atomic precaching, ensuring near-instant load times and 100% offline functionality.
*   **Enhanced Clipboard Support (v1.1.1)**: Improved cross-platform clipboard handling with robust feedback and reliable auto-wipe across various system environments.

### ⚡ Improvements & Refactoring
*   **PWA Architecture Overhaul (v1.1.2)**: Streamlined internal routing and restructured the UI codebase for faster rendering and better maintainability.
*   **Consolidated Prompt Logic (v1.1.5)**: unified the interactive prompt system across CLI and PWA to ensure consistent validation and entropy reporting.
*   **Adaptive Entropy Handling**: Refined the entropy calculator to better account for pooled resources and complex character distributions in multi-mode generation.
*   **UI Polish (v1.1.1/v1.1.3)**: Enhanced scrollbar theming and removed redundant status badges for a cleaner, more focused "Zero-Indentation" interface.

### 📚 Documentation
*   Updated technical deep-dives to cover the new `analyze` API, Service Worker v7 logic, and Paranoid Mode security principles.
*   Enhanced code documentation with architecture diagrams for the restructured PWA frontend.

## [v1.0.14] - 2026-02-10

🚀 **the "iron wall" security & stability update**

This release focuses on hardening the PWA/CLI interface against modern attack vectors and fixing critical stability issues in the web-based generator. We've implemented a "Zero-Leakage" architecture that shields sensitive system files from local network exposure.

### 🛡️ Security Hardening
*   **Zero-Leakage Architecture**: 🛡️ The PWA backend now utilizes a `SecureStaticFiles` handler that explicitly blocks browser access to Python source files (`.py`), internal logs (`.log`), and cryptographic vault keys (`.key`).
*   **Masked Analysis**: 🛡️ The `analyze` command in CLI and Interactive Mode now uses `getpass` for masked input. Sensitive passwords entered for audit are no longer visible on the terminal screen, protecting against shoulder-surfing.
*   **Safe Subprocesses**: Refined clipboard wiper to ensure all arguments are properly escaped via `repr()` before being passed to detached processes.

### ⚡ PWA Stability & Robustness
*   **Defensive Frontend**: 🛡️ Added safety wrappers around the Lucide icon library. The PWA will now initialize gracefully even if CDN assets fail to load or are blocked by a firewall.
*   **API Key Reliability**: Optimized 401 response handling in `app.js` to provide clearer feedback and state recovery for protected history access.
*   **Fetch Integrity**: Resolved a bug where the `history` tab would fail to load due to an undefined URL variable.
*   **Atomic Service Worker**: Updated `sw.js` (v7+) for improved atomic precaching and resilient external asset management.

### 📚 Documentation
*   Updated **Design Philosophy** with new "Defense in Depth" and "Resilient Context" principles.
*   Enhanced **README.md** with security icons and the new v28 PWA architecture details.

## [v1.0.5] - 2026-02-10

🚀 **The Security & Privacy Update**

This release focuses on hardening local data storage and enhancing the quality of generated credentials. We've introduced full AES-128 encryption for your password history and a new "Balanced Mode" for more professional-looking random passwords.

### 🚀 New Features
*   **Analyze Command**: New `analyze` (alias `check`) command to audit any existing password. Combines Shannon entropy with deep `zxcvbn` pattern analysis.
*   **Balanced Distribution Mode**: New `--balanced` flag for random passwords that enforces a 60% Letters / 20% Digits / 20% Symbols ratio—reducing "symbol crowding" while maintaining high entropy.

### ⚡ Security Improvements
*   **Encrypted History Vault**: Your generation history is now encrypted with a machine-unique AES-128 (Fernet) key.
*   **Privacy-First Viewing**: History passwords are now masked with asterisks by default in both CLI (`--redact`) and the Interactive Menu.
*   **Redacted Exports**: Security-first export logic that redacts secrets by default.
*   **Permutation-based Entropy**: Switched to `math.lgamma` for mathematically precise entropy on passwords with `no_repeats=True`.
*   **Single-Pass Composition Analysis**: Optimized entropy analyzer that checks character pools in a single pass for high performance.

### ⚡ UI/UX Enhancements
*   **High-Fidelity Unicode QR Codes**: Switched to Unicode block characters (`█`) for terminal QR codes, improving visual clarity and scan success rates.
*   **Security Status Monitor**: New real-time indicator in the Interactive Menu showing whether your history is being securely encrypted.
*   **Smart Weight Redistribution**: Balanced mode now intelligently shifts weights if specific character pools are disabled via flags.

### 📚 Documentation
*   Updated **Design Philosophy** to reflect our shift to private-by-default history.
*   Updated **Code Documentation** with deep dives into the Vault architecture and permutation math.

---


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
*   **History Viewer Improvements**: History now defaults to 10 entries, added `--all` flag to view complete history, and removed password trimming in the viewer.

### 🛠️ Technical Improvements
*   **Standalone Builds**: Optimised PyInstaller build scripts that bundle all dependencies (including wordlists and config) into a single ~7MB executable.
*   **Zero-Indentation UI**: A clean, professional CLI output style designed for easy reading and piping.
*   **Configuration**: Support for YAML/JSON config files to persist user preferences.
*   **Code Quality**: 100% type-hinted Python codebase with comprehensive unit tests (`pytest`).

### 📚 Documentation
*   **Complete Guide**: Updated `README.md` with usage examples for all 17 modes.
*   **Architecture**: Added `CODE_DOCUMENTATION.md` detailing the modular plugin system.
*   **Philosophy**: published `DESIGN_PHILOSOPHY.md` outlining the security-first and human-centric design principles.
