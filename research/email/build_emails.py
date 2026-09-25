#!/usr/bin/env python3
"""Build the 3-email "Your £10" payday weekend campaign as Klaviyo-ready HTML.

Honest version of the store-credit mechanic: every recipient gets a real,
unique, single-use £10 code (Klaviyo coupon tag), a real deadline that is
never extended, and no transactional disguise. Output: research/email/out/*.html
"""

from pathlib import Path

OUT = Path(__file__).parent / "out"
COUPON = "{% coupon_code 'SANTO10AUTUMN' %}"  # Klaviyo unique-code coupon (create it first, see PLAN)
DEADLINE = "Sunday 27 September, 23:59"
NAME = "{{ first_name|default:'' }}"
HI = "{% if person.first_name %}Hi {{ person.first_name }},{% else %}Hi,{% endif %}"
SHOP = "https://santo.clothing"
UTM = "utm_source=klaviyo&utm_medium=email&utm_campaign=payday10_sep26"

INK, BONE, PAPER, RED, ASPHALT = "#0A0A0B", "#F3F0EA", "#FFFFFF", "#E10600", "#242426"

PRODUCTS = [  # real, in stock (Shopify 2026-09-25), real prices
    {"title": "Retro Essence Washed Zip-Up Hoodie", "handle": "retro-essence-washed-oversized-zip-up-hoodie", "price": 77.99,
     "img": "https://cdn.shopify.com/s/files/1/0606/0598/9121/files/Untitled_design_12.png?v=1765545515"},
    {"title": "Grunge Graffiti Full-Zip Hoodie", "handle": "graffiti-grunge-full-zip-hoodie", "price": 73.99,
     "img": "https://cdn.shopify.com/s/files/1/0606/0598/9121/files/12233.jpg?v=1753340564"},
    {"title": "X-Ray Skeleton Waffle Long Sleeve", "handle": "x-ray-skeleton-waffle-long-sleeve-t-shirt", "price": 40.99,
     "img": "https://cdn.shopify.com/s/files/1/0606/0598/9121/files/5_988b12a2-ee37-476e-806e-9c0b092b7721.jpg?v=1752705367"},
]


def link(path):
    sep = "&" if "?" in path else "?"
    return f"{SHOP}{path}{sep}{UTM}"


def code_link(redirect="/collections/new-arrivals-all"):
    # Shopify pre-applies the code at checkout
    return f"{SHOP}/discount/{COUPON}?redirect={redirect}&{UTM}"


def shell(preheader, body):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>Santo</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter+Tight:wght@400;600&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
<style>
 body{{margin:0;padding:0;background:{PAPER};}}
 .wrap{{max-width:560px;margin:0 auto;padding:28px 22px 36px;font-family:'Inter Tight',Arial,Helvetica,sans-serif;color:{INK};font-size:17px;line-height:1.5;}}
 .logo{{font-family:'Archivo Black','Arial Black',Arial,sans-serif;font-size:20px;letter-spacing:1px;margin:0 0 28px;}}
 h1{{font-family:'Archivo Black','Arial Black',Arial,sans-serif;font-size:34px;line-height:1.05;text-transform:uppercase;margin:0 0 18px;font-weight:400;}}
 p{{margin:0 0 16px;}}
 .code{{font-family:'Space Mono','Courier New',monospace;font-weight:700;font-size:22px;letter-spacing:1px;background:{BONE};padding:14px 16px;display:inline-block;margin:4px 0 18px;}}
 .dl{{font-family:'Space Mono','Courier New',monospace;font-weight:700;color:{RED};}}
 .btn{{display:inline-block;background:{INK};color:{BONE}!important;text-decoration:none;font-weight:600;font-size:17px;padding:16px 26px;}}
 .muted{{color:{ASPHALT};font-size:14px;}}
 .fine{{color:#6b6b6f;font-size:12px;line-height:1.45;margin-top:28px;}}
 a{{color:{INK};}}
 .prod td{{padding:0 0 22px;vertical-align:top;}}
 .prod img{{display:block;width:100%;max-width:516px;height:auto;background:{BONE};}}
 .pname{{font-weight:600;margin:10px 0 2px;}}
 .price{{font-family:'Space Mono','Courier New',monospace;font-weight:700;}}
 .was{{text-decoration:line-through;color:#8a8a8e;font-weight:400;}}
 @media (prefers-color-scheme: dark){{ body,.wrap{{background:{INK}!important;color:{BONE}!important;}} a{{color:{BONE}!important;}}
   .code{{background:{ASPHALT}!important;color:{BONE}!important;}} .btn{{background:{BONE}!important;color:{INK}!important;}} .muted{{color:#c9c6bf!important;}} }}
</style></head>
<body>
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{preheader}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<div class="wrap">
<div class="logo">SANTO</div>
{body}
<div class="fine">Your £10 code works once, on anything, with no minimum spend. It can't be combined with other codes and ends {DEADLINE} (UK time).<br><br>
You're getting this because you signed up at santo.clothing. {{% unsubscribe 'Unsubscribe' %}}.<br>{{{{ organization.name }}}} {{{{ organization.full_address }}}}</div>
</div></body></html>"""


def email1():
    body = f"""
<p>{HI}</p>
<p>It's payday and the weather has turned. So here's <strong>£10 off anything</strong> on Santo, from us.</p>
<div class="code">{COUPON}</div>
<p>It's yours alone and works once. No minimum spend.<br>It ends <span class="dl">{DEADLINE}</span>. We won't extend it.</p>
<p><a class="btn" href="{code_link()}">Use my £10</a></p>
<p class="muted">Tap the button and the £10 comes off at checkout automatically.</p>
<p class="muted">What people are layering up in right now:<br>
<a href="{link('/products/' + PRODUCTS[0]['handle'])}">{PRODUCTS[0]['title']}</a> · <a href="{link('/products/' + PRODUCTS[1]['handle'])}">{PRODUCTS[1]['title']}</a> · <a href="{link('/collections/all-hoodies')}">All hoodies</a></p>
<p>Santo</p>"""
    return shell("No minimum spend. Your code works until Sunday 23:59.", body)


def email2():
    rows = ""
    for pr in PRODUCTS:
        after = pr["price"] - 10
        rows += f"""<tr><td><a href="{code_link('/products/' + pr['handle'])}"><img src="{pr['img']}" alt="{pr['title']}" width="516"></a>
<div class="pname">{pr['title']}</div>
<div class="price"><span class="was">£{pr['price']:.2f}</span> &nbsp;£{after:.2f} with your code</div></td></tr>"""
    body = f"""
<h1>What your £10 gets you</h1>
<p>{HI} your £10 is still there. Here's what it does to the pieces people are buying as the weather turns.</p>
<table class="prod" role="presentation" width="100%" cellpadding="0" cellspacing="0">{rows}</table>
<p>Your code: <span class="code" style="font-size:17px;padding:8px 10px;">{COUPON}</span></p>
<p><a class="btn" href="{code_link('/collections/all-hoodies')}">Shop hoodies with £10 off</a></p>
<p class="muted">Ends <span class="dl">{DEADLINE}</span>.</p>"""
    return shell("Retro Essence zip-up for £67.99. Here's the rest.", body)


def email3():
    body = f"""
<p>{HI}</p>
<p>Your £10 ends tonight at <span class="dl">23:59</span>.</p>
<div class="code">{COUPON}</div>
<p>After that it's gone, and we won't reissue it.</p>
<p><a class="btn" href="{code_link()}">Use it before midnight</a></p>
<p>Santo</p>"""
    return shell("Last day for your £10. No minimum spend.", body)


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in [("1-fri-your-10", email1), ("2-sat-what-it-gets-you", email2), ("3-sun-ends-tonight", email3)]:
        html = fn()
        (OUT / f"{name}.html").write_text(html)
        print(f"{name}.html  {len(html.encode()) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
