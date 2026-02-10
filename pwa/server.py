import sys
import os
import io
import base64
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException, Query, Header, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Security: Restricted CORS Setup
# Read from ALLOWED_ORIGINS env var (comma-separated), default to localhost/wildcard for dev
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:8093,http://127.0.0.1:8093")
if allowed_origins_str == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [o.strip() for o in allowed_origins_str.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security: Basic API Key Authentication
# In production, use a more robust auth system (OAuth2, Sessions, etc.)
PASSFORGE_API_KEY = os.getenv("PASSFORGE_API_KEY", "default_secret_key")

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != PASSFORGE_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid API Key. Protected History access denied."
        )
    return x_api_key

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
    exclude: str = ""
    no_repeats: bool = False
    text: str = ""  # For phonetic


class PasswordAnalysisRequest(BaseModel):
    password: str = ""

@app.get("/api/presets")
async def get_presets():
    return PRESETS

@app.get("/api/generate")
async def generate(
    type: str = "random",
    length: int = Query(16, ge=4, le=1024),
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    words: int = Query(4, ge=2, le=20),
    separator: str = Query("-", max_length=5),
    capitalize: bool = False,
    bits: int = Query(256, ge=128, le=4096),
    hex: bool = False,
    simple: bool = False,
    segments: int = Query(4, ge=1, le=64),
    segment_length: int = Query(4, ge=1, le=32),
    grid: int = Query(3, ge=3, le=10),
    url_safe: bool = False,
    easy_read: bool = False,
    easy_say: bool = False,
    balanced: bool = False,
    min_upper: int = Query(0, ge=0, le=1024),
    min_lower: int = Query(0, ge=0, le=1024),
    min_digits: int = Query(0, ge=0, le=1024),
    min_symbols: int = Query(0, ge=0, le=1024),
    include: str = Query("", max_length=128),
    exclude: str = Query("", max_length=128),
    no_repeats: bool = False,
    text: str = Query("", max_length=1024), # phonetic
    otp_digits: int = Query(6, ge=4, le=10), # OTP specific
    period: int = Query(30, ge=1, le=3600), # OTP
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
            # SECURITY CONSIDERATION: 
            # Password history is stored in a local JSON Lines file (~/.passforge/pass_history.log).
            # By default, passwords are encrypted using Fernet (AES-128) if the 'cryptography' 
            # package is installed. Ensure the .vault.key file is protected.
            pwd_logger = PasswordLogger()
            pwd_logger.log(result)

        # Generate QR if possible using a unique temporary file to avoid race conditions
        qr_base64 = None
        if QRCODE_AVAILABLE:
            # For OTP use URI, otherwise use password
            qr_data = result.parameters.get('otpauth_uri', result.password) if type == "otp" else result.password
            
            # Use unique temporary file for QR generation
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_qr:
                tmp_qr_path = tmp_qr.name
            
            try:
                if generate_qr_image(qr_data, tmp_qr_path):
                    with open(tmp_qr_path, "rb") as f:
                        qr_base64 = base64.b64encode(f.read()).decode("utf-8")
            finally:
                if os.path.exists(tmp_qr_path):
                    os.unlink(tmp_qr_path)

        return {
            "password": result.password,
            "entropy": round(result.entropy_bits, 2),
            "type": type,
            "qr": qr_base64
        }
    except Exception as e:
        logger.exception("Internal error in generate route")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/analyze")
async def analyze(request: PasswordAnalysisRequest, response: Response):
    """
    Analyze password strength. 
    Accepts password in POST body and returns security headers to prevent caching.
    """
    password = request.password
    if not password:
        raise HTTPException(status_code=400, detail="Password required")
    
    # Set Cache-Control headers to prevent sensitive data from being cached
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"

    try:
        calc = EntropyCalculator()
        entropy, pool_size = calc.calculate_from_password(password)
        
        strength = None
        if zxcvbn_available():
            res = zxcvbn_check(password)
            if res:
                strength = {
                    "score": res.score,
                    "warning": res.feedback_warning,
                    "suggestions": res.feedback_suggestions
                }
        
        return {
            "entropy": round(entropy, 2),
            "strength": strength
        }
    except Exception:
        logger.exception("Internal error in analyze route")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/history")
async def get_history(limit: int = 10, search: str = None, _ = Depends(verify_api_key)):
    """Retrieve password history. Requires X-API-Key authentication."""
    pwd_logger = PasswordLogger()
    return pwd_logger.get_history(limit=limit, search=search)

@app.delete("/api/history")
async def clear_history(_ = Depends(verify_api_key)):
    """Clear all history. Requires X-API-Key authentication."""
    pwd_logger = PasswordLogger()
    pwd_logger.clear_history()
    return {"status": "success"}

# Serve Frontend
# Security: Prevent source code exposure via static mount
class SecureStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        if path.endswith((".py", ".sh", ".bat", ".key", ".log", "__pycache__")):
             raise HTTPException(status_code=403, detail="Access denied to system file")
        return await super().get_response(path, scope)

app.mount("/", SecureStaticFiles(directory=Path(__file__).parent, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8093)
