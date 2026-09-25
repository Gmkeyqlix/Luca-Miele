# SANTO email plan: "Your £10" payday weekend (Fri 25 – Sun 27 Sep 2026)

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
| 1 | **Fri 25 Sep, 18:00** (payday evening) | Engaged 90d + one-time buyers at risk + VIP / repeat buyers (see Audience) | A: `{{ first_name }}, £10 off anything. It's yours.` · B: `£10 for you. Ends Sunday.` | "No minimum spend. Your code works until Sunday 23:59." | Plain note, unique code, one button "Use my £10" |
| 2 | **Sat 26 Sep, 11:00** | Email 1 recipients **who haven't ordered** | `What your £10 gets you` | "Retro Essence zip-up for £67.99. Here's the rest." | 3 in-stock autumn heroes with real prices before/after £10 |
| 3 | **Sun 27 Sep, 12:00** | Recipients who **opened or clicked but haven't ordered** | `Your £10 ends tonight` | "Last day for your £10. No minimum spend." | Short: code, "we won't reissue it", one button |

All three are built in `out/` (Klaviyo-ready HTML, 3–5 KB each, dark-mode safe, one call to action). Previews are in `preview/*.png`.

## Audience (fixes the unsubscribe problem as well as the revenue)
- **Include:** `4. [NEW] Engaged Non-Purchasers (90d)`, `[NEW] One-Time Buyers at Risk (60–120d)`, `VIP Customers`, `Ordered more than once last 6 months`.
- **Exclude:** `DIAG - Never subscribed, never bought (cold)`, `DIAG - Bounced / invalid / suppressed`, and anyone who hasn't opened or clicked in 180 days.
- Smart Sending on. UTM `payday10_sep26` on every link.
- Separately, check the live flow **"25 email flow (everyone)"**. A 25-email sequence to everyone is a likely driver of the unsubscribe rate.

## Setup (≈10 minutes)
1. **Shopify → Discounts → Create:** amount off order, £10, **no minimum**, one use per customer, ends **27 Sep 23:59 BST**. Then generate unique codes through Klaviyo:
2. **Klaviyo → Coupons → Create coupon** named `SANTO10AUTUMN`, type **Unique**, linked to that Shopify discount, prefix `SANTO10-`. The templates already use `{% coupon_code 'SANTO10AUTUMN' %}`.
3. Import the three HTML files as templates (or I push them via the API), create the three campaigns with the audiences above, and send test emails to yourself. **Check that the code in the button link matches the code shown.**
4. Schedule. Email 2 excludes anyone who "Placed Order since Email 1". Email 3 includes "opened or clicked email 1 or 2" and excludes "placed order".

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
The comparable honest-mechanic sends were the £9.34 pair (£1,861 across two sends) and "free gift" (4.15% clicks). Expect **3–5% clicks on Email 1 and roughly £1.5k–£3k across the weekend** from a ~25–35k engaged audience. That's a range, not a promise. Your real list and discount redemption will decide it.

## After it sends (to learn, not guess)
- Compare A/B subjects on **click rate**, not opens (Apple Mail Privacy Protection inflates opens).
- Track redemptions of the code and revenue per recipient against the £0.0064 12-month average.
- If unsubscribes stay under 0.3% with the engaged-only audience, make that audience the default.
