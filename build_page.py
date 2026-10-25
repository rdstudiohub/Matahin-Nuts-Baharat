#!/usr/bin/env python3
"""Build the trilingual (AR/EN/UR) single-page site for Matahin Nuts & Spices."""
import json, html, os, urllib.parse

ROOT = "/opt/data/matahin"
PRODUCTS = json.load(open(f"{ROOT}/products.json"))
WA = "966537373257"
TEL = "+966537373257"

CATS = [
    ("all", "All Products", "جميع المنتجات", "تمام مصنوعات"),
    ("nuts", "Nuts", "مكسرات", "میوے"),
    ("dried", "Dried Fruits & Seeds", "فواكه مجففة وبذور", "خشک میوہ جات و بیج"),
    ("spices", "Spices", "بهارات", "مصالحے"),
    ("coffee", "Coffee & Honey", "قهوة وعسل", "قہوہ و شہد"),
]

def wa_link(msg):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)

def card(p):
    order = {
        "en": f"Hello, I would like to order: {p['en']}",
        "ar": f"السلام عليكم، أرغب بطلب: {p['ar']}",
        "ur": f"السلام علیکم، مجھے یہ آرڈر کرنا ہے: {p['ur']}",
    }
    return f"""      <article class="p-card" data-cat="{p['cat']}">
        <div class="p-media"><img src="assets/img/{p['slug']}.webp" alt="{html.escape(p['en'])}" loading="lazy" width="800" height="800"></div>
        <div class="p-body">
          <h3 class="p-name" data-en="{html.escape(p['en'])}" data-ar="{html.escape(p['ar'])}" data-ur="{html.escape(p['ur'])}">{p['ar']}</h3>
          <p class="p-desc" data-en="{html.escape(p['den'])}" data-ar="{html.escape(p['dar'])}" data-ur="{html.escape(p['dur'])}">{p['dar']}</p>
          <div class="p-foot">
            <a class="p-order" href="{wa_link(order['ar'])}" data-href-en="{wa_link(order['en'])}" data-href-ar="{wa_link(order['ar'])}" data-href-ur="{wa_link(order['ur'])}">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-4.3-2.5 10 10 0 0 1-2.1-3c-.2-.5-.3-1.2 0-1.7.2-.4.6-1 .9-1.1l.6-.1h.5c.3 0 .5.1.6.5l.7 1.7c.1.2 0 .4-.1.6l-.4.5c-.1.2-.3.3-.1.6a7 7 0 0 0 3.2 2.8c.3.1.4 0 .6-.1l.8-.9c.2-.2.3-.2.6-.1l1.6.8c.3.1.4.2.5.3.1.3 0 1-.1 1.4Z"/></svg>
              <span data-en="Order on WhatsApp" data-ar="اطلب عبر واتساب" data-ur="واٹس ایپ پر آرڈر کریں">اطلب عبر واتساب</span>
            </a>
          </div>
        </div>
      </article>"""

cards = "\n".join(card(p) for p in PRODUCTS)
cat_btns = "\n".join(
    f'          <button class="chip{" is-on" if c[0]=="all" else ""}" data-filter="{c[0]}" '
    f'data-en="{c[1]}" data-ar="{c[2]}" data-ur="{c[3]}">{c[2]}</button>'
    for c in CATS)

HTML = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مطاحن مكسرات بهارات — الدمام | Matahin Nuts &amp; Spices</title>
<meta name="description" content="مطاحن مكسرات بهارات — مكسرات فاخرة، قهوة مختارة وبهارات مطحونة طازجة في الدمام، العدامة. اطلب عبر واتساب. Premium nuts, fresh-ground spices and Arabic coffee in Dammam.">
<meta name="theme-color" content="#14503B">
<meta property="og:title" content="مطاحن مكسرات بهارات — الدمام">
<meta property="og:description" content="مكسرات فاخرة · قهوة مختارة · طعم أصيل — أفضل الأسعار لدينا">
<meta property="og:image" content="assets/img/banner-poster.jpg">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Noto+Kufi+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --ivory:#FAF7F0; --cream:#F2EBDD; --ink:#241E19; --muted:#6C6259;
  --green:#14503B; --green-2:#1C6B4F; --gold:#B8863B; --gold-soft:#E8D3AC;
  --wa:#1FA855; --line:#E4DACA; --shadow:0 10px 30px rgba(36,30,25,.07);
  --radius:18px;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--ivory);color:var(--ink);font-family:'Noto Kufi Arabic',system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}}
img{{max-width:100%;display:block}}
a{{color:inherit;text-decoration:none}}
.wrap{{width:min(1180px,92vw);margin:0 auto}}

/* ---------- top bar ---------- */
.topbar{{position:sticky;top:0;z-index:60;background:rgba(250,247,240,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}}
.topbar .wrap{{display:flex;align-items:center;gap:14px;height:64px}}
.brand{{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:.2px;color:var(--green);white-space:nowrap}}
.brand svg{{width:32px;height:32px;flex:none}}
.brand b{{font-size:clamp(14px,1.6vw,17px)}}
.top-actions{{margin-inline-start:auto;display:flex;align-items:center;gap:10px}}
.top-phone{{display:inline-flex;align-items:center;gap:7px;font-weight:600;font-size:14px;color:var(--green);direction:ltr}}
.top-phone svg{{width:17px;height:17px;fill:var(--green)}}
.lang{{display:flex;background:var(--cream);border:1px solid var(--line);border-radius:999px;padding:3px;gap:2px}}
.lang button{{border:0;background:transparent;font:inherit;font-size:12px;font-weight:600;color:var(--muted);padding:5px 11px;border-radius:999px;cursor:pointer;transition:.2s}}
.lang button.is-on{{background:var(--green);color:#fff;box-shadow:0 2px 8px rgba(20,80,59,.25)}}

/* ---------- hero video ---------- */
.hero{{position:relative;background:#0d120f;overflow:hidden}}
.hero video{{width:100%;height:clamp(340px,58vh,560px);object-fit:cover;display:block;opacity:.92}}
.hero::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,20,15,.15) 0%,rgba(10,20,15,.05) 40%,rgba(10,20,15,.72) 100%);pointer-events:none}}
.hero-in{{position:absolute;inset:auto 0 0 0;z-index:2;padding:clamp(18px,4vw,42px) 0 clamp(20px,4vw,40px)}}
.hero-badge{{display:inline-flex;align-items:center;gap:8px;background:rgba(232,211,172,.16);border:1px solid rgba(232,211,172,.45);color:#F6EAD3;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:600;letter-spacing:.6px;margin-bottom:14px}}
.hero h1{{margin:0;color:#fff;font-size:clamp(26px,5.2vw,52px);line-height:1.2;text-shadow:0 4px 24px rgba(0,0,0,.45)}}
.hero-sub{{color:#EBDDC4;font-size:clamp(13px,2vw,17px);margin:8px 0 0;max-width:640px}}
.hero-tag{{color:var(--gold-soft);font-weight:600;margin-top:10px;font-size:clamp(13px,1.9vw,16px)}}

/* ---------- action bar ---------- */
.actionbar{{position:sticky;top:64px;z-index:55;background:var(--ivory);border-bottom:1px solid var(--line);box-shadow:0 6px 18px rgba(36,30,25,.05)}}
.actionbar .wrap{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:10px 0}}
.act{{display:flex;align-items:center;justify-content:center;gap:8px;padding:11px 10px;border-radius:12px;font-weight:700;font-size:14px;border:1px solid transparent;transition:.2s}}
.act svg{{width:19px;height:19px;flex:none}}
.act.wa{{background:var(--wa);color:#fff}}
.act.loc{{background:var(--green);color:#fff}}
.act.call{{background:#fff;color:var(--green);border-color:var(--green)}}
.act:hover{{transform:translateY(-1px);filter:brightness(1.04)}}

/* ---------- intro ---------- */
.intro{{padding:clamp(30px,6vw,58px) 0 0;text-align:center}}
.eyebrow{{color:var(--gold);font-weight:700;letter-spacing:2px;font-size:12px;text-transform:uppercase}}
.intro h2{{font-size:clamp(22px,3.4vw,34px);margin:8px 0 10px;color:var(--green)}}
.intro p{{color:var(--muted);max-width:720px;margin:0 auto;font-size:clamp(14px,1.7vw,16px)}}

/* ---------- categories ---------- */
.cats{{display:flex;gap:8px;overflow-x:auto;padding:22px 0 6px;scrollbar-width:none;-ms-overflow-style:none}}
.cats::-webkit-scrollbar{{display:none}}
.chip{{flex:none;border:1px solid var(--line);background:#fff;color:var(--muted);font:inherit;font-size:13px;font-weight:600;padding:9px 16px;border-radius:999px;cursor:pointer;transition:.2s}}
.chip:hover{{border-color:var(--gold-soft)}}
.chip.is-on{{background:var(--green);border-color:var(--green);color:#fff}}

/* ---------- products ---------- */
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;padding:20px 0 10px}}
.p-card{{background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;transition:transform .25s ease,box-shadow .25s ease}}
.p-card:hover{{transform:translateY(-4px);box-shadow:0 18px 40px rgba(36,30,25,.12)}}
.p-media{{aspect-ratio:1/1;background:var(--cream);overflow:hidden}}
.p-media img{{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}}
.p-card:hover .p-media img{{transform:scale(1.05)}}
.p-body{{padding:16px 16px 14px;display:flex;flex-direction:column;gap:6px;flex:1}}
.p-name{{margin:0;font-size:19px;color:var(--green);font-weight:700}}
.p-desc{{margin:0;color:var(--muted);font-size:13.5px;flex:1}}
.p-foot{{margin-top:10px}}
.p-order{{display:inline-flex;align-items:center;gap:7px;background:#F1F7F3;color:var(--green);border:1px solid #D7E7DE;padding:8px 13px;border-radius:999px;font-size:12.5px;font-weight:700;transition:.2s}}
.p-order svg{{width:15px;height:15px;fill:var(--wa)}}
.p-order:hover{{background:var(--wa);color:#fff;border-color:var(--wa)}}
.p-order:hover svg{{fill:#fff}}
.empty{{padding:30px;text-align:center;color:var(--muted);display:none}}

/* ---------- features ---------- */
.features{{padding:clamp(38px,7vw,70px) 0 10px}}
.features h2,.loc h2{{text-align:center;color:var(--green);font-size:clamp(22px,3.2vw,32px);margin:0 0 6px}}
.features .lead{{text-align:center;color:var(--muted);margin:0 auto 26px;max-width:600px;font-size:14.5px}}
.f-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}}
.f-item{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;text-align:center}}
.f-ico{{width:46px;height:46px;margin:0 auto 12px;border-radius:14px;background:var(--cream);display:grid;place-items:center}}
.f-ico svg{{width:24px;height:24px;stroke:var(--green);fill:none;stroke-width:1.7}}
.f-item h3{{margin:0 0 6px;font-size:16px;color:var(--ink)}}
.f-item p{{margin:0;font-size:13.5px;color:var(--muted)}}

/* ---------- location ---------- */
.loc{{padding:clamp(38px,7vw,70px) 0 0}}
.loc-card{{margin-top:22px;display:grid;grid-template-columns:1.05fr .95fr;background:#fff;border:1px solid var(--line);border-radius:22px;overflow:hidden;box-shadow:var(--shadow)}}
.map{{position:relative;min-height:320px;background:
  radial-gradient(circle at 30% 30%,#E9F0E6 0,#E3EBDF 40%,#DCE6D6 100%)}}
.map::before{{content:"";position:absolute;inset:0;background-image:
  linear-gradient(rgba(20,80,59,.07) 1px,transparent 1px),
  linear-gradient(90deg,rgba(20,80,59,.07) 1px,transparent 1px);
  background-size:44px 44px}}
.map .pin{{position:absolute;inset:0;display:grid;place-items:center;text-align:center;padding:20px}}
.pin-dot{{width:56px;height:56px;border-radius:50%;background:var(--green);display:grid;place-items:center;margin:0 auto 10px;box-shadow:0 10px 24px rgba(20,80,59,.28)}}
.pin-dot svg{{width:26px;height:26px;fill:#fff}}
.map .pin p{{margin:0;font-weight:700;color:var(--green);font-size:14px}}
.map .pin small{{color:var(--muted);font-size:12px}}
.loc-info{{padding:clamp(22px,3.4vw,38px)}}
.loc-info h3{{margin:0 0 4px;color:var(--green);font-size:20px}}
.loc-info .sub{{margin:0 0 18px;color:var(--muted);font-size:13.5px}}
.row{{display:flex;gap:12px;align-items:flex-start;padding:11px 0;border-top:1px solid #F0E9DC}}
.row svg{{width:20px;height:20px;flex:none;stroke:var(--gold);fill:none;stroke-width:1.7;margin-top:3px}}
.row b{{display:block;font-size:13px;color:var(--ink)}}
.row span{{font-size:13.5px;color:var(--muted)}}
.row a{{font-size:13.5px;color:var(--green);font-weight:700;direction:ltr;display:inline-block}}
.loc-btns{{display:flex;gap:10px;margin-top:18px;flex-wrap:wrap}}
.loc-btns a{{flex:1 1 130px;text-align:center;padding:11px 14px;border-radius:12px;font-weight:700;font-size:13.5px}}
.btn-wa{{background:var(--wa);color:#fff}}
.btn-map{{background:var(--green);color:#fff}}

/* ---------- footer ---------- */
footer{{margin-top:clamp(40px,7vw,70px);background:#123F2F;color:#D9E7DE;padding:34px 0 26px}}
.foot-top{{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;justify-content:space-between}}
.foot-brand{{display:flex;gap:12px;align-items:center}}
.foot-brand svg{{width:40px;height:40px;fill:#E8D3AC}}
.foot-brand b{{display:block;color:#fff;font-size:17px}}
.foot-brand span{{font-size:12.5px;color:#A9C3B5}}
.foot-links{{display:flex;gap:18px;flex-wrap:wrap;font-size:13px}}
.foot-links a:hover{{color:#E8D3AC}}
.foot-bottom{{margin-top:22px;padding-top:16px;border-top:1px solid rgba(255,255,255,.12);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12px;color:#9AB3A6}}

/* ---------- floating whatsapp ---------- */
.fab{{position:fixed;inset-inline-end:16px;bottom:16px;z-index:70;width:54px;height:54px;border-radius:50%;background:var(--wa);display:grid;place-items:center;box-shadow:0 10px 24px rgba(31,168,85,.4)}}
.fab svg{{width:28px;height:28px;fill:#fff}}

@media(max-width:860px){{
  .loc-card{{grid-template-columns:1fr}}
  .map{{min-height:220px}}
  .top-phone span{{display:none}}
}}
@media(max-width:600px){{
  .topbar .wrap{{height:58px;gap:8px}}
  .brand b{{font-size:13px}}
  .actionbar{{top:58px}}
  .lang button{{padding:5px 8px;font-size:11px}}
  .grid{{grid-template-columns:repeat(2,1fr);gap:12px}}
  .p-body{{padding:11px}}
  .p-name{{font-size:15px}}
  .p-desc{{font-size:12px}}
  .p-order{{font-size:11px;padding:7px 10px}}
  .hero video{{height:clamp(300px,46vh,420px)}}
}}
/* Urdu / Arabic typography */
html[dir="rtl"] .hero h1,html[dir="rtl"] .p-name,html[dir="rtl"] .intro h2{{font-family:'Noto Kufi Arabic',system-ui,sans-serif}}
html[lang="en"] body{{font-family:'Cormorant Garamond',Georgia,serif}}
html[lang="en"] .p-desc,html[lang="en"] .act,html[lang="en"] .chip,html[lang="en"] .row,html[lang="en"] .hero-sub{{font-family:system-ui,-apple-system,'Segoe UI',sans-serif}}
</style>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <a class="brand" href="#top" aria-label="Matahin">
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="24" r="22" fill="none" stroke="#B8863B" stroke-width="2"/>
        <path d="M14 30c0-3 2-5 5-6-2-1-3-3-3-5 3 0 5 1 6 3 1-4 4-7 8-7-1 4-3 7-6 9 3 0 6 1 8 3-2 2-5 3-8 2 1 2 1 4 0 6-2-1-4-3-4-5-2 2-4 3-6 3z" fill="#14503B"/>
      </svg>
      <b data-en="Matahin Nuts &amp; Spices" data-ar="مطاحن مكسرات بهارات" data-ur="مطاحن مكسرات بهارات">مطاحن مكسرات بهارات</b>
    </a>
    <div class="top-actions">
      <a class="top-phone" href="tel:{TEL}">
        <svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2Z"/></svg>
        <span dir="ltr">053 737 3257</span>
      </a>
      <div class="lang" role="group" aria-label="Language">
        <button data-lang="ar" class="is-on">عربي</button>
        <button data-lang="en">EN</button>
        <button data-lang="ur">اردو</button>
      </div>
    </div>
  </div>
</header>

<section class="hero" id="top">
  <video id="heroVid" autoplay muted loop playsinline preload="metadata" poster="assets/img/banner-poster.jpg">
    <source src="assets/video/shop-banner.mp4" type="video/mp4">
  </video>
  <div class="hero-in">
    <div class="wrap">
      <div class="hero-badge" data-en="Dammam · Al-Adama" data-ar="الدمام · العدامة" data-ur="الدمام · العدامة">الدمام · العدامة</div>
      <h1 data-en="Matahin Nuts &amp; Spices" data-ar="مطاحن مكسرات بهارات" data-ur="مطاحن مكسرات بهارات">مطاحن مكسرات بهارات</h1>
      <p class="hero-sub" data-en="Premium nuts · selected coffee · authentic taste" data-ar="مكسرات فاخرة · قهوة مختارة · طعم أصيل" data-ur="مكسرات فاخرة · قهوة مختارة · طعم أصيل">مكسرات فاخرة · قهوة مختارة · طعم أصيل</p>
      <p class="hero-tag" data-en="Best prices — guaranteed" data-ar="أفضل الأسعار لدينا" data-ur="أفضل الأسعار لدينا">أفضل الأسعار لدينا</p>
    </div>
  </div>
</section>

<nav class="actionbar" aria-label="Quick contact">
  <div class="wrap">
    <a class="act wa" href="{wa_link('السلام عليكم، أرغب بالاستفسار عن المنتجات')}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-4.3-2.5 10 10 0 0 1-2.1-3c-.2-.5-.3-1.2 0-1.7.2-.4.6-1 .9-1.1l.6-.1h.5c.3 0 .5.1.6.5l.7 1.7c.1.2 0 .4-.1.6l-.4.5c-.1.2-.3.3-.1.6a7 7 0 0 0 3.2 2.8c.3.1.4 0 .6-.1l.8-.9c.2-.2.3-.2.6-.1l1.6.8c.3.1.4.2.5.3.1.3 0 1-.1 1.4Z"/></svg>
      <span data-en="WhatsApp" data-ar="واتساب" data-ur="واٹس ایپ">واتساب</span>
    </a>
    <a class="act loc" href="#location">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>
      <span data-en="Location" data-ar="الموقع" data-ur="لوکیشن">الموقع</span>
    </a>
    <a class="act call" href="tel:{TEL}">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2Z"/></svg>
      <span data-en="Call" data-ar="اتصال" data-ur="کال">اتصال</span>
    </a>
  </div>
</nav>

<main class="wrap">
  <section class="intro">
    <div class="eyebrow" data-en="Since the first scoop" data-ar="من أول غرفة" data-ur="پہلی مقدار سے">من أول غرفة</div>
    <h2 data-en="Nuts, spices and coffee — weighed fresh, every day" data-ar="مكسرات وبهارات وقهوة — تُوزن طازجة كل يوم" data-ur="میوے، مصالحے اور قہوہ — ہر روز تازہ وزن کیے جاتے ہیں">مكسرات وبهارات وقهوة — تُوزن طازجة كل يوم</h2>
    <p data-en="We grind spices in front of you, roast the nuts in small batches and pack everything by weight, for homes and for kitchens that buy in bulk."
       data-ar="نطحن البهارات أمامك، ونحمص المكسرات بكميات صغيرة، ونعبئ كل شيء بالوزن — للبيوت وللمطابخ التي تشتري بالجملة."
       data-ur="ہم مصالحے آپ کے سامنے پیستے ہیں، میوے چھوٹی مقدار میں بھونتے ہیں اور ہر چیز وزن کے حساب سے پیک کرتے ہیں — گھروں اور تھوک میں خریدنے والے باورچیوں کے لیے۔">نطحن البهارات أمامك، ونحمص المكسرات بكميات صغيرة، ونعبئ كل شيء بالوزن — للبيوت وللمطابخ التي تشتري بالجملة.</p>
  </section>

  <div class="cats" id="cats" role="tablist">
{cat_btns}
  </div>

  <section class="grid" id="grid" aria-live="polite">
{cards}
  </section>
  <p class="empty" id="empty" data-en="No products in this category." data-ar="لا توجد منتجات في هذا القسم." data-ur="اس کیٹگری میں کوئی پروڈکٹ نہیں۔">لا توجد منتجات في هذا القسم.</p>

  <section class="features">
    <h2 data-en="Why buy from us" data-ar="لماذا تشتري من عندنا" data-ur="ہم سے کیوں خریدیں">لماذا تشتري من عندنا</h2>
    <p class="lead" data-en="Four simple reasons the neighbourhood keeps coming back." data-ar="أربعة أسباب بسيطة تجعل أهل الحي يعودون إلينا." data-ur="چار سادہ وجوہات جن کی بنا پر محلہ والے دوبارہ آتے ہیں۔">أربعة أسباب بسيطة تجعل أهل الحي يعودون إلينا.</p>
    <div class="f-grid">
      <div class="f-item">
        <div class="f-ico"><svg viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l3 3M15 15l3 3M18 6l-3 3M9 15l-3 3"/><circle cx="12" cy="12" r="3"/></svg></div>
        <h3 data-en="Ground on order" data-ar="طحن عند الطلب" data-ur="آرڈر پر پیسنا">طحن عند الطلب</h3>
        <p data-en="Spices are ground the moment you order — aroma stays in the bag." data-ar="تُطحن البهارات لحظة الطلب — تبقى الرائحة في الكيس." data-ur="مصالحے آرڈر کے وقت پیسے جاتے ہیں — خوشبو تھیلی میں محفوظ رہتی ہے۔">تُطحن البهارات لحظة الطلب — تبقى الرائحة في الكيس.</p>
      </div>
      <div class="f-item">
        <div class="f-ico"><svg viewBox="0 0 24 24"><path d="M20 7 9 18l-5-5"/></svg></div>
        <h3 data-en="Selected nuts" data-ar="مكسرات منتقاة" data-ur="منتخب میوے">مكسرات منتقاة</h3>
        <p data-en="Sorted by hand, no broken pieces or fillers in the mix." data-ar="تُفرز يدوياً، بلا قطع مكسورة أو إضافات في الخلطة." data-ur="ہاتھ سے چھانٹی، مکس میں ٹوٹے دانے یا ملاوٹ نہیں۔">تُفرز يدوياً، بلا قطع مكسورة أو إضافات في الخلطة.</p>
      </div>
      <div class="f-item">
        <div class="f-ico"><svg viewBox="0 0 24 24"><path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
        <h3 data-en="Best price" data-ar="أفضل سعر" data-ur="بہترین قیمت">أفضل سعر</h3>
        <p data-en="Direct supply, retail or wholesale — the price is on the scale." data-ar="توريد مباشر، تجزئة أو جملة — السعر على الميزان." data-ur="براہِ راست سپلائی، پرچون یا تھوک — قیمت ترازو پر۔">توريد مباشر، تجزئة أو جملة — السعر على الميزان.</p>
      </div>
      <div class="f-item">
        <div class="f-ico"><svg viewBox="0 0 24 24"><path d="M4 7h16l-1.5 12h-13L4 7Z"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/></svg></div>
        <h3 data-en="Packed your way" data-ar="تعبئة على طريقتك" data-ur="آپ کی مرضی سے پیکنگ">تعبئة على طريقتك</h3>
        <p data-en="From a 250 g home pack to a full catering sack." data-ar="من عبوة 250 غرام للبيت إلى كيس كامل للتموين." data-ur="گھر کے 250 گرام پیک سے لے کر پورے کیٹرنگ تھیلے تک۔">من عبوة 250 غرام للبيت إلى كيس كامل للتموين.</p>
      </div>
    </div>
  </section>

  <section class="loc" id="location">
    <h2 data-en="Find us" data-ar="موقعنا" data-ur="ہم کہاں ہیں">موقعنا</h2>
    <div class="loc-card">
      <div class="map">
        <div class="pin">
          <div class="pin-dot"><svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg></div>
          <p data-en="Dammam — Al-Adama" data-ar="الدمام — العدامة" data-ur="الدمام — العدامة">الدمام — العدامة</p>
          <small data-en="Tap “Open in Maps” for the exact pin" data-ar="اضغط «افتح في الخرائط» للموقع الدقيق" data-ur="درست لوکیشن کے لیے «نقشے میں کھولیں» دبائیں">اضغط «افتح في الخرائط» للموقع الدقيق</small>
        </div>
      </div>
      <div class="loc-info">
        <h3 data-en="Matahin Nuts &amp; Spices" data-ar="مطاحن مكسرات بهارات" data-ur="مطاحن مكسرات بهارات">مطاحن مكسرات بهارات</h3>
        <p class="sub" data-en="Nuts mill · spices · Arabic coffee" data-ar="مطاحن مكسرات · بهارات · قهوة عربية" data-ur="مطحنہ میوے · مصالحے · عربی قہوہ">مطاحن مكسرات · بهارات · قهوة عربية</p>
        <div class="row">
          <svg viewBox="0 0 24 24"><path d="M12 21s7-7.8 7-13a7 7 0 1 0-14 0c0 5.2 7 13 7 13Z"/><circle cx="12" cy="8" r="2.5"/></svg>
          <div><b data-en="Address" data-ar="العنوان" data-ur="پتہ">العنوان</b>
          <span data-en="Al-Adama district, Dammam, Saudi Arabia" data-ar="حي العدامة، الدمام، المملكة العربية السعودية" data-ur="العدامة، الدمام، سعودی عرب">حي العدامة، الدمام، المملكة العربية السعودية</span></div>
        </div>
        <div class="row">
          <svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2Z"/></svg>
          <div><b data-en="Phone &amp; WhatsApp" data-ar="الهاتف وواتساب" data-ur="فون اور واٹس ایپ">الهاتف وواتساب</b>
          <a href="tel:{TEL}" dir="ltr">+966 53 737 3257</a></div>
        </div>
        <div class="row">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
          <div><b data-en="Orders" data-ar="الطلبات" data-ur="آرڈرز">الطلبات</b>
          <span data-en="WhatsApp us your list — we weigh and pack it for pickup or delivery." data-ar="أرسل قائمتك على واتساب — نوزنها ونعبئها للاستلام أو التوصيل." data-ur="اپنی فہرست واٹس ایپ پر بھیجیں — ہم وزن کر کے پیک کر دیتے ہیں۔">أرسل قائمتك على واتساب — نوزنها ونعبئها للاستلام أو التوصيل.</span></div>
        </div>
        <div class="loc-btns">
          <a class="btn-wa" href="{wa_link('السلام عليكم، أرغب بالاستفسار عن المنتجات')}" target="_blank" rel="noopener" data-en="WhatsApp us" data-ar="واتساب" data-ur="واٹس ایپ">واتساب</a>
          <a class="btn-map" href="https://www.google.com/maps/search/?api=1&amp;query=%D9%85%D8%B7%D8%A7%D8%AD%D9%86%20%D9%85%D9%83%D8%B3%D8%B1%D8%A7%D8%AA%20%D8%A8%D9%87%D8%A7%D8%B1%D8%A7%D8%AA%20%D8%A7%D9%84%D8%AF%D9%85%D8%A7%D9%85%20%D8%A7%D9%84%D8%B9%D8%AF%D8%A7%D9%85%D8%A9" target="_blank" rel="noopener" data-en="Open in Maps" data-ar="افتح في الخرائط" data-ur="نقشے میں کھولیں">افتح في الخرائط</a>
        </div>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <svg viewBox="0 0 48 48"><path d="M14 30c0-3 2-5 5-6-2-1-3-3-3-5 3 0 5 1 6 3 1-4 4-7 8-7-1 4-3 7-6 9 3 0 6 1 8 3-2 2-5 3-8 2 1 2 1 4 0 6-2-1-4-3-4-5-2 2-4 3-6 3z"/></svg>
        <div>
          <b data-en="Matahin Nuts &amp; Spices" data-ar="مطاحن مكسرات بهارات" data-ur="مطاحن مكسرات بهارات">مطاحن مكسرات بهارات</b>
          <span data-en="Dammam · Al-Adama · Saudi Arabia" data-ar="الدمام · العدامة · المملكة العربية السعودية" data-ur="الدمام · العدامة · سعودی عرب">الدمام · العدامة · المملكة العربية السعودية</span>
        </div>
      </div>
      <div class="foot-links">
        <a href="tel:{TEL}" dir="ltr">+966 53 737 3257</a>
        <a href="{wa_link('السلام عليكم')}" target="_blank" rel="noopener">WhatsApp</a>
        <a href="#top" data-en="Back to top" data-ar="أعلى الصفحة" data-ur="اوپر جائیں">أعلى الصفحة</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span data-en="© 2026 Matahin Nuts &amp; Spices. All rights reserved." data-ar="© 2026 مطاحن مكسرات بهارات. جميع الحقوق محفوظة." data-ur="© 2026 مطاحن مكسرات بهارات۔ جملہ حقوق محفوظ ہیں۔">© 2026 مطاحن مكسرات بهارات. جميع الحقوق محفوظة.</span>
      <span data-en="Site by ABS Est." data-ar="تصميم ABS Est." data-ur="ڈیزائن ABS Est.">تصميم ABS Est.</span>
    </div>
  </div>
</footer>

<a class="fab" href="{wa_link('السلام عليكم، أرغب بالاستفسار عن المنتجات')}" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-4.3-2.5 10 10 0 0 1-2.1-3c-.2-.5-.3-1.2 0-1.7.2-.4.6-1 .9-1.1l.6-.1h.5c.3 0 .5.1.6.5l.7 1.7c.1.2 0 .4-.1.6l-.4.5c-.1.2-.3.3-.1.6a7 7 0 0 0 3.2 2.8c.3.1.4 0 .6-.1l.8-.9c.2-.2.3-.2.6-.1l1.6.8c.3.1.4.2.5.3.1.3 0 1-.1 1.4Z"/></svg>
</a>

<script>
(function(){{
  var langBtns = document.querySelectorAll('.lang button');
  function setLang(lang){{
    var rtl = (lang === 'ar' || lang === 'ur');
    document.documentElement.lang = lang;
    document.documentElement.dir = rtl ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-en]').forEach(function(el){{
      var v = el.getAttribute('data-' + lang);
      if (v === null) return;
      if (el.tagName === 'A' && el.hasAttribute('data-href-' + lang)) {{
        el.setAttribute('href', el.getAttribute('data-href-' + lang));
      }}
      el.innerHTML = v;
    }});
    langBtns.forEach(function(b){{ b.classList.toggle('is-on', b.dataset.lang === lang); }});
    try {{ localStorage.setItem('matahin-lang', lang); }} catch(e){{}}
  }}
  langBtns.forEach(function(b){{ b.addEventListener('click', function(){{ setLang(b.dataset.lang); }}); }});

  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('.p-card');
  var empty = document.getElementById('empty');
  chips.forEach(function(chip){{
    chip.addEventListener('click', function(){{
      chips.forEach(function(c){{ c.classList.remove('is-on'); }});
      chip.classList.add('is-on');
      var f = chip.dataset.filter, shown = 0;
      cards.forEach(function(card){{
        var ok = (f === 'all' || card.dataset.cat === f);
        card.style.display = ok ? '' : 'none';
        if (ok) shown++;
      }});
      empty.style.display = shown ? 'none' : 'block';
    }});
  }});

  var saved = null;
  try {{ saved = localStorage.getItem('matahin-lang'); }} catch(e){{}}
  if (saved) setLang(saved);
}})();
</script>
</body>
</html>
"""

open(f"{ROOT}/index.html", "w", encoding="utf-8").write(HTML)
print("written", len(HTML), "bytes")
