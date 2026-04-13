"""
Block Brawl Rulebook v0.5 — PDF Generator
Same style as v0.4, updated card counts and data.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Colors ──
BG        = HexColor('#0d0600')
SURFACE   = HexColor('#1e0e00')
GOLD      = HexColor('#f0a020')
GOLD2     = HexColor('#ffc840')
EMBER     = HexColor('#c44800')
DIM       = HexColor('#8a5a28')
TEXT      = HexColor('#f5ddb0')
WHITE_HOT = HexColor('#fff8e8')
DARK_BG   = HexColor('#110800')
ROW_ALT   = HexColor('#1a0c00')
ROW_DARK  = HexColor('#120700')
BORDER    = HexColor('#4a2800')

JURASSIC_CLR = HexColor('#2d6b30')
MEDIEVAL_CLR = HexColor('#8b1a1a')
CITY_CLR     = HexColor('#1040a0')
SPACE_CLR    = HexColor('#1a0050')
PERSONAL_CLR = HexColor('#b08030')

# ── Styles ──
sTitle = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=22, textColor=GOLD,
                         alignment=TA_CENTER, spaceAfter=4)
sSubtitle = ParagraphStyle('subtitle', fontName='Helvetica', fontSize=10, textColor=DIM,
                            alignment=TA_CENTER, spaceAfter=12)
sH1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=16, textColor=GOLD,
                      spaceBefore=14, spaceAfter=6)
sH2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, textColor=GOLD2,
                      spaceBefore=10, spaceAfter=4)
sBody = ParagraphStyle('body', fontName='Helvetica', fontSize=9, textColor=TEXT,
                        leading=12, spaceAfter=4)
sSmall = ParagraphStyle('small', fontName='Helvetica', fontSize=8, textColor=TEXT, leading=10)
sFooter = ParagraphStyle('footer', fontName='Helvetica', fontSize=7, textColor=DIM,
                          alignment=TA_CENTER)
sDeckTitle = ParagraphStyle('deckTitle', fontName='Helvetica-Bold', fontSize=14, textColor=GOLD,
                             spaceBefore=6, spaceAfter=2)
sDeckSub = ParagraphStyle('deckSub', fontName='Helvetica', fontSize=9, textColor=DIM, spaceAfter=6)
sTableHead = ParagraphStyle('thead', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE_HOT, leading=10)
sTableCell = ParagraphStyle('tcell', fontName='Helvetica', fontSize=7.5, textColor=TEXT, leading=9.5)
sTableCellBold = ParagraphStyle('tcellb', fontName='Helvetica-Bold', fontSize=7.5, textColor=TEXT, leading=9.5)
sNote = ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=8, textColor=DIM,
                        spaceBefore=2, spaceAfter=4)

W, H = letter
MARGIN = 0.6 * inch

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Footer text
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(DIM)
    canvas.drawCentredString(W/2, 0.35*inch,
        f'Block Brawl Official Rulebook v0.5 -- Designed by Rux & Block Jr. (age 9)')
    canvas.drawRightString(W - MARGIN, 0.35*inch, f'Page {doc.page}')
    canvas.restoreState()

def P(text, style=sBody):
    return Paragraph(text, style)

def make_table(headers, rows, col_widths, header_bg=SURFACE, deck_color=None):
    hdr = [P(h, sTableHead) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([P(str(c), sTableCell) if not isinstance(c, Paragraph) else c for c in row])

    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE_HOT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    # Alternate row colors
    for i in range(1, len(data)):
        bg = ROW_ALT if i % 2 == 0 else ROW_DARK
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    if deck_color:
        style_cmds.append(('LINEABOVE', (0, 0), (-1, 0), 2, deck_color))

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style_cmds))
    return t

def build():
    doc = SimpleDocTemplate(
        r'C:\Users\thefi\OneDrive\Desktop\CARD BLOCK\BlockBrawl_Rulebook_v0.5.pdf',
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=0.6*inch
    )
    story = []
    usable = W - 2*MARGIN

    # ═══════════════════════════════════════
    # PAGE 1 — TITLE + OVERVIEW + SETUP
    # ═══════════════════════════════════════
    story.append(Spacer(1, 30))
    story.append(P('BLOCK BRAWL', sTitle))
    story.append(P('Official Rulebook &amp; Deck Reference', sSubtitle))
    story.append(P('E for Everyone  |  2-4 Players  |  15-20 Minutes', sSubtitle))
    story.append(P('Designed by Rux &amp; Block Jr. (age 9)', sSubtitle))
    story.append(Spacer(1, 10))

    story.append(P('OVERVIEW', sH1))
    story.append(P(
        'Block Brawl is a fast, strategic card game for 2-4 players. Each player selects one of four themed decks '
        'representing an era of civilization -- Jurassic, Medieval, City, and Space. Players race their piece along a '
        '30-space board by winning rounds. The first player to reach 30 spaces wins.'
    ))
    story.append(P(
        '<b>NEW in v0.5:</b> All decks now balanced at 25 cards each. Medieval deck expanded to 12 actions '
        '(added Witch\'s Brew, Knight\'s Shield, Last Stand). Space deck Spore count corrected to x3. '
        'Override card effect updated: removes opponent\'s power boost.',
        sNote
    ))
    story.append(Spacer(1, 4))

    # Era table
    era_headers = ['ERA', 'PLAYSTYLE', 'IDENTITY']
    era_rows = [
        ['Jurassic', 'Aggro / Force Win', 'Hit hard, move far, highest power ceiling'],
        ['Medieval', 'Stall / Strategy Win', 'Defensive shell hiding an instant win condition'],
        ['City', 'Versatile / Movement', 'Flexible upgrades, consistent forward movement'],
        ['Space', 'Control / Manipulation', 'Break the rules, manipulate numbers'],
        ['Personal', 'Mercenary / Support', 'Drafted fighters + counters that boost any army'],
    ]
    story.append(make_table(era_headers, era_rows, [usable*0.15, usable*0.25, usable*0.60]))
    story.append(Spacer(1, 8))

    story.append(P('COMPONENTS', sH2))
    story.append(P('<b>125 cards total</b> -- Jurassic 25, Medieval 25, City 25, Space 25, Personal Pool 20'))
    story.append(P('4 player boards, 4 player pieces, 1 Haste Token'))
    story.append(Spacer(1, 6))

    story.append(P('SETUP', sH2))
    setup_steps = [
        '1. Each player chooses a deck and takes the matching board and piece.',
        '2. Shuffle your deck. Place your piece at space 0 on your board.',
        '3. Place your 5 Lvl 1 cards face down on your bench (4 bench slots + 1 active slot).',
        '4. Choose a starting active from your bench and place it face down in your active slot.',
        '5. Draw 5 cards from your deck into your hand.',
        '6. Randomly determine who gets the Haste Token -- that player goes first.',
    ]
    for s in setup_steps:
        story.append(P(s, sSmall))

    # ═══════════════════════════════════════
    # PAGE 2 — RULES
    # ═══════════════════════════════════════
    story.append(PageBreak())

    story.append(P('TABLE LAYOUT', sH1))
    story.append(P('[ Bench 1 ]  [ Bench 2 ]  [ Bench 3 ]  [ Bench 4 ]   --  Face-down Lvl 1s', sSmall))
    story.append(P('[ ACTIVE ]   --  Face down until round starts', sSmall))
    story.append(P('[ Stack ]    --  Actions played this round', sSmall))
    story.append(Spacer(1, 6))

    story.append(P('ROUND STRUCTURE', sH1))

    story.append(P('<b>STEP 1 -- FLIP:</b> Both players simultaneously flip their active card face up.'))
    story.append(P('<b>STEP 2 -- PLAY PHASE:</b> Haste Token holder goes first. Players alternate ONE action per turn:'))
    story.append(P('&nbsp;&nbsp;&nbsp;&nbsp;<b>Upgrade:</b> Play a card from hand onto your active (Lvl 1&gt;2 or Lvl 2&gt;3)', sSmall))
    story.append(P('&nbsp;&nbsp;&nbsp;&nbsp;<b>Action:</b> Play an action card from hand into your stack.', sSmall))
    story.append(P('&nbsp;&nbsp;&nbsp;&nbsp;<b>Pass:</b> Once both players pass consecutively, the round ends.', sSmall))
    story.append(P('<b>CHAIN RULE:</b> Upgrading within the same chain triggers the chain bonus. Cross-chain upgrades work but no bonus fires.', sNote))

    story.append(P('<b>STEP 3 -- RESOLVE:</b> Compare power (plus modifiers). Higher power wins.'))
    story.append(P('&nbsp;&nbsp;&nbsp;&nbsp;Winner moves forward by their winning power total. Loser does not move. Ties: neither moves.', sSmall))

    story.append(P('<b>STEP 4 -- CLEANUP:</b>'))
    story.append(P('&nbsp;&nbsp;&nbsp;&nbsp;Discard active and full stack. Take a bench card face down as new active. Draw to 5. Pass Haste Token.', sSmall))
    story.append(P('&nbsp;&nbsp;&nbsp;&nbsp;If deck runs out, shuffle discard into a new deck (Lvl 1 chain cards stay retired).', sSmall))
    story.append(Spacer(1, 8))

    story.append(P('DRAFT PHASE', sH1))
    story.append(P(
        'Each player receives their own copy of the 20-card Personal Pool at the start of the game. '
        'After every round, a Draft occurs:'
    ))
    draft_steps = [
        '1. Your remaining Personal Pool cards are laid out face up.',
        '2. Pick 5 cards to add to your deck. They shuffle in immediately.',
        '3. Those 5 cards leave your pool -- they are now part of your deck.',
        '4. Next round: 15 remain. Then 10, then 5. After 4 drafts, all 20 are in your deck.',
    ]
    for s in draft_steps:
        story.append(P(s, sSmall))
    story.append(P(
        'Strategy: Draft chain pairs together for the bonus! Pick counters for your opponent\'s deck, '
        'or support cards to shore up weaknesses. Your army grows stronger every round.', sNote
    ))
    story.append(Spacer(1, 8))

    story.append(P('WIN CONDITIONS', sH1))
    story.append(P('<b>1. BOARD WIN:</b> First to reach space 30 wins immediately.'))
    story.append(P('<b>2. BENCH OUT:</b> When all Lvl 1 bench cards are used, the game ends -- furthest player wins.'))
    story.append(P('<b>3. SPECIAL WIN:</b> King\'s Declaration, Rip in Spacetime, and Pendulum Cosmology each carry instant-win conditions described on the card.'))
    story.append(P('Board length: 30 spaces (2 players). Suggested 25 spaces for 3-4 players.', sNote))

    # ═══════════════════════════════════════
    # PAGE 3 — JURASSIC
    # ═══════════════════════════════════════
    story.append(PageBreak())
    story.append(P('JURASSIC DECK -- AGGRO', sDeckTitle))
    story.append(P('Playstyle: Offense / Aggro -- Hit hard, win big, move far.', sDeckSub))
    story.append(P('Chains: Hatchling Carno &gt; Raptor &gt; T-Rex  |  Hatchling Herbo &gt; Stego &gt; Triceratops  |  Archeologist &gt; Explorer &gt; Paleontologist', sSmall))
    story.append(P('Gimmick: Highest power ceiling in the game. T-Rex at Power 10 plus a +5 move bonus on win.', sNote))
    story.append(Spacer(1, 4))

    j_fight = [
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
    story.append(make_table(
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        j_fight,
        [usable*0.22, usable*0.06, usable*0.06, usable*0.33, usable*0.33],
        deck_color=JURASSIC_CLR
    ))
    story.append(Spacer(1, 6))

    j_act = [
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
    story.append(make_table(
        ['ACTION', 'EFFECT'],
        j_act,
        [usable*0.22, usable*0.78],
        deck_color=JURASSIC_CLR
    ))
    story.append(P('Total: 25/25 cards (13 fighters + 12 actions)', sNote))

    # ═══════════════════════════════════════
    # PAGE 4 — MEDIEVAL
    # ═══════════════════════════════════════
    story.append(PageBreak())
    story.append(P('MEDIEVAL DECK -- STALL', sDeckTitle))
    story.append(P('Playstyle: Defense / Stall -- Defensive shell hiding an assassination win condition.', sDeckSub))
    story.append(P('Chains: Squire &gt; Councilman  |  Peasant &gt; Knight or Bowman &gt; Castle/Field Commander  |  Heir &gt; any Lvl 2 &gt; King', sSmall))
    story.append(P('Royal Court: Councilman on bench when King loses -- King stays on field, Councilman sacrificed. '
                    'Instant Win: King active + opponent has no Lvl 2 or Lvl 3 on field.', sNote))
    story.append(Spacer(1, 4))

    m_fight = [
        ['Squire x2', '1', '1', '--', '--'],
        ['Peasant x2', '1', '1', '--', '--'],
        ['Heir', '1', '1', 'Upgrades to ANY Lvl 2', '--'],
        ['Councilman x2', '2', '7', 'Heir: find King. Else: find Action', 'Opp discards 2'],
        ['Knight x2', '2', '5', 'Draw 1 + Pool +1', 'Move +2 spaces'],
        ['Bowman', '2', '5', 'Opp discards 1 + Pool +1', 'Opp discards 1 more'],
        ['Castle Commander', '3', '8', 'Opp discards 1 + Pool +2', 'Opp skips draw next round'],
        ['Field Commander', '3', '8', 'Draw 1 + Pool +2', 'Move +3 bonus spaces'],
        ['King', '3', '9', 'Draw 2 + Pool +2', 'Opp can\'t play Actions next round'],
    ]
    story.append(make_table(
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        m_fight,
        [usable*0.22, usable*0.06, usable*0.06, usable*0.33, usable*0.33],
        deck_color=MEDIEVAL_CLR
    ))
    story.append(Spacer(1, 6))

    m_act = [
        ['Royal Rally', 'Find a Lvl 2 from your deck.'],
        ['Drawbridge', 'Target opponent discards 2 cards.'],
        ['Knight\'s Shield', 'If you LOSE this round, opponent does not move.'],
        ['Scholarly', 'Promote any bench card to a Lvl 2 Councilman.'],
        ['Royal Ball', 'Find a Lvl 3 from your deck.'],
        ['Hold The Line!', 'Draw 2 cards + move 5 spaces. You cannot move from winning this round.'],
        ['Witch\'s Brew', 'Opponent discards 3 cards then shuffles their deck.'],
        ['King\'s Declaration', 'WIN INSTANTLY if King is active and opponent has no Lvl 2 or 3.'],
        ['Siege', 'Opponent cannot upgrade their active this round.'],
        ['Council Summons', 'Discard 1 card. Add a Councilman from your deck or discard pile to hand.'],
        ['Coronation', 'If King is in your hand, move 3 spaces immediately.'],
        ['Last Stand', 'If your bench is empty, your active gains +5 power this round.'],
    ]
    story.append(make_table(
        ['ACTION', 'EFFECT'],
        m_act,
        [usable*0.22, usable*0.78],
        deck_color=MEDIEVAL_CLR
    ))
    story.append(P('Total: 25/25 cards (13 fighters + 12 actions)', sNote))

    # ═══════════════════════════════════════
    # PAGE 5 — CITY
    # ═══════════════════════════════════════
    story.append(PageBreak())
    story.append(P('CITY DECK -- FLEX', sDeckTitle))
    story.append(P('Playstyle: Utility / Versatility -- Civilians upgrade to ANY Lvl 2. No chain restriction.', sDeckSub))
    story.append(P('Gimmick: 5 Civilians as the only Lvl 1. Each Lvl 2 has a specialist action combo. Block Hero hits Power 10 with +4 win bonus.', sNote))
    story.append(Spacer(1, 4))

    c_fight = [
        ['Civilian x5', '1', '1', '--', '--'],
        ['Farmer', '2', '4', 'Move 1 + Pool +1', 'Move 1 more'],
        ['Captain', '2', '5', 'Find Block Transport', 'Move +2'],
        ['Constr. Worker', '2', '5', 'Draw 2', 'Opp skips draw'],
        ['Officer', '2', '7', 'Draw 1 + Pool +1', 'Opp discards 1'],
        ['Firefighter', '2', '7', 'Block opp Actions round', 'Draw 2'],
        ['Foreman', '3', '7', 'Draw 2', 'Move +2 bonus'],
        ['Police Chief', '3', '9', 'Draw 1 + Pool +1', 'Opp can\'t move next round'],
        ['Block Hero', '3', '10', 'Draw 1', 'Move +4 bonus!'],
    ]
    story.append(make_table(
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        c_fight,
        [usable*0.22, usable*0.06, usable*0.06, usable*0.33, usable*0.33],
        deck_color=CITY_CLR
    ))
    story.append(Spacer(1, 6))

    c_act = [
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
    story.append(make_table(
        ['ACTION', 'EFFECT'],
        c_act,
        [usable*0.22, usable*0.78],
        deck_color=CITY_CLR
    ))
    story.append(P('Total: 25/25 cards (13 fighters + 12 actions)', sNote))

    # ═══════════════════════════════════════
    # PAGE 6 — SPACE
    # ═══════════════════════════════════════
    story.append(PageBreak())
    story.append(P('SPACE DECK -- CONTROL', sDeckTitle))
    story.append(P('Playstyle: Tech / Control -- Break the rules. Manipulate numbers.', sDeckSub))
    story.append(P('Chains: Alien &gt; Spore &gt; Hive Mind  |  Robot &gt; Cyborg &gt; AI Overlord  |  Astronaut &gt; Expeditioner &gt; Phenomenon', sSmall))
    story.append(P('Hive Mind: Gains +1 Power per Spore/Alien on bench. Win: Aliens become Spores, move +6, draw 1. '
                    'Phenomenon (Power 0): Opponent plays NO cards next round. Combine with Wormhole or Rip in Spacetime for instant win lines.', sNote))
    story.append(Spacer(1, 4))

    s_fight = [
        ['Alien x3', '1', '1', '--', '--'],
        ['Astronaut', '1', '1', '--', '--'],
        ['Robot', '1', '1', '--', '--'],
        ['Spore x3', '2', '4', 'Draw 1', 'Find Hive Mind from deck/discard'],
        ['Cyborg', '2', '6', 'Draw 2, discard 1', 'Opp discards 1, move +4'],
        ['Expeditioner', '2', '6', 'See opp hand, discard 1', 'Draw 2, move +5'],
        ['Hive Mind', '3', '10', '+1 Pwr per Spore/Alien', 'Aliens>Spores, move +6, draw 1'],
        ['AI Overlord', '3', '8', 'Shuffle opp hand, give 3', 'Opp skips draw, move +5'],
        ['Phenomenon', '3', '0', 'Draw 2 + Pool +2', 'Opp plays NO cards next round'],
    ]
    story.append(make_table(
        ['CARD', 'L', 'P', 'CHAIN BONUS', 'ON WIN'],
        s_fight,
        [usable*0.22, usable*0.06, usable*0.06, usable*0.33, usable*0.33],
        deck_color=SPACE_CLR
    ))
    story.append(Spacer(1, 6))

    s_act = [
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
    story.append(make_table(
        ['ACTION', 'EFFECT'],
        s_act,
        [usable*0.22, usable*0.78],
        deck_color=SPACE_CLR
    ))
    story.append(P('Total: 25/25 cards (13 fighters + 12 actions; Infestation counts x2)', sNote))

    # ═══════════════════════════════════════
    # PAGE 7 — PERSONAL DECK
    # ═══════════════════════════════════════
    story.append(PageBreak())
    story.append(P('PERSONAL DECK -- MERCENARIES', sDeckTitle))
    story.append(P('Theme: Hired mercenaries that fight alongside any army. Drafted between rounds.', sDeckSub))
    story.append(P('Draft Rule: Each player has their own pool of 20 cards. After every round, pick 5 to add to your deck. '
                    'Pool persists -- all 20 cards remain available every round. You may pick up to 3 copies of any single card.', sSmall))
    story.append(P('Upgrade Rule: Lvl 2 mercenaries upgrade from ANY Lvl 1 on the field (any deck). '
                    'Lvl 3 mercenaries chain from ONE specific Lvl 2 partner only.', sSmall))
    story.append(Spacer(1, 6))

    story.append(P('CHAIN PAIRS -- Lvl 2 Fighters &gt; Lvl 3 Fighters', sH2))
    p_chain = [
        ['Soldier (5)', '>', 'General (8)', '+3 Pwr, Draw 1 + Pool +2', 'Move +5, Draw 2'],
        ['Vanguard (6)', '>', 'Champion (9)', '+2 Pwr, Move 3 + Pool +2', 'Push opp back 5'],
        ['Duelist (6)', '>', 'Warlord (9)', 'Opp discards 2 + Pool +2', 'Opp discards 3'],
        ['Ghost (7)', '>', 'Spectral Being (8)', 'Draw 2 + Block Actions + Pool +2', 'Opp can\'t move'],
        ['Strategist (5)', '>', 'Tactician (8)', 'Draw 2 + Find Action + Pool +2', 'Draw 3, Move +3'],
    ]
    story.append(make_table(
        ['LVL 2 (PWR)', '', 'LVL 3 (PWR)', 'L3 CHAIN BONUS', 'ON WIN'],
        p_chain,
        [usable*0.17, usable*0.04, usable*0.19, usable*0.33, usable*0.27],
        deck_color=PERSONAL_CLR
    ))
    story.append(Spacer(1, 8))

    story.append(P('COUNTER CARDS -- Neutralize Opponent Strategies', sH2))
    p_counter = [
        ['Contact', 'Replace your active with a Lvl 1 from your bench or discard. Active goes to discard.'],
        ['Iron Will', 'Your hand cannot be destroyed this round.'],
        ['Blitz!', 'If you are unable to move this round, move anyway.'],
        ['Override', 'Remove your opponent\'s power boost (set it to 0).'],
        ['Mirror', 'Copy whatever action your opponent just played.'],
    ]
    story.append(make_table(
        ['CARD', 'EFFECT'],
        p_counter,
        [usable*0.18, usable*0.82],
        deck_color=PERSONAL_CLR
    ))
    story.append(Spacer(1, 8))

    story.append(P('SUPPORT CARDS -- Utility for Any Army', sH2))
    p_support = [
        ['Run', 'Move 5 spaces.'],
        ['Pot of Selfishness', 'Draw 2 cards.'],
        ['Revival', 'Return any Lvl 2 or Lvl 3 from your discard to your hand.'],
        ['Grim Reaper', 'Search opponent\'s Personal deck cards, take 1, add to their discard.'],
        ['Jump', 'Draw 1 card and move 3 spaces.'],
    ]
    story.append(make_table(
        ['CARD', 'EFFECT'],
        p_support,
        [usable*0.18, usable*0.82],
        deck_color=PERSONAL_CLR
    ))
    story.append(P('Total: 20 cards in pool (10 chain + 5 counters + 5 support). Pool persists every round. Max 3 copies of any card per draft.', sNote))

    # ═══════════════════════════════════════
    # PAGE 8 — QUICK REFERENCE
    # ═══════════════════════════════════════
    story.append(PageBreak())
    story.append(P('QUICK REFERENCE', sH1))

    story.append(P('ROUND IN 4 STEPS', sH2))
    ref_round = [
        ['1 FLIP', 'Both players flip active cards simultaneously.'],
        ['2 PLAY', 'Alternate 1 action each (upgrade or action). Pass when done.'],
        ['3 RESOLVE', 'Compare power. Winner moves forward by their power total.'],
        ['4 CLEANUP', 'Discard field. New bench card to active. Draw to 5. Pass Haste Token.'],
    ]
    story.append(make_table(['STEP', 'DESCRIPTION'], ref_round, [usable*0.15, usable*0.85]))
    story.append(Spacer(1, 8))

    story.append(P('DRAFT IN 3 STEPS (after every round)', sH2))
    ref_draft = [
        ['1 REVEAL', 'Your remaining Personal Pool cards are shown face up.'],
        ['2 PICK', 'Select 5 cards. They leave your pool permanently.'],
        ['3 SHUFFLE', 'Picked cards shuffle into your deck. Repeat next round until pool is empty.'],
    ]
    story.append(make_table(['STEP', 'DESCRIPTION'], ref_draft, [usable*0.15, usable*0.85]))
    story.append(Spacer(1, 8))

    story.append(P('MATCHUP GUIDE', sH2))
    matchups = [
        ['Jurassic vs Medieval', 'Jurassic', 'Constant Lvl 2/3 presence blocks King\'s Declaration'],
        ['Medieval vs City', 'Medieval', 'Civilians stay low, easier to clear for Declaration'],
        ['City vs Space', 'City', 'Consistent movement hard to fully counter'],
        ['Space vs Jurassic', 'Space', 'Manipulation negates raw power advantage'],
    ]
    story.append(make_table(
        ['MATCHUP', 'FAVORED', 'REASON'],
        matchups,
        [usable*0.25, usable*0.15, usable*0.60]
    ))
    story.append(Spacer(1, 8))

    story.append(P('CARD COUNTS SUMMARY', sH2))
    counts = [
        ['Jurassic', '5', '5', '3', '12', '25', 'COMPLETE'],
        ['Medieval', '5', '5', '3', '12', '25', 'COMPLETE'],
        ['City', '5', '5', '3', '12', '25', 'COMPLETE'],
        ['Space', '5', '5', '3', '12', '25', 'COMPLETE'],
        ['Personal (Pool)', '--', '5', '5', '10', '20', 'DRAFT'],
        ['TOTAL', '20', '25', '17', '58', '120+20', ''],
    ]
    story.append(make_table(
        ['DECK', 'LVL 1', 'LVL 2', 'LVL 3', 'ACTIONS', 'TOTAL', 'STATUS'],
        counts,
        [usable*0.16, usable*0.10, usable*0.10, usable*0.10, usable*0.12, usable*0.12, usable*0.14]
    ))
    story.append(Spacer(1, 12))
    story.append(P('Block Brawl -- Designed by Rux &amp; Block Jr. (age 9)  |  Version 0.5', sFooter))
    story.append(P('v0.5: All decks balanced to 25 cards. Medieval +3 actions. Space Spore x3. Override effect updated.', sFooter))

    # Build
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print('Done! BlockBrawl_Rulebook_v0.5.pdf created.')

if __name__ == '__main__':
    build()
