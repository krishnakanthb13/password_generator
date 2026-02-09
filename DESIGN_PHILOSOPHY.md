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

## 3. Key Design Decisions

### Why Python?
*   **Auditability**: Python code is highly readable, making it easier for security audits.
*   **Standard Library**: The `secrets`, `uuid`, `base64`, and `hmac` libraries provide robust primitives out of the box.
*   **Ubiquity**: Python is pre-installed on most modern developer environments.

### Why Interactive Mode?
*   CLI flags are powerful but hard to discover. The interactive menu (`--interactive`) serves as a self-documenting "wizard" that teaches users about available options and flags.

### Storage Strategy
*   **Plaintext History**: We chose to store history in plaintext JSON lines (`~/.passforge/pass_history.log`) by default.
    *   *Rationale*: This matches the "bash history" model. If an attacker has read access to your home directory, you have bigger problems.
    *   *Mitigation*: History logging is **opt-in** via the `--log` flag (or interactive prompt) to preventing accidental leakage.

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
