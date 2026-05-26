"""
Generate: The Real Work — A Self-Reflection Journal by Brittany Clausen
Beige interior + beige closing, navy cover only. Clean text throughout.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
pt = 1
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Flowable, NextPageTemplate, KeepTogether
)
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Brand colours ─────────────────────────────────────────────────────────────
NAVY    = colors.HexColor('#162040')
NAVY2   = colors.HexColor('#1e2f54')
GOLD    = colors.HexColor('#C9A84C')
GOLD_LT = colors.HexColor('#DBBE6A')
BLUE    = colors.HexColor('#6BAEC6')
BLUE_DK = colors.HexColor('#1A3A6B')
MAG     = colors.HexColor('#B83DAA')
MAG_DK  = colors.HexColor('#7B1E6A')
INDIGO  = colors.HexColor('#4A55C4')
GREEN   = colors.HexColor('#1A5C3A')
GREEN_M = colors.HexColor('#2E8B5A')
BEIGE   = colors.HexColor('#FAF6F0')
MUTED   = colors.HexColor('#6B6B80')
TEXT    = colors.HexColor('#1A1A2E')
WHITE   = colors.white

W, H = letter
MARGIN   = 0.75 * inch
USABLE_W = W - 2 * MARGIN


# ── Custom flowables ──────────────────────────────────────────────────────────

class WritingLines(Flowable):
    """Ruled journal lines."""
    LINE_SPACING = 26

    def __init__(self, num_lines=7):
        super().__init__()
        self.num_lines = num_lines

    def wrap(self, availWidth, availHeight):
        self.width  = availWidth
        self.height = self.num_lines * self.LINE_SPACING + 6
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor('#C8BEB4'))
        c.setLineWidth(0.6)
        for i in range(self.num_lines):
            y = self.height - 6 - i * self.LINE_SPACING
            c.line(0, y, self.width, y)


class AccentBar(Flowable):
    """Left gold bar + italic reflection prompt."""
    def __init__(self, text, bar_color=None, font_size=11.5):
        super().__init__()
        self.text      = text
        self.bar_color = bar_color or GOLD
        self.font_size = font_size

    def wrap(self, availWidth, availHeight):
        self.width  = availWidth
        self.height = 52
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bar_color)
        c.roundRect(0, 6, 3, self.height - 12, 2, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont('Helvetica-BoldOblique', self.font_size)
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.text, 'Helvetica-BoldOblique',
                            self.font_size, self.width - 16)
        y = self.height - 16
        for line in lines[:3]:
            c.drawString(12, y, line)
            y -= self.font_size + 4


class ChapterBand(Flowable):
    """Full-width coloured band for section chapter header on beige pages."""
    def __init__(self, part_label, title, subtitle, bar_color):
        super().__init__()
        self.part_label = part_label
        self.title      = title
        self.subtitle   = subtitle
        self.bar_color  = bar_color
        self.height     = 110

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bar_color)
        c.roundRect(0, 0, self.width, self.height, 8, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, self.width, 3, stroke=0, fill=1)
        # part label — full white so it's visible on dark band
        c.setFillColor(WHITE)
        c.setFont('Helvetica', 8.5)
        c.drawString(16, self.height - 22, self.part_label.upper())
        # title
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 24)
        c.drawString(16, self.height - 52, self.title)
        # subtitle
        c.setFillColor(colors.HexColor('#ffffffd0'))
        c.setFont('Helvetica-Oblique', 10.5)
        c.drawString(16, self.height - 72, self.subtitle)


# ── Page backgrounds ──────────────────────────────────────────────────────────

def beige_bg(canvas, doc):
    """Warm beige — all interior AND closing pages."""
    canvas.saveState()
    canvas.setFillColor(BEIGE)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    # gold top rule
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 4, W, 4, stroke=0, fill=1)
    # footer
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 0.36 * inch,
                      '© 2026 Brittany Clausen  ·  Envision Greatness  ·  brittanyclausen.com')
    canvas.drawRightString(W - MARGIN, 0.36 * inch, str(doc.page))
    canvas.restoreState()


def navy_bg(canvas, doc):
    """Deep navy — cover only."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor('#1e2f54'))
    canvas.setLineWidth(0.4)
    for i in range(-20, 40):
        canvas.line(i * 30, 0, i * 30 + H, H)
    canvas.restoreState()


# ── Paragraph styles ──────────────────────────────────────────────────────────

def styles():
    def P(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        # ── COVER (navy bg) ──────────────────────────────────────────────────
        'cv_eye':   P('cv_eye',  fontName='Helvetica',      fontSize=8.5,
                       textColor=GOLD, alignment=TA_CENTER, leading=13, letterSpacing=2.5),
        'cv_title': P('cv_title', fontName='Helvetica-Bold', fontSize=54,
                       textColor=GOLD, alignment=TA_CENTER, leading=60),
        'cv_sub':   P('cv_sub',  fontName='Helvetica-Oblique', fontSize=12,
                       textColor=colors.HexColor('#C8D4F0'), alignment=TA_CENTER, leading=20),
        'cv_by':    P('cv_by',   fontName='Helvetica-Bold', fontSize=9.5,
                       textColor=GOLD, alignment=TA_CENTER, leading=14, spaceBefore=6),

        # ── HOW-TO-USE page ──────────────────────────────────────────────────
        'ht_kicker': P('ht_kicker', fontName='Helvetica-Bold', fontSize=8,
                        textColor=GOLD, alignment=TA_CENTER, letterSpacing=2),
        'ht_title':  P('ht_title',  fontName='Helvetica-Bold', fontSize=28,
                        textColor=NAVY, alignment=TA_CENTER, leading=38),
        'ht_body':   P('ht_body',   fontName='Helvetica', fontSize=11.5,
                        textColor=TEXT, leading=20),
        'ht_quote':  P('ht_quote',  fontName='Helvetica-BoldOblique', fontSize=12,
                        textColor=NAVY, alignment=TA_CENTER, leading=20),

        # ── BEIGE INTERIOR pages ─────────────────────────────────────────────
        'eye':      P('eye',    fontName='Helvetica-Bold', fontSize=7.5,
                       textColor=GOLD, leading=11, letterSpacing=1.5, spaceAfter=3),
        'h1':       P('h1',     fontName='Helvetica-Bold', fontSize=22,
                       textColor=NAVY, leading=30, spaceAfter=4),
        'intro':    P('intro',  fontName='Helvetica-Oblique', fontSize=11.5,
                       textColor=TEXT, leading=20, spaceAfter=8),
        # prompt number — dark so it's clearly readable
        'pnum':     P('pnum',   fontName='Helvetica-Bold', fontSize=8,
                       textColor=TEXT, leading=12, letterSpacing=1, spaceAfter=2),
        'prompt':   P('prompt', fontName='Helvetica-Bold', fontSize=14,
                       textColor=NAVY, leading=22, spaceBefore=4, spaceAfter=6),
        # brit note — dark gray, readable on beige
        'britt':    P('britt',  fontName='Helvetica-Oblique', fontSize=10,
                       textColor=colors.HexColor('#444455'), leading=16, spaceAfter=10),

        # ── CHAPTER section header ────────────────────────────────────────────
        'sec_deck':  P('sec_deck', fontName='Helvetica-Oblique', fontSize=11.5,
                        textColor=TEXT, alignment=TA_CENTER, leading=19, spaceAfter=6),
        'sec_quote': P('sec_quote', fontName='Helvetica-Oblique', fontSize=11,
                        textColor=TEXT, alignment=TA_CENTER, leading=18),

        # ── CLOSING page (beige bg, dark text) ───────────────────────────────
        'cl_kicker': P('cl_kicker', fontName='Helvetica-Bold', fontSize=8.5,
                        textColor=GOLD, alignment=TA_CENTER, letterSpacing=2),
        'cl_title':  P('cl_title',  fontName='Helvetica-Bold', fontSize=28,
                        textColor=NAVY, alignment=TA_CENTER, leading=38),
        'cl_body':   P('cl_body',   fontName='Helvetica', fontSize=11.5,
                        textColor=TEXT, alignment=TA_CENTER, leading=20),
        'cl_url':    P('cl_url',    fontName='Helvetica-Bold', fontSize=14,
                        textColor=GOLD, alignment=TA_CENTER, leading=20),
        'cl_foot':   P('cl_foot',   fontName='Helvetica', fontSize=8,
                        textColor=MUTED, alignment=TA_CENTER, leading=13),
    }


# ── Helper: one prompt block ──────────────────────────────────────────────────

def prompt_block(num_str, question, brit_note, ST, lines=7):
    """Returns a KeepTogether block: number, question, note, ruled lines."""
    elems = [
        Paragraph(num_str, ST['pnum']),
        Paragraph(question, ST['prompt']),
    ]
    if brit_note:
        elems.append(Paragraph(f'<i>{brit_note}</i>', ST['britt']))
    elems.append(WritingLines(num_lines=lines))
    elems.append(Spacer(1, 14))
    return [KeepTogether(elems)]


# ── Helper: chapter intro block ───────────────────────────────────────────────

def chapter_intro(part_label, title, subtitle, bar_color,
                  brit_quote, h1_text, hr_color, intro_text, ST):
    elems = []
    elems.append(Spacer(1, 0.25 * inch))
    elems.append(ChapterBand(part_label, title, subtitle, bar_color))
    elems.append(Spacer(1, 18))

    q_data = [[Paragraph(f'"{brit_quote}"', ST['sec_quote'])]]
    qt = Table(q_data, colWidths=[USABLE_W - 60])
    qt.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), colors.HexColor('#F0EBE3')),
        ('TOPPADDING',    (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING',   (0, 0), (-1, -1), 18),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 18),
        ('LINEABOVE',     (0, 0), (-1,  0), 1.5, GOLD),
        ('LINEBELOW',     (0,-1), (-1, -1), 1.5, GOLD),
    ]))
    elems.append(qt)
    elems.append(Spacer(1, 22))

    elems.append(Paragraph(h1_text, ST['h1']))
    elems.append(HRFlowable(width=USABLE_W, thickness=1.5, color=hr_color,
                             spaceBefore=2, spaceAfter=10))
    elems.append(Paragraph(intro_text, ST['intro']))
    return elems


# ── Main ──────────────────────────────────────────────────────────────────────

def build_pdf(path):
    frame = Frame(MARGIN, MARGIN,
                  USABLE_W, H - MARGIN - 0.65 * inch,
                  leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0,
                  id='body')

    doc = BaseDocTemplate(
        path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.65 * inch, bottomMargin=MARGIN,
        title='The Real Work — A Self-Reflection Journal',
        author='Brittany Clausen · Envision Greatness',
    )
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[frame], onPage=navy_bg),
        PageTemplate(id='Beige', frames=[frame], onPage=beige_bg),
    ])

    ST    = styles()
    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — COVER  (navy)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph('ENVISION GREATNESS  ·  BRITTANY CLAUSEN', ST['cv_eye']))
    story.append(Spacer(1, 22))
    story.append(Paragraph('THE REAL', ST['cv_title']))
    story.append(Paragraph('WORK', ParagraphStyle('cvtb',
        fontName='Helvetica-Bold', fontSize=54, textColor=WHITE,
        alignment=TA_CENTER, leading=60)))
    story.append(Spacer(1, 20))

    tag_data = [[Paragraph('A Journal for Visionaries Who Feel the Pull',
        ParagraphStyle('tag', fontName='Helvetica-Oblique', fontSize=14,
        textColor=GOLD_LT, alignment=TA_CENTER, leading=20))]]
    tag_t = Table(tag_data, colWidths=[USABLE_W])
    tag_t.setStyle(TableStyle([
        ('LINEABOVE',     (0,0),(-1, 0), 0.8, colors.HexColor('#C9A84C50')),
        ('LINEBELOW',     (0,0),(-1,-1), 0.8, colors.HexColor('#C9A84C50')),
        ('TOPPADDING',    (0,0),(-1,-1), 14),
        ('BOTTOMPADDING', (0,0),(-1,-1), 14),
    ]))
    story.append(tag_t)
    story.append(Spacer(1, 26))
    story.append(Paragraph(
        'Five reflections to help you stop circling the same patterns\n'
        'and start rising from the inside out.',
        ST['cv_sub']))
    story.append(Spacer(1, 36))
    story.append(Paragraph('by Brittany Clausen, MSW', ST['cv_by']))

    story.append(NextPageTemplate('Beige'))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — HOW TO USE  (beige)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph('BEFORE YOU BEGIN', ST['ht_kicker']))
    story.append(Spacer(1, 16))
    story.append(Paragraph("This isn't a quiz.\nThere's no score.", ST['ht_title']))
    story.append(HRFlowable(width=USABLE_W, thickness=1.5, color=GOLD,
                             spaceBefore=12, spaceAfter=16))

    for txt in [
        "What you're holding is a set of questions I wish someone had handed me earlier — "
        "the kind that cut through the résumé, the hustle, and the performance, "
        "and get to what's actually running the show.",
        "There are five themes. Each one has three prompts. They're not easy. "
        "They're not supposed to be.",
        "Write whatever comes up first. The unfiltered version — the one you wouldn't "
        "say out loud in a meeting or on a call. That's the version that's actually true. "
        "And that's the version that changes something.",
        "You don't have to finish in one sitting. Come back to it. Some of these "
        "will land differently on different days. That's the point.",
        "The only rule: no performance. Not here.",
    ]:
        story.append(Paragraph(txt, ST['ht_body']))
        story.append(Spacer(1, 10))

    story.append(Spacer(1, 14))
    q_data = [[Paragraph(
        '"The gap isn\'t what you know. It\'s what you\'re not yet willing to look at."',
        ST['ht_quote'])]]
    qt = Table(q_data, colWidths=[USABLE_W - 60])
    qt.setStyle(TableStyle([
        ('LINEABOVE',  (0,0),(-1, 0), 1,   GOLD),
        ('LINEBELOW',  (0,0),(-1,-1), 1,   GOLD),
        ('TOPPADDING', (0,0),(-1,-1), 14),
        ('BOTTOMPADDING', (0,0),(-1,-1), 14),
        ('ALIGN',      (0,0),(-1,-1), 'CENTER'),
    ]))
    story.append(qt)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PART 1 — THE GAP
    # ══════════════════════════════════════════════════════════════════════════
    story += chapter_intro(
        part_label='Part One of Five',
        title='The Gap',
        subtitle='The space between who you know you are and who actually shows up.',
        bar_color=NAVY2,
        brit_quote=(
            "Everyone I've ever worked with has this gap. The ones who grow fastest "
            "aren't the ones with the smallest gap — they're the ones brave enough to name it."
        ),
        h1_text='You know who you want to be.\nWho actually shows up?',
        hr_color=GOLD,
        intro_text=(
            "We all carry a version of ourselves we believe is the real one — the patient one, "
            "the clear-headed one, the person who handles hard things with grace. "
            "And then there's the version that shows up when we're stressed, challenged, or afraid. "
            "This section is about getting honest about that gap."
        ),
        ST=ST,
    )
    story += prompt_block('PROMPT 1 OF 3',
        'Describe the person you believe you are. Then describe who shows up for others '
        'when you\'re under pressure. Where does the story break down?',
        "Don't narrate this from the outside in. Start with: 'I know I'm at my worst when...'",
        ST, lines=8)

    # ── force Prompt 2 to its own page ──
    story.append(PageBreak())
    story += prompt_block('PROMPT 2 OF 3',
        'What\'s the version of yourself you\'re most afraid people will see — '
        'in your work, your business, your relationships? When does that version come out?',
        "The things we're most afraid of being seen doing — we're usually already doing them.",
        ST, lines=7)
    story += prompt_block('PROMPT 3 OF 3',
        'What would change — right now, this week — if you closed the gap between '
        'who you believe you are and how you actually show up?',
        'This isn\'t hypothetical. Pick one specific relationship or situation.',
        ST, lines=7)
    story.append(AccentBar(
        'Before you move on: What did you notice about yourself while answering these?',
        GOLD))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PART 2 — THE PATTERN
    # ══════════════════════════════════════════════════════════════════════════
    story += chapter_intro(
        part_label='Part Two of Five',
        title='The Pattern',
        subtitle='What keeps showing up, no matter how many times you change the cast.',
        bar_color=BLUE_DK,
        brit_quote=(
            "Your patterns don't come from nowhere. They were once the smartest, safest thing "
            "you could do. They just didn't get the memo that you've grown."
        ),
        h1_text='The same dynamic keeps\nshowing up. Why?',
        hr_color=BLUE,
        intro_text=(
            "Different job. Different team. Different city. Same problem. If the situation keeps "
            "changing but the friction stays the same — a pattern is running the show. "
            "Patterns aren't weaknesses. They're old strategies. "
            "The question is: are they still working for you — or against you?"
        ),
        ST=ST,
    )
    story += prompt_block('PROMPT 1 OF 3',
        'What\'s a conflict or frustration that has shown up repeatedly in your work or personal '
        'life — with different people, but the same basic feeling? Describe it.',
        "Don't analyze it yet. Just describe what it feels like when it happens.",
        ST, lines=8)

    # ── force Prompt 2 to its own page ──
    story.append(PageBreak())
    story += prompt_block('PROMPT 2 OF 3',
        'What do you typically do when conflict or tension shows up? '
        'Do you move toward it, away from it, or manage it by controlling the outcome?',
        "Be honest. Most of us have a default move we've been using since long before our current role.",
        ST, lines=7)
    story += prompt_block('PROMPT 3 OF 3',
        'If the pattern you described started as a way to protect yourself — '
        'what were you protecting yourself from? What\'s it costing you now?',
        "This is the one that changes things. Don't rush it.",
        ST, lines=8)
    story.append(AccentBar('Before you move on: Name the pattern in one sentence. Just one.', BLUE))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PART 3 — THE TRIGGER
    # ══════════════════════════════════════════════════════════════════════════
    story += chapter_intro(
        part_label='Part Three of Five',
        title='The Trigger',
        subtitle='What sets you off — and what it\'s actually about underneath.',
        bar_color=MAG_DK,
        brit_quote=(
            "A trigger isn't a flaw. It's a clue. Every time something gets under your skin "
            "more than it should, it's pointing to something that still needs your attention."
        ),
        h1_text='What gets under your skin —\nand what is it really about?',
        hr_color=MAG,
        intro_text=(
            "Triggers are not weaknesses. They're information. The person who has 'no triggers' "
            "has simply gotten very good at suppressing them — which means they leak out sideways "
            "in ways that are harder to see. Getting clear on your triggers is one of the "
            "highest-leverage moves you can make."
        ),
        ST=ST,
    )
    story += prompt_block('PROMPT 1 OF 3',
        'Think of the last time you reacted to something — at work, in your business, or at home — '
        'more intensely than the situation probably warranted. What happened?',
        "The 'more than warranted' part is the tell. That's where the real information lives.",
        ST, lines=8)

    # ── force Prompt 2 to its own page ──
    story.append(PageBreak())
    story += prompt_block('PROMPT 2 OF 3',
        'What specific behaviors or situations tend to trigger your strongest reactions? '
        'Be specific — not \'people who are disrespectful\' but exactly what disrespect looks '
        'like when it sets you off.',
        'Vague triggers can\'t be managed. Specific ones can.',
        ST, lines=7)
    story += prompt_block('PROMPT 3 OF 3',
        'Under the trigger — what\'s the deeper fear or wound it\'s connected to? '
        'What does this reaction say about what you need, or what you\'re afraid of losing?',
        "This is hard. It's supposed to be. Take your time.",
        ST, lines=8)
    story.append(AccentBar(
        'Before you move on: What would it look like to respond to that trigger instead of react?',
        MAG))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PART 4 — THE STORY
    # ══════════════════════════════════════════════════════════════════════════
    story += chapter_intro(
        part_label='Part Four of Five',
        title='The Story',
        subtitle='The narrative that\'s driving everything — often from years ago.',
        bar_color=INDIGO,
        brit_quote=(
            "Most of us are still operating from a story we wrote about ourselves before "
            "we had any real power. Update the story — and you update everything."
        ),
        h1_text='What story about yourself\nare you still living from?',
        hr_color=INDIGO,
        intro_text=(
            "We all carry a core narrative — about who we are, what we're worth, "
            "what we're capable of, what we have to prove. That story usually got written "
            "in circumstances that had nothing to do with who you've become or the "
            "vision you're carrying. But it runs quietly in the background, influencing every "
            "decision, every relationship, every moment you pull back when you should step forward."
        ),
        ST=ST,
    )
    story += prompt_block('PROMPT 1 OF 3',
        'What\'s the story about yourself that quietly drives how hard you work, '
        'how much you need to achieve, or what you\'re afraid of losing?',
        "Start with: 'If I'm honest, I'm still trying to prove that...'",
        ST, lines=8)

    # ── force Prompt 2 to its own page ──
    story.append(PageBreak())
    story += prompt_block('PROMPT 2 OF 3',
        'Where did that story come from? Who or what told you — directly or indirectly — '
        'that this was true about you?',
        "You don't have to go deep into childhood. Sometimes it's a boss, a failure, a single moment.",
        ST, lines=7)
    story += prompt_block('PROMPT 3 OF 3',
        'Is that story still true? Or is it something you inherited that you\'ve never questioned? '
        'What would you tell someone you loved if they were living by that same story?',
        "You already know the answer. The question is whether you'll let it land.",
        ST, lines=8)
    story.append(AccentBar("Before you move on: Write one sentence starting with 'The truth is...'",
                            INDIGO))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PART 5 — THE MOVE
    # ══════════════════════════════════════════════════════════════════════════
    story += chapter_intro(
        part_label='Part Five of Five',
        title='The Move',
        subtitle='Not someday. Not when things calm down. Right now.',
        bar_color=GREEN,
        brit_quote=(
            "I've never met someone who didn't already know what they needed to do. "
            "What they needed was the courage to stop waiting for the perfect moment to do it."
        ),
        h1_text='You already know.\nWhat are you waiting for?',
        hr_color=GREEN_M,
        intro_text=(
            "The inner work is not a destination. It's a practice. But at some point, "
            "the reflection has to translate into something — a conversation you've been avoiding, "
            "a boundary you've been soft about, a vision you've been shrinking yourself to fit. "
            "This last section is about that."
        ),
        ST=ST,
    )
    story += prompt_block('PROMPT 1 OF 3',
        'Based on everything you\'ve written — what\'s the one thing you\'ve been most afraid '
        'to admit to yourself about how you\'re showing up right now?',
        "Not your team. Not your business. Not your family. You.",
        ST, lines=8)

    # ── force Prompt 2 to its own page ──
    story.append(PageBreak())
    story += prompt_block('PROMPT 2 OF 3',
        'What\'s one specific relationship, conversation, or dynamic in your life that would shift '
        'if you applied even a fraction of what came up in this journal?',
        'Be specific. Name the person. Name the thing. Vagueness is how we stay stuck.',
        ST, lines=7)
    story += prompt_block('PROMPT 3 OF 3',
        'What\'s one thing you will do differently — this week, not someday — '
        'as a direct result of what you discovered here?',
        "Write it as a commitment. Not 'I'll try to...' — 'I will...'",
        ST, lines=6)
    story.append(AccentBar('You just did the work that most people never do. That matters.', GOLD))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # LAST PAGE — CLOSING CTA  (beige, dark text)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph('WHAT COMES NEXT', ST['cl_kicker']))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        'The insight is just the beginning.\nNow it has to go somewhere.',
        ST['cl_title']))
    story.append(Spacer(1, 24))

    for txt in [
        "What you uncovered in this journal doesn't have to stay in these pages. "
        "This is the work I do with driven women and professionals every day — "
        "helping them take what they've seen about themselves and build something better with it. "
        "In their businesses. In their relationships. In the way they show up when it matters.",
        "If something landed for you, let's talk about what's next.",
    ]:
        bd = [[Paragraph(txt, ST['cl_body'])]]
        bt = Table(bd, colWidths=[USABLE_W - 80])
        bt.setStyle(TableStyle([
            ('TOPPADDING',    (0,0),(-1,-1), 0),
            ('BOTTOMPADDING', (0,0),(-1,-1), 12),
            ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
        ]))
        story.append(bt)

    story.append(Spacer(1, 32))

    # Navy info box — only brittanyclausen.com, no EQ newsletter
    url_data = [
        [Paragraph('brittanyclausen.com', ST['cl_url'])],
        [Spacer(1, 6)],
        [Paragraph(
            'Keynotes  ·  Corporate Training  ·  Coaching  ·  Fractional HR',
            ParagraphStyle('clsub', fontName='Helvetica', fontSize=9.5,
            textColor=colors.HexColor('#8899BB'), alignment=TA_CENTER, leading=15))],
    ]
    url_t = Table(url_data, colWidths=[USABLE_W])
    url_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor('#162040')),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('TOPPADDING',    (0,0),(0, 0), 20),
        ('BOTTOMPADDING', (0,-1),(-1,-1), 20),
        ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
    ]))
    story.append(url_t)

    # copyright pinned near bottom with a large spacer before it
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        '© 2026 Brittany Clausen  ·  Envision Greatness LLC  ·  All Rights Reserved\n'
        'For personal use only. Please do not reproduce or redistribute without permission.',
        ST['cl_foot']))

    doc.build(story)
    print(f'✓  PDF saved → {path}')


if __name__ == '__main__':
    build_pdf(
        '/Users/brittanyclausen/Claude Code/brittany-clausen/eq-self-assessment-guide.pdf'
    )
