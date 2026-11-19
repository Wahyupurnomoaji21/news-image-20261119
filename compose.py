"""Compose the front page for 19 November 2026 (1024x1024).

Design: a real broadsheet front page. Times-style serif masthead with a
thick/thin double rule, a dominant lead photograph with a photo caption,
a two-column lead story, three pictured stories below, and an "also
today" strip. All four photographs are realistic press-style images;
headlines and body copy are drawn with PIL in Liberation Serif /
Liberation Sans so the type looks like newsprint.

Every headline was checked against real reporting of 19 November 2026:
the Shenzhen trilateral was scheduled for Thursday (Reuters, 18 Nov);
US jets struck Qeshm Island on 17 Nov and Iranian drones reached
Bahrain and Kuwait overnight, with the tanker Tara Gas catching fire
in the Strait (BBC/Trends MENA, 19 Nov); House Democrats nominated
Hakeem Jeffries for Speaker and Mary Peltola's Alaska win sealed a
56-44 Senate majority (AP, 17-18 Nov); GTA VI rolled out worldwide
on 19 Nov (AP); the EU proposed a 45bn euro Ukraine loan, Cyclone
Akvan neared India, NASA marked Voyager 1's light-day on 19 Nov, and
Pew projected Islam as the largest faith by 2035 (18-19 Nov).

Run: python3 compose.py  ->  writes entry.png beside this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

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


def centred_fit(d, y, text, path, size, x0=MARGIN, x1=RIGHT, fill=INK):
    """Centre text between x0 and x1, shrinking the font until it fits."""
    while size > 9:
        fnt = font(path, size)
        if d.textlength(text, font=fnt) <= x1 - x0:
            break
        size -= 1
    centred(d, y, text, fnt, fill=fill, x0=x0, x1=x1)


def rule(d, y, x0=MARGIN, x1=RIGHT, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def put_photo(d, page, path, x, y, w, h, focus=0.5):
    im = Image.open(path).convert("RGB")
    page.paste(fit(im, w, h, focus), (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(70, 70, 70), width=1)


def column(d, x, y, w, text, fnt, leading=18):
    for line in wrap_text(d, text, fnt, w):
        d.text((x, y), line, font=fnt, fill=BODY_INK)
        y += leading
    return y


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # --- Masthead -------------------------------------------------------
    centred(d, 8, "THE WORLD TODAY", font(SERIF_BOLD, 66))
    rule(d, 88, width=3)
    rule(d, 93, width=1)
    d.text((MARGIN, 100), "LATE CITY EDITION", font=font(SANS_BOLD, 13),
           fill=GREY)
    centred(d, 100, "THURSDAY, NOVEMBER 19, 2026", font(SANS_BOLD, 20))
    price = "PRICE $2.50"
    d.text((RIGHT - d.textlength(price, font=font(SANS_BOLD, 13)), 100),
           price, font=font(SANS_BOLD, 13), fill=GREY)
    rule(d, 126, width=1)

    # --- Lead photograph ------------------------------------------------
    put_photo(d, page, os.path.join(ASSETS, "summit.webp"),
              MARGIN, 136, 976, 250)
    caption = ("Trump, Xi and Putin in Shenzhen on Wednesday, before the "
               "first trilateral meeting of sitting U.S., Chinese and "
               "Russian presidents on Thursday.")
    d.text((MARGIN, 392), caption, font=font(SERIF_ITALIC, 14), fill=GREY)

    # --- Lead story -----------------------------------------------------
    d.text((MARGIN, 416), "SUMMIT IN SHENZHEN  \u2022  APEC",
           font=font(SANS_BOLD, 18), fill=RED)
    y = 440
    for line in ("THREE PRESIDENTS, ONE TABLE",
                 "AS TRUMP, XI AND PUTIN MEET"):
        d.text((MARGIN, y), line, font=font(SERIF_BOLD, 40), fill=INK)
        y += 46
    deck = ("First trilateral of sitting U.S., Chinese and Russian leaders "
            "puts Ukraine, Iran, nuclear arms, AI and trade on the table.")
    y += 4
    for line in wrap_text(d, deck, font(SANS, 17), 976):
        d.text((MARGIN, y), line, font=font(SANS, 17), fill=(52, 50, 46))
        y += 23
    y += 6
    col_w = 478
    left = ("SHENZHEN \u2014 Donald Trump, Xi Jinping and Vladimir Putin "
            "meet on Thursday for the first trilateral meeting of sitting "
            "American, Chinese and Russian presidents, a summit years in "
            "the making that puts the wars in Ukraine and Iran, nuclear "
            "arms, AI and world trade on one table.")
    right = ("Trump arrived in Shenzhen on Wednesday, welcomed at the "
             "airport by Xi, then shook hands with Putin at the APEC "
             "welcome event \u2014 their first meeting in more than a "
             "year. No agreement was expected, but the world watched what "
             "three presidents could say to each other.")
    column(d, MARGIN, y, col_w, left, font(SERIF, 14), leading=18)
    column(d, 522, y, col_w, right, font(SERIF, 14), leading=18)
    y += 5 * 18 + 8
    rule(d, y, width=2)

    # --- Three pictured stories ----------------------------------------
    y += 12
    stories = [
        ("gulf-war.webp",
         "GULF WAR WIDENS AS U.S. STRIKES IRAN",
         "A tanker burns in the Strait as Iranian drones reach Kuwait "
         "and Bahrain.",
         0.45),
        ("senate.webp",
         "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
         "House Democrats nominate him; Peltola's Alaska win seals a "
         "56\u201344 Senate majority.",
         0.5),
        ("vice-city.webp",
         "GAMERS ENTER VICE CITY AS GTA VI LAUNCHES",
         "Queues round the block after a 13-year wait for the game.",
         0.5),
    ]
    for i, (name, head, deck2, focus) in enumerate(stories):
        x = MARGIN + i * 334
        put_photo(d, page, os.path.join(ASSETS, name), x, y, 308, 168,
                  focus=focus)
        ty = y + 178
        for line in wrap_text(d, head, font(SERIF_BOLD, 19), 308):
            d.text((x, ty), line, font=font(SERIF_BOLD, 19), fill=INK)
            ty += 24
        ty += 2
        for line in wrap_text(d, deck2, font(SANS, 13), 308):
            d.text((x, ty), line, font=font(SANS, 13), fill=BODY_INK)
            ty += 17
    bottom = y + 178 + 3 * 24 + 2 + 2 * 17

    # --- Also today ------------------------------------------------------
    rule(d, bottom + 6, fill=RED, width=2)
    centred_fit(d, bottom + 14,
                "ALSO TODAY:  EU \u20ac45BN UKRAINE LOAN  \u2022  CYCLONE "
                "AKVAN NEARS INDIA  \u2022  VOYAGER 1 HITS LIGHT-DAY  "
                "\u2022  PEW: ISLAM LARGEST FAITH BY 2035",
                SANS_BOLD, 14)
    centred(d, bottom + 38,
            "theworld.today  \u2014  All the news of Thursday, November 19, "
            "2026, on one page.",
            font(SERIF_ITALIC, 13), fill=GREY)

    page.save(OUT, "PNG", optimize=True)
    if os.path.getsize(OUT) > 1048576:
        for q in (88, 82, 76):
            page.save(OUT, "JPEG", quality=q, optimize=True)
            if os.path.getsize(OUT) <= 1048576:
                break
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
