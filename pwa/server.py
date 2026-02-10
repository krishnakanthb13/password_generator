import sys
import os
import io
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to sys.path to import from src
sys.path.append(str(Path(__file__).parent.parent))

from src.generators.random_password import RandomPasswordGenerator
from src.generators.passphrase import PassphraseGenerator
from src.generators.pin import PinGenerator
from src.generators.pronounceable import PronounceableGenerator
from src.generators.leetspeak import LeetspeakGenerator
from src.generators.uuid_token import UuidGenerator
from src.generators.base64_secret import Base64SecretGenerator
from src.generators.jwt_secret import JwtSecretGenerator
from src.generators.wifi_key import WifiKeyGenerator
from src.generators.license_key import LicenseKeyGenerator
from src.generators.recovery_codes import RecoveryCodesGenerator
from src.generators.pattern import PatternGenerator
from src.generators.otp import OtpGenerator
from src.generators.phonetic import PhoneticGenerator
from src.output.logger import PasswordLogger
from src.output.qrcode_gen import generate_qr_image, QRCODE_AVAILABLE
from src.config.presets import PRESETS
from src.security.entropy import EntropyCalculator
from src.security.strength_checker import check_strength as zxcvbn_check, is_available as zxcvbn_available

app = FastAPI(title="PassForge API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class GeneratorParams(BaseModel):
    type: str = "random"
    length: int = 16
    uppercase: bool = True
    lowercase: bool = True
    digits: bool = True
    symbols: bool = True
    words: int = 4
    separator: str = "-"
    capitalize: bool = False
    count: int = 1
    bits: int = 256
    hex: bool = False
    simple: bool = False
    segments: int = 4
    segment_length: int = 4
    grid: int = 3
    url_safe: bool = False
    easy_read: bool = False
    easy_say: bool = False
    balanced: bool = False
    min_upper: int = 0
    min_lower: int = 0
    min_digits: int = 0
    min_symbols: int = 0
    include: str = ""
    exclude: str = ""
    no_repeats: bool = False
    text: str = ""  # For phonetic
    password: str = "" # For analyze

@app.get("/api/presets")
async def get_presets():
    return PRESETS

@app.get("/api/generate")
async def generate(
    type: str = "random",
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    words: int = 4,
    separator: str = "-",
    capitalize: bool = False,
    bits: int = 256,
    hex: bool = False,
    simple: bool = False,
    segments: int = 4,
    segment_length: int = 4,
    grid: int = 3,
    url_safe: bool = False,
    easy_read: bool = False,
    easy_say: bool = False,
    balanced: bool = False,
    min_upper: int = 0,
    min_lower: int = 0,
    min_digits: int = 0,
    min_symbols: int = 0,
    include: str = "",
    exclude: str = "",
    no_repeats: bool = False,
    text: str = "", # phonetic
    otp_digits: int = 6, # OTP specific to avoid conflict with 'digits' boolean
    period: int = 30, # OTP
    log: bool = False
):
    try:
        result = None
        if type == "random":
            gen = RandomPasswordGenerator(easy_read=easy_read, easy_say=easy_say)
            result = gen.generate(
                length=length, 
                uppercase=uppercase, 
                lowercase=lowercase, 
                digits=digits, 
                symbols=symbols,
                include_chars=include,
                exclude_chars=exclude,
                no_repeats=no_repeats,
                min_uppercase=min_upper,
                min_lowercase=min_lower,
                min_digits=min_digits,
                min_symbols=min_symbols,
                balanced=balanced
            )
        elif type == "phrase":
            gen = PassphraseGenerator(easy_read=easy_read, easy_say=easy_say)
            result = gen.generate(word_count=words, separator=separator, capitalize=capitalize)
        elif type == "pin":
            gen = PinGenerator()
            result = gen.generate(length=length)
        elif type == "pronounce":
            gen = PronounceableGenerator()
            result = gen.generate(length=length)
        elif type == "leet":
            gen = LeetspeakGenerator()
            result = gen.generate(word_count=words, separator=separator)
        elif type == "uuid":
            gen = UuidGenerator()
            result = gen.generate(uppercase=uppercase)
        elif type == "base64":
            gen = Base64SecretGenerator()
            result = gen.generate(byte_length=length, url_safe=url_safe)
        elif type == "jwt":
            gen = JwtSecretGenerator()
            result = gen.generate(bits=bits, output_hex=hex)
        elif type == "wifi":
            gen = WifiKeyGenerator()
            result = gen.generate(length=length, simple=simple)
        elif type == "license":
            gen = LicenseKeyGenerator()
            result = gen.generate(segments=segments, segment_length=segment_length)
        elif type == "recovery":
            gen = RecoveryCodesGenerator()
            result = gen.generate(count=10, use_words=False)
        elif type == "pattern":
            gen = PatternGenerator()
            result = gen.generate(grid_size=grid)
        elif type == "phonetic":
            gen = PhoneticGenerator()
            result = gen.generate(text=text, length=length)
        elif type == "otp":
            gen = OtpGenerator()
            result = gen.generate(digits=otp_digits, period=period)
        else:
            raise HTTPException(status_code=400, detail="Invalid generator type")

        if log:
            logger = PasswordLogger()
            logger.log(result)

        # Generate QR if possible
        qr_base64 = None
        if QRCODE_AVAILABLE:
            # For OTP use URI, otherwise use password
            qr_data = result.parameters.get('otpauth_uri', result.password) if type == "otp" else result.password
            
            # Temporary file for QR
            qr_path = Path(__file__).parent / "temp_qr.png"
            if generate_qr_image(qr_data, str(qr_path)):
                with open(qr_path, "rb") as f:
                    qr_base64 = base64.b64encode(f.read()).decode("utf-8")
                qr_path.unlink()

        return {
            "password": result.password,
            "entropy": round(result.entropy_bits, 2),
            "type": type,
            "qr": qr_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analyze")
async def analyze(password: str = ""):
    if not password:
        raise HTTPException(status_code=400, detail="Password required")
    
    calc = EntropyCalculator()
    entropy = calc.calculate_from_password(password)
    
    strength = None
    if zxcvbn_available():
        res = zxcvbn_check(password)
        strength = {
            "score": res.get("score"),
            "warning": res.get("feedback", {}).get("warning"),
            "suggestions": res.get("feedback", {}).get("suggestions")
        }
    
    return {
        "password": password,
        "entropy": round(entropy, 2),
        "strength": strength
    }

@app.get("/api/history")
async def get_history(limit: int = 10, search: str = None):
    logger = PasswordLogger()
    return logger.get_history(limit=limit, search=search)

@app.delete("/api/history")
async def clear_history():
    logger = PasswordLogger()
    logger.clear_history()
    return {"status": "success"}

# Serve Frontend
app.mount("/", StaticFiles(directory=Path(__file__).parent, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8093)
