import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = r"c:\Users\ADMIN\OneDrive\Documents\GitHub\password_generator\pwa\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_icon(size):
    # Create simple blue icon with 'PF' text
    img = Image.new('RGB', (size, size), color='#3b82f6')
    d = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font = ImageFont.truetype("arial.ttf", int(size/2))
    except IOError:
        font = ImageFont.load_default()

    text = "PF"
    
    # Calculate text position to center it
    # getbbox returns (left, top, right, bottom)
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) / 2, (size - text_height) / 2 - (size*0.1))
    
    d.text(position, text, fill=(255, 255, 255), font=font)
    
    filename = f"icon-{size}.png"
    path = os.path.join(ASSETS_DIR, filename)
    img.save(path)
    print(f"Created {path}")

if __name__ == "__main__":
    create_icon(192)
    create_icon(512)
