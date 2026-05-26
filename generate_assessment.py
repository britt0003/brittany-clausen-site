"""
Generate: The EQ Edge Self-Assessment Guide
Branded PDF for Brittany Clausen / Envision Greatness
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable

# ── Brand colors ────────────────────────────────────────────────────────────
NAVY     = colors.HexColor('#162040')
GOLD     = colors.HexColor('#C9A84C')
GOLD_LT  = colors.HexColor('#DBBE6A')
BLUE_LT  = colors.HexColor('#6BAEC6')
MAGENTA  = colors.HexColor('#B83DAA')
CREAM    = colors.HexColor('#FAF8F5')
WARM     = colors.HexColor('#F4F1EC')
MUTED    = colors.HexColor('#5A5A72')
WHITE    = colors.white

W, H = letter   # 612 x 792 pts

# ── Custom Flowable: solid color block ──────────────────────────────────────
class ColorBlock(Flowable):
    def __init__(self, width, height, fill_color, radius=8):
        super().__init__()
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.fill_color)
        self.canv.roundRect(0, 0, self.width, self.height,
                            self.radius, stroke=0, fill=1)

# ── Styles ───────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        'cover_eyebrow': s('cover_eyebrow',
            fontName='Helvetica', fontSize=9, leading=13,
            textColor=GOLD, alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=6, letterSpacing=2),

        'cover_title': s('cover_title',
            fontName='Helvetica-Bold', fontSize=34, leading=42,
            textColor=WHITE, alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=10),

        'cover_sub': s('cover_sub',
            fontName='Helvetica', fontSize=13, leading=20,
            textColor=colors.HexColor('#D0D8F0'), alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=0),

        'cover_byline': s('cover_byline',
            fontName='Helvetica-Oblique', fontSize=10, leading=15,
            textColor=GOLD, alignment=TA_CENTER),

        'section_label': s('section_label',
            fontName='Helvetica-Bold', fontSize=8, leading=12,
            textColor=GOLD, spaceBefore=18, spaceAfter=4,
            letterSpacing=1.5),

        'h1': s('h1',
            fontName='Helvetica-Bold', fontSize=22, leading=30,
            textColor=NAVY, spaceBefore=6, spaceAfter=8),

        'h2': s('h2',
            fontName='Helvetica-Bold', fontSize=15, leading=22,
            textColor=NAVY, spaceBefore=14, spaceAfter=6),

        'h3': s('h3',
            fontName='Helvetica-Bold', fontSize=12, leading=18,
            textColor=NAVY, spaceBefore=10, spaceAfter=4),

        'lead': s('lead',
            fontName='Helvetica-Oblique', fontSize=12, leading=20,
            textColor=NAVY, spaceBefore=0, spaceAfter=10),

        'body': s('body',
            fontName='Helvetica', fontSize=10.5, leading=17,
            textColor=colors.HexColor('#1A1A2E'),
            spaceBefore=0, spaceAfter=8),

        'body_bold': s('body_bold',
            fontName='Helvetica-Bold', fontSize=10.5, leading=17,
            textColor=NAVY, spaceBefore=0, spaceAfter=6),

        'q_num': s('q_num',
            fontName='Helvetica-Bold', fontSize=10, leading=15,
            textColor=GOLD, spaceBefore=0, spaceAfter=0),

        'question': s('question',
            fontName='Helvetica-Bold', fontSize=11, leading=17,
            textColor=NAVY, spaceBefore=8, spaceAfter=3),

        'q_note': s('q_note',
            fontName='Helvetica-Oblique', fontSize=9.5, leading=14,
            textColor=MUTED, spaceBefore=0, spaceAfter=6),

        'scale_label': s('scale_label',
            fontName='Helvetica', fontSize=8.5, leading=12,
            textColor=MUTED, alignment=TA_CENTER),

        'score_head': s('score_head',
            fontName='Helvetica-Bold', fontSize=12, leading=17,
            textColor=WHITE, spaceBefore=0, spaceAfter=2),

        'score_body': s('score_body',
            fontName='Helvetica', fontSize=10, leading=15,
            textColor=colors.HexColor('#D0D8F0'),
            spaceBefore=0, spaceAfter=0),

        'callout': s('callout',
            fontName='Helvetica-Oblique', fontSize=11, leading=18,
            textColor=NAVY, spaceBefore=0, spaceAfter=0),

        'footer': s('footer',
            fontName='Helvetica', fontSize=8, leading=11,
            textColor=MUTED, alignment=TA_CENTER),

        'cta_head': s('cta_head',
            fontName='Helvetica-Bold', fontSize=16, leading=24,
            textColor=WHITE, alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=8),

        'cta_body': s('cta_body',
            fontName='Helvetica', fontSize=11, leading=18,
            textColor=colors.HexColor('#D0D8F0'), alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=8),

        'cta_url': s('cta_url',
            fontName='Helvetica-Bold', fontSize=11, leading=16,
            textColor=GOLD, alignment=TA_CENTER),
    }

# ── Rating scale row ──────────────────────────────────────────────────────────
def rating_scale(ST):
    labels = ['1\nNever', '2\nRarely', '3\nSometimes', '4\nOften', '5\nAlways']
    cells = [[Paragraph(l, ST['scale_label']) for l in labels]]
    t = Table(cells, colWidths=[72]*5, rowHeights=[28])
    t.setStyle(TableStyle([
        ('BOX',        (0,0), (-1,-1), 0.5, colors.HexColor('#D0C8BE')),
        ('INNERGRID',  (0,0), (-1,-1), 0.5, colors.HexColor('#D0C8BE')),
        ('BACKGROUND', (0,0), (-1,-1), WARM),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

# ── Scoring band table ────────────────────────────────────────────────────────
def score_band(label, range_str, desc, bg, ST):
    inner = [
        [Paragraph(f"{label}  ·  Score: {range_str}", ST['score_head'])],
        [Paragraph(desc, ST['score_body'])],
    ]
    inner_t = Table(inner, colWidths=[430])
    inner_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 16),
        ('RIGHTPADDING',  (0,0),(-1,-1), 16),
        ('ROUNDEDCORNERS', [8]),
    ]))
    return inner_t

# ── Domain block ─────────────────────────────────────────────────────────────
def domain_block(title, eyebrow, accent, intro, questions, ST):
    elems = []

    # Domain header bar
    header_data = [[
        Paragraph(eyebrow.upper(), ParagraphStyle('deh',
            fontName='Helvetica-Bold', fontSize=8, textColor=WHITE,
            letterSpacing=1.5)),
        Paragraph(title, ParagraphStyle('dht',
            fontName='Helvetica-Bold', fontSize=17, textColor=WHITE,
            leading=22)),
    ]]
    ht = Table(header_data, colWidths=[100, 380], rowHeights=[50])
    ht.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), accent),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING',   (0,0), (-1,-1), 18),
        ('RIGHTPADDING',  (0,0), (-1,-1), 18),
        ('ROUNDEDCORNERS', [8]),
    ]))
    elems.append(ht)
    elems.append(Spacer(1, 10))
    elems.append(Paragraph(intro, ST['lead']))
    elems.append(Spacer(1, 4))

    for i, (q, note) in enumerate(questions, 1):
        elems.append(Paragraph(f"Q{i}", ST['q_num']))
        elems.append(Paragraph(q, ST['question']))
        if note:
            elems.append(Paragraph(note, ST['q_note']))
        elems.append(rating_scale(ST))
        elems.append(Spacer(1, 8))

    # Domain score box
    score_row = Table(
        [[Paragraph("DOMAIN SCORE  /25", ParagraphStyle('ds',
            fontName='Helvetica-Bold', fontSize=10, textColor=WHITE,
            letterSpacing=1)),
          Paragraph("Add your ratings: ___  +  ___  +  ___  +  ___  +  ___ = ______",
            ParagraphStyle('dsb', fontName='Helvetica', fontSize=9.5,
            textColor=colors.HexColor('#D0D8F0'), leading=14))]],
        colWidths=[140, 340]
    )
    score_row.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), accent),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING',   (0,0), (-1,-1), 16),
        ('RIGHTPADDING',  (0,0), (-1,-1), 16),
        ('ROUNDEDCORNERS', [6]),
    ]))
    elems.append(score_row)
    return elems

# ── Page templates ────────────────────────────────────────────────────────────
def add_page_bg(canvas, doc):
    """Cream background + gold top stripe + footer on every inner page."""
    canvas.saveState()
    # cream background
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    # gold top stripe
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 6, W, 6, stroke=0, fill=1)
    # footer
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75*inch, 0.4*inch,
        "© 2026 Brittany Clausen · Envision Greatness LLC · brittanyclausen.com")
    canvas.drawRightString(W - 0.75*inch, 0.4*inch, f"Page {doc.page}")
    canvas.restoreState()

def add_cover_bg(canvas, doc):
    """Full navy cover."""
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    # gold accent bar top
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 8, W, 8, stroke=0, fill=1)
    # subtle grid lines
    canvas.setStrokeColor(colors.HexColor('#1e2f54'))
    canvas.setLineWidth(0.5)
    for y in range(0, int(H), 36):
        canvas.line(0, y, W, y)
    canvas.restoreState()

# ── Main builder ─────────────────────────────────────────────────────────────
def build_pdf(path):
    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.65*inch,
        bottomMargin=0.75*inch,
        title="The EQ Edge Self-Assessment Guide",
        author="Brittany Clausen · Envision Greatness",
    )

    ST = build_styles()
    story = []
    usable = W - 1.5*inch  # 462 pts

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE  (navy bg, handled by add_cover_bg)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 1.6*inch))
    story.append(Paragraph("ENVISION GREATNESS  ·  BRITTANY CLAUSEN", ST['cover_eyebrow']))
    story.append(Spacer(1, 14))

    story.append(Paragraph("THE EQ EDGE", ParagraphStyle('ct1',
        fontName='Helvetica-Bold', fontSize=48, leading=54,
        textColor=GOLD, alignment=TA_CENTER)))
    story.append(Paragraph("Self-Assessment Guide", ParagraphStyle('ct2',
        fontName='Helvetica', fontSize=24, leading=32,
        textColor=WHITE, alignment=TA_CENTER, spaceBefore=4)))

    story.append(Spacer(1, 24))
    story.append(HRFlowable(width=160, thickness=1.5, color=GOLD,
                             spaceAfter=24, spaceBefore=0,
                             hAlign='CENTER'))

    story.append(Paragraph(
        "Discover exactly where emotional intelligence is costing you<br/>"
        "— in your leadership, your relationships, and your results.",
        ST['cover_sub']))

    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "Grounded in the Empathy Bridge Framework (EBF)",
        ST['cover_byline']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "brittanyclausen.com  ·  envisiongreatnessnow.com",
        ST['cover_byline']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — BEFORE YOU BEGIN
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("BEFORE YOU BEGIN", ST['section_label']))
    story.append(Paragraph("You Don't Have a Strategy Problem.", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=GOLD,
                             spaceBefore=0, spaceAfter=14))

    story.append(Paragraph(
        "Let's be honest about why you're here.",
        ST['lead']))

    story.append(Paragraph(
        "You've put in the work. The degrees, the promotions, the business — maybe even the speaking gigs and the "
        "thought leadership content. And still, somewhere in the back of your mind, there's this quiet, persistent "
        "question: <i>Why does this still feel so hard?</i>",
        ST['body']))

    story.append(Paragraph(
        "You avoid certain conversations because you know they'll spiral. You say yes when you mean no — and "
        "then resent the people you said yes to. You replay meetings in your head at 2am, editing your words, "
        "second-guessing your reactions. You watch less-qualified people rise faster and wonder what they know "
        "that you don't.",
        ST['body']))

    story.append(Paragraph(
        "Here's what's actually happening: <b>the gap isn't your strategy. It's your emotional intelligence.</b>",
        ST['body']))

    story.append(Spacer(1, 6))

    # callout box
    callout_data = [[Paragraph(
        '"EQ is not about being soft. It\'s about being precise. '
        'Knowing what\'s driving your behavior — '
        'so you can choose your response instead of being hijacked by it."',
        ParagraphStyle('cq', fontName='Helvetica-Oblique', fontSize=11,
                       leading=18, textColor=NAVY))]]
    ct = Table(callout_data, colWidths=[usable])
    ct.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#F0EBE0')),
        ('LEFTPADDING',   (0,0), (-1,-1), 18),
        ('RIGHTPADDING',  (0,0), (-1,-1), 18),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEAFTER',     (0,0), (0,-1), 4, GOLD),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(ct)
    story.append(Spacer(1, 14))

    story.append(Paragraph("About the Empathy Bridge Framework (EBF)", ST['h2']))
    story.append(Paragraph(
        "This assessment is grounded in the <b>Empathy Bridge Framework</b> — a diagnostic model developed by "
        "Brittany Clausen through years of working with leaders, teams, and organizations in conflict. "
        "EBF identifies three layers where emotional intelligence breaks down:",
        ST['body']))

    ebf_data = [
        [Paragraph("EMOTIONAL", ParagraphStyle('ebfl',
            fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, letterSpacing=1)),
         Paragraph("<b>How you relate to yourself.</b> Self-awareness, self-regulation, "
                   "your patterns under stress. What happens in you before it happens around you.",
                   ST['body'])],
        [Paragraph("RELATIONAL", ParagraphStyle('ebfl2',
            fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, letterSpacing=1)),
         Paragraph("<b>How you relate to others.</b> Empathy, communication style, conflict patterns, "
                   "and whether people feel safe enough to tell you the truth.",
                   ST['body'])],
        [Paragraph("ORGANIZATIONAL", ParagraphStyle('ebfl3',
            fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, letterSpacing=1)),
         Paragraph("<b>How you show up in systems.</b> The culture you're building — intentionally "
                   "or not. Whether your team's emotional environment is an asset or a liability.",
                   ST['body'])],
    ]
    ebf_bg = [NAVY, BLUE_LT, MAGENTA]
    for i, (row, bg) in enumerate(zip(ebf_data, ebf_bg)):
        t = Table([row], colWidths=[110, usable-110])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (0,-1), bg),
            ('BACKGROUND',    (1,0), (1,-1), WARM),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING',    (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING',   (0,0), (0,-1), 14),
            ('RIGHTPADDING',  (0,0), (0,-1), 14),
            ('LEFTPADDING',   (1,0), (1,-1), 14),
            ('RIGHTPADDING',  (1,0), (1,-1), 14),
        ]))
        story.append(t)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 14))
    story.append(Paragraph("How to Use This Assessment", ST['h2']))
    story.append(Paragraph(
        "Each section has <b>5 questions</b>. Rate yourself honestly on a scale of <b>1–5</b>:",
        ST['body']))
    story.append(Paragraph(
        "1 = Never &nbsp;&nbsp; 2 = Rarely &nbsp;&nbsp; 3 = Sometimes &nbsp;&nbsp; "
        "4 = Often &nbsp;&nbsp; 5 = Almost Always",
        ParagraphStyle('scaleinline', fontName='Helvetica-Bold', fontSize=10,
                       leading=16, textColor=NAVY, spaceAfter=8)))
    story.append(Paragraph(
        "<b>No one is watching. No one is grading you.</b> The only person this helps is you — "
        "but only if you answer what's actually true, not what sounds good.",
        ST['body']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # DOMAIN 1 — EMOTIONAL
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PART ONE", ST['section_label']))
    story += domain_block(
        title="Emotional Intelligence",
        eyebrow="Domain 1 of 3",
        accent=NAVY,
        intro="This is where everything starts. Before you can lead anyone else well, "
              "you have to understand what's happening inside you — especially when the pressure is on.",
        questions=[
            (
                "When you're stressed or overwhelmed at work, do you notice it in your body before you react?",
                "Think: jaw tension, chest tightening, voice going flat. Your body signals stress before your brain does."
            ),
            (
                "How often do you say 'I'm fine' — at work or to yourself — when you're clearly not?",
                "This is the emotional suppression pattern. High-achievers are especially good at this one."
            ),
            (
                "After a difficult meeting or conversation, do you replay it for hours — editing, rehearsing, second-guessing?",
                "This is called rumination. It's exhausting, and it signals unprocessed emotional charge."
            ),
            (
                "When you receive critical feedback, can you sit with it — or do you immediately start building a defense?",
                "Self-regulation under ego threat. This is one of the highest-leverage EQ skills in leadership."
            ),
            (
                "Can you name the top 3 situations or behaviors that reliably trigger a strong emotional reaction in you at work?",
                "If you can't name them, you can't manage them. Triggers unnamed are triggers in charge."
            ),
        ],
        ST=ST
    )

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # DOMAIN 2 — RELATIONAL
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PART TWO", ST['section_label']))
    story += domain_block(
        title="Relational Intelligence",
        eyebrow="Domain 2 of 3",
        accent=BLUE_LT,
        intro="Leadership is relational. The question isn't just how smart you are — "
              "it's whether people feel safe enough to be honest with you, "
              "and whether you can actually hear them when they are.",
        questions=[
            (
                "When conflict comes up with a colleague or direct report, is your first instinct toward it — or away from it?",
                "Conflict avoidance is one of the most common EQ gaps in high-functioning leaders. Avoidance compounds everything."
            ),
            (
                "Do the people closest to you at work feel like they can tell you hard things — without managing your reaction first?",
                "This is psychological safety at the interpersonal level. If people pre-edit around you, you're leading with fear."
            ),
            (
                "When someone on your team is visibly struggling, is your first move to create space — or to solve it for them because it's faster?",
                "Over-functioning as a leader kills people's agency and signals that you don't trust them to figure things out."
            ),
            (
                "In disagreements, are you more focused on being right — or on being understood (and understanding)?",
                "The need to win arguments is one of the clearest signs that ego is driving, not leadership."
            ),
            (
                "Are you aware of how differently you show up in high-stakes conversations versus low-pressure ones?",
                "This gap — the difference between your 'best self' and your 'under fire' self — is exactly what EQ training closes."
            ),
        ],
        ST=ST
    )

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # DOMAIN 3 — ORGANIZATIONAL
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PART THREE", ST['section_label']))
    story += domain_block(
        title="Organizational Intelligence",
        eyebrow="Domain 3 of 3",
        accent=MAGENTA,
        intro="Your EQ doesn't just affect you — it builds or erodes the culture around you. "
              "This section looks at how your patterns are showing up in your team, your systems, "
              "and the emotional environment you're creating whether you mean to or not.",
        questions=[
            (
                "Does your team have genuine psychological safety — meaning they can disagree with you, flag problems, and take risks without fear?",
                "Not 'do you think they feel safe' — do they actually act like it? There's usually a gap here."
            ),
            (
                "Do you unconsciously favor and promote people who communicate and lead like you — and undervalue those who don't?",
                "This is affinity bias. It's one of the most common ways leaders accidentally build monocultures."
            ),
            (
                "Does your team's conflict pattern lean toward: avoiding it, exploding with it, or engaging it directly?",
                "Teams take on the conflict pattern of their leader. Your answer here reflects more than just your team."
            ),
            (
                "Do you know the emotional temperature of your team right now — not their performance numbers, their actual emotional state?",
                "Most leaders track KPIs. Almost none can answer this question accurately. That gap has a cost."
            ),
            (
                "When something goes wrong organizationally, is your first instinct to find the systemic cause — or the individual to hold accountable?",
                "Systems thinking vs. blame culture. Where your attention goes when things break tells you a lot about how you lead."
            ),
        ],
        ST=ST
    )

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SCORING PAGE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("YOUR RESULTS", ST['section_label']))
    story.append(Paragraph("What Your Score Actually Means", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=GOLD,
                             spaceBefore=0, spaceAfter=12))

    story.append(Paragraph(
        "Add up your scores across all three domains. Maximum total: <b>75 points.</b>",
        ST['body']))

    # Total score box
    ts_data = [[
        Paragraph("DOMAIN 1\nEmotional\n_____ / 25",
            ParagraphStyle('tsb', fontName='Helvetica-Bold', fontSize=10,
                           textColor=WHITE, leading=16, alignment=TA_CENTER)),
        Paragraph("+", ParagraphStyle('tsplus', fontName='Helvetica-Bold',
                  fontSize=18, textColor=GOLD, alignment=TA_CENTER)),
        Paragraph("DOMAIN 2\nRelational\n_____ / 25",
            ParagraphStyle('tsb2', fontName='Helvetica-Bold', fontSize=10,
                           textColor=WHITE, leading=16, alignment=TA_CENTER)),
        Paragraph("+", ParagraphStyle('tsplus2', fontName='Helvetica-Bold',
                  fontSize=18, textColor=GOLD, alignment=TA_CENTER)),
        Paragraph("DOMAIN 3\nOrganizational\n_____ / 25",
            ParagraphStyle('tsb3', fontName='Helvetica-Bold', fontSize=10,
                           textColor=WHITE, leading=16, alignment=TA_CENTER)),
        Paragraph("=", ParagraphStyle('tseq', fontName='Helvetica-Bold',
                  fontSize=18, textColor=GOLD, alignment=TA_CENTER)),
        Paragraph("TOTAL\n\n_____ / 75",
            ParagraphStyle('tst', fontName='Helvetica-Bold', fontSize=10,
                           textColor=GOLD, leading=16, alignment=TA_CENTER)),
    ]]
    ts = Table(ts_data, colWidths=[80, 22, 80, 22, 86, 22, 74])
    ts.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), NAVY),
        ('BACKGROUND',    (2,0), (2,-1), BLUE_LT),
        ('BACKGROUND',    (4,0), (4,-1), MAGENTA),
        ('BACKGROUND',    (6,0), (6,-1), colors.HexColor('#1e2f54')),
        ('BACKGROUND',    (1,0), (1,-1), WARM),
        ('BACKGROUND',    (3,0), (3,-1), WARM),
        ('BACKGROUND',    (5,0), (5,-1), WARM),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(ts)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Score Ranges", ST['h2']))

    bands = [
        ("Foundations Stage", "15 – 34",
         "Your self-awareness is just beginning to surface — and that's not a criticism, it's a starting point. "
         "Most high-achievers have spent years optimizing their external performance at the expense of their internal world. "
         "The awareness you're building now is the most important shift you'll ever make.",
         colors.HexColor('#8B2252')),
        ("Emerging Awareness", "35 – 49",
         "You have genuine self-awareness — you can see your patterns, even if you can't always interrupt them in real time. "
         "The work here is consistency: closing the gap between who you are on your good days "
         "and who you are when the pressure is highest.",
         colors.HexColor('#1A3A6B')),
        ("Practicing EQ", "50 – 62",
         "You're doing the inner work and it shows. Your emotional intelligence is active — but there are still "
         "specific triggers, relationships, or environments that reveal the edge. "
         "Targeted practice in your weakest domain will create a disproportionate return.",
         BLUE_LT),
        ("Leading with EQ", "63 – 75",
         "You're operating at a high level of emotional intelligence. The question now isn't whether you have EQ — "
         "it's whether your environment, your team, and your systems reflect it. "
         "The next frontier is scaling your inner work into organizational culture.",
         colors.HexColor('#2D6B4A')),
    ]

    for label, rng, desc, bg in bands:
        story.append(score_band(label, rng, desc, bg, ST))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # Important note
    note_data = [[Paragraph(
        "<b>Important:</b> Your score is a starting point, not a verdict. "
        "EQ is not fixed — it is the most learnable, most changeable dimension of human performance. "
        "The leaders who grow the fastest are the ones who stop treating their emotional patterns "
        "as personality and start treating them as <i>skills to be developed.</i>",
        ParagraphStyle('note', fontName='Helvetica', fontSize=10.5,
                       leading=17, textColor=NAVY))]]
    nt = Table(note_data, colWidths=[usable])
    nt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#F0EBE0')),
        ('LEFTPADDING',   (0,0), (-1,-1), 18),
        ('RIGHTPADDING',  (0,0), (-1,-1), 18),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEAFTER',     (0,0), (0,-1), 4, GOLD),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(nt)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # DOMAIN DEEP DIVES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("GOING DEEPER", ST['section_label']))
    story.append(Paragraph("What to Focus On Next", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=GOLD,
                             spaceBefore=0, spaceAfter=12))
    story.append(Paragraph(
        "Look at your three domain scores individually. The lowest score is your highest-leverage starting point — "
        "not because it's your 'worst' area, but because growth there will ripple into everything else.",
        ST['body']))

    deep_dives = [
        (
            "If Emotional was your lowest score:",
            NAVY,
            [
                "Your nervous system is running the show — and it doesn't know the difference between a 'threatening' performance review and an actual threat. "
                "The psychological concept at play is <b>amygdala hijack</b> (Goleman, 1995): when we're triggered, "
                "the emotional brain overrides the reasoning brain before we're even aware it happened.",
                "Start here: <b>daily body check-ins</b> (3x/day — morning, midday, end of day). "
                "Not journaling, not meditating — just 60 seconds of noticing where you're holding tension and naming the feeling driving it. "
                "What you name, you can regulate. What you don't name, you act out.",
            ]
        ),
        (
            "If Relational was your lowest score:",
            BLUE_LT,
            [
                "Your relationships are likely functional — but are they honest? "
                "The psychological principle here is <b>psychological safety</b> (Amy Edmondson, Harvard): "
                "teams perform significantly better when members feel safe to speak up, take risks, and be wrong without punishment.",
                "Start here: <b>ask one brave question this week</b> — to someone on your team or in your orbit: "
                "<i>'What's something you haven't told me that you think I should know?'</i> "
                "Then listen without defending, explaining, or pivoting. Just receive it.",
            ]
        ),
        (
            "If Organizational was your lowest score:",
            MAGENTA,
            [
                "The culture you're building is a mirror of your inner world — amplified. "
                "The research is clear (<b>Gallup, McKinsey, Edmondson</b>): the #1 predictor of team performance "
                "isn't talent or process. It's whether people feel emotionally safe enough to do their best work.",
                "Start here: <b>audit your reactions</b> — for one week, notice how you respond when someone brings you a problem, "
                "a mistake, or a disagreement. What's the emotional environment you're modeling in those moments? "
                "Your team is watching, and they're calibrating their behavior accordingly.",
            ]
        ),
    ]

    for title, accent, paras in deep_dives:
        story.append(Spacer(1, 8))
        # accent bar title
        tb_data = [[Paragraph(title, ParagraphStyle('ddt',
            fontName='Helvetica-Bold', fontSize=12, textColor=WHITE, leading=16))]]
        tb = Table(tb_data, colWidths=[usable])
        tb.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), accent),
            ('TOPPADDING',    (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING',   (0,0), (-1,-1), 16),
            ('ROUNDEDCORNERS', [6]),
        ]))
        story.append(tb)
        story.append(Spacer(1, 6))
        for p in paras:
            story.append(Paragraph(p, ST['body']))
            story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # FINAL PAGE — CTA
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("WHAT COMES NEXT", ST['section_label']))
    story.append(Paragraph(
        "Self-awareness is the beginning.\nNot the destination.", ST['h1']))
    story.append(HRFlowable(width=usable, thickness=1.5, color=GOLD,
                             spaceBefore=0, spaceAfter=14))

    story.append(Paragraph(
        "This assessment is designed to show you where the work is — not make you feel bad about it. "
        "Every leader has gaps. The ones who close them are the ones who stop pretending the gaps don't exist.",
        ST['body']))

    story.append(Paragraph(
        "The <b>Empathy Bridge Framework</b> doesn't just diagnose — it gives you a path. "
        "Whether you're navigating conflict on your team, trying to break a leadership pattern that keeps costing you, "
        "or building a culture that can actually hold under pressure — this is the work.",
        ST['body']))

    story.append(Spacer(1, 14))

    # CTA box
    cta_items = [
        [Paragraph("Ready to Close the Gap?", ST['cta_head'])],
        [Paragraph(
            "Book a keynote, workshop, or strategy session with Brittany —\n"
            "or explore the full suite of EQ and leadership resources at Envision Greatness.",
            ST['cta_body'])],
        [Spacer(1, 6)],
        [Paragraph("brittanyclausen.com", ST['cta_url'])],
        [Paragraph("envisiongreatnessnow.com", ST['cta_url'])],
        [Spacer(1, 4)],
        [Paragraph("bizdev@envisiongreatnessnow.com  ·  651-273-9965",
            ParagraphStyle('ctacontact', fontName='Helvetica', fontSize=9.5,
                           textColor=colors.HexColor('#A0B0C8'),
                           alignment=TA_CENTER, leading=14))],
    ]
    cta_t = Table(cta_items, colWidths=[usable])
    cta_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), NAVY),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 32),
        ('RIGHTPADDING',  (0,0), (-1,-1), 32),
        ('TOPPADDING',    (0,0), (0,0), 28),
        ('BOTTOMPADDING', (-1,-1), (-1,-1), 24),
        ('ROUNDEDCORNERS', [10]),
    ]))
    story.append(cta_t)

    story.append(Spacer(1, 22))

    story.append(Paragraph(
        "Also available: the <b>EQ Edge Newsletter</b> — weekly insight on emotional intelligence, "
        "leadership, and the inner work that actually moves the needle. "
        "Subscribe at <b>brittanyclausen.com</b>",
        ParagraphStyle('also', fontName='Helvetica', fontSize=9.5,
                       leading=15, textColor=MUTED, alignment=TA_CENTER)))

    story.append(Spacer(1, 18))
    story.append(HRFlowable(width=usable, thickness=0.5, color=colors.HexColor('#D0C8BE'),
                             spaceBefore=0, spaceAfter=10))
    story.append(Paragraph(
        "© 2026 Brittany Clausen · Envision Greatness LLC · All Rights Reserved\n"
        "This document is for personal use only. Please do not reproduce or redistribute without permission.",
        ST['footer']))

    # ── BUILD ────────────────────────────────────────────────────────────────
    # First page uses navy cover bg, all others use cream inner bg
    def page_template(canvas, doc):
        if doc.page == 1:
            add_cover_bg(canvas, doc)
        else:
            add_page_bg(canvas, doc)

    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    print(f"PDF created: {path}")

if __name__ == '__main__':
    build_pdf('/Users/brittanyclausen/Claude Code/brittany-clausen/eq-self-assessment-guide.pdf')
