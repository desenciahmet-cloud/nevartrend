import os
from PIL import Image, ImageFilter, ImageDraw

def make_clean_studio_backdrop(output_path, width=699, height=1536):
    # Create base studio gradient background (warm luxury neutral studio wall + spotlight floor)
    img = Image.new("RGB", (width, height), (242, 240, 235))
    draw = ImageDraw.Draw(img)
    
    # Draw warm vertical gradient
    for y in range(height):
        # Top: neutral warm grey-beige (#e8e4de -> #f5f2ec)
        r = int(225 + (250 - 225) * (y / height))
        g = int(220 + (247 - 220) * (y / height))
        b = int(212 + (242 - 212) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Draw soft studio floor shadow at bottom
    floor_y = int(height * 0.78)
    for y in range(floor_y, height):
        ratio = (y - floor_y) / (height - floor_y)
        r = int(240 - 30 * ratio)
        g = int(237 - 30 * ratio)
        b = int(230 - 30 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add subtle spotlight glow in top center behind model
    spot = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(spot)
    center_x = width // 2
    center_y = int(height * 0.4)
    radius = int(width * 0.75)
    s_draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], fill=(255, 255, 255, 45))
    spot = spot.filter(ImageFilter.GaussianBlur(80))
    
    img = Image.alpha_composite(img.convert("RGBA"), spot).convert("RGB")
    img.save(output_path, quality=95)
    print(f"Generated clean studio backdrop: {output_path}")

# Create ultra-clean backdrops for catwalk poses 1..4
os.makedirs("static/images/catwalk", exist_ok=True)
for i in range(1, 5):
    make_clean_studio_backdrop(f"static/images/catwalk/clean_catwalk_{i}_bg.jpg")
    make_clean_studio_backdrop(f"static/images/catwalk/catwalk_{i}_bg.jpg")

