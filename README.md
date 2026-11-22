# Kaptagat Farm Resort website

Static, mobile-first site: plain HTML, CSS and JavaScript with no build step and no dependencies.

## Pages
`index.html` (home + booking bar), `accommodations.html`, `experiences.html`, `gallery.html`, `contact.html`

## Before launch
1. **Contact details and rates:** edit `CONFIG` at the top of `js/main.js` (WhatsApp number, email, KES→USD rate, room rates). Room cards in the HTML carry `data-kes` prices; keep them in step with `CONFIG.rooms`.
2. **Photos:** replace the illustrations in `img/` with real WebP photos (1600 px wide, under 250 KB each) and update the `alt` text.
3. **Inquiry form:** set `CONFIG.formEndpoint` to a Formspree/Web3Forms endpoint to receive submissions by email. While it is empty, the form hands the inquiry off to WhatsApp or email.
4. **Map:** swap the map placeholder on `contact.html` for the resort's Google Maps embed (see the comment there).
5. **SEO:** replace the sample domain in canonical/OG tags, `sitemap.xml` and `robots.txt`; add `img/og-image.jpg` (1200×630).
6. **Reviews:** add real guest reviews (with permission) in the commented block on `index.html`.

## Deploy
Any static host works: GitHub Pages, Netlify, Vercel or cPanel shared hosting. Upload the folder as-is.
