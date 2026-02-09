# PassForge Test Report

**Generated:** 2026-02-09  
**Platform:** Windows 10, Python 3.12.10  
**Test Framework:** pytest 9.0.2  

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | 41 |
| **Passed** | 41 |
| **Failed** | 0 |
| **Skipped** | 0 |
| **Duration** | 0.71s |
| **Status** | ✅ **ALL PASS** |

---

## Test Coverage by Module

### 1. RandomPasswordGenerator (10 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_default_length` | Default password length is 16 | ✅ PASS |
| `test_custom_length` | Custom length (24 chars) | ✅ PASS |
| `test_no_uppercase` | Exclude uppercase letters | ✅ PASS |
| `test_no_lowercase` | Exclude lowercase letters | ✅ PASS |
| `test_no_digits` | Exclude digits | ✅ PASS |
| `test_no_symbols` | Exclude symbols | ✅ PASS |
| `test_minimum_requirements` | Min char type requirements | ✅ PASS |
| `test_no_repeats` | No duplicate characters | ✅ PASS |
| `test_entropy_positive` | Entropy is calculated | ✅ PASS |
| `test_easy_read_mode` | Excludes ambiguous chars | ✅ PASS |

### 2. PassphraseGenerator (5 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_default_word_count` | Default 4 words | ✅ PASS |
| `test_custom_word_count` | Custom word count (6) | ✅ PASS |
| `test_custom_separator` | Custom separator (_) | ✅ PASS |
| `test_capitalize` | Word capitalization | ✅ PASS |
| `test_entropy_positive` | Entropy is positive | ✅ PASS |

### 3. LeetspeakGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_contains_substitutions` | Contains numeric substitutions | ✅ PASS |
| `test_separator` | Custom separator works | ✅ PASS |

### 4. PinGenerator (3 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_default_length` | Default PIN length is 6 | ✅ PASS |
| `test_numeric_only` | PIN contains only digits | ✅ PASS |
| `test_custom_length` | Custom PIN length (8) | ✅ PASS |

### 5. PronounceableGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_default_length` | Approximate default length | ✅ PASS |
| `test_contains_only_letters` | Alphabetic only | ✅ PASS |

### 6. UuidGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_uuid_format` | RFC 4122 v4 format | ✅ PASS |
| `test_uppercase_option` | Uppercase output | ✅ PASS |

### 7. Base64SecretGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_output_length` | Length for byte count | ✅ PASS |
| `test_entropy` | Entropy matches bytes | ✅ PASS |

### 8. JwtSecretGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_256_bit_secret` | 256-bit / HS256 | ✅ PASS |
| `test_512_bit_secret` | 512-bit / HS512 | ✅ PASS |

### 9. WifiKeyGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_minimum_length` | Minimum WPA length (8) | ✅ PASS |
| `test_simple_mode` | Alphanumeric only | ✅ PASS |

### 10. LicenseKeyGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_default_format` | Default 4x4 format | ✅ PASS |
| `test_uppercase_output` | Uppercase output | ✅ PASS |

### 11. RecoveryCodesGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_default_count` | Default 10 codes | ✅ PASS |
| `test_word_based_codes` | Word-based format | ✅ PASS |

### 12. OtpGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_base32_format` | Base32 encoding | ✅ PASS |
| `test_otpauth_uri` | otpauth:// URI generated | ✅ PASS |

### 13. PatternGenerator (2 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_path_length` | Correct path length | ✅ PASS |
| `test_no_duplicate_points` | No duplicate points | ✅ PASS |

### 14. EntropyCalculator (3 tests)

| Test | Description | Status |
|------|-------------|--------|
| `test_entropy_from_pool` | Entropy calculation formula | ✅ PASS |
| `test_strength_labels` | Strength thresholds | ✅ PASS |
| `test_crack_time_estimate` | Crack time estimation | ✅ PASS |

---

## Test Execution Details

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\ADMIN\OneDrive\Documents\GitHub\password_generator
plugins: anyio-4.12.0, langsmith-0.4.59
collected 41 items

tests/test_generators.py::TestRandomPasswordGenerator::test_custom_length PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_default_length PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_easy_read_mode PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_entropy_positive PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_minimum_requirements PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_no_digits PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_no_lowercase PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_no_repeats PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_no_symbols PASSED
tests/test_generators.py::TestRandomPasswordGenerator::test_no_uppercase PASSED
tests/test_generators.py::TestPassphraseGenerator::test_capitalize PASSED
tests/test_generators.py::TestPassphraseGenerator::test_custom_separator PASSED
tests/test_generators.py::TestPassphraseGenerator::test_custom_word_count PASSED
tests/test_generators.py::TestPassphraseGenerator::test_default_word_count PASSED
tests/test_generators.py::TestPassphraseGenerator::test_entropy_positive PASSED
tests/test_generators.py::TestLeetspeakGenerator::test_contains_substitutions PASSED
tests/test_generators.py::TestLeetspeakGenerator::test_separator PASSED
tests/test_generators.py::TestPinGenerator::test_custom_length PASSED
tests/test_generators.py::TestPinGenerator::test_default_length PASSED
tests/test_generators.py::TestPinGenerator::test_numeric_only PASSED
tests/test_generators.py::TestPronounceableGenerator::test_contains_only_letters PASSED
tests/test_generators.py::TestPronounceableGenerator::test_default_length PASSED
tests/test_generators.py::TestUuidGenerator::test_uppercase_option PASSED
tests/test_generators.py::TestUuidGenerator::test_uuid_format PASSED
tests/test_generators.py::TestBase64SecretGenerator::test_entropy PASSED
tests/test_generators.py::TestBase64SecretGenerator::test_output_length PASSED
tests/test_generators.py::TestJwtSecretGenerator::test_256_bit_secret PASSED
tests/test_generators.py::TestJwtSecretGenerator::test_512_bit_secret PASSED
tests/test_generators.py::TestWifiKeyGenerator::test_minimum_length PASSED
tests/test_generators.py::TestWifiKeyGenerator::test_simple_mode PASSED
tests/test_generators.py::TestLicenseKeyGenerator::test_default_format PASSED
tests/test_generators.py::TestLicenseKeyGenerator::test_uppercase_output PASSED
tests/test_generators.py::TestRecoveryCodesGenerator::test_default_count PASSED
tests/test_generators.py::TestRecoveryCodesGenerator::test_word_based_codes PASSED
tests/test_generators.py::TestOtpGenerator::test_base32_format PASSED
tests/test_generators.py::TestOtpGenerator::test_otpauth_uri PASSED
tests/test_generators.py::TestPatternGenerator::test_no_duplicate_points PASSED
tests/test_generators.py::TestPatternGenerator::test_path_length PASSED
tests/test_generators.py::TestEntropyCalculator::test_crack_time_estimate PASSED
tests/test_generators.py::TestEntropyCalculator::test_entropy_from_pool PASSED
tests/test_generators.py::TestEntropyCalculator::test_strength_labels PASSED

============================= 41 passed in 0.71s ==============================
```

---

## Bug Fixes Applied

### 1. `no_repeats` Bug (Fixed 2026-02-09)

**Issue:** When generating passwords with `no_repeats=True`, duplicate characters could still appear because the available character pool wasn't being updated after each selection.

**Root Cause:** The loop was using `secrets.choice(available)` but not removing the chosen character from `available`.

**Fix:** Changed to use `available.pop(idx)` to remove each chosen character from the pool:

```python
# Before (buggy)
password_chars.extend(secrets.choice(available) for _ in range(remaining))

# After (fixed)
for _ in range(remaining):
    if available:
        idx = secrets.randbelow(len(available))
        chosen = available.pop(idx)
        password_chars.append(chosen)
```

---

## Security Notes

1. **CSPRNG Usage:** All generators use Python's `secrets` module backed by the OS CSPRNG
2. **No Weak RNG:** Standard `random` module is never used for password generation
3. **Entropy Calculation:** Uses correct formula: `length * log2(pool_size)`
4. **History Storage:** Logs stored in `~/.passforge/` (outside repository, gitignored)

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test class
python -m pytest tests/test_generators.py::TestRandomPasswordGenerator -v
```
