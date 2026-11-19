#!/usr/bin/env python3
"""Compose the front page for Thursday 19 November 2026.

Renders a 1024x1024 newspaper front page from four editorial illustrations
(assets/*.png, generated for this entry, no text inside them) plus story
text drawn here with PIL. Fully deterministic: no network, no clock, no
randomness -- the same inputs always produce the same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
MARGIN = 26
CW = W - 2 * MARGIN  # 972 content width

PAPER = (250, 246, 238)
INK = (18, 18, 18)
GREY = (92, 90, 86)
RULE = (18, 18, 18)
ACCENT = (158, 32, 26)      # deep editorial red
GULF_BG = (26, 28, 34)      # dark slate for the Gulf box
GULF_HEAD = (232, 196, 120)  # warm gold on dark
CAPTION_BG = (236, 231, 220)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cover(img, w, h):
    """Centre-crop img to exactly w x h."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    resized = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return resized.crop((left, top, left + w, top + h))


def draw_text(draw, x, y, text, fnt, fill=INK, anchor="la"):
    draw.text((x, y), text, font=fnt, fill=fill, anchor=anchor)


def draw_para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_brief(draw, x, y, tag, text, f_tag, f_text, max_w, leading=15):
    """One brief: bold red tag inline at the start of the first line."""
    head = tag + " \u2014 "
    head_w = draw.textlength(head, font=f_tag)
    words = text.split()
    lines, cur, first = [], "", True
    for word in words:
        avail = max_w - (head_w if first else 0)
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f_text) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            first = False
    if cur:
        lines.append(cur)
    draw.text((x, y), head, font=f_tag, fill=ACCENT)
    draw.text((x + head_w, y), lines[0], font=f_text, fill=INK)
    for line in lines[1:]:
        y += leading
        draw.text((x, y), line, font=f_text, fill=INK)
    return y + leading


def kicker(draw, x, y, text, fnt):
    draw.text((x, y), text, font=fnt, fill=ACCENT)


# ---------------------------------------------------------------- stories

LEAD = {
    "kick": "SHENZHEN  ·  APEC SUMMIT",
    "head": "Three powers, one table",
    "deck": (
        "Donald Trump, Xi Jinping and Vladimir Putin hold the first trilateral "
        "summit of the United States, China and Russia in Shenzhen. Nuclear "
        "arms, Ukraine, Iran and trade top the agenda \u2014 officials expect "
        "talk, not a deal. A Trump\u2013Xi bilateral on AI chips and rare "
        "earths comes first."
    ),
    "cap": "The flags of the US, China and Russia over the Shenzhen summit hall.",
}

FEATURES = [
    {
        "img": "vicecity.png",
        "kick": "CULTURE  ·  GAMING",
        "head": "Vice City opens its doors",
        "deck": (
            "Grand Theft Auto VI begins its global rollout after a 13-year "
            "wait \u2014 midnight launches rolling time zone by time zone, "
            "with pre-orders past $1.5bn and eight Game Awards nominations "
            "already in hand."
        ),
    },
    {
        "img": "ipo.png",
        "kick": "BUSINESS  ·  AI",
        "head": "Anthropic goes public at $83",
        "deck": (
            "The Claude maker debuts on Nasdaq as ANT today after pricing "
            "above its $70\u2013$78 range \u2014 825m shares in one of "
            "history\u2019s largest IPOs, valuing the firm near $1.4tn."
        ),
    },
]

BERLIN = {
    "kick": "EUROPE  ·  UKRAINE",
    "head": "Allies gather in Berlin",
    "deck": (
        "Leaders of 20-plus nations meet on postwar security guarantees for "
        "Kyiv, with Trump\u2019s envoys Witkoff and Kushner attending."
    ),
}

GULF = [
    "Iran hits a US air base in Kuwait \u2014 its first strike there since September.",
    "Bahrain intercepts Iranian attacks for a third time this week.",
    "US jets struck a missile site on Qeshm Island on Tuesday.",
    "Saudi-led coalition says it downed a Houthi missile aimed at Riyadh.",
]

BRIEFS = [
    ("US HOUSE", "Democrats nominate Hakeem Jeffries, set to be the first Black Speaker."),
    ("PEW REPORT", "Islam on track to be the world\u2019s largest religion by 2035."),
    ("EBOLA", "DRC outbreak tops 11,500 cases and 5,600 deaths; WHO warns it is still expanding."),
    ("CYCLONE AKVAN", "Severe storm nears Andhra coast; landfall due Fri; 200,000 to evacuate in Odisha."),
    ("EU\u2013UKRAINE", "Brussels proposes a \u20ac45bn loan to keep Kyiv funded into 2027."),
    ("VOYAGER 1", "NASA confirms the probe has reached one light-day from Earth."),
    ("FED MINUTES", "Most officials expect further rate rises if inflation stays hot."),
    ("MARKETS", "S&P 500 falls 1.03%; gold drops below $3,800, a first in over a year."),
    ("NVIDIA", "Acting chief Kress promises earlier raises; revenue doubled to $115.8bn."),
    ("CONGRESS", "Liu Yunping is the first Taiwanese American to chair the House Democratic Caucus."),
    ("GAZA", "Heavy rain displaces 46,000 households; 150,000 tents await entry."),
    ("ESTONIA", "Road borders with Russia to close on 1 Dec after an alleged GRU sabotage plot."),
    ("RED SEA", "Houthis seize coastal posts near Bab el-Mandeb as Yemeni forces fall back to Aden."),
    ("KYIV", "Zelensky urges Washington to lift Starshield limits on drone defence."),
    ("SCIENCE", "Earth is missing a billion years of geology. Researchers may have found why."),
    ("INDIA", "Modi meets the Prince and Princess of Wales to boost UK\u2013India ties."),
    ("CANADA", "Carney recalibrates China ties while seeking the \u201cright deal\u201d with the US."),
    ("CYBER", "US senators warn AI-enabled threats are outpacing defences."),
    ("FRANCE", "Justice minister says hard-left leader M\u00e9lenchon could win the presidency."),
    ("SAUDI ARABIA", "All-clear sounded in three southern cities after alerts."),
    ("LIBYA", "Cocaine and millions of pills seized in the east."),
]


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    f_mast = font(SERIF_B, 58)
    f_date = font(SANS_B, 17)
    f_tag = font(SERIF_I, 16)
    f_kick = font(SANS_B, 13)
    f_head_lead = font(SERIF_B, 40)
    f_deck_lead = font(SERIF, 17)
    f_head_feat = font(SERIF_B, 24)
    f_deck_feat = font(SERIF, 15)
    f_head_ber = font(SERIF_B, 22)
    f_deck_ber = font(SERIF, 14)
    f_cap = font(SERIF_I, 12)
    f_gulf_head = font(SANS_B, 14)
    f_gulf = font(SANS, 13)
    f_also = font(SANS_B, 15)
    f_brief_k = font(SANS_B, 12)
    f_brief = font(SERIF, 13)
    f_foot = font(SANS, 11)

    # ---- masthead ------------------------------------------------------
    d.rectangle([MARGIN, 14, W - MARGIN, 16], fill=RULE)
    draw_text(d, W // 2, 20, "THE WORLD TODAY", f_mast, anchor="ma")
    d.rectangle([MARGIN, 82, W - MARGIN, 84], fill=RULE)
    draw_text(d, MARGIN, 88, "THURSDAY  \u00b7  19 NOVEMBER 2026", f_date)
    tag = "One day in the world\u2019s news"
    draw_text(d, W - MARGIN, 88, tag, f_tag, anchor="ra")
    d.rectangle([MARGIN, 112, W - MARGIN, 115], fill=RULE)
    y = 122

    # ---- lead image ----------------------------------------------------
    lead_img = cover(Image.open(os.path.join(ASSETS, "shenzhen.png")), CW, 140)
    page.paste(lead_img, (MARGIN, y))
    y += 148

    # ---- lead story ----------------------------------------------------
    kicker(d, MARGIN, y, LEAD["kick"], f_kick)
    y += 19
    draw_text(d, MARGIN, y, LEAD["head"], f_head_lead)
    y += 46
    y = draw_para(d, MARGIN, y, LEAD["deck"], f_deck_lead, CW, 20)
    y += 6
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 8

    # ---- two features --------------------------------------------------
    col_w = (CW - 24) // 2
    img_h = 110
    feat_top = y
    feat_bottom = feat_top
    for i, feat in enumerate(FEATURES):
        x = MARGIN + i * (col_w + 24)
        img = cover(Image.open(os.path.join(ASSETS, feat["img"])), col_w, img_h)
        page.paste(img, (x, feat_top))
        fy = feat_top + img_h + 7
        kicker(d, x, fy, feat["kick"], f_kick)
        fy += 18
        fy = draw_para(d, x, fy, feat["head"], f_head_feat, col_w, 26, max_lines=2)
        fy += 1
        fy = draw_para(d, x, fy, feat["deck"], f_deck_feat, col_w, 18, max_lines=4)
        feat_bottom = max(feat_bottom, fy)
    y = feat_bottom + 6
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 8

    # ---- Berlin + Gulf box ---------------------------------------------
    row_top = y
    row_h = 96
    thumb_w, thumb_h = 150, row_h
    berlin_img = cover(Image.open(os.path.join(ASSETS, "berlin.png")), thumb_w, thumb_h)
    page.paste(berlin_img, (MARGIN, row_top))
    bx = MARGIN + thumb_w + 12
    bw = 494 - thumb_w - 12
    kicker(d, bx, row_top, BERLIN["kick"], f_kick)
    by = row_top + 18
    by = draw_para(d, bx, by, BERLIN["head"], f_head_ber, bw, 25, max_lines=1)
    by += 1
    draw_para(d, bx, by, BERLIN["deck"], f_deck_ber, bw, 17, max_lines=4)

    gx = MARGIN + 494
    gw = CW - 494
    d.rectangle([gx, row_top, gx + gw, row_top + row_h], fill=GULF_BG)
    draw_text(d, gx + 12, row_top + 6, "THE GULF, ON EDGE", f_gulf_head, fill=GULF_HEAD)
    gy = row_top + 27
    for item in GULF:
        lines = wrap(d, "\u25aa  " + item, f_gulf, gw - 24)
        for line in lines:
            draw_text(d, gx + 12, gy, line, f_gulf, fill=(232, 230, 224))
            gy += 15
        gy += 1
    y = row_top + row_h + 8
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 6

    # ---- Also today ----------------------------------------------------
    draw_text(d, MARGIN, y, "ALSO TODAY", f_also)
    d.line([MARGIN + 108, y + 8, W - MARGIN, y + 8], fill=GREY, width=1)
    y += 22

    ncol = 3
    gap = 18
    bcol_w = (CW - gap * (ncol - 1)) // 3
    per_col = (len(BRIEFS) + ncol - 1) // ncol
    brief_bottom = y
    for ci in range(ncol):
        x = MARGIN + ci * (bcol_w + gap)
        by2 = y
        for tag, text in BRIEFS[ci * per_col:(ci + 1) * per_col]:
            by2 = draw_brief(d, x, by2, tag, text, f_brief_k, f_brief, bcol_w)
            by2 += 4
        brief_bottom = max(brief_bottom, by2)
    print("briefs end at y =", brief_bottom, "(footer rule at", H - 30, ")")

    # ---- footer --------------------------------------------------------
    d.rectangle([MARGIN, H - 30, W - MARGIN, H - 28], fill=RULE)
    draw_text(
        d, MARGIN, H - 24,
        "Every story above was reported on Thursday 19 November 2026. "
        "Sources include AP, Reuters, AFP, BBC, IMD, WHO and Pew Research.",
        f_foot, fill=GREY,
    )

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
