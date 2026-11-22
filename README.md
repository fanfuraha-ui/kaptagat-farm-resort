# Kaptagat Farm Resort website

Static, mobile-first site in plain HTML, CSS and JavaScript, with no dependencies. Any static host can serve it (GitHub Pages, Netlify, cPanel).

Content is based on the resort's public listings (Google Hotels, Facebook, travel reviews): decagon bush-stone cottages, the pond cottage, the Mill Bar, the bandas, a conference hall for 200, check-in 2 pm and check-out 10 am.

## Structure
- `index.html`, `accommodations.html`, `experiences.html`, `gallery.html`, `contact.html`
- `css/style.css`: design tokens and components (decagon motif via the `--deca` clip-path)
- `js/main.js`: booking bar, KES/USD toggle, inquiry form, map legend and gallery. **Edit `CONFIG` at the top for phones, rates and the exchange rate.**
- `img/`: generated SVG illustrations
- `tools/`: `build.py` regenerates the pages and `art.py` the illustrations (`python3 tools/build.py .`)

## Confirm with the resort before launch
1. **Rates:** Standard Room (KES 4,900) and Decagon Cottage (KES 7,700) come from a third-party listing. Pond Cottage, Deluxe Cabin, Garden Villa and Dormitory rates are placeholders.
2. **WhatsApp number:** `CONFIG.whatsapp` uses 0706 508 637 (Facebook page). Confirm it's on WhatsApp. The main phone line is 0725 859 860 (Google listing).
3. **Email:** add it to `CONFIG.email` and the email buttons appear automatically.
4. **Photos:** swap the illustrations in `img/` for real WebP photos (1600 px wide, under 250 KB) and update the alt text.
5. **Farm activities:** the greenhouses, fish ponds and poultry are from a 2016 source. Confirm they still run.
6. **Domain:** replace the placeholder in the canonical/OG tags, `sitemap.xml` and `robots.txt`, and add `img/og-image.jpg` (1200×630).
7. **Form delivery:** set `CONFIG.formEndpoint` (e.g. Formspree) to receive inquiries by email. Without it, inquiries are handed off to WhatsApp.
