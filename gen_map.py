#!/usr/bin/env python3
"""Build a self-hosted static map image for the shop location (no iframe, no API key).

Fetches OpenStreetMap tiles once, stitches them, draws a pin and attribution,
and writes assets/img/location-map.jpg (plus a 2x-friendly 1200x620 JPEG).
"""
import math, os, time, urllib.request
from PIL import Image, ImageDraw

LAT, LNG = 26.4291755, 50.1067007
Z = 17
W, H = 1200, 620
OUT = "/opt/data/matahin/assets/img/location-map.jpg"
UA = "MatahinNutsSite/1.0 (one-off static map build; contact abs@awekertraders.de)"

def deg2num(lat, lng, z):
    n = 2 ** z
    x = (lng + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2.0 * n
    return x, y

def fetch(tx, ty, tries=3):
    path = f"/tmp/osmtile_{Z}_{tx}_{ty}.png"
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return Image.open(path).convert("RGB")
    url = f"https://tile.openstreetmap.org/{Z}/{tx}/{ty}.png"
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
            open(path, "wb").write(data)
            return Image.open(path).convert("RGB")
        except Exception as e:
            print("retry", tx, ty, e)
            time.sleep(1.5 * (i + 1))
    return Image.new("RGB", (256, 256), "#E9EFE6")

cx, cy = deg2num(LAT, LNG, Z)
# pixel coordinates of the pin inside the whole map
pin_px, pin_py = cx * 256, cy * 256
# keep the pin slightly below the centre
left = int(pin_px - W / 2)
top = int(pin_py - H * 0.56)

tx0, ty0 = left // 256, top // 256
tx1 = (left + W) // 256 + 1
ty1 = (top + H) // 256 + 1

canvas = Image.new("RGB", ((tx1 - tx0) * 256, (ty1 - ty0) * 256), "#E9EFE6")
for ty in range(ty0, ty1):
    for tx in range(tx0, tx1):
        canvas.paste(fetch(tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))

img = canvas.crop((left - tx0 * 256, top - ty0 * 256,
                   left - tx0 * 256 + W, top - ty0 * 256 + H)).convert("RGBA")

# soften the map a touch so the pin and text sit on top cleanly
from PIL import ImageEnhance
img = ImageEnhance.Color(img).enhance(0.92)
img = ImageEnhance.Brightness(img).enhance(1.03)

d = ImageDraw.Draw(img, "RGBA")
px, py = W / 2, H * 0.56

# pin shadow
d.ellipse([px - 20, py - 6, px + 20, py + 14], fill=(0, 0, 0, 45))
# teardrop body
GREEN = (20, 80, 59, 255)
d.polygon([(px - 15, py - 30), (px + 15, py - 30), (px, py)], fill=GREEN)
d.ellipse([px - 17, py - 62, px + 17, py - 28], fill=GREEN)
# white ring + dot
d.ellipse([px - 8, py - 53, px + 8, py - 37], fill=(255, 255, 255, 255))
d.ellipse([px - 4, py - 49, px + 4, py - 41], fill=(184, 134, 59, 255))

# attribution lives in the HTML overlay so it is never cropped

img.convert("RGB").save(OUT, "JPEG", quality=84, optimize=True, progressive=True)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB", img.size)
