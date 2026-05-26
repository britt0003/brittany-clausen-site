"""
Generate: The Real Work — A Self-Reflection Journal by Brittany Clausen
Warm, real-talk, journal-prompt format. No scales. No scores. Just depth.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Flowable, NextPageTemplate
)
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Brand ────────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor('#162040')
NAVY2   = colors.HexColor('#1e2f54')
GOLD    = colors.HexColor('#C9A84C')
GOLD_LT = colors.HexColor('#DBBE6A')
BLUE    = colors.HexColor('#6BAEC6')
MAG     = colors.HexColor('#B83DAA')
CREAM   = colors.HexColor('#FAF8F5')
MUTED   = colors.HexColor('#555570')   # darkened for readability on cream
TEXT    = colors.HexColor('#1A1A2E')
WHITE   = colors.white

W, H = letter

# ── Lines flowable ───────────────────────────────────────────────────────────
class WritingLines(Flowable):
    """Ruled lines for journaling."""
    def __init__(self, num_lines=8, line_color=None, width=None):
        super().__init__()
        self.num_lines = num_lines
        self.line_color = line_color or colors.HexColor('#C8C0B8')
        self.width = width or (W - 1.5*inch)
        self.height = num_lines * 28 + 8

    def draw(self):
        self.canv.setStrokeColor(self.line_color)
        self.canv.setLineWidth(0.7)
        for i in range(self.num_lines):
            y = self.height - 28 - i * 28
            self.canv.line(0, y, self.width, y)

class AccentLine(Flowable):
    """Bold colored left-margin accent with text beside it."""
    def __init__(self, text, accent_color, width=None, font_size=13):
        super().__init__()
        self.text = text
        self.accent_color = accent_color
        self.width = width or (W - 1.5*inch)
        self.font_size = font_size
        self.height = 60

    def draw(self):
        self.canv.setFillColor(self.accent_color)
        self.canv.roundRect(0, 8, 4, self.height - 14, 2, stroke=0, fill=1)
        self.canv.setFillColor(TEXT)
        self.canv.setFont('Helvetica-BoldOblique', self.font_size)
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.text, 'Helvetica-BoldOblique', self.font_size, self.width - 18)
        y = self.height - 18
        for line in lines[:3]:
            self.canv.drawString(14, y, line)
            y -= self.font_size + 5

# ── Page backgrounds ─────────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor('#1e2f54'))
    canvas.setLineWidth(0.5)
    for i in range(-20, 40):
        canvas.line(i * 30, 0, i * 30 + H, H)
    canvas.restoreState()

def inner_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 5, W, 5, stroke=0, fill=1)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75*inch, 0.38*inch,
        '© 2026 Brittany Clausen · Envision Greatness · brittanyclausen.com')
    canvas.drawRightString(W - 0.75*inch, 0.38*inch, str(doc.page))
    canvas.restoreState()

def section_bg(canvas, doc):
    """Navy full-bleed for section intro and how-to-use pages."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 5, W, 5, stroke=0, fill=1)
    canvas.restoreState()

# ── Styles ───────────────────────────────────────────────────────────────────
def S():
    def p(name, **kw): return ParagraphStyle(name, **kw)
    return {
        # Cover (navy bg)
        'c_eyebrow': p('c_eyebrow', fontName='Helvetica', fontSize=9,
            textColor=GOLD, alignment=TA_CENTER, leading=14, letterSpacing=2),
        'c_title1': p('c_title1', fontName='Helvetica-Bold', fontSize=52,
            textColor=GOLD, alignment=TA_CENTER, leading=58),
        'c_sub': p('c_sub', fontName='Helvetica-Oblique', fontSize=12,
            textColor=colors.HexColor('#C8D4F0'), alignment=TA_CENTER, leading=20),
        'c_by': p('c_by', fontName='Helvetica-Bold', fontSize=10,
            textColor=GOLD, alignment=TA_CENTER, leading=15, spaceBefore=8),

        # Section intro (navy bg)
        'sec_num': p('sec_num', fontName='Helvetica-Bold', fontSize=11,
            textColor=GOLD, alignment=TA_CENTER, leading=16, letterSpacing=2),
        'sec_deck': p('sec_deck', fontName='Helvetica-Oblique', fontSize=14,
            textColor=colors.HexColor('#C8D4F0'), alignment=TA_CENTER,
            leading=22, spaceBefore=10),

        # Inner pages (cream bg — all text must be dark)
        'eyebrow': p('eyebrow', fontName='Helvetica-Bold', fontSize=8,
            textColor=GOLD, leading=12, letterSpacing=1.5, spaceAfter=4),
        'h1': p('h1', fontName='Helvetica-Bold', fontSize=24,
            textColor=NAVY, leading=32, spaceBefore=0, spaceAfter=6),
        'intro': p('intro', fontName='Helvetica-Oblique', fontSize=12.5,
            textColor=TEXT, leading=21, spaceAfter=10),
        'prompt_num': p('prompt_num', fontName='Helvetica-Bold', fontSize=9,
            textColor=MUTED, leading=13, spaceAfter=2, letterSpacing=1),
        'prompt': p('prompt', fontName='Helvetica-Bold', fontSize=15,
            textColor=NAVY, leading=24, spaceBefore=6, spaceAfter=8),
        'brit_note': p('brit_note', fontName='Helvetica-Oblique', fontSize=10.5,
            textColor=MUTED, leading=17, spaceAfter=16),
        'cta_url': p('cta_url', fontName='Helvetica-Bold', fontSize=13,
            textColor=GOLD, alignment=TA_CENTER, leading=20),
    }

# ── Helper: prompt block with lines ──────────────────────────────────────────
def prompt_block(num_str, question, brit_note, accent, ST, lines=7):
    elems = []
    elems.append(Paragraph(num_str, ST['prompt_num']))
    elems.append(Paragraph(question, ST['prompt']))
    if brit_note:
        elems.append(Paragraph(f"<i>{brit_note}</i>", ST['brit_note']))
    elems.append(WritingLines(num_lines=lines))
    elems.append(Spacer(1, 18))
    return elems

# ── Section intro page — returns elements, NO trailing PageBreak ──────────────
def section_page(num, title, deck, brittany_says, accent, ST):
    elems = []
    elems.append(Spacer(1, 1.1*inch))
    elems.append(Paragraph(f"PART {num}  ·  OF FIVE", ST['sec_num']))
    elems.append(Spacer(1, 8))

    bar_data = [[Paragraph(title, ParagraphStyle('stb',
        fontName='Helvetica-Bold', fontSize=36, textColor=WHITE,
        leading=44, alignment=TA_CENTER))]]
    bt = Table(bar_data, colWidths=[W - 1.5*inch])
    bt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), accent),
        ('TOPPADDING',    (0,0), (-1,-1), 22),
        ('BOTTOMPADDING', (0,0), (-1,-1), 22),
        ('LEFTPADDING',   (0,0), (-1,-1), 24),
        ('RIGHTPADDING',  (0,0), (-1,-1), 24),
        ('ROUNDEDCORNERS', [12]),
    ]))
    elems.append(bt)
    elems.append(Spacer(1, 24))
    elems.append(Paragraph(deck, ST['sec_deck']))
    elems.append(Spacer(1, 20))

    bq_data = [[Paragraph(f'"{brittany_says}"', ParagraphStyle('bq',
        fontName='Helvetica-Oblique', fontSize=12, textColor=colors.HexColor('#A8BCDC'),
        leading=20, alignment=TA_CENTER))]]
    bqt = Table(bq_data, colWidths=[W - 2.5*inch])
    bqt.setStyle(TableStyle([
        ('LINEABOVE',     (0,0), (-1,0), 1, colors.HexColor('#2e4070')),
        ('LINEBELOW',     (0,-1), (-1,-1), 1, colors.HexColor('#2e4070')),
        ('TOPPADDING',    (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ]))
    elems.append(bqt)
    # Caller adds NextPageTemplate('Inner') + PageBreak()
    return elems

# ── Main ──────────────────────────────────────────────────────────────────────
def build_pdf(path):
    usable = W - 1.5*inch

    inner_frame = Frame(0.75*inch, 0.75*inch, W - 1.5*inch, H - 1.4*inch,
                        id='inner', leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)

    doc = BaseDocTemplate(path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.65*inch, bottomMargin=0.75*inch,
        title='The Real Work — A Self-Reflection Journal',
        author='Brittany Clausen · Envision Greatness')

    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[inner_frame], onPage=cover_bg),
        PageTemplate(id='Navy',  frames=[inner_frame], onPage=section_bg),
        PageTemplate(id='Inner', frames=[inner_frame], onPage=inner_bg),
    ])

    ST = S()
    story = []

    # ════════════════════════════════════════════════
    # COVER  (Cover template)
    # ════════════════════════════════════════════════
    story.append(Spacer(1, 1.4*inch))
    story.append(Paragraph("ENVISION GREATNESS  ·  BRITTANY CLAUSEN", ST['c_eyebrow']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("THE REAL", ST['c_title1']))
    story.append(Paragraph("WORK", ParagraphStyle('ct2b',
        fontName='Helvetica-Bold', fontSize=52, textColor=WHITE,
        alignment=TA_CENTER, leading=58)))
    story.append(Spacer(1, 18))

    div_data = [[Paragraph("A Journal for Visionaries Who Feel the Pull",
        ParagraphStyle('div', fontName='Helvetica-Oblique', fontSize=14,
        textColor=GOLD_LT, alignment=TA_CENTER, leading=20))]]
    dt = Table(div_data, colWidths=[usable])
    dt.setStyle(TableStyle([
        ('LINEABOVE',     (0,0), (-1,0), 1, colors.HexColor('#C9A84C60')),
        ('LINEBELOW',     (0,-1), (-1,-1), 1, colors.HexColor('#C9A84C60')),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(dt)
    story.append(Spacer(1, 28))
    story.append(Paragraph(
        "Five reflections to help you stop circling the same patterns\n"
        "and start rising from the inside out.",
        ST['c_sub']))
    story.append(Spacer(1, 32))
    story.append(Paragraph("by Brittany Clausen, MSW", ST['c_by']))
    story.append(Paragraph("Founder · Envision Greatness · Empathy Bridge Framework", ST['c_by']))
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # HOW TO USE  (Navy template)
    # ════════════════════════════════════════════════
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph("BEFORE YOU BEGIN", ParagraphStyle('bybey',
        fontName='Helvetica-Bold', fontSize=9, textColor=GOLD,
        alignment=TA_CENTER, letterSpacing=2)))
    story.append(Spacer(1, 16))

    iht_data = [[Paragraph("This isn't a quiz.\nThere's no score.", ParagraphStyle('ih',
        fontName='Helvetica-Bold', fontSize=30, textColor=WHITE,
        alignment=TA_CENTER, leading=40))]]
    iht = Table(iht_data, colWidths=[usable])
    iht.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 0),
                              ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(iht)
    story.append(Spacer(1, 24))

    for p_text in [
        "What you're holding is a set of questions I wish someone had handed me earlier — "
        "the kind that cut through the résumé, the title, the hustle, and the performance, "
        "and get to what's actually running the show.",
        "There are five themes. Each one has three prompts. They're not easy. They're not supposed to be.",
        "Write whatever comes up first. The unfiltered version. The one you wouldn't say out loud "
        "in a meeting, on a call, or in a pitch. That's the version that's actually true — "
        "and that's the version that changes something.",
        "You don't have to answer every prompt in one sitting. Come back to it. Sleep on it. "
        "Some of these will land differently on different days. That's the point.",
        "The only rule: no performance. Not here.",
    ]:
        d = [[Paragraph(p_text, ParagraphStyle('bup', fontName='Helvetica', fontSize=12,
            textColor=colors.HexColor('#C8D4F0'), leading=21))]]
        t = Table(d, colWidths=[usable - 40])
        t.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 0),
                                ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
        story.append(t)

    story.append(Spacer(1, 20))
    qt_data = [[Paragraph(
        '"The gap isn\'t what you know. It\'s what you\'re not yet willing to look at."',
        ParagraphStyle('iq', fontName='Helvetica-BoldOblique', fontSize=13,
        textColor=GOLD, alignment=TA_CENTER, leading=22))]]
    qt = Table(qt_data, colWidths=[usable - 60])
    qt.setStyle(TableStyle([
        ('LINEABOVE',  (0,0), (-1,0), 1, colors.HexColor('#C9A84C50')),
        ('LINEBELOW',  (0,-1), (-1,-1), 1, colors.HexColor('#C9A84C50')),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(qt)
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # PART 1 — THE GAP
    # ════════════════════════════════════════════════
    story += section_page(
        num="ONE", title="The Gap",
        deck="The space between who you know you are\nand who actually shows up under pressure.",
        brittany_says="Everyone I've ever worked with has this gap. The ones who grow the fastest "
                      "aren't the ones with the smallest gap — they're the ones brave enough to name it.",
        accent=NAVY2, ST=ST)
    story.append(NextPageTemplate('Inner'))
    story.append(PageBreak())

    story.append(Paragraph("PART ONE  ·  THE GAP", ST['eyebrow']))
    story.append(Paragraph("You know who you want to be.\nWho actually shows up?", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=GOLD, spaceBefore=0, spaceAfter=14))
    story.append(Paragraph(
        "We all carry a version of ourselves we believe is the real one — the patient one, "
        "the clear-headed one, the person who handles hard things with grace. "
        "And then there's the version that shows up when we're stressed, challenged, or afraid. "
        "This section is about getting honest about that gap.",
        ST['intro']))

    story += prompt_block("PROMPT 1 OF 3",
        "Describe the person you believe you are. Then describe who shows up for others "
        "when you're under pressure. Where does the story break down?",
        "Don't narrate this from the outside in. Start with: 'I know I'm at my worst when...'",
        NAVY, ST, lines=8)
    story += prompt_block("PROMPT 2 OF 3",
        "What's the version of yourself you're most afraid people will see — "
        "in your work, your business, your relationships? When does that version tend to come out?",
        "The things we're most afraid of being seen doing — we're usually already doing them.",
        GOLD, ST, lines=7)
    story += prompt_block("PROMPT 3 OF 3",
        "What would change — right now, this week — if you closed the gap between "
        "who you believe you are and how you actually show up?",
        "This isn't hypothetical. Pick one specific relationship or situation.",
        MAG, ST, lines=7)
    story.append(AccentLine(
        "Before you move on: What did you notice about yourself while answering these?",
        GOLD, font_size=12))
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # PART 2 — THE PATTERN
    # ════════════════════════════════════════════════
    story += section_page(
        num="TWO", title="The Pattern",
        deck="What keeps showing up in your relationships —\nno matter how many times you change the cast.",
        brittany_says="Your patterns don't come from nowhere. They were once the smartest, safest thing you could do. "
                      "They just didn't get the memo that you've grown.",
        accent=colors.HexColor('#1A3A6B'), ST=ST)
    story.append(NextPageTemplate('Inner'))
    story.append(PageBreak())

    story.append(Paragraph("PART TWO  ·  THE PATTERN", ST['eyebrow']))
    story.append(Paragraph("The same dynamic keeps\nshowing up. Why?", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=BLUE, spaceBefore=0, spaceAfter=14))
    story.append(Paragraph(
        "Different job. Different team. Different city. Same problem. If the situation keeps changing "
        "but the friction stays the same — a pattern is running the show. "
        "Patterns aren't weaknesses. They're old strategies. "
        "The question is: are they still working for you — or are they working against you?",
        ST['intro']))

    story += prompt_block("PROMPT 1 OF 3",
        "What's a conflict or frustration that has shown up repeatedly in your work or personal life "
        "— with different people, but the same basic feeling? Describe it.",
        "Don't analyze it yet. Just describe what it feels like when it happens.",
        BLUE, ST, lines=8)
    story += prompt_block("PROMPT 2 OF 3",
        "What do you typically do when conflict or tension shows up? "
        "Do you move toward it, away from it, or do you manage it by controlling the outcome?",
        "Be honest. Most of us have a default move we've been using since long before our current role.",
        NAVY, ST, lines=7)
    story += prompt_block("PROMPT 3 OF 3",
        "If the pattern you described above started as a way to protect yourself — "
        "what were you protecting yourself from? What's it costing you now?",
        "This is the one that changes things. Don't rush it.",
        BLUE, ST, lines=8)
    story.append(AccentLine(
        "Before you move on: Name the pattern in one sentence. Just one.",
        BLUE, font_size=12))
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # PART 3 — THE TRIGGER
    # ════════════════════════════════════════════════
    story += section_page(
        num="THREE", title="The Trigger",
        deck="What sets you off — and what it's\nactually about under the surface.",
        brittany_says="A trigger isn't a flaw. It's a clue. Every time something gets under your skin "
                      "more than it should, it's pointing to something that still needs your attention.",
        accent=colors.HexColor('#7B1E6A'), ST=ST)
    story.append(NextPageTemplate('Inner'))
    story.append(PageBreak())

    story.append(Paragraph("PART THREE  ·  THE TRIGGER", ST['eyebrow']))
    story.append(Paragraph("What gets under your skin —\nand what is it really about?", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=MAG, spaceBefore=0, spaceAfter=14))
    story.append(Paragraph(
        "Triggers are not weaknesses. They're information. The person who has 'no triggers' "
        "has simply gotten very good at suppressing them — which means they leak out sideways "
        "in ways that are harder to see and harder to own. "
        "Getting clear on your triggers is one of the highest-leverage moves you can make.",
        ST['intro']))

    story += prompt_block("PROMPT 1 OF 3",
        "Think of the last time you reacted to something — at work, in your business, or at home — "
        "more intensely than the situation probably warranted. What happened? What did you do?",
        "The 'more than warranted' part is the tell. That's where the real information lives.",
        MAG, ST, lines=8)
    story += prompt_block("PROMPT 2 OF 3",
        "What specific behaviors or situations tend to trigger your strongest reactions? "
        "Be specific — not 'people who are disrespectful' but what exactly disrespect looks like "
        "when it sets you off.",
        "Vague triggers can't be managed. Specific ones can.",
        NAVY, ST, lines=7)
    story += prompt_block("PROMPT 3 OF 3",
        "Under the trigger — what's the deeper fear or wound it's connected to? "
        "What does this reaction say about what you need, or what you're afraid of losing?",
        "This is hard. It's supposed to be. Take your time.",
        MAG, ST, lines=8)
    story.append(AccentLine(
        "Before you move on: What would it look like to respond to that trigger instead of react to it?",
        MAG, font_size=12))
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # PART 4 — THE STORY
    # ════════════════════════════════════════════════
    story += section_page(
        num="FOUR", title="The Story",
        deck="The narrative about yourself that's driving\neverything — often from years ago.",
        brittany_says="Most of us are still operating from a story we wrote about ourselves before "
                      "we had any real power. Update the story — and you update everything.",
        accent=colors.HexColor('#4A55C4'), ST=ST)
    story.append(NextPageTemplate('Inner'))
    story.append(PageBreak())

    story.append(Paragraph("PART FOUR  ·  THE STORY", ST['eyebrow']))
    story.append(Paragraph("What story about yourself\nare you still living from?", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=colors.HexColor('#4A55C4'),
                             spaceBefore=0, spaceAfter=14))
    story.append(Paragraph(
        "We all carry a core narrative — a story about who we are, what we're worth, "
        "what we're capable of, what we have to prove. That story usually got written in circumstances "
        "that had nothing to do with the woman you've become, the business you're building, "
        "or the vision you're carrying. But it runs quietly in the background, influencing every decision, "
        "every relationship, every moment you pull back when you should step forward.",
        ST['intro']))

    story += prompt_block("PROMPT 1 OF 3",
        "What's the story about yourself that quietly drives how hard you work, "
        "how much you need to achieve, or what you're afraid of losing?",
        "Start with: 'If I'm honest, I'm still trying to prove that...'",
        colors.HexColor('#4A55C4'), ST, lines=8)
    story += prompt_block("PROMPT 2 OF 3",
        "Where did that story come from? Who or what told you — directly or indirectly — "
        "that this was true about you?",
        "You don't have to go deep into childhood. Sometimes it's a boss, a failure, a single moment.",
        NAVY, ST, lines=7)
    story += prompt_block("PROMPT 3 OF 3",
        "Is that story still true? Or is it something you inherited that you've never questioned? "
        "What would you tell someone you loved if they were living by that same story?",
        "You already know the answer to this one. The question is whether you'll let it land.",
        colors.HexColor('#4A55C4'), ST, lines=8)
    story.append(AccentLine(
        "Before you move on: Write one sentence that starts with 'The truth is...'",
        colors.HexColor('#4A55C4'), font_size=12))
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # PART 5 — THE MOVE
    # ════════════════════════════════════════════════
    story += section_page(
        num="FIVE", title="The Move",
        deck="Not someday. Not when things calm down.\nWhat changes — right now.",
        brittany_says="I've never met someone who didn't already know what they needed to do. "
                      "What they needed was the courage to stop waiting for the perfect moment to do it.",
        accent=colors.HexColor('#1A5C3A'), ST=ST)
    story.append(NextPageTemplate('Inner'))
    story.append(PageBreak())

    story.append(Paragraph("PART FIVE  ·  THE MOVE", ST['eyebrow']))
    story.append(Paragraph("You already know.\nWhat are you waiting for?", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=colors.HexColor('#2E8B5A'),
                             spaceBefore=0, spaceAfter=14))
    story.append(Paragraph(
        "The inner work is not a destination. It's a practice. But at some point, "
        "the reflection has to translate into something — a conversation you've been avoiding, "
        "a boundary you've been soft about, a vision you've been shrinking yourself to fit. "
        "This last section is about that.",
        ST['intro']))

    story += prompt_block("PROMPT 1 OF 3",
        "Based on everything you've written — what's the one thing you've been most afraid "
        "to admit to yourself about how you're showing up right now?",
        "Not your team. Not your business. Not your family. You.",
        colors.HexColor('#2E8B5A'), ST, lines=8)
    story += prompt_block("PROMPT 2 OF 3",
        "What's one specific relationship, conversation, or dynamic in your life that would shift "
        "if you applied even a fraction of what came up in this journal?",
        "Be specific. Name the person. Name the thing. Vagueness is how we stay stuck.",
        NAVY, ST, lines=7)
    story += prompt_block("PROMPT 3 OF 3",
        "What's one thing you will do differently — this week, not someday — "
        "as a direct result of what you discovered here?",
        "Write it as a commitment. Not 'I'll try to...' — 'I will...'",
        colors.HexColor('#2E8B5A'), ST, lines=6)
    story.append(AccentLine(
        "You just did the work that most people never do. That matters.",
        GOLD, font_size=13))
    story.append(NextPageTemplate('Navy'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════
    # CLOSING CTA  (Navy template)
    # ════════════════════════════════════════════════
    story.append(Spacer(1, 0.9*inch))
    story.append(Paragraph("WHAT COMES NEXT", ParagraphStyle('wcn',
        fontName='Helvetica-Bold', fontSize=9, textColor=GOLD,
        alignment=TA_CENTER, letterSpacing=2)))
    story.append(Spacer(1, 18))
    story.append(Paragraph(
        "The insight is just the beginning.\nNow it has to go somewhere.",
        ParagraphStyle('cph', fontName='Helvetica-Bold', fontSize=28,
        textColor=WHITE, alignment=TA_CENTER, leading=38)))
    story.append(Spacer(1, 22))

    for pt in [
        "What you uncovered in this journal doesn't have to stay in these pages. "
        "This is the work I do with driven women and professionals every day — "
        "helping them take what they've seen about themselves and build something better with it. "
        "In their businesses. In their relationships. In the way they show up when it matters.",
        "If something landed for you, let's talk about what's next.",
    ]:
        d = [[Paragraph(pt, ParagraphStyle('ctap', fontName='Helvetica', fontSize=12,
            textColor=colors.HexColor('#C8D4F0'), leading=21, alignment=TA_CENTER))]]
        t = Table(d, colWidths=[usable - 60])
        t.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 0),
                                ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
        story.append(t)

    story.append(Spacer(1, 20))
    links_data = [
        [Paragraph("brittanyclausen.com", ST['cta_url'])],
        [Spacer(1, 6)],
        [Paragraph("The EQ Edge Newsletter  ·  Keynotes  ·  Corporate Training  ·  Coaching",
            ParagraphStyle('ctasub', fontName='Helvetica', fontSize=10,
            textColor=colors.HexColor('#8899BB'), alignment=TA_CENTER, leading=16))],
    ]
    lt = Table(links_data, colWidths=[usable])
    lt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#0e1830')),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING',    (0,0), (0,0), 22),
        ('BOTTOMPADDING', (-1,-1), (-1,-1), 22),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('ROUNDEDCORNERS', [10]),
    ]))
    story.append(lt)
    story.append(Spacer(1, 22))
    story.append(Paragraph(
        "© 2026 Brittany Clausen · Envision Greatness LLC · All Rights Reserved\n"
        "For personal use only. Please do not reproduce or redistribute without permission.",
        ParagraphStyle('lastfoot', fontName='Helvetica', fontSize=8,
        textColor=colors.HexColor('#6A7A9A'), alignment=TA_CENTER, leading=13)))

    doc.build(story)
    print(f'PDF created: {path}')

if __name__ == '__main__':
    build_pdf('/Users/brittanyclausen/Claude Code/brittany-clausen/eq-self-assessment-guide.pdf')
