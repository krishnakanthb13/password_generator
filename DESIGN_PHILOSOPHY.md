# Design Philosophy

This document outlines the core principles, decisions, and constraints that shaped **PassForge**. It serves as a guide for understanding *why* the system is built this way and how future contributions should align with its vision.

## 1. The Core Problem

Developers, sysadmins, and security-conscious users often need various types of credentials—random passwords, PINs, API keys, OTP secrets—but lack a unified, trustworthy tool to generate them.

Existing solutions often fall into two categories:
1.  **Web-based generators**: Convenient but inherently insecure (shipping secrets over the wire, trust in server-side RNG).
2.  **Fragmented CLI one-liners**: `openssl rand -base64 32` is great, but memorizing syntax for 15 differents use cases is terrible UX.

**PassForge** bridges this gap by providing a **single, secure, offline CLI** for every credential generation need.

## 2. Guiding Principles

### A. Security First, Always
*   **CSPRNG Only**: We exclusively use Python's `secrets` module (backed by the OS CSPRNG). The standard `random` module is strictly forbidden for generation logic.
*   **Entropy Transparency**: Users should know *exactly* how strong a generated secret is. We calculate and display Shannon entropy for every result.
*   **Offline by Default**: No network calls are made during generation. The tool must be safe to run on air-gapped machines.

### B. Developer Experience (DX)
*   **Memorability**: Commands should be intuitive (`passforge random`, `passforge pin`).
*   **Composability**: The tool should work well in pipes and scripts. Support for JSON output (`--json`) and silent mode is crucial.
*   **Cross-Platform Consistency**: A script written on macOS should work identically on Windows and Linux.

### C. Modularity & Extensibility
*   **Plugin-like Architecture**: Each generator (`random`, `uuid`, `otp`) is an isolated module inheriting from a `BaseGenerator`. Adding a new generator should never require modifying existing core logic.
*   **Zero-Dependency Core**: The core library relies only on Python standard libraries where possible. External dependencies (like `colorama` or `pyperclip`) are kept minimal and optional where feasible.

### D. Visual Excellence (UI/UX)
*   **The "Zero-Indentation" Rule**: All prompts, headers, and passwords are aligned to Column 0. This creates a sharp vertical alignment for technical precision.
*   **The "One-Line Spacing" Rule**: Exactly one blank line is maintained before and after generated secrets to ensure visual prominence without excessive scrolling.
*   **Numbered Selection**: In launchers and menus, options are always numbered. Users should never have to type a full filename (e.g., "animals.txt") when they can type "1".

### F. Defense in Depth (Hardening)
*   **Masked Inputs**: 🛡️ Sensitive operations (like analyzing an existing password in the CLI) use `getpass` to mask input, preventing shoulder-surfing.
*   **Source Sequestration**: 🛡️ The PWA server utilizes `SecureStaticFiles` to explicitly block access to its own source code, logs, and system keys via the browser.
*   **Resilient Context**: Frontend logic assumes external resources (like CDNs) might fail and provides safe fallbacks and Service Worker caching to ensure core generation remains functional.

### E. Human-Centric Design
*   **Verbal Communication**: Support for NATO phonetic output ensures passwords can be shared over the phone unambiguously.
*   **Themed Generation**: Allowing users to choose themes (Positive, Biology, Sci-Fi) makes security personal and memorable.
*   **The "Crowding" Problem**: Pure uniform randomness often results in passwords that are 40% symbols, making them feel like "noise" and reducing readability.
*   **Weighted distribution**: We believe security shouldn't be hostile. Our "Balanced Mode" ensures a distribution that looks "human-generated" (mostly letters) while maintaining the mathematical strength of cryptographically secure selection.

## 3. Key Design Decisions

### Why Python?
*   **Auditability**: Python code is highly readable, making it easier for security audits.
*   **Standard Library**: The `secrets`, `uuid`, `base64`, and `hmac` libraries provide robust primitives out of the box.
*   **Ubiquity**: Python is pre-installed on most modern developer environments.

### Why Interactive Mode & Launchers?
*   CLI flags are powerful but hard to discover. The interactive menu (`--interactive`) and platform-specific launchers (`passforge_launch.bat/sh`) serve as a self-documenting "wizard" that guides users through complex configurations.

### Security Profiles (Presets)
*   Manual configuration of 15+ flags is error-prone. We provide `PRESETS` (`--preset strong`) to codify industry-standard security patterns (e.g., 32 chars for "strong", 40 char alphanumeric for "dev"). This ensures users can generate high-quality credentials with zero cognitive load.

### Storage Strategy
*   **Encrypted History Vault**: We store history in AES-128 encrypted blocks.
    *   *Rationale*: While history is essential for convenience, secrets should never reside on disk in plaintext. By using a machine-unique key and `cryptography.fernet`, we protect the user's history against casual data theft while maintaining the seamless UX of a local tool.
    *   *Shared Persistence*: The PWA and CLI share the same encrypted vault, providing a unified experience across terminal and browser.
    *   *Consent & Transparency*: History remains opt-in for CLI users but is auto-enabled in launchers to prevent data loss. Export functionality requires explicit flags to bypass redaction, ensuring users make a conscious decision when handling raw secrets.

## 4. Trade-offs

| Decision | Pros | Cons |
| :--- | :--- | :--- |
| **Python Runtime** | Rapid dev, readable code | Requires Python installed (mitigated by PyInstaller builds) |
| **CLI-First** | Scriptable, efficient | Higher learning curve for non-technical users |
| **Strict CSPRNG** | Cryptographically secure | Slower than PRNG (not noticeable for passwords) |

## 5. Future Vision

PassForge aims to be the standard "credential Swiss Army Knife" for the terminal. Future enhancements should focus on:
1.  **Enterprise Policies**: Enforcing complexity rules defined in configuration.
2.  **Integrations**: Direct export to password managers (KeepassXC, Bitwarden CLI).
3.  **Hardware Token Support**: Writing TOTP secrets directly to YubiKeys.
