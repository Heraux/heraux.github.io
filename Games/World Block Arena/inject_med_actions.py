"""
Inject medieval action card images into blockbrawl_dnb.html.
Converts PNG files to JPEG base64 (quality 60, max 200px wide)
and adds them to CARD_IMGS + updates card definitions with img properties.
"""

import base64
import io
import re
from PIL import Image

BASE_DIR = r"C:\Users\thefi\OneDrive\Desktop\CARD BLOCK"
PICS_DIR = BASE_DIR + r"\Pics\Medieval Actions"
HTML_FILE = BASE_DIR + r"\blockbrawl_dnb.html"

# Mapping: card_id -> (img_key, filename)
CARD_MAP = [
    ("royal_rally",       "med_royal_rally",       "Block Royal Rally.png"),
    ("castle_drawbridge", "med_castle_drawbridge", "Block Castle DrawBridge.png"),
    ("knights_shield",    "med_knights_shield",    "Knights Shield.png"),
    ("scholarly",         "med_scholarly",          "Block Scholarly.png"),
    ("royal_ball",        "med_royal_ball",         "Block Royal Ball.png"),
    ("hold_the_line",     "med_hold_the_line",      "Block Hold the Line.png"),
    ("witchs_brew",       "med_witchs_brew",        "Block Witches brew.png"),
    ("kings_declaration", "med_kings_declaration",  "Blocky Kings Declaration.png"),
    ("siege",             "med_siege",              "Block Siege.png"),
    ("council_summons",   "med_council_summons",    "Block Court Summon.png"),
    ("coronation",        "med_coronation",         "Block Coronation.png"),
    ("last_stand",        "med_last_stand",         "Block Last stand.png"),
]

MAX_WIDTH = 200
JPEG_QUALITY = 60


def png_to_jpeg_base64(filepath):
    """Read a PNG, resize to max 200px wide, convert to JPEG base64."""
    img = Image.open(filepath)
    # Convert RGBA to RGB (JPEG doesn't support alpha)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    # Resize if wider than MAX_WIDTH
    w, h = img.size
    if w > MAX_WIDTH:
        ratio = MAX_WIDTH / w
        new_h = int(h * ratio)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
    # Save to JPEG in memory
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def main():
    # 1. Generate base64 strings for all cards
    img_entries = {}
    for card_id, img_key, filename in CARD_MAP:
        filepath = f"{PICS_DIR}\\{filename}"
        print(f"Processing {filename}...")
        b64_str = png_to_jpeg_base64(filepath)
        img_entries[img_key] = b64_str
        print(f"  -> {img_key}: {len(b64_str)} chars")

    # 2. Read the HTML file
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # 3. Find the last med_ entry in CARD_IMGS to insert after it
    # Look for the last line starting with  'med_
    last_med_line = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("'med_") and "data:image/jpeg;base64," in line:
            last_med_line = i

    if last_med_line is None:
        print("ERROR: Could not find existing med_ entries in CARD_IMGS!")
        return

    print(f"\nLast existing med_ entry at line {last_med_line + 1}")

    # Build new CARD_IMGS entries
    new_img_lines = []
    for card_id, img_key, filename in CARD_MAP:
        new_img_lines.append(f"  '{img_key}': '{img_entries[img_key]}',")

    # Insert after the last med_ entry
    lines = lines[:last_med_line + 1] + new_img_lines + lines[last_med_line + 1:]
    print(f"Inserted {len(new_img_lines)} CARD_IMGS entries after line {last_med_line + 1}")

    # 4. Update card definitions to add img property
    # The card defs shifted by len(new_img_lines) lines
    updated_count = 0
    for card_id, img_key, filename in CARD_MAP:
        # Find the card definition line
        for i, line in enumerate(lines):
            # Match the card definition pattern, e.g.: royal_rally:{id:'royal_rally',...
            if line.strip().startswith(f"{card_id}:{{id:'{card_id}'"):
                if f"img:'{img_key}'" not in line:
                    # Add img property before the closing },
                    # Insert img:'med_xxx' before desc:
                    line_new = line.replace(
                        f"desc:'",
                        f"img:'{img_key}',desc:'"
                    )
                    if line_new != line:
                        lines[i] = line_new
                        updated_count += 1
                        print(f"  Updated {card_id} with img:'{img_key}'")
                    else:
                        print(f"  WARNING: Could not update {card_id}")
                else:
                    print(f"  {card_id} already has img property")
                break

    print(f"\nUpdated {updated_count} card definitions")

    # 5. Write back
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nDone! File saved: {HTML_FILE}")


if __name__ == "__main__":
    main()
