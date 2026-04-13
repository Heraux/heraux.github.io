#!/usr/bin/env python3
"""Generate Block Brawl Rulebook v0.4 PDF — dark theme matching v0.3 aesthetics."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

W, H = letter
MARGIN = 18  # border inset
INNER = 36   # content margin from page edge
TEXT_L = 83  # left text margin
TEXT_R = W - 83  # right text margin
TEXT_W = TEXT_R - TEXT_L

# ═══════════════════════════════════════════════════════════
# COLOR PALETTE (extracted from v0.3)
# ═══════════════════════════════════════════════════════════
PAGE_BG     = (0.051, 0.024, 0.0)        # very dark brown/black
BORDER_COL  = (0.290, 0.157, 0.0)        # gold-brown border
TITLE_GOLD  = (1.0, 0.784, 0.251)        # bright gold — titles
SECTION_GOLD= (0.941, 0.627, 0.125)      # amber — section headers
BODY_CREAM  = (0.961, 0.867, 0.69)       # parchment cream — body text
DIM_BROWN   = (0.541, 0.353, 0.157)      # medium brown — footer/notes
TABLE_DARK  = (0.082, 0.039, 0.0)        # dark row bg for tables

# Deck accent colors (text on banner)
JURASSIC_BG    = (0.055, 0.141, 0.063)
JURASSIC_ACC   = (0.659, 0.878, 0.376)
MEDIEVAL_BG    = (0.133, 0.039, 0.118)
MEDIEVAL_ACC   = (0.878, 0.502, 0.753)
CITY_BG        = (0.031, 0.094, 0.188)
CITY_ACC       = (0.376, 0.753, 1.0)
SPACE_BG       = (0.039, 0.0, 0.188)
SPACE_ACC      = (0.753, 0.627, 1.0)
PERSONAL_BG    = (0.188, 0.118, 0.0)
PERSONAL_ACC   = (1.0, 0.878, 0.502)

page_num = 0

def new_page(c):
    """Draw dark background, border, footer for a new page."""
    global page_num
    if page_num > 0:
        c.showPage()
    page_num += 1
    # Full page dark bg
    c.setFillColorRGB(*PAGE_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Border rect
    c.setStrokeColorRGB(*BORDER_COL)
    c.setLineWidth(1.5)
    c.setFillColorRGB(*PAGE_BG)
    c.rect(MARGIN, MARGIN, W - 2*MARGIN, H - 2*MARGIN, fill=1, stroke=1)
    # Footer
    c.setFont('Helvetica', 7)
    c.setFillColorRGB(*DIM_BROWN)
    c.drawString(TEXT_L, 28, f"Block Brawl Official Rulebook v0.4 -- Designed by Rux & Block Jr. (age 9)")
    c.drawRightString(TEXT_R, 28, f"Page {page_num}")

def draw_title(c, text, y, size=28):
    c.setFont('Helvetica-Bold', size)
    c.setFillColorRGB(*TITLE_GOLD)
    c.drawCentredString(W/2, y, text)

def draw_section(c, text, y):
    c.setFont('Helvetica-Bold', 15)
    c.setFillColorRGB(*SECTION_GOLD)
    c.drawString(TEXT_L, y, text)
    return y

def draw_subsection(c, text, y):
    c.setFont('Helvetica-Bold', 12)
    c.setFillColorRGB(*TITLE_GOLD)
    c.drawString(TEXT_L, y, text)
    return y

def draw_body(c, text, y, indent=0, bold=False, size=9, color=None):
    col = color or BODY_CREAM
    c.setFillColorRGB(*col)
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    # Simple word wrap
    words = text.split(' ')
    line = ''
    x = TEXT_L + indent
    max_w = TEXT_W - indent
    lines_drawn = 0
    for word in words:
        test = (line + ' ' + word).strip()
        if c.stringWidth(test, c._fontname, c._fontsize) > max_w:
            c.drawString(x, y, line)
            y -= size + 3
            lines_drawn += 1
            line = word
        else:
            line = test
    if line:
        c.drawString(x, y, line)
        y -= size + 3
        lines_drawn += 1
    return y

def draw_bullet(c, text, y, bold_prefix=None, size=9):
    c.setFillColorRGB(*BODY_CREAM)
    c.setFont('Helvetica', size)
    bullet_x = TEXT_L + 8
    text_x = TEXT_L + 18
    max_w = TEXT_W - 18
    # Draw bullet
    c.drawString(bullet_x, y, chr(8226))  # bullet char
    if bold_prefix:
        c.setFont('Helvetica-Bold', size)
        c.drawString(text_x, y, bold_prefix)
        bw = c.stringWidth(bold_prefix, 'Helvetica-Bold', size)
        c.setFont('Helvetica', size)
        rest = text
        text_start = text_x + bw
    else:
        rest = text
        text_start = text_x
    # Word wrap the rest
    words = rest.split(' ')
    line = ''
    x = text_start
    first = True
    for word in words:
        test = (line + ' ' + word).strip()
        tw = c.stringWidth(test, 'Helvetica', size)
        available = TEXT_R - x
        if tw > available:
            c.drawString(x, y, line)
            y -= size + 3
            line = word
            x = text_x  # wrap to indent
            first = False
        else:
            line = test
    if line:
        c.drawString(x, y, line)
        y -= size + 3
    return y

def draw_note(c, text, y, size=8, color=None):
    col = color or DIM_BROWN
    return draw_body(c, text, y, size=size, color=col)

def draw_deck_banner(c, y, deck_bg, deck_acc, title, subtitle=None):
    """Draw a colored deck title banner like v0.3."""
    # Main banner
    c.setFillColorRGB(*deck_bg)
    c.rect(TEXT_L + 25, y - 4, TEXT_W - 25, 28, fill=1, stroke=0)
    # Accent block on right
    c.setFillColorRGB(*deck_acc)
    c.rect(TEXT_R - 108, y - 4, 108, 28, fill=1, stroke=0)
    # Title text
    c.setFont('Helvetica-Bold', 14)
    c.setFillColorRGB(*deck_acc)
    c.drawString(TEXT_L + 35, y + 4, title)
    return y - 12

def draw_chain_table(c, y, rows, header_bg, text_color, acc_color):
    """Draw a card table with dark theme. rows[0] is header."""
    col_widths = [120, 20, 20, 145, 145]  # CARD, L, P, CHAIN BONUS, ON WIN
    total_w = sum(col_widths)
    x_start = TEXT_L + 3
    row_h = 16
    header_h = 18

    # Header row
    c.setFillColorRGB(*header_bg)
    c.rect(x_start, y - header_h + 4, total_w, header_h, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 9)
    c.setFillColorRGB(0, 0, 0)
    x = x_start
    for i, cell in enumerate(rows[0]):
        c.drawString(x + 3, y - 9, cell)
        x += col_widths[i]
    y -= header_h

    # Data rows
    for ri, row in enumerate(rows[1:]):
        # Alternating row bg
        if ri % 2 == 0:
            c.setFillColorRGB(*TABLE_DARK)
        else:
            c.setFillColorRGB(*PAGE_BG)
        c.rect(x_start, y - row_h + 4, total_w, row_h, fill=1, stroke=0)

        c.setFont('Helvetica', 8)
        c.setFillColorRGB(*BODY_CREAM)
        x = x_start
        for i, cell in enumerate(row):
            c.drawString(x + 3, y - 8, cell)
            x += col_widths[i]
        y -= row_h

    # Bottom line
    c.setStrokeColorRGB(*BORDER_COL)
    c.setLineWidth(0.5)
    c.line(x_start, y + 4, x_start + total_w, y + 4)
    return y

def draw_instant_table(c, y, rows, header_bg, text_color):
    """Draw an instant/action table."""
    col_widths = [130, 320]
    total_w = sum(col_widths)
    x_start = TEXT_L + 3
    row_h = 16
    header_h = 18

    # Header
    c.setFillColorRGB(*header_bg)
    c.rect(x_start, y - header_h + 4, total_w, header_h, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 9)
    c.setFillColorRGB(0, 0, 0)
    x = x_start
    for i, cell in enumerate(rows[0]):
        c.drawString(x + 3, y - 9, cell)
        x += col_widths[i]
    y -= header_h

    for ri, row in enumerate(rows[1:]):
        # Measure if we need extra height for wrapping
        c.setFont('Helvetica', 7.5)
        effect_text = row[1] if len(row) > 1 else ''
        tw = c.stringWidth(effect_text, 'Helvetica', 7.5)
        lines_needed = max(1, int(tw / (col_widths[1] - 6)) + 1)
        actual_h = max(row_h, lines_needed * 11)

        if ri % 2 == 0:
            c.setFillColorRGB(*TABLE_DARK)
        else:
            c.setFillColorRGB(*PAGE_BG)
        c.rect(x_start, y - actual_h + 4, total_w, actual_h, fill=1, stroke=0)

        c.setFont('Helvetica', 7.5)
        c.setFillColorRGB(*BODY_CREAM)
        c.drawString(x_start + 3, y - 9, row[0])

        # Word-wrap effect text
        if len(row) > 1:
            words = row[1].split(' ')
            line = ''
            lx = x_start + col_widths[0] + 3
            ly = y - 9
            max_ew = col_widths[1] - 6
            for word in words:
                test = (line + ' ' + word).strip()
                if c.stringWidth(test, 'Helvetica', 7.5) > max_ew:
                    c.drawString(lx, ly, line)
                    ly -= 11
                    line = word
                else:
                    line = test
            if line:
                c.drawString(lx, ly, line)

        y -= actual_h

    c.setStrokeColorRGB(*BORDER_COL)
    c.setLineWidth(0.5)
    c.line(x_start, y + 4, x_start + total_w, y + 4)
    return y

def draw_personal_chain_table(c, y, rows):
    """Special table for Personal Deck chain pairs."""
    col_widths = [70, 22, 20, 85, 22, 115, 116]
    total_w = sum(col_widths)
    x_start = TEXT_L + 3
    row_h = 16
    header_h = 18

    # Header
    c.setFillColorRGB(*PERSONAL_BG)
    c.rect(x_start, y - header_h + 4, total_w, header_h, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 8)
    c.setFillColorRGB(*PERSONAL_ACC)
    x = x_start
    for i, cell in enumerate(rows[0]):
        c.drawString(x + 3, y - 9, cell)
        x += col_widths[i]
    y -= header_h

    for ri, row in enumerate(rows[1:]):
        if ri % 2 == 0:
            c.setFillColorRGB(*TABLE_DARK)
        else:
            c.setFillColorRGB(*PAGE_BG)
        c.rect(x_start, y - row_h + 4, total_w, row_h, fill=1, stroke=0)

        c.setFont('Helvetica', 8)
        c.setFillColorRGB(*BODY_CREAM)
        x = x_start
        for i, cell in enumerate(row):
            # Arrow column in gold
            if i == 2:
                c.setFillColorRGB(*TITLE_GOLD)
                c.setFont('Helvetica-Bold', 10)
                c.drawCentredString(x + col_widths[i]/2, y - 9, cell)
                c.setFont('Helvetica', 8)
                c.setFillColorRGB(*BODY_CREAM)
            else:
                c.drawString(x + 3, y - 8, cell)
            x += col_widths[i]
        y -= row_h

    c.setStrokeColorRGB(*BORDER_COL)
    c.setLineWidth(0.5)
    c.line(x_start, y + 4, x_start + total_w, y + 4)
    return y

def build():
    filepath = r"C:\Users\thefi\OneDrive\Desktop\CARD BLOCK\BlockBrawl_Rulebook_v0.4.pdf"
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setTitle("Block Brawl Official Rulebook v0.4")
    c.setAuthor("Rux & Block Jr.")

    # ════════════════ PAGE 1: TITLE + OVERVIEW + SETUP ════════════════
    new_page(c)

    draw_title(c, "BLOCK BRAWL", H - 80, 28)
    y = H - 105
    c.setFont('Helvetica', 11)
    c.setFillColorRGB(*DIM_BROWN)
    c.drawCentredString(W/2, y, "Official Rulebook & Deck Reference")
    y -= 16
    c.drawCentredString(W/2, y, "E for Everyone  |  2-4 Players  |  15-20 Minutes")
    y -= 16
    c.drawCentredString(W/2, y, "Designed by Rux & Block Jr. (age 9)")
    y -= 30

    draw_section(c, "OVERVIEW", y)
    y -= 20
    y = draw_body(c, "Block Brawl is a fast, strategic card game for 2-4 players. Each player selects one of four themed decks representing an era of civilization -- Jurassic, Medieval, City, and Space. Players race their piece along a 30-space board by winning rounds. The first player to reach 30 spaces wins.", y)
    y -= 4
    y = draw_body(c, "NEW in v0.4: Each player receives their own 20-card Personal Deck of mercenary cards. After each round, draft 5 to add to your army -- hired fighters, counters, and support that grow your deck over 4 rounds.", y, color=SECTION_GOLD, size=9)
    y -= 8

    # Era table
    era_rows = [
        ['ERA', 'PLAYSTYLE', 'IDENTITY'],
        ['Jurassic', 'Aggro / Force Win', 'Hit hard, move far, highest power ceiling'],
        ['Medieval', 'Stall / Strategy Win', 'Defensive shell hiding an instant win condition'],
        ['City', 'Versatile / Movement', 'Flexible upgrades, consistent forward movement'],
        ['Space', 'Control / Manipulation', 'MTG Blue -- break the rules, manipulate numbers'],
        ['Personal', 'Mercenary / Support', 'Drafted fighters + counters that boost any army'],
    ]
    era_cols = [85, 130, 235]
    x0 = TEXT_L + 3
    # Header
    c.setFillColorRGB(*TABLE_DARK)
    c.rect(x0, y - 14, sum(era_cols), 18, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 9)
    c.setFillColorRGB(*TITLE_GOLD)
    ex = x0
    for i, h in enumerate(era_rows[0]):
        c.drawString(ex + 3, y - 9, h)
        ex += era_cols[i]
    y -= 18
    for ri, row in enumerate(era_rows[1:]):
        bg = TABLE_DARK if ri % 2 == 0 else PAGE_BG
        # Personal row highlighted
        if ri == 4:
            bg = PERSONAL_BG
        c.setFillColorRGB(*bg)
        c.rect(x0, y - 14, sum(era_cols), 16, fill=1, stroke=0)
        c.setFont('Helvetica', 8)
        if ri == 4:
            c.setFillColorRGB(*PERSONAL_ACC)
        else:
            c.setFillColorRGB(*BODY_CREAM)
        ex = x0
        for i, cell in enumerate(row):
            c.drawString(ex + 3, y - 9, cell)
            ex += era_cols[i]
        y -= 16
    y -= 10

    draw_section(c, "COMPONENTS", y)
    y -= 18
    y = draw_bullet(c, "113 cards total -- Jurassic 25, Medieval 22, City 25, Space 21, Personal Pool 20", y)
    y = draw_bullet(c, "4 player boards, 4 player pieces, 1 Haste Token", y)
    y -= 6

    draw_section(c, "SETUP", y)
    y -= 18
    y = draw_body(c, "1. Each player chooses a deck and takes the matching board and piece.", y, indent=10)
    y = draw_body(c, "2. Shuffle your deck. Place your piece at space 0 on your board.", y, indent=10)
    y = draw_body(c, "3. Place your 5 Lvl 1 cards face down on your bench (4 bench slots + 1 active slot).", y, indent=10)
    y = draw_body(c, "4. Choose a starting active from your bench and place it face down in your active slot.", y, indent=10)
    y = draw_body(c, "5. Draw 5 cards from your deck into your hand.", y, indent=10)
    y = draw_body(c, "6. Randomly determine who gets the Haste Token -- that player goes first.", y, indent=10)

    # ════════════════ PAGE 2: RULES ════════════════
    new_page(c)
    y = H - 55

    draw_section(c, "TABLE LAYOUT", y)
    y -= 22
    c.setFont('Courier', 9)
    c.setFillColorRGB(*BODY_CREAM)
    c.drawString(TEXT_L + 10, y, "[ Bench 1 ]  [ Bench 2 ]  [ Bench 3 ]  [ Bench 4 ]")
    c.setFont('Helvetica', 8)
    c.setFillColorRGB(*DIM_BROWN)
    c.drawString(TEXT_L + 310, y, "Face-down Lvl 1s")
    y -= 14
    c.setFont('Courier', 9)
    c.setFillColorRGB(*BODY_CREAM)
    c.drawString(TEXT_L + 10, y, "[ ACTIVE ]")
    c.setFont('Helvetica', 8)
    c.setFillColorRGB(*DIM_BROWN)
    c.drawString(TEXT_L + 310, y, "Face down until round starts")
    y -= 14
    c.setFont('Courier', 9)
    c.setFillColorRGB(*BODY_CREAM)
    c.drawString(TEXT_L + 10, y, "[ Stack ]")
    c.setFont('Helvetica', 8)
    c.setFillColorRGB(*DIM_BROWN)
    c.drawString(TEXT_L + 310, y, "Instants played this round")
    y -= 22

    draw_section(c, "ROUND STRUCTURE", y)
    y -= 20
    y = draw_body(c, "STEP 1 -- FLIP: Both players simultaneously flip their active card face up.", y, bold=True)
    y -= 2
    y = draw_body(c, "STEP 2 -- PLAY PHASE: Haste Token holder goes first. Players alternate ONE action per turn:", y, bold=True)
    y = draw_bullet(c, "Play a card from hand onto your active (Lvl 1>2 or Lvl 2>3)", y, bold_prefix="Upgrade: ")
    y = draw_bullet(c, "Play an instant card from hand into your stack.", y, bold_prefix="Instant: ")
    y = draw_bullet(c, "Once both players pass consecutively, the round ends.", y, bold_prefix="Pass: ")
    y -= 2
    y = draw_note(c, "CHAIN RULE: Upgrading within the same chain triggers the chain bonus. Cross-chain upgrades work but no bonus fires.", y, size=8, color=DIM_BROWN)
    y -= 4
    y = draw_body(c, "STEP 3 -- RESOLVE: Compare power (plus modifiers). Higher power wins.", y, bold=True)
    y = draw_bullet(c, "Winner moves forward by their winning power total.", y)
    y = draw_bullet(c, "Loser does not move (unless a card effect says otherwise). Ties: neither moves.", y)
    y -= 2
    y = draw_body(c, "STEP 4 -- CLEANUP:", y, bold=True)
    y = draw_bullet(c, "Discard active and full stack. Take a bench card face down as new active. Draw to 5. Pass Haste Token.", y)
    y = draw_bullet(c, "If deck runs out, shuffle discard into a new deck.", y)
    y -= 10

    draw_section(c, "DRAFT PHASE (NEW in v0.4)", y)
    y -= 20
    y = draw_body(c, "Each player receives their own copy of the 20-card Personal Pool at the start of the game. After every round, a Draft occurs:", y)
    y = draw_body(c, "1. Your remaining Personal Pool cards are laid out face up.", y, indent=10)
    y = draw_body(c, "2. Pick 5 cards to add to your deck. They shuffle in immediately.", y, indent=10)
    y = draw_body(c, "3. Those 5 cards leave your pool -- they are now part of your deck.", y, indent=10)
    y = draw_body(c, "4. Next round: 15 remain. Then 10, then 5. After 4 drafts, all 20 are in your deck.", y, indent=10)
    y -= 2
    y = draw_note(c, "Strategy: Draft chain pairs together for the bonus! Pick counters for your opponent's deck, or support cards to shore up weaknesses. Your army grows stronger every round.", y)
    y -= 10

    draw_section(c, "WIN CONDITIONS", y)
    y -= 18
    y = draw_body(c, "1. BOARD WIN: First to reach space 30 wins immediately.", y, bold=True)
    y = draw_body(c, "2. BENCH OUT: When all Lvl 1 bench cards are used, the game ends -- furthest player wins.", y, bold=True)
    y = draw_body(c, "3. SPECIAL WIN: King's Declaration, Rip in Spacetime, and Pendulum Cosmology each carry instant-win conditions described on the card.", y, bold=True)
    y -= 4
    y = draw_note(c, "Board length: 30 spaces (2 players). Suggested 25 spaces for 3-4 players.", y)

    # ════════════════ PAGE 3: JURASSIC ════════════════
    new_page(c)
    y = H - 48
    draw_deck_banner(c, y, JURASSIC_BG, JURASSIC_ACC, "JURASSIC DECK -- AGGRO")
    y -= 26
    y = draw_body(c, "Playstyle: Offense / Aggro -- Hit hard, win big, move far.", y, bold=True)
    y = draw_note(c, "Chains: Hatchling Carno > Raptor > T-Rex  |  Hatchling Herbo > Stego > Triceratops  |  Archeologist > Explorer > Paleontologist", y)
    y = draw_note(c, "Gimmick: Highest power ceiling in the game. T-Rex at Power 10 plus a +5 move bonus on win.", y)
    y -= 6

    jchain = [
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        ['Hatchling Carno x2', '1', '1', '--', '--'],
        ['Hatchling Herbo x2', '1', '1', '--', '--'],
        ['Archeologist', '1', '1', '--', '--'],
        ['Raptor x2', '2', '5', 'Draw 1 + Pool +3', 'Opp discards 1'],
        ['Stego x2', '2', '5', 'Draw 1 + Pool +3', 'Move +2 spaces'],
        ['Explorer', '2', '4', 'Find an Action', 'Draw 2'],
        ['T-Rex', '3', '10', 'Draw 1 + Pool +4', 'Move +5 bonus!'],
        ['Triceratops', '3', '8', 'Draw 1 + Pool +4', 'Push opp back 3'],
        ['Paleontologist', '3', '7', 'Draw 2', 'Opp discards 2'],
    ]
    y = draw_chain_table(c, y, jchain, JURASSIC_ACC, (0,0,0), JURASSIC_ACC)
    y -= 10

    jinstants = [
        ['INSTANT', 'EFFECT'],
        ['Fossil Thief', 'Add a Lvl 3 from your deck to hand.'],
        ['Dino Roar', 'Place a Lvl 3 directly on a Lvl 1 (skip Lvl 2).'],
        ['Dino Instinct', 'Swap your active with a bench card.'],
        ['Dig Site', 'Find a Lvl 2 from your deck -- add to hand.'],
        ['Meteor', 'Everyone loses the round. You move 1 space.'],
        ['Dino Stampede', 'If you win this round, move +3 extra spaces.'],
        ['Block Evolution', 'Search for Archeologist, Explorer, or Paleontologist.'],
        ['Research Project', 'If you lose with an Explorer chain card, keep them active.'],
        ['Territorial Strike', 'Opponent swaps their active with a bench card of their choice.'],
        ['Fossil Fuel', 'Add +4 to your Power Pool.'],
        ['Pack Mentality', 'If you have 2+ Lvl 1s on bench, draw 3 cards.'],
        ['Extinction Event', 'Opponent discards their entire hand. They draw 2.'],
    ]
    y = draw_instant_table(c, y, jinstants, JURASSIC_ACC, (0,0,0))
    y -= 6
    draw_note(c, "Total: 25/25 cards", y, color=JURASSIC_ACC)

    # ════════════════ PAGE 4: MEDIEVAL ════════════════
    new_page(c)
    y = H - 48
    draw_deck_banner(c, y, MEDIEVAL_BG, MEDIEVAL_ACC, "MEDIEVAL DECK -- STALL")
    y -= 26
    y = draw_body(c, "Playstyle: Defense / Stall -- Defensive shell hiding an assassination win condition.", y, bold=True)
    y = draw_note(c, "Chains: Squire > Councilman  |  Peasant > Knight or Bowman > Castle/Field Commander  |  Heir > any Lvl 2 > King", y)
    y = draw_note(c, "Royal Court: Councilman on bench when King loses -- King stays on field, Councilman removed instead.", y)
    y = draw_note(c, "Instant Win: King active + opponent has no Lvl 2 or Lvl 3 on field. King only reachable via Heir lineage.", y)
    y -= 6

    mchain = [
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        ['Squire x2', '1', '1', '--', '--'],
        ['Peasant x2', '1', '1', '--', '--'],
        ['Heir', '1', '1', 'Upgrades to ANY Lvl 2', '--'],
        ['Councilman x2', '2', '7', 'Heir: find King. Else: find Action', 'Opp discards 2'],
        ['Knight x2', '2', '5', 'Draw 1 + Pool +1', 'Move +2 spaces'],
        ['Bowman', '2', '5', 'Opp discards 1 + Pool +1', 'Opp discards 1 more'],
        ['Castle Commander', '3', '8', 'Opp discards 1 + Pool +2', 'Opp skips draw next round'],
        ['Field Commander', '3', '8', 'Draw 1 + Pool +2', 'Move +3 bonus spaces'],
        ['King', '3', '9', 'Draw 2 + Pool +2', 'Opp cannot play Actions next round'],
    ]
    y = draw_chain_table(c, y, mchain, MEDIEVAL_ACC, (0,0,0), MEDIEVAL_ACC)
    y -= 10

    minstants = [
        ['INSTANT', 'EFFECT'],
        ['Royal Rally', 'Find a Lvl 2 from your deck.'],
        ['Drawbridge', 'Target opponent discards 2 cards.'],
        ['Scholarly', 'Promote any bench card to a Lvl 2 Councilman.'],
        ['Royal Ball', 'Find a Lvl 3 from your deck.'],
        ['Hold The Line!', 'Draw 2 cards + move 5 spaces. You cannot move from winning this round.'],
        ['Siege', 'Opponent cannot upgrade their active this round.'],
        ['Council Summons', 'Discard 1 card. Add a Councilman from your deck or discard pile to hand.'],
        ['Coronation', 'If King is in your hand, move 3 spaces immediately.'],
        ['Last Stand', 'If your bench is empty, your active gains +5 power this round.'],
    ]
    y = draw_instant_table(c, y, minstants, MEDIEVAL_ACC, (0,0,0))
    y -= 6
    draw_note(c, "Total: 22/22 cards (13 chain + 9 instants)", y, color=MEDIEVAL_ACC)

    # ════════════════ PAGE 5: CITY ════════════════
    new_page(c)
    y = H - 48
    draw_deck_banner(c, y, CITY_BG, CITY_ACC, "CITY DECK -- FLEX")
    y -= 26
    y = draw_body(c, "Playstyle: Utility / Versatility -- Civilians upgrade to ANY Lvl 2. No chain restriction.", y, bold=True)
    y = draw_note(c, "Gimmick: 5 Civilians as the only Lvl 1. Each Lvl 2 has a specialist instant combo.", y)
    y = draw_note(c, "Win Condition: Consistent movement + specialist synergies. Block Hero hits Power 10 with +4 win bonus.", y)
    y -= 6

    cchain = [
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        ['Civilian x5', '1', '1', '--', '--'],
        ['Farmer', '2', '4', 'Move 1 + Pool +1', 'Move 1 more'],
        ['Captain', '2', '5', 'Find Block Transport', 'Move +2'],
        ['Constr. Worker', '2', '5', 'Draw 2', 'Opp skips draw'],
        ['Officer', '2', '7', 'Draw 1 + Pool +1', 'Opp discards 1'],
        ['Firefighter', '2', '7', 'Block opp Actions round', 'Draw 2'],
        ['Foreman', '3', '7', 'Draw 2', 'Move +2 bonus'],
        ['Police Chief', '3', '9', 'Draw 1 + Pool +1', 'No Actions next round'],
        ['Block Hero', '3', '10', 'Draw 1', 'Move +4 bonus!'],
    ]
    y = draw_chain_table(c, y, cchain, CITY_ACC, (0,0,0), CITY_ACC)
    y -= 10

    cinstants = [
        ['INSTANT', 'EFFECT'],
        ['Career Change', 'Swap active with a bench Civilian. Find one Action from discard.'],
        ['Citywide Search', 'Find a Lvl 2 from your deck.'],
        ['Block Transport', 'Move 5 spaces if Captain is your active.'],
        ['Constr. Site', 'Opponent cannot move even if they win this round.'],
        ['Block House', 'Lvl 1 active only -- find any Action from your deck.'],
        ['Traffic Jam', 'No one can draw cards next turn.'],
        ['Block Taxi', 'Move 2 spaces and draw 2 cards immediately.'],
        ['Block Mayor', 'Lvl 1 Civilian only: find Block Hero and play it directly, or add to hand.'],
        ['Block Tractor', 'Farmer active only: +5 Power this round AND move 2 spaces.'],
        ['Dispatch', 'Officer or Police Chief active: opponent cannot play Actions this round.'],
        ['Backdraft', 'Firefighter active only: move 4 spaces and draw 1 card.'],
        ['City Planning', 'Look at top 4 cards of your deck and rearrange in any order.'],
    ]
    y = draw_instant_table(c, y, cinstants, CITY_ACC, (0,0,0))
    y -= 6
    draw_note(c, "Total: 25/25 cards", y, color=CITY_ACC)

    # ════════════════ PAGE 6: SPACE ════════════════
    new_page(c)
    y = H - 48
    draw_deck_banner(c, y, SPACE_BG, SPACE_ACC, "SPACE DECK -- CONTROL")
    y -= 26
    y = draw_body(c, "Playstyle: Tech / Control -- MTG Blue. Break the rules. Manipulate numbers.", y, bold=True)
    y = draw_note(c, "Chains: Alien > Spore > Hive Mind  |  Robot > Cyborg > AI Overlord  |  Astronaut > Expeditioner > Phenomenon", y)
    y = draw_note(c, "Hive Mind: Gains +1 Power per Spore/Alien on bench. Win: Aliens become Spores, move +6, draw 1.", y)
    y = draw_note(c, "Phenomenon (Power 0): Opponent plays NO cards next round. Combine with Wormhole or Rip in Spacetime for instant win lines.", y)
    y -= 6

    schain = [
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        ['Alien x3', '1', '1', '--', '--'],
        ['Astronaut', '1', '1', '--', '--'],
        ['Robot', '1', '1', '--', '--'],
        ['Spore', '2', '4', 'Draw 1', 'Find Hive Mind from deck/discard'],
        ['Cyborg', '2', '6', 'Draw 2, discard 1', 'Opp discards 1, move +4'],
        ['Expeditioner', '2', '6', 'See opp hand, discard 1', 'Draw 2, move +5'],
        ['Hive Mind', '3', '10', '+1 Pwr per Spore/Alien', 'Aliens>Spores, move +6, draw 1'],
        ['AI Overlord', '3', '8', 'Shuffle opp hand, give 3', 'Opp skips draw, move +5'],
        ['Phenomenon', '3', '0', 'Draw 2 + Pool +2', 'Opp plays NO cards next round'],
    ]
    y = draw_chain_table(c, y, schain, SPACE_ACC, (0,0,0), SPACE_ACC)
    y -= 10

    sinstants = [
        ['INSTANT', 'EFFECT'],
        ['Wormhole', 'Phenomenon active: move half remaining distance to 30.'],
        ['Infestation x2', 'Turn one bench card sideways -- it becomes a Lvl 2 Spore.'],
        ['To the Beginning..', 'Discard a Lvl 3 -- active to discard, summon any fighter from deck/hand/discard.'],
        ['Pendulum Cosmology', 'Move +10. If 30+: WIN. Otherwise -10 back. Phenomenon: skip the -10.'],
        ['Rip in Spacetime', 'Phenomenon active + no bench cards remain -- WIN INSTANTLY.'],
        ['Quantum Entangle.', 'Your power becomes equal to opponent\'s power this round.'],
        ['Cybernetic Underst.', 'Discard Cyborg/Expeditioner -- take any from deck/discard.'],
        ['Emergence Principle', 'Count Aliens + Spores on bench. Move that many x2 spaces.'],
        ['Blast Off!', 'Round 1: Move 3 + Draw 3. Any other round: Move 2 + Draw 2.'],
        ['Quantum Tunneling', 'AI Overlord/Phenomenon active: see opponent deck, bury a card.'],
        ['Event Horizon', 'Position 15+: move 5 spaces immediately.'],
    ]
    y = draw_instant_table(c, y, sinstants, SPACE_ACC, (0,0,0))
    y -= 6
    draw_note(c, "Total: 23/23 cards (11 chain + 12 instants; Infestation counts x2)", y, color=SPACE_ACC)

    # ════════════════ PAGE 7: PERSONAL DECK ════════════════
    new_page(c)
    y = H - 48
    draw_deck_banner(c, y, PERSONAL_BG, PERSONAL_ACC, "PERSONAL DECK -- MERCENARIES")

    # NEW tag
    c.setFont('Helvetica-Bold', 9)
    c.setFillColorRGB(*SECTION_GOLD)
    c.drawString(TEXT_R - 30, y + 4, "NEW")

    y -= 26
    y = draw_body(c, "Theme: Hired mercenaries that fight alongside any army. Drafted between rounds.", y, bold=True)
    y = draw_note(c, "Draft Rule: Each player has their own pool of 20 cards. After every round, pick 5 to add to your deck. Pool persists -- all 20 cards remain available every round. You may pick up to 3 copies of any single card.", y)
    y = draw_note(c, "Upgrade Rule: Lvl 2 mercenaries upgrade from ANY Lvl 1 on the field (any deck). Lvl 3 mercenaries chain from ONE specific Lvl 2 partner only.", y)
    y -= 8

    draw_subsection(c, "CHAIN PAIRS -- Lvl 2 Fighters > Lvl 3 Fighters", y)
    y -= 16

    pchain = [
        ['LVL 2', 'P', '>', 'LVL 3', 'P', 'CHAIN BONUS', 'ON WIN'],
        ['Soldier', '5', '>', 'General', '8', 'L2: Draw 2 / L3: +3 Pwr, Draw 1', 'Move +5, Draw 2'],
        ['Vanguard', '6', '>', 'Champion', '9', 'L2: Move 3 / L3: +2 Pwr, Move 3', 'Push opp back 5'],
        ['Duelist', '6', '>', 'Warlord', '9', 'L2: Opp discard 1 / L3: Opp disc 2', 'Opp discards 3'],
        ['Ghost', '7', '>', 'Spectral Being', '8', 'L2: Draw 1+Move 2 / L3: Draw 2+Block', 'Opp can\'t move'],
        ['Strategist', '5', '>', 'Tactician', '8', 'L2: Find Action / L3: Draw 2+Find', 'Draw 3, Move +3'],
    ]
    y = draw_personal_chain_table(c, y, pchain)
    y -= 12

    draw_subsection(c, "COUNTER CARDS -- Neutralize Opponent Strategies", y)
    y -= 16
    pcounters = [
        ['CARD', 'EFFECT'],
        ['Contact', 'Swap one bench card with a Lvl 1 from your discard.'],
        ['Iron Will', 'Your hand cannot be destroyed this round.'],
        ['Blitz!', 'If you are unable to move this round, move anyway.'],
        ['Override', 'Search your deck or discard for a Personal fighter (Lvl 2/3) and add to hand.'],
        ['Mirror', 'Copy whatever action your opponent just played.'],
    ]
    y = draw_instant_table(c, y, pcounters, PERSONAL_ACC, (0,0,0))
    y -= 12

    draw_subsection(c, "SUPPORT CARDS -- Utility for Any Army", y)
    y -= 16
    psupport = [
        ['CARD', 'EFFECT'],
        ['Run', 'Move 5 spaces.'],
        ['Pot of Selfishness', 'Draw 2 cards.'],
        ['Revival', 'Return any Lvl 2 or Lvl 3 from your discard to your hand.'],
        ['Grim Reaper', 'Search opponent\'s Personal deck cards, take 1, add to their discard.'],
        ['Jump', 'Draw 1 card and move 3 spaces.'],
    ]
    y = draw_instant_table(c, y, psupport, PERSONAL_ACC, (0,0,0))
    y -= 8
    draw_note(c, "Total: 20 cards in pool (10 chain + 5 counters + 5 support). Pool persists every round. Max 3 copies of any card per draft.", y, color=PERSONAL_ACC)

    # ════════════════ PAGE 8: QUICK REFERENCE ════════════════
    new_page(c)
    y = H - 55

    draw_section(c, "QUICK REFERENCE", y)
    y -= 24

    draw_subsection(c, "ROUND IN 4 STEPS", y)
    y -= 18
    steps = [
        ('1 FLIP', 'Both players flip active cards simultaneously.'),
        ('2 PLAY', 'Alternate 1 action each (upgrade or instant). Pass when done.'),
        ('3 RESOLVE', 'Compare power. Winner moves forward by their power total.'),
        ('4 CLEANUP', 'Discard field. New bench card to active. Draw to 5. Pass Haste Token.'),
    ]
    for label, desc in steps:
        c.setFillColorRGB(*TABLE_DARK)
        c.rect(TEXT_L + 3, y - 12, TEXT_W - 6, 16, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 9)
        c.setFillColorRGB(*TITLE_GOLD)
        c.drawString(TEXT_L + 8, y - 8, label)
        c.setFont('Helvetica', 9)
        c.setFillColorRGB(*BODY_CREAM)
        c.drawString(TEXT_L + 85, y - 8, desc)
        y -= 18
    y -= 8

    draw_subsection(c, "DRAFT IN 3 STEPS (after every round)", y)
    y -= 18
    draft_steps = [
        ('1 REVEAL', 'Your remaining Personal Pool cards are shown face up.'),
        ('2 PICK', 'Select 5 cards. They leave your pool permanently.'),
        ('3 SHUFFLE', 'Picked cards shuffle into your deck. Repeat next round until pool is empty.'),
    ]
    for label, desc in draft_steps:
        c.setFillColorRGB(*TABLE_DARK)
        c.rect(TEXT_L + 3, y - 12, TEXT_W - 6, 16, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 9)
        c.setFillColorRGB(*TITLE_GOLD)
        c.drawString(TEXT_L + 8, y - 8, label)
        c.setFont('Helvetica', 9)
        c.setFillColorRGB(*BODY_CREAM)
        c.drawString(TEXT_L + 85, y - 8, desc)
        y -= 18
    y -= 8

    draw_subsection(c, "MATCHUP GUIDE", y)
    y -= 16
    matchup_rows = [
        ['MATCHUP', 'FAVORED', 'REASON'],
        ['Jurassic vs Medieval', 'Jurassic', 'Constant Lvl 2/3 presence blocks King\'s Declaration'],
        ['Medieval vs City', 'Medieval', 'Civilians stay low, easier to clear for Declaration'],
        ['City vs Space', 'City', 'Consistent movement hard to fully counter'],
        ['Space vs Jurassic', 'Space', 'Manipulation negates raw power advantage'],
    ]
    match_cols = [130, 80, 240]
    x0 = TEXT_L + 3
    # Header
    c.setFillColorRGB(*TABLE_DARK)
    c.rect(x0, y - 14, sum(match_cols), 18, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 9)
    c.setFillColorRGB(*TITLE_GOLD)
    mx = x0
    for i, h in enumerate(matchup_rows[0]):
        c.drawString(mx + 3, y - 9, h)
        mx += match_cols[i]
    y -= 18
    for ri, row in enumerate(matchup_rows[1:]):
        bg = TABLE_DARK if ri % 2 == 1 else PAGE_BG
        c.setFillColorRGB(*bg)
        c.rect(x0, y - 14, sum(match_cols), 16, fill=1, stroke=0)
        c.setFont('Helvetica', 8)
        c.setFillColorRGB(*BODY_CREAM)
        mx = x0
        for i, cell in enumerate(row):
            if i == 1:
                c.setFillColorRGB(*SECTION_GOLD)
            else:
                c.setFillColorRGB(*BODY_CREAM)
            c.drawString(mx + 3, y - 9, cell)
            mx += match_cols[i]
        y -= 16
    y -= 12

    draw_subsection(c, "CARD COUNTS SUMMARY", y)
    y -= 16
    count_rows = [
        ['DECK', 'LVL 1', 'LVL 2', 'LVL 3', 'INSTANTS', 'TOTAL', 'STATUS'],
        ['Jurassic', '5', '5', '3', '12', '25', 'COMPLETE'],
        ['Medieval', '5', '5', '3', '9', '22', 'COMPLETE'],
        ['City', '5', '5', '3', '12', '25', 'COMPLETE'],
        ['Space', '5', '3', '3', '10', '21', 'COMPLETE'],
        ['Personal (Pool)', '--', '5', '5', '10', '20', 'NEW'],
        ['TOTAL', '20', '23', '17', '53', '113', ''],
    ]
    count_cols = [100, 45, 45, 45, 60, 50, 65]
    x0 = TEXT_L + 3
    # Header
    c.setFillColorRGB(*TABLE_DARK)
    c.rect(x0, y - 14, sum(count_cols), 18, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 8)
    c.setFillColorRGB(*TITLE_GOLD)
    cx = x0
    for i, h in enumerate(count_rows[0]):
        c.drawString(cx + 3, y - 9, h)
        cx += count_cols[i]
    y -= 18
    for ri, row in enumerate(count_rows[1:]):
        if ri == 4:  # Personal row
            c.setFillColorRGB(*PERSONAL_BG)
        elif ri == 5:  # Total row
            c.setFillColorRGB(*TABLE_DARK)
        elif ri % 2 == 0:
            c.setFillColorRGB(*PAGE_BG)
        else:
            c.setFillColorRGB(*TABLE_DARK)
        c.rect(x0, y - 14, sum(count_cols), 16, fill=1, stroke=0)
        c.setFont('Helvetica-Bold' if ri == 5 else 'Helvetica', 8)
        if ri == 4:
            c.setFillColorRGB(*PERSONAL_ACC)
        elif ri == 5:
            c.setFillColorRGB(*TITLE_GOLD)
        else:
            c.setFillColorRGB(*BODY_CREAM)
        cx = x0
        for i, cell in enumerate(row):
            c.drawString(cx + 3, y - 9, cell)
            cx += count_cols[i]
        y -= 16
    y -= 20

    # Footer credits
    c.setFont('Helvetica', 9)
    c.setFillColorRGB(*BODY_CREAM)
    c.drawCentredString(W/2, y, "Block Brawl -- Designed by Rux & Block Jr. (age 9)  |  Version 0.4")
    y -= 14
    c.setFont('Helvetica', 8)
    c.setFillColorRGB(*SECTION_GOLD)
    c.drawCentredString(W/2, y, "NEW in v0.4: Personal Deck and Draft system added")

    c.save()
    print(f"Done! Wrote {filepath}")

if __name__ == '__main__':
    build()
