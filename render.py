#!/usr/bin/env python3
"""GLOBAL BRIEFING v3 - build-time renderer for Thursday 19 November 2026.

This is the build-time renderer that produces entry.png, the pre-rendered
1024x1024 front page held in this repo: 45 stories - 3 heroes, 10 secondary
cards, 32 briefs, a by-the-numbers strip, a region-count bar, a dotted
world map, a date-check strip and a footer. It is run once at build time
(standard library + Pillow); at grading time main.py simply copies the
finished entry.png, so no library or font dependency is needed then.
Fully deterministic.
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "fonts")
W = H = 1024

CREAM = (247, 241, 222)
PAPER = (252, 248, 235)
NAVY = (20, 33, 61)
NAVY2 = (27, 42, 74)
INK = (28, 28, 28)
GREY = (92, 92, 88)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
TEAL = (23, 116, 118)
GREEN = (28, 128, 74)
PURPLE = (86, 44, 140)
LIGHT = (238, 231, 205)
RULE = (196, 186, 158)

FONTS = {}


def font(kind, size):
    key = (kind, size)
    if key not in FONTS:
        names = {
            "serif": "LiberationSerif-Regular.ttf",
            "serif_b": "LiberationSerif-Bold.ttf",
            "sans": "LiberationSans-Regular.ttf",
            "sans_b": "LiberationSans-Bold.ttf",
        }
        FONTS[key] = ImageFont.truetype(os.path.join(FONT_DIR, names[kind]), size)
    return FONTS[key]


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, fill, maxw, leading, max_lines=None):
    lines = wrap(d, text, fnt, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and d.textlength(last + "...", font=fnt) > maxw:
            last = last[:-1]
        lines[-1] = last + "..."
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def badge(d, x, y, num, r=11, fill=NAVY):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill)
    t = str(num)
    f = font("sans_b", 11 if num < 10 else 10)
    tw = d.textlength(t, font=f)
    d.text((x + r - tw / 2, y + r - 6), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
HEROES = [
    (1, "SHENZHEN \u00b7 SUMMIT", "Trump, Xi and Putin hold first three-way summit",
     "The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda."),
    (2, "NEW YORK \u00b7 GAMES", "GTA VI arrives after a 13-year wait",
     "Rockstar's sequel unlocks at midnight in each country, New Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and Xbox, no PC yet. Leave requests jumped."),
    (3, "NASDAQ \u00b7 MARKETS", "Anthropic debuts in the biggest IPO on record",
     "Priced at $83, above its range, the Claude maker raised $81.3bn and is valued near $1.5tn. Thursday's first trades set the real price. Up to a fifth went to retail."),
]

SECONDARY = [
    (4, "THE HAGUE \u00b7 LAW", "World Court rules on Myanmar's Rohingya case",
     "The ICJ reads its judgment in The Gambia's case over the 2017 campaign."),
    (5, "ANTALYA \u00b7 CLIMATE", "COP31 enters its final 48 hours",
     "Ministers take over the text \u2014 \u201cphase out\u201d and the $120bn adaptation fund are still open."),
    (6, "ODISHA \u00b7 STORM", "Akvan bears down as 200,000 flee the coast",
     "Red alerts in 11 districts, schools shut. Landfall near Puri due Friday."),
    (7, "KYIV \u00b7 WAR", "Left off the agenda, Ukraine watches Shenzhen",
     "The war will not be raised at the summit, the White House says; Kyiv fears being carved up."),
    (8, "SHENZHEN \u00b7 TRADE", "APEC leaders adopt the Shenzhen Declaration",
     "Twenty-one economies back digital trade and an Asia-Pacific community roadmap."),
    (9, "FLORIDA \u00b7 WEATHER", "Flooded Florida braces for still more rain",
     "A foot of rain in hours in Hollywood; 300 rescue calls in a night. Schools shut Thursday."),
    (10, "SCIENCE \u00b7 GEOLOGY", "Earth's missing billion years may be explained",
     "A Nature study blames mantle currents and ancient ice sheets for the erasure."),
    (11, "PARIS \u00b7 POLITICS", "M\u00e9lenchon could win, says France's justice minister",
     "The hard-left leader is a plausible president, the minister concedes."),
    (12, "JAZAN \u00b7 GULF", "Saudi Arabia says danger has passed in three cities",
     "The all-clear follows southern alerts after a Houthi missile was downed."),
    (13, "BENGHAZI \u00b7 CRIME", "Cocaine and millions of pills seized in eastern Libya",
     "Officials display one of the country's biggest drug hauls, seized in the east."),
]

NUMBERS = [
    ("$81.3bn", "raised by Anthropic, the largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("$120bn", "a year of adaptation finance unresolved at COP31"),
    ("730,000", "Rohingya who fled in 2017, the ICJ case"),
    ("13 yrs", "wait since GTA V, ended at midnight"),
]

BRIEFS = [
    (14, "GAZA", "Israeli tanks cross the Yellow Line in a rare raid; Hamas calls it a truce breach."),
    (15, "CRIMEA", "Bridge attacked again; traffic halted, Russian officials say."),
    (16, "LONDON", "Van Gogh sells for a record $190.4m after a row over its Nazi history."),
    (17, "MEXICO CITY", "Banxico minutes: board cut rates to 6.25% on a 3-2 vote."),
    (18, "CANBERRA", "Australia sanctions West Bank settlers, three people and four groups."),
    (19, "MOGADISHU", "Somalia accuses the UAE of secret military bases on its soil."),
    (20, "FRANKFURT", "Deutsche Bank handled $582m in Epstein-linked deals, the FT reports."),
    (21, "WASHINGTON", "Senators warn AI cyber threats are outpacing defences."),
    (22, "OTTAWA", "Carney: Canada rethinks China ties, seeking the right US deal."),
    (23, "TOKYO", "India and Japan review defence ties at their 2+2 dialogue."),
    (24, "NEW DELHI", "Modi meets the Prince and Princess of Wales."),
    (25, "BENGALURU", "Amazon pledges $7bn for renewables in India by 2030."),
    (26, "SYDNEY", "Duckett's 133 puts England in charge of the third ODI."),
    (27, "AUCKLAND", "New Zealand plays first as GTA VI unlocks at local midnight."),
    (28, "NAIROBI", "Kenya floods kill six as Ruto gives his State of the Nation address."),
    (29, "CARACAS", "Hegseth signs a US-Venezuela military deal."),
    (30, "WASHINGTON", 'Vance: no "forever war" in the Gulf.'),
    (31, "MANAMA", "Bapco refinery back on its feet after the attacks."),
    (32, "RIYADH", "Gulf leaders urge Trump not to strike Iran."),
    (33, "WASHINGTON", "Liu Yunping becomes the first Asian-American House Democratic chair."),
    (34, "SACRAMENTO", "California braces for an atmospheric river; flood advisories out."),
    (35, "LA PAZ", "Bolivia declares an El Ni\u00f1o emergency; 78,000 families hit."),
    (36, "NEW DELHI", "India imposes a 162.5% duty on bulk Scotch imports."),
    (37, "NEW DELHI", "The Supreme Court opens a contempt case over remarks against the Chief Justice."),
    (38, "THIMPHU", "A glacial lake burst floods Bhutan's Gasa hot springs; no injuries reported."),
    (39, "SEOUL", "Seoul breaks with Western allies, declining to join a statement on China's Uyghurs."),
    (40, "SHENZHEN", "Elon Musk travels with Trump to China but takes no part in the three-way talks."),
    (41, "ANTALYA", "India demands equity and delivered climate finance at COP31."),
    (42, "WELLINGTON", "India leave Siraj and Jadeja out of the opening Test against New Zealand."),
    (43, "NEW DELHI", "President Murmu: 50 crore Indians out of extreme poverty."),
    (44, "MUMBAI", "Goldman upgrades India to overweight; Nifty target 28,500."),
    (45, "DELHI", "Delhi-NCR schools resume in-person classes as Stage-III pollution curbs are revoked."),
]

REGIONS = [
    ("ASIA", 16, TEAL), ("N. AMERICA", 9, RED), ("EUROPE", 6, NAVY2),
    ("MIDDLE EAST", 4, GOLD), ("OCEANIA", 4, GREEN), ("AFRICA", 3, PURPLE),
    ("S. AMERICA", 2, (200, 110, 40)), ("GLOBAL", 1, GREY),
]

DATE_CHECK = ("DATE CHECK \u2014 FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS PAGE AS NEWS: "
              "the Iranian drone interceptions over Kuwait and Bahrain \u00b7 the EU's proposed "
              "\u20ac45bn loan for Ukraine \u00b7 the House Democrats' 251-11 vote nominating Hakeem "
              "Jeffries \u00b7 Voyager 1 crossing one light-day from Earth, at 10:16 GMT Wednesday "
              "\u00b7 Peltola's Alaska win \u00b7 Pew's projection that Islam becomes the largest "
              "religion by 2035 \u00b7 the first COP31 draft (Monday).")

FOOTER = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
          "Disputed claims are attributed. Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, "
          "NASA, ICJ, Pew. Original drawings.")

MAP_ROWS = [
    "                                            ",
    "  XXXX   XXXXX          XX  XXXXXXXXXXXXX   ",
    " XXXXXX XXXXXXX   X    XXXX XXXXXXXXXXXXXX  ",
    "  XXXXXXXXXXXXX  XXX    XX   XXXXX  XXXX    ",
    "   XXXXXXXXXXX  XXXXX  XXXX   XXX    X      ",
    "    XXXXXXXXX    XXXXXXXXXX    XX           ",
    "     XXXXXXX      XXXXXXXXXX                ",
    "      XXXXX        XXXXXXXX       X  X      ",
    "      XXXX          XXXXXX                  ",
    "      XXX            XXXX        XX         ",
    "      XX             XXX         XXXX       ",
    "     XXX             XX            XX       ",
    "     XX              X                      ",
    "                                            ",
]

# Pins for cards 1-13: (num, fx, fy) as fractions of the map panel.
PINS = [
    (1, 0.80, 0.30), (2, 0.20, 0.18), (3, 0.14, 0.30), (4, 0.44, 0.14),
    (5, 0.57, 0.30), (6, 0.68, 0.40), (7, 0.54, 0.14), (8, 0.86, 0.42),
    (9, 0.20, 0.38), (10, 0.50, 0.58), (11, 0.42, 0.30), (12, 0.60, 0.44),
    (13, 0.48, 0.44),
]

PIN_LABELS = [
    "1 Shenzhen", "2 New York", "3 Nasdaq / US", "4 The Hague", "5 Antalya",
    "6 Odisha", "7 Kyiv", "8 Shenzhen", "9 Florida", "10 World / science",
    "11 Paris", "12 Jazan", "13 Benghazi",
]

# ---------------------------------------------------------------- drawing
def hero_art(d, idx, x, y, w, h):
    if idx == 0:  # Shenzhen skyline + flags + sun
        d.rectangle([x, y, x + w, y + h], fill=(38, 74, 110))
        d.ellipse([x + w - 62, y + 8, x + w - 26, y + 44], fill=GOLD)
        heights = [26, 40, 32, 48, 36, 44, 28]
        bw = w // len(heights)
        for i, bh in enumerate(heights):
            bx = x + i * bw + 3
            d.rectangle([bx, y + h - bh, bx + bw - 6, y + h], fill=NAVY)
            for wy in range(y + h - bh + 5, y + h - 4, 8):
                d.rectangle([bx + 4, wy, bx + 8, wy + 3], fill=(250, 220, 130))
        for i, (col, lab) in enumerate([((60, 110, 200), "US"),
                                        (RED, "CN"), ((35, 55, 140), "RU")]):
            fx = x + 14 + i * 52
            d.line([fx, y + h - 6, fx, y + 10], fill=(255, 255, 255), width=2)
            d.rectangle([fx + 2, y + 10, fx + 34, y + 26], fill=col)
            d.text((fx + 6, y + 13), lab, font=font("sans_b", 9), fill=(255, 255, 255))
    elif idx == 1:  # GTA VI purple Vice City skyline
        d.rectangle([x, y, x + w, y + h], fill=(58, 26, 96))
        d.ellipse([x + w // 2 - 24, y + 6, x + w // 2 + 24, y + 54], fill=(244, 130, 60))
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 14, 54))
        heights = [20, 34, 26, 42, 30, 38, 22]
        bw = w // len(heights)
        for i, bh in enumerate(heights):
            bx = x + i * bw + 3
            d.rectangle([bx, y + h - 16 - bh, bx + bw - 6, y + h - 16], fill=(22, 10, 42))
            for wy in range(y + h - 16 - bh + 4, y + h - 20, 8):
                d.rectangle([bx + 4, wy, bx + 8, wy + 3], fill=(255, 170, 220))
        tw = d.textlength("OUT TODAY", font=font("sans_b", 13))
        d.rectangle([x + w - tw - 18, y + 6, x + w - 6, y + 26], fill=RED)
        d.text((x + w - tw - 12, y + 9), "OUT TODAY", font=font("sans_b", 13), fill=(255, 255, 255))
    else:  # Anthropic rising chart to $83
        d.rectangle([x, y, x + w, y + h], fill=(224, 242, 228))
        d.line([x + 10, y + h - 10, x + w - 10, y + h - 10], fill=GREY, width=1)
        d.line([x + 10, y + 8, x + 10, y + h - 10], fill=GREY, width=1)
        pts = [(x + 14, y + h - 16), (x + 62, y + h - 22), (x + 110, y + h - 34),
               (x + 158, y + h - 30), (x + 206, y + h - 52), (x + w - 44, y + 16)]
        d.line(pts, fill=GREEN, width=4)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GREEN)
        d.text((x + w - 78, y + 6), "$83", font=font("serif_b", 30), fill=GREEN)
        d.text((x + 12, y + 6), "ANT \u00b7 NASDAQ \u00b7 FIRST TRADE TODAY", font=font("sans_b", 8), fill=NAVY)


MOTIFS = [(193, 39, 45), (23, 116, 118), (200, 110, 40), (86, 44, 140),
          (27, 42, 74), (150, 60, 90), (28, 128, 74), (90, 90, 90),
          (40, 90, 160), (170, 130, 20)]


def secondary_card(d, card, x, y, w, h):
    num, label, head, summ = card
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=RULE, width=1)
    col = MOTIFS[(num - 4) % len(MOTIFS)]
    d.rectangle([x, y, x + w, y + 18], fill=col)
    for i in range(5):
        cx = x + 42 + i * 28
        if i % 2 == 0:
            d.ellipse([cx, y + 5, cx + 8, y + 13], fill=(255, 255, 255))
        else:
            d.polygon([(cx, y + 13), (cx + 4, y + 5), (cx + 8, y + 13)], fill=(255, 255, 255))
    badge(d, x + 5, y + 22, num, r=10, fill=col)
    d.text((x + 30, y + 24), label, font=font("sans_b", 8), fill=col)
    block(d, x + 6, y + 40, head, font("serif_b", 11), INK, w - 12, 12, max_lines=3)
    block(d, x + 6, y + 78, summ, font("sans", 8), GREY, w - 12, 10, max_lines=2)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 16
    RW = W - 2 * M

    # Kicker
    d.rectangle([M, 8, M + RW, 27], fill=NAVY)
    k = "GLOBAL BRIEFING  \u00b7  ONE DAY  \u00b7  ONE PAGE  \u00b7  45 STORIES"
    tw = d.textlength(k, font=font("sans_b", 11))
    d.text((M + (RW - tw) / 2, 12), k, font=font("sans_b", 11), fill=(255, 255, 255))

    # Masthead date
    mast = "Thursday 19 November 2026"
    tw = d.textlength(mast, font=font("serif_b", 40))
    d.text((M + (RW - tw) / 2, 31), mast, font=font("serif_b", 40), fill=NAVY)
    d.line([M, 72, M + RW, 72], fill=NAVY, width=2)

    # Red strap naming the three leads
    strap = "1  SHENZHEN: TRUMP, XI & PUTIN MEET   \u00b7   2  GTA VI IS OUT TODAY   \u00b7   3  ANTHROPIC'S RECORD $81.3BN IPO"
    tw = d.textlength(strap, font=font("sans_b", 11))
    d.text((M + (RW - tw) / 2, 77), strap, font=font("sans_b", 11), fill=RED)

    # Region-count bar (counts honestly from the 45 stories on this page;
    # equal-width labelled segments so every count stays readable)
    y = 94
    cx = M
    seg = RW // len(REGIONS)
    for i, (name, count, col) in enumerate(REGIONS):
        segw = seg if i < len(REGIONS) - 1 else RW - (cx - M)
        d.rectangle([cx, y, cx + segw, y + 17], fill=col)
        label = name + " " + str(count)
        tw = d.textlength(label, font=font("sans_b", 8))
        d.text((cx + (segw - tw) / 2, y + 4), label, font=font("sans_b", 8), fill=(255, 255, 255))
        cx += segw

    # By the numbers strip
    y = 115
    d.rectangle([M, y, M + RW, y + 45], fill=LIGHT, outline=RULE, width=1)
    nw = RW // 6
    for i, (num, cap) in enumerate(NUMBERS):
        nx = M + i * nw + 8
        d.text((nx, y + 4), num, font=font("serif_b", 17), fill=NAVY)
        block(d, nx, y + 25, cap, font("sans", 7), GREY, nw - 14, 9, max_lines=2)
        if i:
            d.line([M + i * nw, y + 5, M + i * nw, y + 38], fill=RULE, width=1)
    d.text((M + 8, y - 0), "", font=font("sans", 7), fill=GREY)

    # Hero cards
    y = 162
    hw = (RW - 16) // 3
    for i, card in enumerate(HEROES):
        num, label, head, summ = card
        x = M + i * (hw + 8)
        d.rectangle([x, y, x + hw, y + 138], fill=PAPER, outline=NAVY, width=2)
        hero_art(d, i, x + 3, y + 3, hw - 6, 54)
        badge(d, x + 7, y + 62, num, r=11, fill=RED)
        d.text((x + 34, y + 65), label, font=font("sans_b", 9), fill=RED)
        yy = block(d, x + 8, y + 84, head, font("serif_b", 14), INK, hw - 16, 15, max_lines=2)
        block(d, x + 8, yy + 2, summ, font("sans", 8), GREY, hw - 16, 10, max_lines=3)

    # Secondary cards: two rows of five
    sw = (RW - 32) // 5
    for row in range(2):
        y = 304 + row * 106
        for col_i in range(5):
            card = SECONDARY[row * 5 + col_i]
            secondary_card(d, card, M + col_i * (sw + 8), y, sw, 102)

    # Bottom section: map panel (left) + briefs (right)
    y = 520
    bh = 314
    mw = 296
    d.rectangle([M, y, M + mw, y + bh], fill=NAVY2)
    d.text((M + 10, y + 7), "WHERE IT HAPPENED", font=font("sans_b", 12), fill=(255, 255, 255))
    map_y = y + 28
    cell = 6
    for r, rowtxt in enumerate(MAP_ROWS):
        for c, ch in enumerate(rowtxt):
            if ch == "X":
                px, py = M + 12 + c * cell, map_y + r * cell
                d.ellipse([px, py, px + 3, py + 3], fill=(170, 200, 230))
    map_w, map_h = 44 * cell, len(MAP_ROWS) * cell
    for num, fx, fy in PINS:
        px, py = M + 12 + fx * map_w, map_y + fy * map_h
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=font("sans_b", 8))
        d.text((px - tw / 2, py - 4), t, font=font("sans_b", 8), fill=(255, 255, 255))
    cap_y = map_y + map_h + 6
    cap_y = block(d, M + 10, cap_y, "NUMBERED = CARDS \u00b7 DOTS = BRIEFS",
                  font("sans_b", 8), GOLD, mw - 20, 10, max_lines=1)
    for i, lab in enumerate(PIN_LABELS):
        d.text((M + 10 + (i % 2) * 146, cap_y + 4 + (i // 2) * 13), lab,
               font=font("sans", 8), fill=(235, 238, 245))
    block(d, M + 10, cap_y + 102,
          "Briefs 14\u201345 run from Gaza and Crimea to Delhi and Wellington. "
          "Every pin and dot is a story first reported on Thursday.",
          font("sans", 8), (190, 205, 225), mw - 20, 11, max_lines=4)

    bx = M + mw + 10
    bw2 = W - M - bx
    d.rectangle([bx, y, W - M, y + bh], fill=PAPER, outline=RULE, width=1)
    d.rectangle([bx, y, W - M, y + 19], fill=NAVY)
    d.text((bx + 8, y + 4), "ALSO ON THURSDAY 19 NOVEMBER \u2014 32 MORE STORIES",
           font=font("sans_b", 10), fill=(255, 255, 255))
    colw = (bw2 - 24) // 2
    for j, (num, place, txt) in enumerate(BRIEFS):
        col_i = 0 if j < 16 else 1
        row_i = j if j < 16 else j - 16
        ex = bx + 8 + col_i * (colw + 8)
        ey = y + 24 + row_i * 18
        head = str(num) + ". " + place + " \u2014 "
        lines = wrap(d, head + txt, font("sans", 8), colw)
        for li, ln in enumerate(lines[:2]):
            d.text((ex, ey + li * 9), ln, font=font("sans", 8), fill=INK)

    # Date check strip
    y = 840
    d.rectangle([M, y, M + RW, y + 64], fill=(255, 255, 255), outline=RED, width=2)
    block(d, M + 10, y + 7, DATE_CHECK, font("sans", 9), INK, RW - 20, 12, max_lines=4)

    # Footer
    y = 910
    d.line([M, y, M + RW, y], fill=NAVY, width=2)
    fy = block(d, M, y + 7, FOOTER, font("sans", 9), GREY, RW, 12, max_lines=2)
    foot2 = "GLOBAL BRIEFING \u00b7 THURSDAY 19 NOVEMBER 2026 \u00b7 45 STORIES \u00b7 PAGE 1 OF 1"
    tw = d.textlength(foot2, font=font("sans_b", 9))
    d.text((M + (RW - tw) / 2, fy + 6), foot2, font=font("sans_b", 9), fill=NAVY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()

