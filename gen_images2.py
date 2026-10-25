#!/usr/bin/env python3
"""Second batch: pansari/kiryana product photos for the full catalogue."""
import json, os, socket, time, urllib.request

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
         "photography, ultra realistic, no text, no words, no letters, no labels, no watermark, no hands.")

ITEMS = {
    "red-lentils": "a generous pile of split red lentils",
    "chana-dal": "a generous pile of yellow split chickpeas (chana dal)",
    "white-chickpeas": "a generous pile of dried white chickpeas",
    "red-kidney-beans": "a generous pile of dried red kidney beans",
    "whole-red-chillies": "a generous pile of dried whole round red chillies",
    "coriander-seeds": "a generous pile of whole coriander seeds",
    "dried-ginger": "a small pile of dried whole ginger pieces",
    "bay-leaves": "a small pile of dried bay leaves",
    "semolina": "a mound of fine golden semolina with a wooden scoop",
    "rock-sugar": "a small pile of white rock sugar crystals",
    "pomegranate-seeds": "a small pile of dried pomegranate seeds",
    "tamarind": "a block of dark tamarind paste with pods",
    "basmati-rice": "a generous pile of long-grain basmati rice with a wooden scoop",
    "garam-masala": "a mound of dark brown garam masala powder with whole spices around it",
    "biryani-masala": "a mound of aromatic biryani spice blend with whole cardamom, cloves and bay leaves around it",
    "black-tea": "a pile of fine black tea leaves with a glass cup of brewed tea beside it",
    "corn-oil": "a clear glass bottle of golden corn oil, plain unlabelled bottle",
    "olive-oil": "a dark glass bottle of olive oil with a few olives beside it, plain unlabelled bottle",
    "rose-syrup": "a glass bottle of deep red rose syrup with rose petals beside it, plain unlabelled bottle",
    "amla-oil": "a glass bottle of dark green amla hair oil with fresh amla fruit beside it, plain unlabelled bottle",
    "pickle-jar": "a glass jar of mixed mango and lemon pickle in oil",
    "tomato-paste": "a bowl of thick tomato paste with fresh tomatoes beside it",
    "green-peas": "a small bowl of canned green peas",
    "noodles": "a stack of dried instant noodle cakes with a bowl of cooked noodles",
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

state_file = "/opt/data/matahin/raw/_tasks2.json"
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
                tasks[slug] = {"taskId": r["data"]["taskId"], "key": key}
                print("submitted", slug, flush=True)
                break
            if r.get("code") == 402:
                key = ALT if key == KEY else KEY
                print("402 switch", key[-6:], flush=True)
                continue
            print("err", slug, r, flush=True)
        except Exception as e:
            print("exc", slug, e, flush=True)
        time.sleep(3)
    json.dump(tasks, open(state_file, "w"), indent=1)
    time.sleep(0.8)

print("submitted total", len(tasks), flush=True)
pending = {s: t for s, t in tasks.items() if not os.path.exists(f"{OUT}/{s}.png")}
deadline = time.time() + 1500
while pending and time.time() < deadline:
    time.sleep(15)
    for slug, t in list(pending.items()):
        try:
            d = (get(f"{BASE}/api/v1/jobs/recordInfo?taskId={t['taskId']}", t["key"]).get("data") or {})
            st = d.get("state")
            if st == "success":
                rj = d.get("resultJson") or "{}"
                rj = json.loads(rj) if isinstance(rj, str) else rj
                urls = rj.get("resultUrls") or []
                if urls:
                    urllib.request.urlretrieve(urls[0], f"{OUT}/{slug}.png")
                    print("done", slug, flush=True)
                    pending.pop(slug)
            elif st in ("fail", "failed"):
                print("FAILED", slug, d.get("failMsg"), flush=True)
                pending.pop(slug)
        except Exception as e:
            print("poll exc", slug, e, flush=True)
print("remaining", list(pending), flush=True)
