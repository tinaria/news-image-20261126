#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Thursday 26 November 2026.

Draws a one-page newspaper front page summing up the world's news of
26 November 2026 (36 stories, 8 regions) and writes it as entry.png.
Stdlib + Pillow only. All font sizes are integers. Deterministic: the
same code always produces the same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 22

PAPER = (245, 240, 225)
INK = (26, 26, 26)
MUTED = (107, 101, 88)
RED = (163, 30, 34)
NAVY = (29, 53, 87)
TEAL = (42, 111, 107)
OCHRE = (201, 138, 27)
LIGHT = (232, 226, 208)
CARD = (250, 247, 236)
LINE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), int(size))


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width. Returns a list of lines."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text, return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def status_tag(draw, x, y, status):
    """Draw a small outlined status tag, return its right edge."""
    fnt = F_SANS_B(10)
    w = int(draw.textlength(status, font=fnt)) + 10
    draw.rectangle([x, y, x + w, y + 14], outline=INK, width=1)
    draw.text((x + 5, y + 2), status, font=fnt, fill=INK)
    return x + w


# ---------------------------------------------------------------- stories

HEROES = [
    {
        "num": 1,
        "headline": "Macy's 100th Thanksgiving parade put off to Saturday",
        "body": "A nor'easter brings gusts near 60 mph to New York, grounding the balloons in a first for the parade.",
        "source": "REUTERS",
        "status": "CONFIRMED",
        "art": "macys",
    },
    {
        "num": 2,
        "headline": "India marks 18 years since the 26/11 Mumbai attacks",
        "body": "Tributes honour the 166 killed in 2008, as India also marks 77 years of its Constitution.",
        "source": "PTI",
        "status": "OFFICIAL",
        "art": "india",
    },
    {
        "num": 3,
        "headline": "Gukesh meets Sindarov in Game 3 of the title match",
        "body": "The title match is level at 1-1 after two draws; Game 3 is played in Geneva, Sindarov to move.",
        "source": "FIDE",
        "status": "ONGOING",
        "art": "chess",
    },
]

MEDIUM = [
    {
        "num": 4,
        "headline": "Houthis say they hit Saudi Arabia's Ras Tanura refinery",
        "body": "The group claims strikes on Saudi ports and the kingdom's largest refinery.",
        "source": "REUTERS",
        "status": "CLAIM",
        "art": "houthi",
    },
    {
        "num": 5,
        "headline": "Two tankers hit naval mines in the Strait of Hormuz",
        "body": "Iran tells shipping to plan passage carefully after the blasts.",
        "source": "REUTERS",
        "status": "REPORTED",
        "art": "hormuz",
    },
    {
        "num": 6,
        "headline": "Israeli strike kills Hamas security chief in Gaza",
        "body": "The strike hits Gaza as the fragile ceasefire strains.",
        "source": "AP",
        "status": "REPORTED",
        "art": "gaza",
    },
    {
        "num": 7,
        "headline": "Ukraine says it hit a Russian airbase; five jets damaged",
        "body": "Kyiv claims the strike on Savasleyka airfield in the Nizhny Novgorod region.",
        "source": "REUTERS",
        "status": "CLAIM",
        "art": "airbase",
    },
    {
        "num": 8,
        "headline": "Russian ballistic missiles hit Kyiv",
        "body": "Explosions sound across the capital as air defences engage.",
        "source": "REUTERS",
        "status": "REPORTED",
        "art": "kyiv",
    },
    {
        "num": 9,
        "headline": "US proposes new tariffs on 14 trading partners",
        "body": "China, the EU, Japan and India are named in a move aimed at factory overcapacity.",
        "source": "REUTERS",
        "status": "CONFIRMED",
        "art": "tariffs",
    },
    {
        "num": 10,
        "headline": "Bangladesh garment pay rise sparks fresh protests",
        "body": "A 36% rise to Tk17,000 a month is the smallest since 1986; workers wanted more.",
        "source": "AFP",
        "status": "CONFIRMED",
        "art": "bangladesh",
    },
    {
        "num": 11,
        "headline": "Shenzhou-24 docks; first Pakistani in space reaches Tiangong",
        "body": "Muhammad Zeeshan Ali is the first foreign national aboard China's space station.",
        "source": "XINHUA",
        "status": "CONFIRMED",
        "art": "shenzhou",
    },
    {
        "num": 12,
        "headline": "Leaked records put Russian war dead near 490,000",
        "body": "BBC analysis of Rosstat data; Mediazona puts the true toll near 700,000.",
        "source": "BBC",
        "status": "REPORTED",
        "art": "wardata",
    },
    {
        "num": 13,
        "headline": "Solomon Islands names Australia its top security partner",
        "body": "A new treaty rules out foreign military bases on its soil.",
        "source": "AP",
        "status": "CONFIRMED",
        "art": "solomon",
    },
]

# Briefs 14-36: (text, source). Text kept short so each fits one line.
BRIEFS = [
    ("Cairo tanker fire kills at least 31", "REUTERS"),
    ("Kim orders wider rollout of tactical nuclear arms", "KCNA"),
    ("Second judge blocks Trump birthright order", "REUTERS"),
    ("2,000 migrants reach Canary Islands in a day", "REUTERS"),
    ("Liverpool beat Club Brugge 3-0", "AP"),
    ("Jennifer Barreto wins Miss Universe 2026", "AP"),
    ("AI sell-off pushes Nasdaq near bear market", "REUTERS"),
    ("Murmansk governor held on corruption charges", "REUTERS"),
    ("Lebanon to open second airport next month", "REUTERS"),
    ("Nations urge Russia to halt riot-agent use", "REUTERS"),
    ("How China got Nvidia AI chips despite curbs", "REUTERS"),
    ("Kenyan cult leader convicted of new charges", "REUTERS"),
    ("Ecuador: US talks focus on reviewing operations", "REUTERS"),
    ("India clears 6,000 new IIT seats for AI and space", "PTI"),
    ("Sooryavanshi, 15, smashes 204 off 53 balls", "CRICINFO"),
    ("North Korea expels Swiss diplomat in sanctions row", "AP"),
    ("Swiss tourist killed by elephants in Cameroon", "AP"),
    ("California warns of flooding as king tides peak", "AP"),
    ("India clears Rs 4,288 cr terminal at Kamarajar Port", "PTI"),
    ("Merz defends Ukraine aid as Russia threat grows", "REUTERS"),
    ("EU urges Schengen halt to old Russian passports", "REUTERS"),
    ("Storm threatens 1.76m Palestinians in Gaza", "AP"),
    ("Hasina says she intends to return to Bangladesh", "PTI"),
]

UTC_ITEMS = [
    ("00:00 UTC", "Thanksgiving Day begins in the US"),
    ("05:00 UTC", "Tributes begin in Delhi for 26/11"),
    ("13:30 UTC", "Macy's 100th parade was due to step off"),
    ("14:00 UTC", "Chess Game 3 begins in Geneva"),
    ("15:00 UTC", "High-wind warning begins in New York"),
    ("23:00 UTC", "The day's 36 stories filed"),
]

DATE_CHECK = [
    ("Gukesh-Sindarov Game 2 ends in a 20-move draw", "25 Nov"),
    ("Gukesh-Sindarov Game 1 ends in a 38-move draw", "24 Nov"),
    ("Bangladesh wage board settles 36% rise", "25 Nov"),
    ("Solomon Islands-Australia treaty signed", "25 Nov"),
    ("BBC publishes Rosstat leak analysis", "25 Nov"),
    ("Le Monde publishes Rosstat leak", "24 Nov"),
    ("US shelves Russia business-deal peace plan", "25 Nov"),
    ("COP31 ends without a pact", "22 Nov"),
]

REGIONS = [
    ("North America", 6, (29, 53, 87)),
    ("South Asia", 6, (163, 30, 34)),
    ("Europe", 10, (42, 111, 107)),
    ("Middle East", 5, (201, 138, 27)),
    ("East Asia", 4, (120, 90, 40)),
    ("Africa", 3, (90, 90, 90)),
    ("Oceania", 1, (140, 60, 120)),
    ("South America", 1, (60, 120, 60)),
]


# ---------------------------------------------------------------- art
# Every illustration is drawn from scratch with Pillow primitives:
# flat shapes, no photos, no copied pixels.

def _num_badge(draw, x, y, num, fill=RED):
    r = 11
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill, outline=(255, 255, 255), width=2)
    fnt = F_SANS_B(12)
    t = str(num)
    tw = int(draw.textlength(t, font=fnt))
    draw.text((x + r - tw // 2, y + 4), t, font=fnt, fill=(255, 255, 255))


def _banner(draw, x, y, w, text, fill=RED):
    fnt = F_SANS_B(10)
    draw.rectangle([x, y, x + w, y + 16], fill=fill)
    tw = int(draw.textlength(text, font=fnt))
    draw.text((x + (w - tw) // 2, y + 3), text, font=fnt, fill=(255, 255, 255))


def draw_macys(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 42, 70))
    # rain
    for i in range(14):
        rx = x + 12 + i * 20
        draw.line([rx, y + 8, rx - 6, y + 30], fill=(120, 150, 190), width=1)
    # skyline
    for i, bh in enumerate([48, 60, 40, 56, 62, 46, 54]):
        bx = x + 8 + i * 40
        draw.rectangle([bx, y + h - 18 - bh, bx + 32, y + h - 18], fill=(12, 22, 38))
        for wy in range(y + h - 12 - bh, y + h - 22, 12):
            for wx in (bx + 6, bx + 18):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(240, 200, 90))
    # balloon
    draw.ellipse([x + w // 2 - 52, y + 12, x + w // 2 + 52, y + 62], fill=(245, 240, 225))
    draw.ellipse([x + w // 2 - 14, y + 30, x + w // 2 - 4, y + 40], fill=INK)
    draw.ellipse([x + w // 2 + 4, y + 30, x + w // 2 + 14, y + 40], fill=INK)
    draw.ellipse([x + w // 2 - 8, y + 46, x + w // 2 + 8, y + 54], fill=RED)
    # gold 100 badge
    draw.ellipse([x + w - 52, y + h - 52, x + w - 16, y + h - 16], fill=(201, 138, 27))
    fnt = F_SANS_B(13)
    draw.text((x + w - 44, y + h - 43), "100", font=fnt, fill=(255, 255, 255))
    _banner(draw, x, y + h - 18, 168, "POSTPONED TO SATURDAY")


def draw_india(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 150, 60))
    draw.ellipse([x + w - 66, y + 10, x + w - 26, y + 50], fill=(245, 220, 140))
    # India Gate style arch
    ax = x + 24
    draw.rectangle([ax, y + 34, ax + 84, y + h - 20], fill=(120, 60, 40))
    draw.rectangle([ax + 10, y + 24, ax + 74, y + 38], fill=(120, 60, 40))
    draw.pieslice([ax + 22, y + 44, ax + 62, y + 96], 180, 360, fill=(232, 150, 60))
    draw.rectangle([ax + 32, y + 58, ax + 52, y + h - 20], fill=(232, 150, 60))
    # tricolour stripes
    for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        draw.rectangle([x + w - 96, y + h - 34 + i * 5, x + w - 14, y + h - 29 + i * 5], fill=c)
    # candles
    for i in range(7):
        cx = x + 130 + i * 16
        draw.rectangle([cx, y + h - 30, cx + 7, y + h - 16], fill=(245, 240, 225))
        draw.ellipse([cx + 1, y + h - 38, cx + 6, y + h - 30], fill=(255, 200, 40))
    _banner(draw, x + w - 78, y + 6, 78, "18 YEARS", fill=INK)


def draw_chess(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 66, 52))
    bs = 13
    bx = x + 16
    by = y + 12
    for r in range(4):
        for c in range(4):
            col = (235, 228, 205) if (r + c) % 2 == 0 else (52, 88, 70)
            draw.rectangle([bx + c * bs, by + r * bs, bx + (c + 1) * bs, by + (r + 1) * bs], fill=col)
    draw.ellipse([bx + 5, by + 5, bx + 21, by + 21], fill=(255, 255, 255), outline=INK)
    draw.ellipse([bx + 34, by + 34, bx + 48, by + 48], fill=INK, outline=(255, 255, 255))
    # clocks
    for i, cx in enumerate((x + 92, x + 176)):
        draw.rectangle([cx, y + 18, cx + 74, y + 52], fill=(245, 240, 225), outline=INK, width=2)
        fnt = F_SANS_B(16)
        draw.text((cx + 12, y + 26), "1:32", font=fnt, fill=INK)
    fnt = F_SANS_B(13)
    draw.text((x + 92, y + 58), "GUKESH  1 - 1  SINDAROV", font=fnt, fill=(255, 255, 255))
    _banner(draw, x + w - 82, y + h - 20, 82, "GAME 3", fill=RED)


def draw_houthi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 128, 84))
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 50, 40))
    for tx in (x + 14, x + 52, x + 96):
        draw.rectangle([tx, y + 16, tx + 14, y + h - 10], fill=(70, 40, 34))
        draw.rectangle([tx + 4, y + 10, tx + 10, y + 16], fill=(70, 40, 34))
    draw.ellipse([x + 128, y + 8, x + w - 12, y + 30], fill=(240, 200, 90))
    draw.polygon([(x + 150, y + 18), (x + 158, y + 6), (x + 166, y + 18)], fill=(255, 120, 30))
    draw.polygon([(x + 138, y + 20), (x + 146, y + 10), (x + 154, y + 20)], fill=(255, 170, 40))


def draw_hormuz(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(70, 130, 170))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 90, 130))
    for sx in (x + 16, x + 92):
        draw.rectangle([sx, y + 30, sx + 56, y + 48], fill=(40, 40, 44))
        draw.rectangle([sx + 18, y + 18, sx + 34, y + 30], fill=(40, 40, 44))
        draw.rectangle([sx + 6, y + 44, sx + 66, y + 48], fill=(30, 30, 34))
    # spiky mine
    mx, my = x + w - 34, y + 18
    draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=INK)
    for a in range(0, 360, 45):
        import math
        dx = int(13 * math.cos(math.radians(a)))
        dy = int(13 * math.sin(math.radians(a)))
        draw.line([mx, my, mx + dx, my + dy], fill=INK, width=2)


def draw_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(206, 190, 160))
    for bx, bw, bh in ((x + 12, 44, 24), (x + 64, 52, 32), (x + 124, 40, 20)):
        draw.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10], fill=(120, 104, 84))
        for wy in range(y + h - 6 - bh, y + h - 14, 10):
            draw.rectangle([bx + 8, wy, bx + 16, wy + 5], fill=(60, 52, 44))
    for cx, cy, r in ((x + 140, y + 16, 11), (x + 158, y + 8, 8), (x + 122, y + 10, 7)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))


def draw_airbase(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(150, 155, 150))
    draw.polygon([(x, y + h - 14), (x + w, y + 30), (x + w, y + 44), (x, y + h)], fill=(90, 92, 90))
    for i in range(4):
        draw.line([x + 20 + i * 34, y + h - 22 - i * 7, x + 32 + i * 34, y + h - 26 - i * 7], fill=(255, 255, 255), width=2)
    # jet silhouette
    draw.polygon([(x + 30, y + 30), (x + 78, y + 22), (x + 70, y + 34), (x + 44, y + 40)], fill=(40, 44, 48))
    draw.polygon([(x + 52, y + 26), (x + 62, y + 12), (x + 66, y + 26)], fill=(40, 44, 48))
    # blast star
    cx, cy = x + 128, y + 22
    for a in range(0, 360, 30):
        import math
        dx = int(16 * math.cos(math.radians(a)))
        dy = int(16 * math.sin(math.radians(a)))
        draw.line([cx, cy, cx + dx, cy + dy], fill=(255, 140, 20), width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 200, 60))


def draw_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 34, 52))
    for i, bh in enumerate([22, 30, 19, 26]):
        bx = x + 10 + i * 42
        draw.rectangle([bx, y + h - 8 - bh, bx + 32, y + h - 8], fill=(14, 18, 30))
        for wy in range(y + h - 4 - bh, y + h - 12, 9):
            draw.rectangle([bx + 6, wy, bx + 11, wy + 4], fill=(240, 200, 90))
    for sx, sy in ((x + 120, y + 12), (x + 60, y + 22), (x + 150, y + 30)):
        draw.line([sx, sy, sx - 26, sy + 26], fill=(255, 120, 40), width=2)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 120))


def draw_tariffs(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(196, 208, 220))
    boxes = [(x + 12, y + 8, (163, 30, 34)), (x + 64, y + 8, (29, 53, 87)),
             (x + 116, y + 8, (42, 111, 107)), (x + 38, y + 26, (201, 138, 27)),
             (x + 90, y + 26, (120, 90, 40))]
    for bx, by, col in boxes:
        draw.rectangle([bx, by, bx + 44, by + 16], fill=col, outline=(255, 255, 255), width=1)
        draw.line([bx + 8, by, bx + 8, by + 16], fill=(255, 255, 255), width=1)
        draw.line([bx + 36, by, bx + 36, by + 16], fill=(255, 255, 255), width=1)
    fnt = F_SERIF_B(20)
    draw.text((x + w - 34, y + 26), "%", font=fnt, fill=RED)


def draw_bangladesh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 214, 196))
    draw.rectangle([x + 12, y + 26, x + 108, y + h - 12], fill=(150, 120, 90))
    draw.rectangle([x + 20, y + 14, x + 30, y + 26], fill=(150, 120, 90))
    for wx in range(x + 22, x + 100, 18):
        draw.rectangle([wx, y + 28, wx + 10, y + 34], fill=(245, 240, 225))
    # shirt
    draw.polygon([(x + 128, y + 14), (x + 142, y + 8), (x + 158, y + 14), (x + 158, y + 30),
                  (x + 128, y + 30)], fill=(42, 111, 107))
    draw.polygon([(x + 128, y + 14), (x + 118, y + 24), (x + 128, y + 28)], fill=(42, 111, 107))
    draw.polygon([(x + 158, y + 14), (x + 168, y + 24), (x + 158, y + 28)], fill=(42, 111, 107))
    _banner(draw, x + 112, y + h - 18, 76, "Tk 17,000", fill=RED)


def draw_shenzhou(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(10, 12, 24))
    for sx, sy in ((x + 14, y + 10), (x + 60, y + 22), (x + 150, y + 8), (x + 176, y + 30), (x + 30, y + 40)):
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # earth arc first, so the station sits on top of it
    draw.pieslice([x - 10, y + h - 24, x + w + 10, y + h + 24], 180, 360, fill=(60, 120, 180))
    draw.arc([x - 10, y + h - 24, x + w + 10, y + h + 24], 180, 360, fill=(140, 200, 240), width=2)
    # station: central cylinder + panels
    draw.rectangle([x + 70, y + 26, x + 118, y + 44], fill=(220, 224, 230))
    draw.rectangle([x + 88, y + 18, x + 100, y + 26], fill=(180, 186, 196))
    draw.rectangle([x + 30, y + 30, x + 70, y + 40], fill=(40, 80, 160))
    draw.rectangle([x + 118, y + 30, x + 158, y + 40], fill=(40, 80, 160))
    draw.ellipse([x + 82, y + 30, x + 92, y + 40], fill=(255, 200, 60))


def draw_wardata(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    for i in range(3):
        draw.rectangle([x + 18 + i * 6, y + 8 + i * 5, x + 150 + i * 6, y + h - 8], fill=(255, 255, 255), outline=(150, 146, 134))
    for wy in (y + 16, y + 23):
        draw.rectangle([x + 34, wy, x + 130, wy + 3], fill=(120, 118, 110))
    fnt = F_SANS_B(16)
    draw.text((x + 34, y + 28), "490,334", font=fnt, fill=RED)


def draw_solomon(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(140, 190, 210))
    for ex, ey, ew, eh in ((x + 16, y + 30, 52, 16), (x + 78, y + 20, 44, 14), (x + 128, y + 32, 48, 14)):
        draw.ellipse([ex, ey, ex + ew, ey + eh], fill=(70, 140, 80))
    draw.rectangle([x + 96, y + 8, x + 104, y + 34], fill=(120, 90, 60))
    draw.polygon([(x + 104, y + 8), (x + 128, y + 16), (x + 104, y + 24)], fill=(255, 255, 255))
    # treaty document
    draw.rectangle([x + 120, y + h - 30, x + 166, y + h - 6], fill=(255, 255, 255), outline=INK)
    for wy in range(y + h - 25, y + h - 12, 5):
        draw.line([x + 126, wy, x + 160, wy], fill=(100, 100, 100), width=1)
    draw.ellipse([x + 152, y + h - 11, x + 162, y + h - 1], fill=RED)


ART = {
    "macys": draw_macys,
    "india": draw_india,
    "chess": draw_chess,
    "houthi": draw_houthi,
    "hormuz": draw_hormuz,
    "gaza": draw_gaza,
    "airbase": draw_airbase,
    "kyiv": draw_kyiv,
    "tariffs": draw_tariffs,
    "bangladesh": draw_bangladesh,
    "shenzhou": draw_shenzhou,
    "wardata": draw_wardata,
    "solomon": draw_solomon,
}


# ---------------------------------------------------------------- map

CONTINENTS = [
    [(28, 28), (78, 18), (108, 30), (96, 52), (70, 62), (48, 78), (30, 58)],
    [(95, 10), (104, 8), (108, 16), (98, 20)],
    [(78, 92), (108, 86), (118, 110), (100, 140), (82, 120)],
    [(150, 28), (178, 20), (190, 38), (168, 52), (150, 44)],
    [(150, 66), (180, 62), (196, 84), (178, 118), (158, 104), (146, 82)],
    [(190, 24), (280, 18), (312, 40), (296, 72), (250, 84), (214, 66), (196, 44)],
    [(272, 118), (296, 112), (306, 128), (282, 134)],
]

# (num, map x, map y)
PINS = [
    (1, 58, 42), (2, 238, 86), (3, 168, 38), (4, 208, 76), (5, 226, 68),
    (6, 194, 58), (7, 200, 26), (8, 178, 36), (9, 52, 52), (10, 248, 80),
    (11, 262, 58), (12, 192, 16), (13, 300, 124),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 230, 228), outline=INK, width=1)
    sx = w / 330.0
    sy = h / 168.0
    for poly in CONTINENTS:
        pts = [(x + px * sx, y + py * sy) for px, py in poly]
        draw.polygon(pts, fill=(196, 198, 170), outline=(140, 142, 118))
    fnt = F_SANS_B(10)
    for num, px, py in PINS:
        cx = int(x + px * sx)
        cy = int(y + py * sy)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=2)
        t = str(num)
        tw = int(draw.textlength(t, font=fnt))
        draw.text((cx - tw // 2, cy - 6), t, font=fnt, fill=(255, 255, 255))


# ---------------------------------------------------------------- layout

def draw_masthead(draw):
    y = 10
    fnt = F_SERIF_B(56)
    title = "THE WORLD IN ONE DAY"
    tw = int(draw.textlength(title, font=fnt))
    draw.text(((W - tw) // 2, y), title, font=fnt, fill=INK)
    y += 66
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    y += 4
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    y += 10
    fnt = F_SANS_B(20)
    date = "THURSDAY 26 NOVEMBER 2026"
    tw = int(draw.textlength(date, font=fnt))
    draw.text(((W - tw) // 2, y), date, font=fnt, fill=INK)
    y += 28
    deck = ("A nor'easter grounds New York's 100th Thanksgiving parade, India marks "
            "18 years since the 26/11 Mumbai attacks, and Gukesh meets Sindarov in "
            "Game 3 of the world title match in Geneva.")
    fnt = F_SERIF(16)
    for line in wrap(draw, deck, fnt, 920):
        tw = int(draw.textlength(line, font=fnt))
        draw.text(((W - tw) // 2, y), line, font=fnt, fill=INK)
        y += 19
    return y + 6


def draw_stats(draw, y):
    box_w = 320
    gap = 10
    stats = [("36", " STORIES"), ("8", " REGIONS"), ("9", " SOURCES · 12 FIELDS")]
    for i, (num, lab) in enumerate(stats):
        x = MARGIN + i * (box_w + gap)
        draw.rectangle([x, y, x + box_w, y + 28], outline=INK, width=1)
        fn = F_SERIF_B(24)
        fl = F_SANS_B(12)
        tw = int(draw.textlength(num, font=fn)) + int(draw.textlength(lab, font=fl))
        tx = x + (box_w - tw) // 2
        draw.text((tx, y + 2), num, font=fn, fill=RED)
        draw.text((tx + int(draw.textlength(num, font=fn)), y + 8), lab, font=fl, fill=INK)
    y += 32
    # region strip
    total = sum(c for _, c, _ in REGIONS)
    x = MARGIN
    for _, count, col in REGIONS:
        w = int(980 * count / total)
        draw.rectangle([x, y, x + w, y + 8], fill=col)
        x += w
    y += 12
    fnt = F_SANS(11)
    line = "  ·  ".join("%s %d" % (name, count) for name, count, _ in REGIONS)
    tw = int(draw.textlength(line, font=fnt))
    draw.text(((W - tw) // 2, y), line, font=fnt, fill=MUTED)
    return y + 14


def draw_hero(draw, x, y, w, story):
    ART[story["art"]](draw, x, y, w, 88)
    _num_badge(draw, x + 6, y + 6, story["num"])
    y += 92
    fnt = F_SERIF_B(17)
    y = text_block(draw, x, y, story["headline"], fnt, w, leading=20, max_lines=2)
    y += 2
    fnt = F_SANS(12)
    y = text_block(draw, x, y, story["body"], fnt, w, leading=14, max_lines=2)
    y += 2
    fnt = F_SANS(10)
    draw.text((x, y), "SOURCE: " + story["source"], font=fnt, fill=MUTED)
    status_tag(draw, x + w - 74, y - 1, story["status"])
    return y + 14


def draw_medium(draw, x, y, w, story):
    ART[story["art"]](draw, x, y, w, 48)
    _num_badge(draw, x + 4, y + 4, story["num"])
    y += 52
    fnt = F_SERIF_B(12)
    y = text_block(draw, x, y, story["headline"], fnt, w, leading=14, max_lines=3)
    fnt = F_SANS(10)
    draw.text((x, y + 2), story["source"], font=fnt, fill=MUTED)
    status_tag(draw, x + w - 74, y + 1, story["status"])
    return y + 16


def draw_utc(draw, y):
    draw.text((MARGIN, y), "THE DAY IN UTC", font=F_SANS_B(12), fill=INK)
    draw.line([MARGIN, y + 16, W - MARGIN, y + 16], fill=INK, width=1)
    y += 22
    col_w = 326
    for i, (t, txt) in enumerate(UTC_ITEMS):
        row, col = divmod(i, 3)
        x = MARGIN + col * col_w
        yy = y + row * 16
        draw.text((x, yy), t, font=F_SANS_B(11), fill=NAVY)
        draw.text((x + 74, yy), txt, font=F_SANS(11), fill=INK)
    return y + 34


def draw_bottom(draw, y):
    draw.text((MARGIN, y), "WHERE IT HAPPENED — PINS 1-13", font=F_SANS_B(12), fill=INK)
    draw.text((368, y), "AND ALSO — STORIES 14-36", font=F_SANS_B(12), fill=INK)
    y += 18
    draw_map(draw, MARGIN, y, 330, 168)
    fnt = F_SANS(9)
    left = BRIEFS[:12]
    right = BRIEFS[12:]
    for col_i, items in enumerate((left, right)):
        x = 368 + col_i * 318
        yy = y
        for i, (text, src) in enumerate(items):
            num = 14 + (i if col_i == 0 else 12 + i)
            line = "%d. %s — %s" % (num, text, src)
            for ln in wrap(draw, line, fnt, 306):
                draw.text((x, yy), ln, font=fnt, fill=INK)
                yy += 12
    return y + 168


def draw_datecheck(draw, y):
    draw.rectangle([MARGIN, y, W - MARGIN, y + 70], fill=PAPER, outline=RED, width=2)
    draw.text((MARGIN + 8, y + 5), "DATE CHECK — THESE ARE NOT 26 NOVEMBER",
              font=F_SANS_B(12), fill=RED)
    fnt = F_SANS(11)
    for i, (text, when) in enumerate(DATE_CHECK):
        col, row = divmod(i, 4)
        x = MARGIN + 8 + col * 490
        yy = y + 22 + row * 12
        draw.text((x, yy), "x  %s — %s" % (text, when), font=fnt, fill=INK)
    return y + 70


def draw_footer(draw, y):
    fnt = F_SANS(10)
    line1 = ("Every story here happened or was first reported on Thursday 26 November 2026. "
             "Sources are named on each story.")
    tw = int(draw.textlength(line1, font=fnt))
    draw.text(((W - tw) // 2, y), line1, font=fnt, fill=INK)
    y += 11
    line2 = ("HOW SURE: OFFICIAL = government or institution · CONFIRMED = named outlet or two sources · "
             "REPORTED = one named outlet · CLAIM = one side's claim · ONGOING = still unfolding.")
    tw = int(draw.textlength(line2, font=fnt))
    draw.text(((W - tw) // 2, y), line2, font=fnt, fill=MUTED)
    y += 11
    line3 = "THE WORLD IN ONE DAY  ·  26 NOV 2026  ·  36 STORIES, 8 REGIONS"
    fntb = F_SANS_B(10)
    tw = int(draw.textlength(line3, font=fntb))
    draw.text(((W - tw) // 2, y), line3, font=fntb, fill=INK)
    return y + 12


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_stats(draw, y)
    hero_y = y + 4
    col_w = 320
    for i, story in enumerate(HEROES):
        draw_hero(draw, MARGIN + i * (col_w + 10), hero_y, col_w, story)
    y = hero_y + 188
    med_w = 188
    for r in range(2):
        for c in range(5):
            story = MEDIUM[r * 5 + c]
            draw_medium(draw, MARGIN + c * (med_w + 10), y + r * 122, med_w, story)
    y = y + 2 * 122 + 4
    y = draw_utc(draw, y)
    y = draw_bottom(draw, y + 4)
    y = draw_datecheck(draw, y + 4)
    y = draw_footer(draw, y + 4)
    print("BOTTOM_Y:", y)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "JPEG", quality=88, optimize=True)
    print("WROTE:", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
