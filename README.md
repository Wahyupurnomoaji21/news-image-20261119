# The World Today — 19 November 2026

Front page of the day's world news, as a real broadsheet. Lead story:
the first-ever Trump–Xi–Putin trilateral, scheduled for Thursday in
Shenzhen on the APEC sidelines. Below it: the Gulf war widening (US
jets strike Qeshm Island; Iranian drones reach Bahrain and Kuwait; a
tanker burns in the Strait), Hakeem Jeffries nominated as the first
Black Speaker-to-be with Peltola's Alaska win sealing a 56–44 Senate
majority, and Grand Theft Auto VI launching after a 13-year wait.
Also today: the EU's €45bn Ukraine loan proposal, Cyclone Akvan
nearing India, Voyager 1's light-day confirmed, and Pew's projection
that Islam becomes the world's largest faith by 2035.

Every headline was checked against real reporting of 18–19 November
2026 (Reuters/AP/BBC/NASA/Pew via search, 19 Nov 2026). Two claims in
the first draft were corrected during verification: the trilateral is
presented as Thursday's scheduled meeting, not as already held, and
the Nvidia item was dropped — Huang had said he would be honoured to
return, so "no Huang return" was wrong; Pew replaces it.

## v2 (branch `v2`, from v1 HEAD 5a9307f)

v1 was submitted and scored dev rank 2175/3243 (judge 966495) — outside
the top-50 prize zone. v2 is a genuine redesign, same verified facts:

- Headline moves ABOVE the lead photograph (classic broadsheet
  hierarchy) and grows to 45 pt; lead story runs in three columns
  with a staff byline.
- All four photographs are new, sharper press shots (summit handshake
  at the table with the three flags, burning tanker at dusk, House
  chamber with the Speaker's gavel, neon midnight launch queue).
- The "also today" strip becomes a four-column IN BRIEF section, so
  the EU loan, Cyclone Akvan, Voyager 1 and Pew items each get a
  headline of their own instead of one dense line.

Four realistic press-style photographs, Times-style serif type, photo
captions and three-column body copy.

`python3 compose.py` rebuilds `entry.png` (1024x1024, under 1 MiB)
from the photos in `assets/`; `main.py` copies it byte-for-byte to
`/output/entry.png` (no network, deterministic).
