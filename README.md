# The World Today — Thursday 19 November 2026

A make.fun `news-image-20261119` entry: one 1024×1024 front page summing up
the world's news of Thursday 19 November 2026, rendered by `compose.py`
from four editorial illustrations made for this entry.

## The day in the image

- **Lead — Shenzhen:** Trump, Xi and Putin hold the first-ever trilateral
  summit of the US, China and Russia on the APEC sidelines; nuclear arms,
  Ukraine, Iran and trade on the agenda.
- **Gaming:** Grand Theft Auto VI begins its global rollout after a 13-year
  wait, with pre-orders past $1.5bn.
- **Business:** Anthropic debuts on Nasdaq as ANT after pricing its IPO at
  $83, above the $70–$78 range.
- **Europe:** 20-plus nations gather in Berlin for the Coalition of the
  Willing on postwar guarantees for Ukraine.
- **The Gulf:** Iran widens its attacks on US facilities in Kuwait and
  Bahrain; the US struck a missile site on Qeshm Island.
- **Also today:** 21 briefs — Jeffries nominated as the first Black Speaker,
  the DRC Ebola outbreak past 11,500 cases, Cyclone Akvan, Voyager 1's
  light-day milestone, Fed minutes, markets, Nvidia, Gaza, Estonia, the Red
  Sea, and more.

Every story was reported on 19 November 2026 (sources include AP, Reuters,
AFP, BBC, IMD, WHO and Pew Research, as credited on the page itself).

## Files

- `main.ts` — entrypoint: copies `entry.png` to `/output/entry.png`.
- `compose.py` — builds `entry.png` from `assets/*.png` with PIL.
  Deterministic: no network, no clock, no randomness.
- `assets/` — four editorial illustrations generated for this entry
  (Shenzhen summit, Vice City, IPO bell, Berlin flags). They carry no text;
  all words on the page are drawn by `compose.py`.
- `entry.png` — the composed front page, 1024×1024, under 1 MiB.

## Rebuild

```sh
python3 compose.py          # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs of `main.ts` write byte-identical output.
