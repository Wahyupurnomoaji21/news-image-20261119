[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Wahyupurnomoaji21/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Wahyupurnomoaji21/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# THE WORLD TODAY — Thursday, November 19, 2026

A one-page broadsheet front page for Thursday, November 19, 2026, built
entirely from local assets with Pillow — no network access at any step.

The lead story is the summit in Shenzhen: the first trilateral of sitting
U.S., Chinese and Russian presidents, scheduled for Thursday, with Ukraine,
Iran, nuclear arms, AI and trade on the agenda. Around it, the page carries
the day's other verified stories: the Gulf war widening as the U.S. strikes
Iran, Hakeem Jeffries set to become the first Black Speaker after the
Democrats' nomination and Peltola's win sealing a 56–44 Senate majority,
GTA VI launching as Vice City opens, Cyclone Akvan bearing down on India,
the EU's proposed €45bn loan to keep Ukraine funded, Voyager 1 reaching a
light-day from Earth, and a Pew projection that Islam becomes the world's
largest faith by 2035.

## v3 — what changed vs v2

- **Taller hero:** the summit photo is now 252px tall across the full
  976px content width, so the three leaders dominate the page.
- **Four pictured stories:** "The Day in Pictures" is now a row of four
  photo stories (Gulf, Senate, GTA VI, Cyclone Akvan), each with its own
  photo, headline and deck, instead of a narrower strip.
- **Bigger date:** the dateline is set in bold 22pt sans, flanked by the
  "LATE CITY EDITION" and "PRICE $2.50" labels under a double rule.
- **Wider IN BRIEF:** the three briefs now run in full 312px columns with
  20px gutters, matching the lead-story columns above them.
- **Larger type throughout:** 48pt headline, 18pt kicker, 15pt lead body
  and 18pt pictured-story headlines give the page a denser, more
  broadsheet feel.

## Rebuild

```sh
python3 compose.py
```

That renders `entry.png` (1024×1024, under 1 MiB) from the photos in
`assets/`, printing the layout bottom y and the bytes written. `main.py` then copies `entry.png` byte-for-byte to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), refusing if it is
over 1,048,576 bytes, and prints the byte count and sha256. Nothing in
either script touches the network.
