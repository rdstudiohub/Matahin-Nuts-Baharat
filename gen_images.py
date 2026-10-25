#!/usr/bin/env python3
"""Generate 26 product photos for Matahin Nuts & Spices via KIE gpt4o-image."""
import json, os, socket, time, urllib.request, sys

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _orig(h, p, socket.AF_INET, t, pr, fl)

KEY = "376b0cd8d21b26989bf4d333428889e6"
ALT = "8e447a45e51ba550def3549a48595204"
BASE = "https://api.kie.ai"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
OUT = "/opt/data/matahin/raw"
os.makedirs(OUT, exist_ok=True)

STYLE = ("Top-down product photograph, {item}, in a shallow cream ceramic bowl on a warm off-white "
         "linen surface, soft diffused daylight from the side, shallow depth of field, premium food "
         "photography, ultra realistic, 4k detail, no text, no words, no letters, no watermark, no hands.")

ITEMS = {
    "almonds": "a generous pile of premium whole raw almonds",
    "pistachios": "a generous pile of roasted salted pistachios in their open shells",
    "cashews": "a generous pile of cream-coloured whole roasted cashew nuts",
    "walnuts": "a generous pile of cracked walnut halves",
    "hazelnuts": "a generous pile of whole roasted hazelnuts",
    "peanuts": "a generous pile of roasted red-skin peanuts",
    "mixed-nuts": "an elegant mix of almonds, cashews, pistachios and hazelnuts",
    "pine-nuts": "a small cream bowl filled with pale pine nuts",
    "pumpkin-seeds": "a generous pile of green pumpkin seeds",
    "sunflower-seeds": "a generous pile of striped sunflower seeds",
    "raisins": "a generous pile of dark golden raisins",
    "dried-apricots": "a generous pile of bright orange dried apricots",
    "figs": "a generous pile of dried figs",
    "dates": "a generous pile of glossy medjool dates",
    "saffron": "a small glass dish of deep red saffron threads",
    "cardamom": "a generous pile of green cardamom pods, a few split open",
    "cinnamon": "a bundle of rolled cinnamon sticks with ground cinnamon",
    "cloves": "a generous pile of whole cloves",
    "black-pepper": "a generous pile of whole black peppercorns with a wooden scoop of ground pepper",
    "cumin": "a generous pile of cumin seeds beside a small mound of ground cumin",
    "turmeric": "a mound of vivid golden turmeric powder with a few turmeric roots",
    "sumac": "a mound of deep reddish-purple sumac powder with a lemon wedge",
    "kabsa-spice": "a mound of warm brown kabsa spice mix with whole cardamom, cloves and cinnamon around it",
    "chili-powder": "a mound of deep red chili powder with dried red chillies",
    "arabic-coffee": "a bowl of freshly roasted dark Arabic coffee beans with a brass dallah pot",
    "honey": "a glass jar of golden honey with a wooden dipper drizzling honey",
}

def post(url, body, key):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

def get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

state_file = "/opt/data/matahin/raw/_tasks.json"
tasks = json.load(open(state_file)) if os.path.exists(state_file) else {}

key = KEY
for slug, item in ITEMS.items():
    if slug in tasks:
        continue
    prompt = STYLE.format(item=item)
    for attempt in range(4):
        try:
            r = post(f"{BASE}/api/v1/gpt4o-image/generate", {"prompt": prompt, "model": "gpt-4o", "size": "1:1"}, key)
            if r.get("code") == 200:
                tid = r["data"]["taskId"]
                tasks[slug] = {"taskId": tid, "key": key}
                print("submitted", slug, tid, flush=True)
                break
            if r.get("code") == 402:
                print("402 on", key, "switching", flush=True)
                key = ALT if key == KEY else KEY
                continue
            print("err", slug, r, flush=True)
        except Exception as e:
            print("exc", slug, e, flush=True)
        time.sleep(3)
    json.dump(tasks, open(state_file, "w"), indent=1)
    time.sleep(0.8)

print("submitted total", len(tasks), flush=True)

# poll
pending = {s: t for s, t in tasks.items() if not os.path.exists(f"{OUT}/{s}.png")}
deadline = time.time() + 1500
while pending and time.time() < deadline:
    time.sleep(15)
    for slug, t in list(pending.items()):
        try:
            r = get(f"{BASE}/api/v1/jobs/recordInfo?taskId={t['taskId']}", t["key"])
            d = r.get("data") or {}
            st = d.get("state")
            if st == "success":
                rj = d.get("resultJson") or "{}"
                rj = json.loads(rj) if isinstance(rj, str) else rj
                urls = rj.get("resultUrls") or []
                if urls:
                    urllib.request.urlretrieve(urls[0], f"{OUT}/{slug}.png")
                    print("done", slug, os.path.getsize(f"{OUT}/{slug}.png"), flush=True)
                    pending.pop(slug)
            elif st in ("fail", "failed"):
                print("FAILED", slug, d.get("failMsg"), flush=True)
                pending.pop(slug)
        except Exception as e:
            print("poll exc", slug, e, flush=True)

print("remaining", list(pending), flush=True)
