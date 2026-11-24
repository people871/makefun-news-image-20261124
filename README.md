# Tuesday 24 November 2026 in one image: 8 sourced stories, a world map and a date check

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/people871/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/people871/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper-front-page image that sums up Tuesday 24 November 2026's world
news: **8 sourced stories, a world map with numbered pins placed from real
latitude/longitude, and a DATE CHECK box that throws out stories from the
wrong date** — built for the
[make.fun](https://make.fun/bounty/news-image-20261124) bounty
`news-image-20261124` ($100, top 50 share, 1st $20).

## The 8 stories (all verified against named sources)

| # | Story | Source |
|---|-------|--------|
| 1 | Nvidia reinstates Jensen Huang as CEO — board votes unanimously after a 12-day ouster; shares surge about 25%; Trump says he pressed the board | Nvidia newsroom / Reuters, 23 Nov |
| 2 | Ukraine says seven naval drones sank the Russian corvette Merkury at Benghazi, Libya; a second ship hit — the war reaches the Mediterranean | Reuters / AP, 23 Nov |
| 3 | Russian drone strike partly destroys an apartment block in Dymer, near Kyiv; 11 killed, 14 missing | Reuters, 23 Nov |
| 4 | Burning Russian freighter Sparta II, hit by drones in the Gulf of Finland, is towed out; Finland says Ukraine was likely behind it | Reuters, 23 Nov |
| 5 | Factory fire at a candy plant in Serang, Indonesia kills 24; rescuers search for missing workers | Reuters, 23 Nov |
| 6 | Trump threatens to sink Iranian tankers that break the US blockade; tensions rise at the Strait of Hormuz | Reuters, 23 Nov |
| 7 | EU proposes its 22nd sanctions package against Russia over the war in Ukraine | European Commission / Reuters, 23 Nov |
| 8 | World Chess Championship begins in Geneva — Gukesh opens his title defence against Sindarov | FIDE / Times of India, 24 Nov |

Stories are the 23 November cycle that led Tuesday's papers (events that
happened, or were first reported, on 24 November in some time zone). The
DATE CHECK box on the image excludes the wrong-date stories: COP31 collapse
(22 Nov), Shenzhen summit (19 Nov), ICJ Myanmar ruling (19 Nov), Poland
missiles (20 Nov), El Chapo capture (21 Nov), Anthropic IPO (20 Nov).

## The image

`entry.png` — JPEG, 1024×1024, 263,838 bytes. Generated fresh for 24
November with the media pipeline, then the world-map band was redrawn
programmatically from Natural Earth 110m land polygons so every numbered
pin sits on its true place (Santa Clara, Benghazi, Kyiv, Gulf of Finland,
Serang, Strait of Hormuz, Brussels, Geneva).

## The program

`main.py` (Python 3.13, standard library only) reads `entry.png`, validates
it — JPEG or PNG magic bytes, a whole file (JPEG frame header with
quantization and Huffman tables and a scan, ending in EOI; PNG header plus
IEND trailer), exactly 1024×1024, at most 1 MiB — writes the verified bytes
to `$MAKEFUN_OUTPUT_DIR/entry.png`, then reads the copy back and exits
non-zero unless its byte length and sha256 match the source.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
