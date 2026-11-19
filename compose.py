#!/usr/bin/env python3
"""Compose the v3 front page for news-image-20261119 as entry.png.

Page: 1024x1024 broadsheet front page, "THE WORLD TODAY", dated
Thursday, November 19, 2026. All photos are local files under assets/,
rendered with Pillow only; no network access is used anywhere.
Run:  python3 compose.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 24
RIGHT = 1000
CONTENT_W = RIGHT - MARGIN  # 976

PAPER = (247, 243, 235)
INK = (16, 16, 16)
RED = (158, 16, 16)
GREY = (88, 84, 76)
BODY = (38, 36, 33)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF_ITALIC = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_centred(draw, y, text, fnt, fill, centre_x=512):
    """Draw text centred on centre_x with its top at y; returns its width."""
    width = draw.textlength(text, font=fnt)
    draw.text((centre_x - width / 2, y), text, font=fnt, fill=fill)
    return width


def hrule(draw, y, thickness, fill, x0=MARGIN, x1=RIGHT):
    """Draw a horizontal rule of the given thickness starting at y."""
    draw.rectangle([x0, y, x1, y + thickness - 1], fill=fill)
    return y + thickness


def paste_photo(img, path, x, y, w, h, focus_y=0.42):
    """Centre-crop a photo to w:h (focus_y = vertical focus, 0..1),
    resize with LANCZOS, paste it, and draw a thin dark border."""
    photo = Image.open(path).convert("RGB")
    sw, sh = photo.size
    target = w / h
    src = sw / sh
    if src > target:
        # Too wide: crop the sides, keep the full height.
        crop_w = int(sh * target)
        left = (sw - crop_w) // 2
        box = (left, 0, left + crop_w, sh)
    else:
        # Too tall: crop top/bottom around the focus point.
        crop_h = int(sw / target)
        centre = int(sh * focus_y)
        top = max(0, min(sh - crop_h, centre - crop_h // 2))
        box = (0, top, sw, top + crop_h)
    photo = photo.crop(box).resize((w, h), Image.LANCZOS)
    img.paste(photo, (x, y))
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)
    return y + h


def draw_column(draw, x, y, text, fnt, width, leading):
    """Draw wrapped body text in a column; returns the y it ends at."""
    lines = wrap_text(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=BODY)
        y += leading
    return y


def main():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 8

    # --- Masthead ---
    mast = font(SERIF_BOLD, 64)
    draw_centred(draw, y, "THE WORLD TODAY", mast, INK)
    y += 72
    y = hrule(draw, y, 3, INK)
    y += 3
    y = hrule(draw, y, 1, INK)
    y += 6

    # --- Dateline row ---
    date_font = font(SANS_BOLD, 22)
    side_font = font(SANS_BOLD, 13)
    draw.text((MARGIN, y + 5), "LATE CITY EDITION", font=side_font, fill=GREY)
    draw_centred(draw, y, "THURSDAY, NOVEMBER 19, 2026", date_font, INK)
    price = "PRICE $2.50"
    draw.text((RIGHT - draw.textlength(price, font=side_font), y + 5),
              price, font=side_font, fill=GREY)
    y += 30
    y = hrule(draw, y, 1, RED)
    y += 8

    # --- Kicker + headline + deck + byline ---
    draw.text((MARGIN, y), "SUMMIT IN SHENZHEN  \u2022  APEC",
              font=font(SANS_BOLD, 18), fill=RED)
    y += 26
    head_font = font(SERIF_BOLD, 48)
    draw.text((MARGIN, y), "THREE PRESIDENTS, ONE TABLE",
              font=head_font, fill=INK)
    y += 54
    draw.text((MARGIN, y), "AND THE WHOLE WORLD WATCHING",
              font=head_font, fill=INK)
    y += 56
    deck_font = font(SANS, 16)
    deck = ("First trilateral of sitting U.S., Chinese and Russian leaders "
            "puts Ukraine, Iran, nuclear arms, AI and trade on the table.")
    for line in wrap_text(draw, deck, deck_font, CONTENT_W):
        draw.text((MARGIN, y), line, font=deck_font, fill=BODY)
        y += 20
    y += 2
    by_font = font(SANS_BOLD, 11)
    draw.text((MARGIN, y), "By THE WORLD TODAY STAFF",
              font=by_font, fill=GREY)
    right_by = "SHENZHEN, WASHINGTON AND LONDON"
    draw.text((RIGHT - draw.textlength(right_by, font=by_font), y),
              right_by, font=by_font, fill=GREY)
    y += 16

    # --- Hero photo + caption ---
    y = paste_photo(img, os.path.join(ASSETS, "summit-v3.webp"),
                    MARGIN, y, CONTENT_W, 252, focus_y=0.42)
    draw = ImageDraw.Draw(img)
    y += 6
    cap_font = font(SERIF_ITALIC, 13)
    caption = ("Trump, Xi and Putin at the table in Shenzhen on Wednesday, "
               "ahead of the first trilateral meeting of sitting U.S., "
               "Chinese and Russian presidents on Thursday.")
    for line in wrap_text(draw, caption, cap_font, CONTENT_W):
        draw.text((MARGIN, y), line, font=cap_font, fill=GREY)
        y += 17
    y += 4

    # --- Lead body: three columns ---
    lead_font = font(SERIF, 15)
    col_w, gutter = 312, 20
    lead_texts = [
        ("SHENZHEN \u2014 Donald Trump, Xi Jinping and Vladimir Putin meet "
         "on Thursday for the first trilateral of sitting American, "
         "Chinese and Russian presidents."),
        ("The agenda runs from the wars in Ukraine and Iran to nuclear "
         "arms, artificial intelligence and world trade."),
        ("Trump arrived on Wednesday, welcomed by Xi, then shook hands "
         "with Putin at the APEC welcome event."),
    ]
    end_y = y
    for i, text in enumerate(lead_texts):
        x = MARGIN + i * (col_w + gutter)
        end_y = max(end_y, draw_column(draw, x, y, text, lead_font,
                                       col_w, 19))
    y = end_y + 6

    # --- The Day in Pictures ---
    y = hrule(draw, y, 2, INK)
    y += 6
    label_font = font(SANS_BOLD, 14)
    draw.text((MARGIN, y), "THE DAY IN PICTURES", font=label_font, fill=RED)
    y += 22
    stories = [
        ("gulf-v3.webp", "GULF WAR WIDENS AS U.S. STRIKES IRAN",
         "A tanker burns in the Strait as Iranian drones reach Kuwait "
         "and Bahrain."),
        ("senate-v3.webp", "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
         "Democrats nominate him; Peltola's win seals a 56\u201344 majority."),
        ("vice-city-v3.webp", "VICE CITY OPENS AS GTA VI LAUNCHES",
         "Queues round the block after a 13-year wait for the game."),
        ("cyclone-v3.webp", "CYCLONE AKVAN BEARS DOWN ON INDIA",
         "The storm nears the coast as evacuations begin."),
    ]
    story_w, story_gutter = 232, 16
    story_head = font(SERIF_BOLD, 18)
    story_deck = font(SANS, 13)
    block_end = y
    for i, (photo_name, headline, deck_text) in enumerate(stories):
        x = MARGIN + i * (story_w + story_gutter)
        sy = paste_photo(img, os.path.join(ASSETS, photo_name),
                         x, y, story_w, 116, focus_y=0.45)
        draw = ImageDraw.Draw(img)
        sy += 6
        for line in wrap_text(draw, headline, story_head, story_w):
            draw.text((x, sy), line, font=story_head, fill=INK)
            sy += 22
        sy += 2
        deck_lines = wrap_text(draw, deck_text, story_deck, story_w)[:2]
        for line in deck_lines:
            draw.text((x, sy), line, font=story_deck, fill=BODY)
            sy += 17
        block_end = max(block_end, sy)
    y = block_end + 4

    # --- In Brief ---
    y = hrule(draw, y, 2, RED)
    y += 6
    draw.text((MARGIN, y), "IN BRIEF", font=label_font, fill=RED)
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
    brief_head = font(SANS_BOLD, 13)
    brief_body = font(SERIF, 13)
    brief_end = y
    for i, (headline, body_text) in enumerate(briefs):
        x = MARGIN + i * (col_w + gutter)
        by = y
        draw.text((x, by), headline, font=brief_head, fill=INK)
        by += 17
        for line in wrap_text(draw, body_text, brief_body, col_w)[:2]:
            draw.text((x, by), line, font=brief_body, fill=BODY)
            by += 17
        brief_end = max(brief_end, by)
    y = brief_end + 6

    # --- Footer ---
    foot_font = font(SERIF_ITALIC, 12)
    draw_centred(draw, y,
                 "theworld.today  \u2014  All the news of Thursday, "
                 "November 19, 2026, on one page.",
                 foot_font, GREY)
    y += 18

    assert y <= PAGE_H, f"layout overflow: bottom y={y} > {PAGE_H}"
    print(f"layout bottom y={y} (page height {PAGE_H})")

    # Save PNG optimised; fall back to JPEG qualities if over 1 MiB.
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    if size > 1_048_576:
        for quality in (88, 82, 76):
            img.convert("RGB").save(OUT, format="JPEG", quality=quality,
                                    optimize=True)
            size = os.path.getsize(OUT)
            print(f"PNG over 1 MiB; saved JPEG quality {quality}: "
                  f"{size} bytes")
            if size <= 1_048_576:
                break
    print(f"wrote {OUT}: {size} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
