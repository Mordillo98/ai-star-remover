# AI Star Remover

> Take the sparkle off a Gemini image.

A free, private, 100% client-side tool that removes the Google Gemini star watermark from images. Everything runs in your browser — no upload, no server, no tracking, no login.

## How it works

The Gemini watermark isn't pasted on — it's **alpha blended**. Pure white is mixed into the bottom-right corner under a fixed star-shaped alpha map:

```
watermarked = α·255 + (1−α)·original
```

Since the alpha map is fixed and public (MIT-licensed by the [gemini-watermark-remover](https://github.com/dearabhin/gemini-watermark-remover) project), the blend is **exactly reversible**:

```
original = (watermarked − α·255) / (1−α)
```

Each pixel in the corner patch is solved, and the star is gone — not guessed, **computed**.

## Features

- 🔒 **100% private** — images never leave your browser
- 🚫 **No login** — nothing to sign up for
- ⚡ **Instant** — processed locally on a `<canvas>`, result auto-clears in 30s
- 🖼️ **Original/unmodified PNG files only** — preserves lossless quality
- 🆓 **Free** — no ads, no paywall, no catch

## Tech

- Single static site — no backend, no build step
- Vanilla HTML/CSS/JS (no frameworks, no dependencies)
- Hosted on [GitHub Pages](https://pages.github.com/) — free, zero config
- Two alpha maps bundled in `assets/` — no runtime fetch

## Local dev

```bash
python3 serve.py      # serves at http://localhost:8765/
```

The dev server resolves pretty URLs (same as GitHub Pages in production) and sends no-cache headers.

## Structure

```
index.html              ← the tool (landing page)
style.css               ← shared theme
serve.py                ← local dev server with pretty URLs
assets/
  bg_48.png             ← 48px star alpha map (small images)
  bg_96.png             ← 96px star alpha map (large images)
privacy.html            ← privacy policy (100% private, no ads, no tracking)
404.html
_redirects              ← pretty-URL redirect rules
sitemap.xml
robots.txt
```

## Deploy

Push to GitHub → enable Pages on `main` branch → done. No build command needed; output directory is the repo root.

## Credits

- Alpha maps: [gemini-watermark-remover](https://github.com/dearabhin/gemini-watermark-remover) (MIT)
- *"Gemini" is a Google LLC trademark. This site is independent and unaffiliated. Only edit images you own or have rights to.*

## License

MIT