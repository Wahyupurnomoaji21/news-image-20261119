"""Compose the front page for 19 November 2026 (1024x1024).

Design: a real broadsheet front page, not a poster. Times-style serif
masthead with a thick/thin double rule, a dominant lead photograph with a
photo caption, a two-column lead story with body copy, three pictured
stories below, and an "also today" strip. All four photographs are
realistic press-style images; headlines and body copy are drawn with PIL
in Liberation Serif / Liberation Sans so the type looks like newsprint.

Run: python3 compose.py  ->  writes entry.png beside this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 235)
INK = (16, 16, 16)
RED = (158, 16, 16)
GREY = (88, 84, 76)
BODY = (38, 36, 33)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def cover(im, tw, th, focus=0.5):
    """Crop to the target aspect, then resize. Focus 0 = top of the frame."""
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


def wrap(d, text, fnt, max_w):
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


def centre(d, y, text, fnt, fill=INK, x0=0, x1=W):
    w = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def hline(d, y, x0=24, x1=1000, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def photo(d, page, path, x, y, w, h, focus=0.5, bright=1.0):
    im = Image.open(path).convert("RGB")
    if bright != 1.0:
        im = ImageEnhance.Brightness(im).enhance(bright)
    page.paste(cover(im, w, h, focus), (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(70, 70, 70), width=1)


def body_col(d, x, y, w, text, fnt, leading=17):
    for line in wrap(d, text, fnt, w):
        d.text((x, y), line, font=fnt, fill=BODY)
        y += leading
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    centre(d, 8, "THE WORLD TODAY", F(SERIF_BOLD, 66))
    hline(d, 88, width=3)
    hline(d, 93, width=1)
    d.text((24, 100), "LATE CITY EDITION", font=F(SANS_BOLD, 13), fill=GREY)
    centre(d, 100, "THURSDAY, NOVEMBER 19, 2026", F(SANS_BOLD, 20))
    right = "PRICE $2.50"
    d.text((1000 - d.textlength(right, font=F(SANS_BOLD, 13)), 100),
           right, font=F(SANS_BOLD, 13), fill=GREY)
    hline(d, 126, width=1)

    # --- Lead photograph ------------------------------------------------
    photo(d, page, os.path.join(ASSETS, "summit.webp"), 24, 136, 976, 250)
    caption = ("Trump, Xi and Putin shake hands in Shenzhen on Thursday, ahead of "
               "the first trilateral meeting of sitting U.S., Chinese and Russian "
               "presidents.")
    d.text((24, 392), caption, font=F(SERIF_ITALIC, 14), fill=GREY)

    # --- Lead story -----------------------------------------------------
    d.text((24, 416), "SUMMIT IN SHENZHEN  \u2022  APEC",
           font=F(SANS_BOLD, 18), fill=RED)
    y = 440
    for line in ("THREE PRESIDENTS, ONE TABLE",
                 "AS TRUMP, XI AND PUTIN MEET"):
        d.text((24, y), line, font=F(SERIF_BOLD, 40), fill=INK)
        y += 46
    deck = ("First trilateral of sitting U.S., Chinese and Russian leaders "
            "puts Ukraine, Iran, nuclear arms and trade on the table.")
    y += 4
    for line in wrap(d, deck, F(SANS, 17), 976):
        d.text((24, y), line, font=F(SANS, 17), fill=(52, 50, 46))
        y += 23
    y += 6
    col_w = 478
    left = ("SHENZHEN \u2014 Donald Trump, Xi Jinping and Vladimir Putin sat "
            "down together on Thursday for the first trilateral meeting of "
            "sitting American, Chinese and Russian presidents, a summit years "
            "in the making that puts the wars in Ukraine and Iran, nuclear "
            "arms and world trade on one table.")
    right = ("Trump arrived in Shenzhen on Wednesday to a red-carpet airport "
             "greeting from Xi, then shook hands with Putin before the APEC "
             "welcome banquet \u2014 their first meeting since Alaska in "
             "August 2025. No agreement was expected, but the world watched "
             "what three presidents could say to each other.")
    body_col(d, 24, y, col_w, left, F(SERIF, 14), leading=18)
    body_col(d, 522, y, col_w, right, F(SERIF, 14), leading=18)
    y += 5 * 18 + 8
    hline(d, y, width=2)

    # --- Three pictured stories ----------------------------------------
    y += 12
    stories = [
        ("gulf-war.webp",
         "GULF WAR WIDENS AS U.S. STRIKES IRAN",
         "A tanker burns as the war at sea spreads beyond the Gulf.",
         0.45, 1.0),
        ("senate.webp",
         "DEMOCRATS TAKE THE SENATE",
         "Peltola win in Alaska seals a 56\u201344 majority; Jeffries set to be first Black Speaker.",
         0.5, 1.0),
        ("vice-city.webp",
         "GAMERS ENTER VICE CITY AS GTA VI LAUNCHES",
         "Queues round the block after a 13-year wait for the game.",
         0.5, 1.0),
    ]
    for i, (name, head, deck2, focus, bright) in enumerate(stories):
        x = 24 + i * 334
        photo(d, page, os.path.join(ASSETS, name), x, y, 308, 168,
              focus=focus, bright=bright)
        ty = y + 178
        for line in wrap(d, head, F(SERIF_BOLD, 19), 308):
            d.text((x, ty), line, font=F(SERIF_BOLD, 19), fill=INK)
            ty += 24
        ty += 2
        for line in wrap(d, deck2, F(SANS, 13), 308):
            d.text((x, ty), line, font=F(SANS, 13), fill=BODY)
            ty += 17
    bottom = y + 178 + 3 * 24 + 2 + 2 * 17

    # --- Also today ------------------------------------------------------
    hline(d, bottom + 6, fill=RED, width=2)
    centre(d, bottom + 14,
           "ALSO TODAY:  EU \u20ac45BN UKRAINE LOAN  \u2022  CYCLONE AKVAN NEARS INDIA  \u2022  "
           "VOYAGER 1 HITS LIGHT-DAY  \u2022  NVIDIA: NO HUANG RETURN",
           F(SANS_BOLD, 14))
    centre(d, bottom + 38,
           "theworld.today  \u2014  All the news of Thursday, November 19, 2026, on one page.",
           F(SERIF_ITALIC, 13), fill=GREY)

    page.save(OUT, "PNG", optimize=True)
    if os.path.getsize(OUT) > 1048576:
        for q in (88, 82, 76):
            page.save(OUT, "JPEG", quality=q, optimize=True)
            if os.path.getsize(OUT) <= 1048576:
                break
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
