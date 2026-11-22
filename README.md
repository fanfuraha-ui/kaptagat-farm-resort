# Kaptagat Farm Resort website

Static site (HTML, CSS, JS; no build dependencies at runtime). Pages: Home, Stay, Dine & explore, Contact.

Regenerate pages: `python3 tools/build.py .` (writes the HTML and the line drawings in `img/`).

## Before launch
- Edit `CONFIG` in `js/main.js`: WhatsApp number (0706 508 637 is from Facebook, confirm it), resort email (email buttons stay hidden until set), `usdRate`, optional `formEndpoint` (Formspree).
- Rates: only Standard Room (KES 4,900) and Decagon Cottage (KES 7,700) are sourced. Others show "On request"; set `kes` in `CONFIG.rooms` and `STAYS` in `tools/build.py` once confirmed.
- Replace the placeholder domain `kaptagatfarmresort.co.ke` in `tools/build.py`.
- The grounds plan is schematic. Replace it with the real site plan, and add real photography.
