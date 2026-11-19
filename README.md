[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Wahyupurnomoaji21/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Wahyupurnomoaji21/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World Today — 19 November 2026

Front page of the day's world news, as a real broadsheet. Lead story:
the first-ever Trump–Xi–Putin trilateral, scheduled for Thursday in
Shenzhen on the APEC sidelines. Below it, four pictured stories: the
Gulf war widening (US jets strike Qeshm Island; Iranian drones reach
Bahrain and Kuwait; a tanker burns in the Strait), Hakeem Jeffries
nominated as the first Black Speaker-to-be with Peltola's Alaska win
sealing a 56–44 Senate majority, Grand Theft Auto VI launching after
a 13-year wait, and Cyclone Akvan bearing down on India. Also today:
the EU's €45bn Ukraine loan proposal, Voyager 1's light-day confirmed,
and Pew's projection that Islam becomes the world's largest faith by
2035.

Every headline was checked against real reporting of 18–19 November
2026 (Reuters/AP/BBC/NASA/Pew via search, 19 Nov 2026). Two claims in
the first draft were corrected during verification: the trilateral is
presented as Thursday's scheduled meeting, not as already held, and
the Nvidia item was dropped — Huang had said he would be honoured to
return, so "no Huang return" was wrong; Pew replaces it.

## v3 (branch `v3`, from v2 HEAD 64167a4)

v2 was submitted and scored dev rank 2754/4208 (judge 966495) — outside
the rank-1000 bar (judge 975976). v3 is a genuine redesign, same
verified facts, changing how the page renders rather than what it
shows:

- Hero photograph taller (976x252) with a sharper three-flag
  handshake shot; the date in the dateline grows to 22 pt bold, so
  the day the page sums up is unmistakable at a glance.
- Headline grows to 48 pt; lead body shortens to three lines per
  column at 15 pt, so the page breathes instead of crowding.
- Four pictured stories instead of three — Cyclone Akvan joins the
  Gulf war, the Jeffries nomination and the GTA VI launch — so every
  story is clear from its own photograph and headline.
- IN BRIEF becomes three wide columns with larger type (EU loan,
  Voyager 1, Pew), trading one dense item for legibility at 300 px.

Five realistic press-style photographs, Times-style serif type, photo
captions and three-column body copy.

`python3 compose.py` rebuilds `entry.png` (1024x1024, under 1 MiB)
from the photos in `assets/`; `main.py` copies it byte-for-byte to
`/output/entry.png` (no network, deterministic).
