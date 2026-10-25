#!/usr/bin/env python3
"""Build a tiny index.html from src/index.html.

1. Re-encodes the embedded sound clips as small mono MP3s (ffmpeg).
2. Shrinks the logo mask: alpha only, resized and palette-quantised (Pillow).
3. Minifies the HTML, CSS and JS (html-minifier-terser, via minify.mjs).
"""
import base64, io, re, subprocess, sys, tempfile, os
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding="utf-8").read()

def b64(data): return base64.b64encode(data).decode()

# 1. sound clips: mono, 32 kHz, 40 kbps, trailing silence trimmed
for name in ["ONE_B64", "ACK_B64", "WOW_B64", "FAH_B64"]:
    m = re.search(name + r' = "([A-Za-z0-9+/=]+)"', s)
    if not m: continue
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "in.mp3"), os.path.join(d, "out.mp3")
        open(a, "wb").write(base64.b64decode(m.group(1)))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af",
                        "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
                        "-ac", "1", "-ar", "32000", "-b:a", "40k", b], check=True)
        s = s.replace(m.group(1), b64(open(b, "rb").read()), 1)

# 2. logo: only its alpha is used (as a CSS mask), so keep alpha alone
m = re.search(r"--logo:url\(data:image/png;base64,([A-Za-z0-9+/=]+)\)", s)
if m:
    im = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).getchannel("A")
    w = 900; im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    rgba = Image.new("RGBA", im.size, (0, 0, 0, 0)); rgba.putalpha(im)
    q = rgba.quantize(colors=16, method=Image.FASTOCTREE)
    buf = io.BytesIO(); q.save(buf, "PNG", optimize=True)
    s = s.replace(m.group(1), b64(buf.getvalue()), 1)

# 3. icons: palette-quantise too
for rel in ["icon", "apple-touch-icon"]:
    m = re.search(r'rel="' + rel + r'"[^>]*href="data:image/png;base64,([A-Za-z0-9+/=]+)"', s)
    if not m: continue
    im = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("RGBA")
    buf = io.BytesIO(); im.quantize(colors=32, method=Image.FASTOCTREE).save(buf, "PNG", optimize=True)
    s = s.replace(m.group(1), b64(buf.getvalue()), 1)

tmp = out + ".tmp.html"
open(tmp, "w", encoding="utf-8").write(s)
subprocess.run(["node", os.path.join(here, "minify.mjs"), tmp, out], check=True)
os.remove(tmp)
print(f"{src}: {os.path.getsize(src)//1024} KB  ->  {out}: {os.path.getsize(out)//1024} KB")
