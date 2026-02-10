import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Portable path resolution
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

def _ensure_assets_dir():
    """Ensure the assets directory exists on-demand."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def create_icon(size):
    """Generate a PWA icon with centered text and scalable font fallback."""
    _ensure_assets_dir()
    
    # Create simple blue icon with 'PF' text
    img = Image.new('RGB', (size, size), color='#3b82f6')
    d = ImageDraw.Draw(img)
    
    # Tiered font fallback: System TrueType -> Scalable Fallback -> Default
    font = None
    font_size = int(size / 2)
    
    for font_name in ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]:
        try:
            font = ImageFont.truetype(font_name, font_size)
            if font: break
        except IOError:
            continue
            
    if not font:
        # Final resort: tiny default bitmap font
        font = ImageFont.load_default()

    text = "PF"
    
    # Center text using bbox
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) / 2, (size - text_height) / 2 - (size * 0.1))
    
    d.text(position, text, fill=(255, 255, 255), font=font)
    
    filename = f"icon-{size}.png"
    path = ASSETS_DIR / filename
    img.save(path)
    print(f"Created {path}")

if __name__ == "__main__":
    create_icon(192)
    create_icon(512)
