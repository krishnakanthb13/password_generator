"""
Preset Profiles - Predefined security configurations for PassForge.
"""

PRESETS = {
    "strong": {
        "command": "random",
        "length": 32,
        "uppercase": True,
        "lowercase": True,
        "digits": True,
        "symbols": True,
        "min_uppercase": 4,
        "min_lowercase": 4,
        "min_digits": 4,
        "min_symbols": 4
    },
    "memorable": {
        "command": "pronounce",
        "length": 12
    },
    "dev": {
        "command": "random",
        "length": 40,
        "symbols": False,
        "no_repeats": True
    },
    "pin": {
        "command": "pin",
        "length": 6
    },
    "web": {
        "command": "random",
        "length": 16,
        "min_uppercase": 1,
        "min_lowercase": 1,
        "min_digits": 1,
        "min_symbols": 1
    },
    "wifi": {
        "command": "wifi",
        "length": 20,
        "simple": False
    },
    "key": {
        "command": "license",
        "segments": 5,
        "segment_length": 5
    }
}
