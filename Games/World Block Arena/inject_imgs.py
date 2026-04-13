import re

HTML_PATH = r"C:\Users\thefi\OneDrive\Desktop\CARD BLOCK\blockbrawl_dnb.html"
IMGS_PATH = r"C:\Users\thefi\OneDrive\Desktop\CARD BLOCK\city_action_imgs.js"

# Read the city action image JS lines
with open(IMGS_PATH, "r") as f:
    img_lines = f.read().strip()

# Read the HTML
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Find the closing of CARD_IMGS object: the line with just "};"
# after "const CARD_IMGS = {"
# We need to insert the new entries before the closing "};"
# Find the CARD_IMGS block
start_marker = "const CARD_IMGS = {"
end_pattern = "\n};\n"

start_idx = html.index(start_marker)
# Find the closing }; after the start
# Search for "\n};\n" after start_idx
search_from = start_idx
end_idx = html.index("\n};\n", search_from)

# Insert new entries before the closing };
# The position is right before the \n};
insert_pos = end_idx

# Check if last line before }; already has a comma
before = html[insert_pos-1]
prefix = "\n" if before != "\n" else ""

new_html = html[:insert_pos] + prefix + img_lines + "\n" + html[insert_pos:]

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Injected {img_lines.count(chr(10))+1} image entries into CARD_IMGS")
print(f"HTML file updated: {HTML_PATH}")
