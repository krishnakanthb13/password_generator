# Password Generator Literature

This document provides context for each password generator type included in PassForge, detailing what it is, who it's for, why it's used, and when to use it.

## 1. Random Password
**What it is:** Generates a random sequence of characters including uppercase, lowercase, numbers, and symbols.  
**Who uses it:** General users, system administrators, automated systems.  
**Why is it present:** To provide the highest level of entropy and security for passwords that don't need to be memorized (e.g., stored in a password manager).  
**When to use it:** For primary account passwords, root passwords, and any scenario where security is paramount and memorability is not a concern.

## 2. Passphrase
**What it is:** Generates a sequence of random words separated by a delimiter (e.g., `correct-horse-battery-staple`).  
**Who uses it:** Users who need to type or remember their passwords.  
**Why is it present:** To balance high security (entropy) with human memorability.  
**When to use it:** For master passwords, disk encryption keys, or login credentials that must be typed frequently on mobile devices.

## 3. PIN
**What it is:** Generates a numeric-only sequence.  
**Who uses it:** Mobile users, banking systems, physical access control systems.  
**Why is it present:** To support legacy systems or interfaces restricted to numeric input.  
**When to use it:** For ATM cards, lock screens, SIM cards, or 2FA fallback codes.

## 4. Pronounceable
**What it is:** Generates nonsensical but pronounceable words using alternating consonants and vowels.  
**Who uses it:** Users who need to verbally communicate passwords.  
**Why is it present:** To create passwords that "sound" like real words, making them easier to read and say aloud without them being dictionary words.  
**When to use it:** When sharing a password over the phone or in person.

## 5. Leetspeak
**What it is:** Generates a passphrase where letters are substituted with visually similar numbers or symbols (e.g., `P4ssw0rd`).  
**Who uses it:** Users accustomed to internet slang or complying with legacy "complexity" rules.  
**Why is it present:** To modify memorable words into strings that pass strict character composition rules (must have numbers/symbols).  
**When to use it:** On sites with specific, possibly outdated, password complexity requirements.

## 6. UUID (Universally Unique Identifier)
**What it is:** Generates a standard 128-bit label. Supports RFC 4122/9562 versions:
*   **v1**: Time + Node (MAC) based.
*   **v4**: Completely random (most common).
*   **v7**: Unix Epoch time-based (chronologically sortable).
*   **Short**: Base58 encoded (~22 chars) for compact URLs.
**Who uses it:** Developers, database administrators, system architects.  
**Why is it present:** To provide standard unique identifiers for database records, API keys, or session tokens. v7 is specifically useful for database primary keys as it preserves insertion order.  
**When to use it:** Use v4 for general purpose, v7 for database indexing, and Short Base58 for public-facing IDs or compact tokens.

## 7. Base64 Secret
**What it is:** Generates cryptographically strong random bytes and encodes them in Base64.  
**Who uses it:** DevOps engineers, API developers.  
**Why is it present:** To create compact, safe-for-transport strings that represent binary data.  
**When to use it:** For API keys, session secrets, or cryptographic salts.

## 8. JWT Secret (JSON Web Token)
**What it is:** Generates a specific length random string suitable for signing JWTs (HS256/HS512).  
**Who uses it:** Web developers, security engineers.  
**Why is it present:** To ensure authentication tokens are signed with keys of adequate length and entropy to prevent brute-force attacks.  
**When to use it:** Configuring authentication middleware or setting up OAuth providers.

## 9. WiFi Key (WPA/WPA2)
**What it is:** Generates long hexadecimal or alphanumeric strings optimized for router configurations.  
**Who uses it:** Network administrators, home users setting up routers.  
**Why is it present:** To secure wireless networks against brute-force intrusion.  
**When to use it:** When setting up a new WiFi network or resetting a router.

## 10. License Key
**What it is:** Generates formatted strings (usually in groups) that look like software serial numbers (e.g., `XXXX-XXXX-XXXX-XXXX`).  
**Who uses it:** Software vendors, content creators.  
**Why is it present:** To distribute unique access tokens for software or digital products.  
**When to use it:** Generating keys for software distribution or redeemable codes.

## 11. Recovery Codes
**What it is:** Generates a batch of short, random codes.  
**Who uses it:** System architects implementing 2FA.  
**Why is it present:** To provide backup access methods when primary authentication factors are lost.  
**When to use it:** Implementing "backup codes" for user accounts.

## 12. Pattern
**What it is:** Generates a visual grid pattern (like Android lock screens) and its numeric path.  
**Who uses it:** Mobile users, UI designers.  
**Why is it present:** To visualize spatial passwords.  
**When to use it:** Setting up mobile device locks or testing pattern-lock security.

## 13. OTP (One-Time Password)
**What it is:** Generates a TOTP (Time-based One-Time Password) secret and the corresponding current code.  
**Who uses it:** Users setting up 2FA, developers testing MFA flows.  
**Why is it present:** To test or manually generate 2FA codes without a phone app.  
**When to use it:** Debugging 2FA implementations or generating a secret key for a new user.

## 14. Phonetic
**What it is:** Converts text to the NATO phonetic alphabet (e.g., "a" -> "Alpha") or generates a random phonetic sequence.  
**Who uses it:** Support staff, military/aviation personnel, anyone communicating codes verbally.  
**Why is it present:** To eliminate ambiguity when reading passwords or codes over voice channels (preventing "B" vs "D" confusion).  
**When to use it:** Reading a complex password over the phone.
