# Spec — gemini-watermark-remover web app

## Goal
Free, ad-supported site to remove the Gemini star watermark from uploaded
images. 100% private: processing happens in the browser, no server, no
upload, no logs, nothing stored.

## Lazy architecture (the ponytail win)
- **One static HTML file** + one JS file. No backend.
- Image processing: pure client-side Canvas 2D (`getImageData`/`putImageData`).
- The algorithm (reverse alpha blending on a 48/96px corner patch) is ~30
  lines of JS. Ported 1:1 from `~/.local/bin/remove_gemini.py`.
- Alpha maps (bg_48.png, bg_96.png): bundled in the repo as static assets,
  fetched once per visitor, cached in memory.
- **Nothing is uploaded.** The privacy claim is structural, not a feature.

## Privacy / retention
- No backend = no server-side storage, by construction.
- Browser: processed image lives in memory + an object URL until the user
  leaves or clicks "remove." No `localStorage`, no `IndexedDB`, no cookies
  except AdSense's (Google sets those, disclose it).
- Add a visible "auto-clear after download" button and a 5-min JS timer
  that clears the canvas + object URL and shows "image cleared."

## Hosting / monetization
| Item          | Choice                                  | Cost |
|---------------|-----------------------------------------|------|
| Hosting       | Cloudflare Pages (static)               | $0  |
| Domain        | Any .com (~$12/yr) or .pages.dev free   | $0-12 |
| Ads           | Google AdSense (top 728×90 + in-content) | rev share |
| Analytics     | None, or privacy-friendly Plausible free tier | $0 |

## AdSense reality check (the spec's real cost)
- AdSense rejects pure tool sites as "low value content."
- Shipping requirement = tool + ~10 short original articles + the 3 legal
  pages below. Apply after content exists, expect 1-2 rejections first.
- Mandatory pages before applying:
  - /privacy — disclose AdSense cookies + the "nothing stored" claim
  - /terms — lawful-use clause (user must own/rights to the image)
  - /about
  - /contact
- Ads placement: top banner + one in-article unit. No more, or AdSense
  dings "excessive ads."

## Pages
1. `/` — the tool (hero 728×90 ad + uploader + result + articles links below)
2. `/blog/remove-gemini-watermark` — primary SEO target
3. `/blog/is-gemini-watermark-copyrighted`
4. `/blog/free-ai-watermark-removers-2026`
5. `/blog/how-gemini-watermark-works` (explain alpha blend, builds trust)
6. `/privacy`, `/terms`, `/about`, `/contact`

## Algorithm (JS port of the Python)
```
is_large = w > 1024 && h > 1024
size   = 96 if is_large else 48
margin = 64 if is_large else 32
x = w - margin - size
y = h - margin - size

for each pixel in the size×size patch at (x,y):
  alpha = alphaMap[row][col]            // 0..1, from bg_???.png
  if alpha < 0.002: continue
  alpha = min(alpha, 0.99)
  for rgb channel c:
    watermarked = patch[r][c]
    original = (watermarked - alpha*255) / (1 - alpha)
    patch[r][c] = clamp(round(original), 0, 255)
putImageData(patch at x,y)
```

## Legal cover (in /terms)
- User affirms they own or have rights to the image.
- Tool is for personal use; site is not liable for misuse.
- "Gemini" is a Google trademark; site is unofficial, not affiliated.

## Risks
- **AdSense rejection** (most likely) — mitigated by the articles above.
- **Trademark complaint from Google** on domain name — avoid
  "geminiwatermark.com"; use a generic name like "aistarremover.com" and
  mention "Gemini™ (Google)" in copy only.
- **Google removes the watermark in a future update** — the alpha maps
  change; this is a maintenance risk for any remover, not just this one.

## What to skip (YAGNI)
- User accounts, comments, history — a tool site doesn't need them.
- Backend, API, database — none; static only.
- Multi-language for v1 — add on traffic signal.
- A custom CMS — write articles as Markdown in the same repo.

## Build order
1. Single `index.html` + `remove.js` with the algorithm + uploader.
2. Bundle `bg_48.png`, `bg_96.png`. Test on a real Gemini image.
3. Add the 5-min auto-clear + clear button.
4. Write the 4 articles + 4 legal/about pages as static HTML.
5. Deploy to Cloudflare Pages.
6. Add AdSense after a month of organic traffic — applying too early =
   rejection that follows the domain.