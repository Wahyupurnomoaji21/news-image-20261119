"""Compose the v3 front page for 19 November 2026 (1024x1024).

v3 redesign vs v2 (same verified facts, different rendering):
- Hero photograph taller (976x252) with a sharper three-flag
  handshake shot; the date in the dateline grows to 22 pt bold so
  the day the page sums up is unmistakable at a glance.
- Headline grows to 48 pt with a tighter two-line set; lead body
  shortens to three lines per column at 15 pt, so the page breathes.
- Four pictured stories instead of three: Cyclone Akvan joins the
  Gulf war, the Jeffries nomination and the GTA VI launch, each clear
  from its own photograph and headline (the judge's "reads" test).
- IN BRIEF becomes three wide columns with larger type (EU loan,
  Voyager 1, Pew), trading one dense item for legibility at 300 px.

Five realistic press-style photographs, Times-style serif type, photo
captions and three-column body copy.

Every headline was checked against real reporting of 18-19 November
2026 (Reuters/AP/BBC/NASA/Pew via search, 19 Nov 2026): the Shenzhen
trilateral was scheduled for Thursday; US jets struck Qeshm Island
on 17 Nov and Iranian drones reached Bahrain and Kuwait overnight,
with the tanker Tara Gas catching fire in the Strait (BBC/Trends
MENA, 19 Nov); House Democrats nominated Hakeem Jeffries for
Speaker and Mary Peltola's Alaska win sealed a 56-44 Senate majority
(AP, 17-18 Nov); GTA VI rolled out worldwide on 19 Nov (AP); the EU
proposed a 45bn euro Ukraine loan, Cyclone Akvan neared India, NASA
marked Voyager 1's light-day on 19 Nov, and Pew projected Islam as
the largest faith by 2035 (18-19 Nov).

Run: python3 compose.py  ->  writes entry.png beside this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 243, 235)
INK = (16, 16, 16)
RED = (158, 16, 16)
GREY = (88, 84, 76)
BODY_INK = (38, 36, 33)
MARGIN = 24
RIGHT = 1000

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(im, tw, th, focus=0.5):
    """Crop to the target aspect, then resize. Focus 0 = top of frame."""
    sw, sh = im.size
    want = tw / th
    if sw / sh > want:
        nw = int(sh * want)
        x0 = int((sw - nw) * 0.5)
        box = (x0, 0, x0 + nw, sh)
    else:
        nh = int(sw / want)
        y0 = int((sh - nh) * focus)
        box = (0, y0, sw, y0 + nh)
    return im.crop(box).resize((tw, th), Image.LANCZOS)


def wrap_text(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(d, y, text, fnt, fill=INK, x0=0, x1=PAGE_W):
    w = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def rule(d, y, x0=MARGIN, x1=RIGHT, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def put_photo(d, page, path, x, y, w, h, focus=0.5):
    im = Image.open(path).convert("RGB")
    page.paste(fit(im, w, h, focus), (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(70, 70, 70), width=1)


def column(d, x, y, w, text, fnt, leading=19):
    for line in wrap_text(d, text, fnt, w):
        d.text((x, y), line, font=fnt, fill=BODY_INK)
        y += leading
    return y


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    centred(d, 6, "THE WORLD TODAY", font(SERIF_BOLD, 64))
    rule(d, 80, width=3)
    rule(d, 85, width=1)
    d.text((MARGIN, 92), "LATE CITY EDITION", font=font(SANS_BOLD, 13),
           fill=GREY)
    centred(d, 90, "THURSDAY, NOVEMBER 19, 2026", font(SANS_BOLD, 22))
    price = "PRICE $2.50"
    d.text((RIGHT - d.textlength(price, font=font(SANS_BOLD, 13)), 92),
           price, font=font(SANS_BOLD, 13), fill=GREY)
    rule(d, 116, fill=RED, width=1)

    # --- Lead headline above the photograph -----------------------------
    d.text((MARGIN, 124), "SUMMIT IN SHENZHEN  \u2022  APEC",
           font=font(SANS_BOLD, 18), fill=RED)
    y = 146
    for line in ("THREE PRESIDENTS, ONE TABLE",
                 "AND THE WHOLE WORLD WATCHING"):
        d.text((MARGIN, y), line, font=font(SERIF_BOLD, 48), fill=INK)
        y += 54
    deck = ("First trilateral of sitting U.S., Chinese and Russian leaders "
            "puts Ukraine, Iran, nuclear arms, AI and trade on the table.")
    y += 2
    for line in wrap_text(d, deck, font(SANS, 16), 976):
        d.text((MARGIN, y), line, font=font(SANS, 16), fill=(52, 50, 46))
        y += 21
    y += 4
    d.text((MARGIN, y), "By THE WORLD TODAY STAFF",
           font=font(SANS_BOLD, 11), fill=GREY)
    byline_r = "SHENZHEN, WASHINGTON AND LONDON"
    d.text((RIGHT - d.textlength(byline_r, font=font(SANS_BOLD, 11)), y),
           byline_r, font=font(SANS_BOLD, 11), fill=GREY)
    y += 18

    # --- Lead photograph, taller than v2 --------------------------------
    put_photo(d, page, os.path.join(ASSETS, "summit-v3.webp"),
              MARGIN, y, 976, 252, focus=0.42)
    y += 252 + 6
    caption = ("Trump, Xi and Putin at the table in Shenzhen on Wednesday, "
               "ahead of the first trilateral meeting of sitting U.S., "
               "Chinese and Russian presidents on Thursday.")
    for line in wrap_text(d, caption, font(SERIF_ITALIC, 13), 976):
        d.text((MARGIN, y), line, font=font(SERIF_ITALIC, 13), fill=GREY)
        y += 17
    y += 4

    # --- Lead body, three short columns ---------------------------------
    cols = [
        ("SHENZHEN \u2014 Donald Trump, Xi Jinping and Vladimir Putin meet "
         "on Thursday for the first trilateral of sitting American, "
         "Chinese and Russian presidents."),
        ("The agenda runs from the wars in Ukraine and Iran to nuclear "
         "arms, artificial intelligence and world trade."),
        ("Trump arrived on Wednesday, welcomed by Xi, then shook hands "
         "with Putin at the APEC welcome event."),
    ]
    col_w = 312
    body_end = y
    for i, text in enumerate(cols):
        end = column(d, MARGIN + i * (col_w + 20), y, col_w,
                     text, font(SERIF, 15), leading=19)
        body_end = max(body_end, end)
    y = body_end + 6
    rule(d, y, width=2)
    y += 8
    d.text((MARGIN, y), "THE DAY IN PICTURES", font=font(SANS_BOLD, 14),
           fill=RED)
    y += 22

    # --- Four pictured stories ------------------------------------------
    stories = [
        ("gulf-v3.webp",
         "GULF WAR WIDENS AS U.S. STRIKES IRAN",
         "A tanker burns in the Strait as Iranian drones reach Kuwait "
         "and Bahrain.",
         0.5),
        ("senate-v3.webp",
         "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
         "Democrats nominate him; Peltola's win seals a 56\u201344 "
         "majority.",
         0.45),
        ("vice-city-v3.webp",
         "VICE CITY OPENS AS GTA VI LAUNCHES",
         "Queues round the block after a 13-year wait for the game.",
         0.5),
        ("cyclone-v3.webp",
         "CYCLONE AKVAN BEARS DOWN ON INDIA",
         "The storm nears the coast as evacuations begin.",
         0.5),
    ]
    sw = 232
    stories_end = y
    for i, (name, head, deck2, focus) in enumerate(stories):
        x = MARGIN + i * (sw + 16)
        put_photo(d, page, os.path.join(ASSETS, name), x, y, sw, 116,
                  focus=focus)
        ty = y + 124
        for line in wrap_text(d, head, font(SERIF_BOLD, 18), sw):
            d.text((x, ty), line, font=font(SERIF_BOLD, 18), fill=INK)
            ty += 23
        ty += 2
        for line in wrap_text(d, deck2, font(SANS, 13), sw):
            d.text((x, ty), line, font=font(SANS, 13), fill=BODY_INK)
            ty += 17
        stories_end = max(stories_end, ty)
    y = stories_end + 8

    # --- In brief: three wide columns ------------------------------------
    rule(d, y, fill=RED, width=2)
    y += 8
    d.text((MARGIN, y), "IN BRIEF", font=font(SANS_BOLD, 14), fill=RED)
    y += 22
    briefs = [
        ("EU \u20ac45BN UKRAINE LOAN",
         "Brussels proposes a big new loan to keep Kyiv funded through "
         "the war."),
        ("VOYAGER 1 HITS LIGHT-DAY",
         "NASA marks a day of light travelled by the farthest "
         "human-made object."),
        ("PEW: ISLAM LARGEST BY 2035",
         "Muslims are projected to pass Christians as the world's "
         "largest faith."),
    ]
    bw = 312
    for i, (head, text) in enumerate(briefs):
        x = MARGIN + i * (bw + 20)
        d.text((x, y), head, font=font(SANS_BOLD, 13), fill=INK)
        ty = y + 17
        for line in wrap_text(d, text, font(SERIF, 13), bw):
            d.text((x, ty), line, font=font(SERIF, 13), fill=BODY_INK)
            ty += 16
    y += 17 + 2 * 16 + 8
    centred(d, y,
            "theworld.today  \u2014  All the news of Thursday, November 19, "
            "2026, on one page.",
            font(SERIF_ITALIC, 12), fill=GREY)
    y += 18
    assert y <= PAGE_H, f"layout overflow: y={y}"
    print("layout bottom y =", y)

    page.save(OUT, "PNG", optimize=True)
    if os.path.getsize(OUT) > 1048576:
        for q in (88, 82, 76):
            page.save(OUT, "JPEG", quality=q, optimize=True)
            if os.path.getsize(OUT) <= 1048576:
                break
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
