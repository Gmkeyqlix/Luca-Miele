# SANTO email plan: "Your £10" payday weekend (Fri 25 – Sun 27 Sep 2026)

## LIVE STATUS (created 25 Sep 2026, 22:45 UK): everything is built, nothing is sent

| What | Where | Status |
|---|---|---|
| Discount **PAYDAY10**: £10 off, no minimum, once per customer, ends **Sun 27 Sep 23:59 BST** (can stack with free delivery, not with other money-off codes) | Shopify → Discounts (`gid://shopify/DiscountCodeNode/1796564386049`) | **Active now** |
| Segment **Real engaged (click 60d / order 120d / new 15d)**: **5,099 profiles** | Klaviyo `V85MZ5` | Live |
| Segment **PAYDAY10 · opened/clicked since Sat send, no order** (fills after email 1 sends) | Klaviyo `VKdABa` | Live |
| Campaign **1: Sat 26 Sep 11:00 BST, "Your £10"**. Subject: "{name}, £10 off anything. Ends Sunday." Excludes the cold and bounced DIAG segments | Klaviyo `01M3D8J8DVJQEKMFCGPK1XP6VG` | **Draft, send time pre-filled** |
| Campaign **3: Sun 27 Sep 18:00 BST, "Your £10 ends tonight"**, to openers and clickers with no order | Klaviyo `01M3D8JGK4W6TTN6H159DSAN8S` | **Draft, send time pre-filled** |
| Campaign **2 (optional), "What your £10 gets you"** | Klaviyo `01M3D8JNAKDA1YHH8Z505MZQ66` | Draft, no time set. Only use it if you want a third email |

**Changes from the original plan:**
- **Shared honest code instead of unique codes.** Klaviyo's automatic Shopify unique codes can only be switched on in its web app, and uploading ~14k codes by API wasn't reliable. `PAYDAY10` is shared and once per customer, and the copy no longer claims the code is "yours alone". To switch to unique codes later: Klaviyo → Coupons → Create → Shopify, then replace `PAYDAY10` in the templates with `{% coupon_code 'NAME' %}`.
- **Timing.** The Friday 18:00 slot passed while things were being built, so email 1 moves to Saturday 11:00 ("payday weekend"). The deadline stays Sunday 23:59. Email 2 is optional, to protect unsubscribes.

**To go live:** open each campaign in Klaviyo (`klaviyo.com/campaign/{id}/wizard`), send a test to yourself, click the button in the test and check the £10 comes off at checkout, then press **Schedule**.

## Why this, from your own data
- Last 12 months: 47 campaigns, ~1.1M sends, **£7,045 attributed revenue**. The typical campaign gets **0.3% clicks** (the fashion average is 1–1.5%) and **0.4–1.1% unsubscribes** (the norm is ~0.2%).
- Three emails beat everything else, and all three felt like **"something of yours is waiting"**:
  - "your £9.34 store credit expires in 7 days": **5.05% clicks, 39 orders, £1,230**, which is 17% of the year's campaign revenue.
  - Its resend: 3.11% clicks, 16 orders, £631.
  - "you forgot your free gift": 4.15% clicks.
- The format of the winner: **almost plain text, one button, no product grid.**
- The losers were generic sale, drop and season emails. "🍂 Fall Essentials – Up to 80% Off" got 0.28%, and the drop-day series got 0.24–0.27%.
- Shopify, last 3 weeks: sweatshirts and zip hoodies overtook shorts, so the season has turned. Today is the last Friday of the month, which is UK payday.

## What changes from the £9.34 email (and why)
That email's pull came from three things: money that feels already yours, a personal-looking note, and a deadline. It also had problems that are now illegal in the UK under the DMCC Act 2024 (CMA direct fines since April 2025, up to 10% of global turnover):
- the credit wasn't real account credit (everyone got the same code, `SANTO-9F34KQ2M`);
- the deadline contradicted itself ("48 hours" / "7 days" / "49 hours");
- it said "cannot be reissued or extended" and was then resent;
- the subject was dressed as an "[Account notice]".

This campaign keeps all three pull factors and makes each one true:

| Pull factor | £9.34 email | This campaign |
|---|---|---|
| "It's already mine" | Fake credit, shared code | **Real unique single-use £10 code per person** (Klaviyo coupon) |
| Personal, plain note | Plain text + one button ✓ | Same format, SANTO brand type and colours |
| Deadline | Contradictory, then extended | **One real deadline: Sunday 27 Sep 23:59, never extended** |
| Framing | "[Account notice]" | Honest promo: "£10 off anything, from us" |

What it costs: the £10 only comes off orders that use it. That's the same as the "credit" cost you before.

## The sequence
| # | When (UK) | Audience | Subject A / B | Preview | Content |
|---|---|---|---|---|---|
| 1 | **Fri 25 Sep, 18:00** (payday evening; if you miss it, Sat 11:00) | Real-engaged audience (see Audience) | A: `{{ first_name }}, £10 off anything. Ends Sunday.` · B: `Your £10 code is inside` | "No minimum spend. Your code works until Sunday 23:59." | Plain note, unique code, one button "Use my £10" |
| 2 | **Sat 26 Sep, 11:00** | Email 1 recipients **who haven't ordered** | `What your £10 gets you` | "Retro Essence zip-up for £67.99. Here's the rest." | 3 in-stock autumn heroes with real prices before/after £10 |
| 3 | **Sun 27 Sep, 12:00** | Recipients who **opened or clicked but haven't ordered** | `Your £10 ends tonight` | "Last day for your £10. No minimum spend." | Short: code, "we won't reissue it", one button |

All three are built in `out/` (Klaviyo-ready HTML, 3–5 KB each, dark-mode safe, one call to action). Previews are in `preview/*.png`.

## Audience (fixes the unsubscribe problem as well as the revenue)
Your `4. [NEW] Engaged Non-Purchasers (90d)` segment has **31,774 people** because it counts Apple Mail Privacy auto-opens. Real human engagement is probably a few thousand. Sending to ~40k mostly-unengaged profiles is what drives the 0.4–1.1% unsubscribes and 0.3% clicks (research `E3`).

Build one new segment, **"Real engaged (click/order)"**, from:
- **Clicked Email** at least once in the last **60 days**, OR
- **Placed Order** at least once in the last **120 days**, OR
- **Subscribed to Email Marketing** in the last **15 days**,
- AND can receive email marketing.

Also include `VIP Customers` and `Ordered more than once last 6 months`.

- **Exclude:** `DIAG - Never subscribed, never bought (cold)`, `DIAG - Bounced / invalid / suppressed`.
- Expect a much smaller send (a few thousand to ~10k). That's the point: fewer, real readers give better clicks, fewer unsubscribes, and better inbox placement for every future send.
- Don't email the `DIAG - Past customers, no email consent (soft opt-in pool)` segment unless checkout clearly offered an opt-out (UK PECR soft opt-in).
- Smart Sending on. UTM `payday10_sep26` on every link.
- Separately, check the live flow **"25 email flow (everyone)"**. A 25-email sequence to everyone is a likely driver of the unsubscribe rate.

## Setup (≈10 minutes)
1. **Shopify → Discounts → Create:** amount off order, £10, **no minimum**, one use per customer, ends **27 Sep 23:59 BST**. Then generate unique codes through Klaviyo:
2. **Klaviyo → Coupons → Create coupon** named `SANTO10AUTUMN`, type **Unique**, linked to that Shopify discount, prefix `SANTO10-`. The templates already use `{% coupon_code 'SANTO10AUTUMN' %}`.
3. Import the three HTML files as templates (or I push them via the API), create the three campaigns with the audiences above, and send test emails to yourself. **Check that the code in the button link matches the code shown.**
4. Schedule. Email 2 excludes anyone who "Placed Order since Email 1". Email 3 includes "opened or clicked email 1 or 2" and excludes "placed order".

## Already done
- Three **draft templates** are in Klaviyo (nothing is scheduled or sent):
  - `YkTPC7`: 1 Fri, "Your £10"
  - `T84bHD`: 2 Sat, "What your £10 gets you"
  - `YnFzKb`: 3 Sun, "Ends tonight"
  - Edit them at `klaviyo.com/email-editor/{id}/edit`.
- **Coupon caveat:** each email renders `{% coupon_code %}` itself, so emails 2 and 3 may show a *different* unique code from email 1. Protect against this by setting the Shopify discount to **"Limit to one use per customer"**, so each person still gets £10 once whichever code they use. Check it in the Klaviyo preview with a test profile.

## Products (live Shopify, 25 Sep)
In stock, featured:
- Retro Essence Washed Zip-Up Hoodie, £77.99 (9,257 units)
- Grunge Graffiti Full-Zip Hoodie, £73.99 (11,910)
- X-Ray Skeleton Waffle Long Sleeve, £40.99 (3,551)

**Not featured until you confirm they ship:** the actual top sellers of the last 3 weeks show **negative stock** but keep selling:
- DON'T F*CK YOURSELF… waffle sweatshirt (−215)
- I THINK ABOUT YOU… sweatshirt (−211)
- FASHION KILLA (−261)
- Washed Denim Fur jacket (−103)

If they're made to order and ship fine, swap them into Email 2. They're what people are actually buying.

## What to expect (honest range)
The comparable honest-mechanic sends were the £9.34 pair (£1,861 across two sends) and "free gift" (4.15% clicks). Expect **3–6% clicks on Email 1** (a smaller, real-engaged audience clicks at a higher rate) and **roughly £1k–£2.5k across the weekend**. Nearly all of the £9.34 revenue came from engaged buyers, so cutting the cold profiles should cost little revenue and save a lot of unsubscribes. That's a range, not a promise. Your real list and discount redemption will decide it.

## What the research changed (research/email/E1–E3)
- **Subjects:** top streetwear subjects are short (median 25 characters) and name the product or offer, with 0 exclamation marks and 0 discount percentages (`E1`). Preview text adds a new fact rather than repeating the subject (one test: +95.6% revenue per email).
- **Letter layout, 2–5 links, one main button.** Plainer emails won HubSpot's tests, and 2–5 links convert best across 317k campaigns (`E1`, `E2`).
- **The mechanics that won are real psychology:** endowment and loss aversion, an exact £ amount, a named deadline, no friction ("no minimum"). People holding gift cards spend more than the balance (68–75%). Short deadlines get used more (`E2`).
- **Legal:** since April 2025 the CMA fines directly (StubHub £889k, Marks Electrical £720k). Marketing must be recognisable as marketing from the subject line (CAP 2.1): the ICO fined Flybe £70k for marketing dressed as service messages, and the FTC fined Experian $650k. **So: no "[Account notice]" prefix, no reissuing the same credit, exact date and time in the email** (`E3`).
- **Deliverability:** Gmail and Yahoo reject non-compliant bulk mail since Nov 2025. Keep spam complaints under 0.1%, keep one-click unsubscribe, check DMARC on `send.santo.clothing`, and keep HTML under ~90 KB (ours are 3–5 KB) (`E3`).
- **Also found:** automated flows earn ~22× more per email than campaigns (`E1`). Next paydays are 23 Oct, 30 Oct and 27 Nov. The Met Office outlook leans warm and wet, so "rain / layering" beats "cold" until a real cold snap (`E2`).

## Stop doing
- "[Account notice]" and other transactional-looking subjects on promos.
- Shared codes presented as personal "account credit". Contradictory or extended deadlines. Reissuing "can't be reissued" offers.
- "Up to 80% off" unless ~10% of items really are 80% off. Stacked codes (FIVER + GLFS) and repeated deep discounts, which lower future spend (`E2`).
- Drop emails with no announcement beforehand. Top brands announce a fixed drop time days ahead (`E1`).
- Sending to open-based "engaged" segments inflated by Apple Mail Privacy.

## After it sends (to learn, not guess)
- Compare A/B subjects on **click rate**, not opens (Apple Mail Privacy Protection inflates opens).
- Track redemptions of the code and revenue per recipient against the £0.0064 12-month average.
- If unsubscribes stay under 0.3% with the engaged-only audience, make that audience the default.
