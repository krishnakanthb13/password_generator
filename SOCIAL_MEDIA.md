# Social Media Announcements

This document contains social media posts for each release.

## [v1.0.14] - 2026-02-10

### 💼 LinkedIn

🛡️ The "Iron Wall" Update: Introducing PassForge v1.0.14 🚀

Security isn't just about the strength of the passwords we generate; it's about the resilience of the tools we use. Today's update for PassForge focuses on "Defense in Depth"—hardening our CLI and Web interfaces against modern security concerns.

Key technical upgrades in v1.0.14:
- 🛡️ Zero-Leakage Architecture: Our PWA backend now explicitly blocks browser access to Python source code, logs, and cryptographic keys. 
- 🙈 Masked CLI Analysis: Auditing an existing password? Your input is now masked via `getpass`, ensuring sensitive data never hits the screen.
- 🧱 CDN Resilience: We've implemented defensive safety wrappers in the frontend. PassForge now initializes flawlessly even when offline or behind restrictive firewalls that block standard CDNs.
- ⚡ Fetch Integrity: Resolved history loading issues and optimized API key error handling for a smoother, more reliable PWA experience.

At PassForge, we believe security should be uncompromising and tools should be resilient. Whether you're in the terminal or on the web, your secrets are safe with the Iron Wall.

Check out the full release notes:
https://github.com/krishnakanthb13/password_generator

#CyberSecurity #OpenSource #DevSecOps #Privacy #Python #PassForge #WebSecurity

---

### 🤖 Reddit (r/python, r/commandline, r/opensource, r/netsec, r/sysadmin)

**Title: PassForge v1.0.14: Hardening the "Iron Wall" – Masked CLI Inputs, Source Sequestration, and CDN Resilience**

Hey everyone!

Following some great feedback on local security boundaries, I've just pushed **PassForge v1.0.14**. This release is dedicated to "Defense in Depth" – ensuring the tool is not only secure to use but also resilient in restrictive environments.

**What's new in the Iron Wall update?**

1.  🛡️ **Zero-Leakage (PWA)**: I've implemented a custom `SecureStaticFiles` handler in the FastAPI backend. It explicitly forbids the browser from reading `.py`, `.sh`, `.bat`, or `.key` files. No more "local source exposure" risks.
2.  🙈 **Masked Analysis (CLI)**: When using `passforge analyze`, the input is now masked via `getpass`. You can audit your most sensitive passwords without worrying about shoulder-surfers or terminal logs catching the plaintext.
3.  🧱 **Defensive Frontend**: The PWA now includes safety checks for Lucide icons and other CDN-delivered assets. If your firewall blocks the CDN or you're offline, the app still initializes gracefully.
4.  ⚡ **SW v7 & Fetch Fixes**: Improved service worker caching and fixed a bug in the history fetching logic that was causing silent failures in some browsers.

PassForge started as a simple generator; it's now becoming a platform for secure credential orchestration.

**Repo:** https://github.com/krishnakanthb13/password_generator

Audit the code, run it offline, and let me know what you think! 🛠️

---

### 🐦 X (Twitter)

PassForge v1.0.14 is here: The "Iron Wall" Update 🛡️🚀

✨ 🛡️ Zero-Leakage: PWA source code & keys now blocked from browser access
✨ 🙈 Masked CLI: `analyze` cmd now uses `getpass` for privacy
✨ 🧱 CDN Resilience: Defensive UI works even when CDNs are blocked
✨ ⚡ Improved History Loading

Security-first, always.
https://github.com/krishnakanthb13/password_generator

#Security #Python #OpenSource #DevTools #CLI

---

## [v1.0.5] - 2026-02-10

### 💼 LinkedIn

🔒 Hardening Local Password Security: Introducing PassForge v1.0.5 🚀

The latest update for PassForge is all about privacy and precision. While generating strong passwords is critical, storing them securely on your local machine is equally important.

What's new in v1.0.5:
- 🔐 Encrypted History Vault: Your generation history is now automatically protected with AES-128 (Fernet) encryption using a machine-unique key. 
- 🙈 Privacy-First Viewing: We've implemented mandatory redaction in terminal displays and history exports. Your secrets stay secret, even when sharing your screen.
- ⚖️ Balanced Mode: A new generation algorithm that ensures a 60/20/20 ratio of letters, digits, and symbols—creating highly secure passwords that actually look professional.
- 📊 Standalone Auditing: Use the new 'analyze' command to audit the strength of any existing password using both Shannon entropy and zxcvbn pattern analysis.

We've also upgraded our terminal QR codes to high-fidelity Unicode blocks for a cleaner, more scan-friendly experience.

Maintaining security in a CLI environment often means balancing power with safety. With v1.0.5, PassForge sets a new standard for local credential management.

Check out the full release notes and the open-source repo:
https://github.com/krishnakanthb13/password_generator

#CyberSecurity #OpenSource #DevSecOps #Python #PassForge #Privacy #CLI

---

### 🤖 Reddit (r/python, r/commandline, r/opensource, r/netsec, r/sysadmin)

**Title: PassForge v1.0.5: Enhancing CLI Password Security with AES-128 History Vaults and Balanced Distribution**

Hey everyone!

I've just released **PassForge v1.0.5**, and this update pushes the tool from a simple generator to a more robust local credential manager.

**The Privacy Problem:**
Many users requested a way to keep a history of generated passwords (for those "did I copy that?" moments), but keeping a plaintext log file is a huge security risk.

**The Solution:**
In v1.0.5, I've implemented a **Secured Vault**. All generation history is now encrypted on-the-fly using **AES-128 (Fernet)** with a key that's unique to your machine and protected with strict 0600 file permissions.

**Other Major Technical Updates:**
1.  **Analyze Command**: You can now audit external passwords (`passforge analyze "input"`) using a combination of Shannon entropy and `zxcvbn` pattern detection.
2.  **Balanced Mode**: Standard uniform randomness often yields "noisy" passwords (e.g., $$$&%92ka). The new `--balanced` flag uses weighted selection (60% letters, 20% digits, 20% symbols) to create credentials that look human-made but are mathematically robust.
3.  **Permutation Math**: Entropy for non-repeating passwords is now calculated using `math.lgamma` for permutation-based accuracy ($P(n, k)$) rather than standard power logic ($n^k$).
4.  **Unicode QR Codes**: We've ditched the ASCII `@@` blocks for high-fidelity Unicode `█` blocks, making terminal-based TOTP setup much more reliable for camera apps.

**Check it out on GitHub:**
https://github.com/krishnakanthb13/password_generator

Feedback is (as always) very welcome!

---

### 🐦 X (Twitter)

PassForge v1.0.5 is out! 🔐🚀

✨ New AES-128 Encrypted History Vault
✨ Balanced Mode for cleaner passwords
✨ Standalone Password Auditing (`analyze`)
✨ High-fidelity Unicode QR codes
✨ Masked/Redacted history viewing

Secure your terminal workflow.
https://github.com/krishnakanthb13/password_generator

#Security #Python #OpenSource #DevTools #CLI

---


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
