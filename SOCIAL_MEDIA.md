# Social Media Announcements

This document contains social media posts for each release.

## [v1.0.0] - 2026-02-09

### 💼 LinkedIn

Introducing PassForge v1.0.0 - The Ultimate CLI Password Generator 🚀

We are thrilled to announce the official release of PassForge v1.0.0!

PassForge is a production-ready, cryptographically secure password generator designed for developers, sysadmins, and security professionals who demand control and offline security.

Why we built this:
We faced a common problem: needing a secure, reliable way to generate all types of credentials—from simple passwords to JWT tokens and WiFi WPA keys—without leaving the terminal or trusting online generators. PassForge is the solution.

🔑 Value Add:
- 17 Generation Modes: Cover every use case from standard Passwords to License Keys, Recovery Codes, and NATO Phonetic output.
- Human-Centric Security: Generate memorable "Themed Passphrases" and pronounceable passwords that balance security with usability.
- Complete Auditability: Real-time entropy calculation ensures you know exactly how strong your secret is.
- Zero-Trust Architecture: 100% offline, using OS-level CSPRNG. No data ever leaves your machine.

Technical Highlights:
- Cross-platform launchers for Windows, Linux, and macOS.
- Single binary distribution (~7MB) with zero external dependencies.
- Interactive TUI wizard for complex configurations.

Whether you're securing a server, generating API keys, or just need a new Netflix password, PassForge puts the power in your hands.

Check out the repository and download the latest release here:
https://github.com/krishnakanthb13/password_generator

#OpenSource #Security #Python #CyberSecurity #DevTools #PasswordManager #CLI

---

### 🤖 Reddit (r/python, r/commandline, r/opensource, r/programming, r/netsec, r/sysadmin)

**Title: I built a "Swiss Army Knife" for credentials – PassForge v1.0.0 (17 modes, Offline, Python)**

Hey r/commandline!

I'm excited to share **PassForge v1.0.0**, an open-source CLI tool I've been working on to solve the "fragmented credential generation" problem.

**The Problem:**
I got tired of googling "random string generator" or remembering 15 different `openssl` commands just to get a JWT secret, a UUID, or a decent WPA2 key. I wanted one tool that could do it all, offline, and securely.

**The Solution:**
PassForge is a single binary (Python-based) that handles **17 different generation modes**:
*   `random`: Standard secure passwords (configurable charset/length).
*   `phrase`: Diceware-style passphrases (e.g., `Correct-Horse-Battery-Staple`).
*   **NEW** `themed`: Generate phrases from themes like **Animals**, **Sci-Fi**, or **Biology** (e.g., `Nebula-Photon-Galaxy-Void`).
*   `phonetic`: Output passwords in NATO alphabet (`Papa-Alpha-Sierra`) for over-the-phone sharing.
*   `jwt`: Generate HS256/384/512 secrets.
*   `otp`: Create TOTP/HOTP secrets and display a **scannable QR code** directly in your terminal.
*   `wifi`: Generate WPA2/3 compatible preshared keys.
*   `license`: Create software license keys (e.g., `XXXX-YYYY-ZZZZ`).

**Why you might like it:**
1.  **Entropy Transparency**: It calculates and displays the Shannon entropy bits for every generated secret.
2.  **Interactive Mode**: Don't like flags? Run `passforge --interactive` for a TUI wizard.
3.  **Secure Clipboard**: Auto-copies and then **auto-wipes** the clipboard after 30 seconds.
4.  **Zero-Indentation UI**: Clean output designed for easy reading and piping.

**Tech Stack:**
*   Python 3.12+ (Type Hinted)
*   `secrets` module (CSPRNG) for all randomness.
*   `pytest` with high coverage.
*   Builds to a single executable (~7MB) using PyInstaller.

I'd love for you to give it a spin and let me know what you think!

**Repository:** https://github.com/krishnakanthb13/password_generator

---

### 🐦 X (Twitter)

PassForge v1.0.0 is live! 🚀

The ultimate CLI credential generator.
✨ 17 Modes (JWT, OTP, WiFi, UUID)
🔐 100% Offline & Secure (CSPRNG)
📱 Terminal QR Codes for TOTP
🖥️ Single Binary (Win/Linux/Mac)

Take control of your secrets.
https://github.com/krishnakanthb13/password_generator

#CyberSecurity #Python #OpenSource #DevTools
