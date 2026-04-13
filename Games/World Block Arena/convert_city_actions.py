from PIL import Image
import base64, io, os

IMG_DIR = r"C:\Users\thefi\OneDrive\Desktop\CARD BLOCK\Pics\City Action"

# Map filename → JS key name
FILE_MAP = {
    "Block Backdraft.png": "city_backdraft",
    "Block Career Change.png": "city_career_change",
    "Block City Planning.png": "city_planning",
    "Block City Wide Search.png": "city_search",
    "Block Constrution Site.png": "city_construction_site",
    "Block Dispatch.png": "city_dispatch",
    "Block House.png": "city_block_house",
    "Block Mayor.png": "city_mayor",
    "Block Taxi.png": "city_taxi",
    "Block Tractor.png": "city_tractor",
    "Block Traffic Jam.png": "city_traffic_jam",
    "Block Transport.png": "city_transport",
}

MAX_DIM = 256  # resize to max 256px on longest side
QUALITY = 60   # JPEG quality

results = {}

for filename, key in FILE_MAP.items():
    path = os.path.join(IMG_DIR, filename)
    img = Image.open(path).convert("RGB")

    # Resize keeping aspect ratio
    w, h = img.size
    if max(w, h) > MAX_DIM:
        scale = MAX_DIM / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # Encode to JPEG base64
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=QUALITY, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    results[key] = f"data:image/jpeg;base64,{b64}"
    print(f"{key}: {len(b64)} chars (from {filename})")

# Write JS snippet
with open(r"C:\Users\thefi\OneDrive\Desktop\CARD BLOCK\city_action_imgs.js", "w") as f:
    for key, val in results.items():
        f.write(f"{key}:'{val}',\n")

print(f"\nDone! {len(results)} images written to city_action_imgs.js")
