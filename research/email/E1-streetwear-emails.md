# E1: What top streetwear and fashion brand emails look like, and why they work

Research date: 2026-09-25. Angle: teardown of real emails from Corteiz, Represent, Unknown London, Aimé Leon Dore (ALD), Kith, Stüssy, Supreme, SKIMS and Gymshark, plus published A/B tests and apparel case studies.

## How this was researched, and its limits
- **Access.** milled.com, reallygoodemails.com, klaviyo.com, stussy.com, kith.com, dtcpatterns, growthcurve and web.archive.org are all **blocked by the egress proxy** (WebFetch and curl both got CONNECT 403). I could not open any email body. Everything below comes from **search-engine index data**: Milled page titles (which are the verbatim subject lines), search snippets (sometimes dates and body lines) and published articles.
- **What that means.** Evidence on subject lines, naming, cadence and mechanics is solid. Evidence on inside-the-email structure (product count, CTA count, image vs text) is thin. I say so wherever it matters.
- **Coverage gaps.** Search returned no Milled archive for Trapstar, Broken Planet, Hellstar, Sp5der, Minus Two or Palace's own list (only retailers' emails about them). The session's web-search budget ran out (200 calls, shared) before I could go deeper.

### The subject-line sample (verbatim Milled titles, used in the findings below)
| Brand | Subject lines seen (Milled URL slug = subject) |
|---|---|
| Corteiz | "SOLITARY ENDS SOON. ⏳" (5 Dec 2025) — https://milled.com/crtz.xyz/solitary-ends-soon-FMyLm1Ldg_AFK38A |
| Represent | "REPRESENT x Liam Gallagher - 27.07.22", "247 Collection \| 14.04.21", "THE VIRTUS SNEAKER", "THE VAULT IS NOW OPEN", "OWNERS CLUB COLLECTION - NOW LIVE", "A Decade Of Dedication - LIVE NOW", "REPRESENT X MEGADETH - LIVE NOW", "INITIAL MULES & SANDALS - NOW LIVE", "Summer Denim", "Summer 2022 - Shop the collection", "THE BLACK FRIDAY SALE - NOW LIVE", "Introducing a smarter way to return" — e.g. https://milled.com/www-representclo-com/the-vault-is-now-open-Ya2KH-L0Qa76lVVI , https://milled.com/representclo/represent-x-liam-gallagher-27-07-22-UW5PMFNKHynvFNb9 , https://milled.com/www-representclo-com/247-collection-14-04-21-AZMhr9tyleQ5nZrD |
| Unknown London | "New Drop Online.", "Early Access Code", "CLUB KNITS + MORE", "BLACK ZIP TRACKIE RESTOCK", "CHIEF KEEF X ED HARDY", "CHIEF KEEF X ED HARDY RELOAD", "UNKNOWN X RIZLA ONLINE NOW", "THE UNKNOWN CYPHER THIS THURSDAY" — e.g. https://milled.com/unknownlondon.com-1/early-access-code-SBRdNwK-gwaglWBz , https://milled.com/unknownlondon.com-1/black-zip-trackie-restock-venxca-ui31YDcNH , https://milled.com/unknownlondon.com-1/the-unknown-cypher-this-thursday-mP9U1cmy9zuzlVOy |
| Aimé Leon Dore | "FALL / WINTER 2023 ALD GARDEN MULE", "ALD PÁPIA MOC BOOT", "CAFÉ LEON DORE", "GROTESK FOR AIMÉ LEON DORE", "ALD / NEW YORK METS COLLECTION", "END OF SEASON SALE", "ARCHIVE SALE", "END OF SEASON ARCHIVE SALE" — e.g. https://milled.com/aimeleondore.com/fall-winter-2023-ald-garden-mule-4dEWhUEy7wTtouzW |
| Kith | "A Closer Look at Kith Fall 1", "This Week at Kith", "KITH NYC: Weekly Newsletter 3/13", "Recent Arrivals", "Monday Program™ \| Kith Gotham Hoodies" — e.g. https://milled.com/kith/a-closer-look-at-kith-fall-1-4yU3slRpSHt7HEl5 |
| Stüssy | "Stüssy / Harris Tweed", "Stüssy & Our Legacy", "Stüssy / Dickies International Workgear", "Stüssy Archive", "Stüssy & Oakley" — e.g. https://milled.com/Stussy/stussy-harris-tweed-2cARYHGJKDfwDohB |
| Supreme | "Web Shop Now Open", "Online Shop Update", "Supreme/Zoo York" — https://milled.com/supreme/web-shop-now-open-8K63fdN5oup6x62j |
| SKIMS | "The Bra That Everyone Swears By", "New Arrivals Are Here", "Want 20% Off Your Next Order?", "UNLOCK ACCESS: JOIN SKIMS REWARDS", "Free Express Shipping For a Limited Time" — https://milled.com/skims |
| Gymshark | "Less than 24 hours to go...", "Shop your size in the Winter Sale", "On Sale - And In Your Size", "Your basket is nearly gone!", "24 HOURS TIL THE GYMSHARK SALE 🤯", "Introducing: The Legacy Range" — https://milled.com/gymshark-eu , https://milled.com/gymshark-eu/on-sale-and-in-your-size-F3jjg7DsXorpuIjF |

**Counts (my tally of 72 subjects).**
- **Core streetwear, 52 subjects** (Corteiz, Represent, Unknown, ALD, Kith, Stüssy, Supreme): median **25 characters**, **1 emoji** (Corteiz's ⏳), **0 exclamation marks**, **0 percentages or discount codes**, 25 of 52 in ALL CAPS.
- **SKIMS and Gymshark, 20 subjects**: median 27–29 characters, 2 emojis, 2 exclamation marks, discount language appears.
- **Bias warning:** this is the sample search engines happened to index, not a full archive.

---

## Findings

### 1. Name the thing, then add one status word. No adjectives, no offer.
- **What to do.** Build the subject from `[PRODUCT or COLLECTION] + [status]`. Status words: NOW LIVE / ONLINE NOW / RESTOCK / RELOAD / ENDS SOON / THIS THURSDAY. Keep it to about 18–30 characters. For SANTO:
  - "THE WAFFLE-KNIT SWEATSHIRT — RESTOCK"
  - "FUR-LINED DENIM JACKET. ONLINE NOW."
  - "FASHION KILLA LONG SLEEVE — BACK"
- **Why.** Across 52 subjects from the brands with the most cultural pull, almost none carry a discount, an emoji or an exclamation mark. Examples: "THE VIRTUS SNEAKER" (Represent), "BLACK ZIP TRACKIE RESTOCK" (Unknown), "ALD PÁPIA MOC BOOT" (ALD), "Stüssy / Harris Tweed". Scarcity and the product carry the email. Rebel8's browse-abandon email makes the same point: "sell out forever" does the work of a discount ([Drip, fashion examples](https://www.drip.com/blog/apparel-email-marketing-examples)).
- **Strength: B.** Many brands and many subjects, but no performance data attached.
- **SANTO.** This matches the brand rules ("lead with product", "short, certain") and is the opposite of the losing "🍂 Fall Essentials – Up to 80% Off" (0.28% click).

### 2. Drop emojis and exclamation marks from drop and season emails.
- **What to do.**
  - Zero emojis on product, season and drop emails.
  - At most one emoji, and only functional ones such as ⏳ on a real deadline.
  - Remove "!" everywhere.
- **Why.**
  - Emojis appear in 1 of 52 core-streetwear subjects.
  - Gymshark does use emojis in about 63% of emails ([Enrich Labs](https://www.enrichlabs.ai/case-study/gymshark-email-marketing), [MailCharts](https://pr.mailcharts.com/companies/gymshark-email-marketing)). But Gymshark is a mass fitness brand with a huge list, not a hype label.
  - Klaviyo's own guidance caps it at "one emoji maximum… never replacing a word" ([Klaviyo](https://www.klaviyo.com/blog/subject-lines-best-practices)).
  - The "73% of marketers say emojis help" stat ([Omnisend](https://www.omnisend.com/blog/email-marketing-statistics/)) is a survey of opinion, not a test.
- **Strength: B.**
- **SANTO.** Klaviyo auto-detected SANTO's current voice as "emoji-heavy, exclamation marks". Every one of SANTO's 3 winners had no emoji.

### 3. SANTO's best emails already look like account or service notices. Make that a format.
- **What to do.** Build a recurring "notice" format:
  - bracketed tag, e.g. `[Account notice]`, `[Order update]`, `[Restock notice]`
  - one concrete object with a number (£ value, size, hours left)
  - a preview line that adds a new fact
  - Example: "[Restock notice] Waffle-knit sweatshirt, your size (M) is back" / preview "32 units. No code needed."
- **Why.**
  - SANTO's internal data is the strongest evidence in this file: store credit got 5.05% click and 3.11% on the clone; the free-gift email got 4.15%. Both are 10–20x the typical 0.25–0.6%.
  - Externally, a loyalty-points reminder automation got a 70% open rate and **12.23% click**, and naming the money value ("500 points ($25 value) expire in 7 days") beats naming points ([LoyaltyLion](https://loyaltylion.com/blog/loyalty-program-emails), [Sequenzy](https://www.sequenzy.com/blog/ecommerce-loyalty-program-emails)).
  - Top brands also send "service" emails that read as information, e.g. Represent's "Introducing a smarter way to return".
- **Strength: A** (own data plus an external case). **Caution:** only use the bracket when the content really is an account or restock fact. A fake notice will get flagged and burn trust.

### 4. Use preview text for a second fact. Never repeat the subject.
- **What to do.** The subject names the thing. The preview adds a number or a condition, e.g. "It expires in 49 hours" / "No minimum spend" / "Sizes S–XL. Ships Monday."
- **Why.**
  - An A/B test that changed only the preheader, from repeating the subject to adding a new benefit, lifted revenue per email by **95.6%** and conversion by about 93% ([Email Optimization Shop](https://emailopshop.com/preheader-text-6-models-and-a-case-study-with-a-96-lift-in-revenue-per-email/)).
  - Litmus-cited data puts optimised preheaders at 14–22% higher opens ([SMTPedia summary](https://smtpedia.com/email-preheaders/)).
  - SANTO's two top emails both used this pattern.
- **Strength: B** (one clean A/B test, plus SANTO's own pattern).

### 5. Drops run on a fixed, public slot, and email announces the time days ahead.
- **What to do.**
  - Pick one weekly slot and never move it, e.g. **Thursday 6pm UK**.
  - Send an announce email T-2 or T-3 days ("THURSDAY, 6PM: THE AUTUMN KNITS").
  - Send a "LIVE NOW" email at the slot.
  - At most one reminder, only to people who clicked the announce email.
- **Why.**
  - Supreme drops every Thursday at 11am ET (4pm UK) ([Droplist](https://www.drop-list.com/guides/supreme-drops-explained/)).
  - Kith's Monday Program drops every Monday at 11am EST ([Kith](https://kith.com/collections/kith-monday-program)).
  - Palace drops weekly ([Palace Community droplists](https://www.palacecmty.com/droplists/)).
  - Stüssy emailed its Fall '25 collection on 12 Aug 2025 for **Friday 15 Aug, 10am, with separate times per region** ([Stüssy Fall '25](https://www.stussy.com/blogs/news/stussy-fall-25-collection)).
  - Unknown London sends "THE UNKNOWN CYPHER THIS THURSDAY". Represent puts the date in the subject ("247 Collection | 14.04.21").
  - The fixed time is the ritual that builds the audience.
- **Strength: A** (5+ brands, all consistent).
- **SANTO.** "ITS LIVE, FIRST 10 ORDERS ARE FREE!" (0.24–0.27%) came with no advance date, so nobody was waiting for it. Announce first.

### 6. Sell access, not discounts: codes, early windows, "the vault".
- **What to do.** Instead of % off, give subscribers something only the email has:
  - an early-access code, or
  - a 1-hour-early window.

  Subject: "Early access code" / preview "Opens 5pm Thursday. Public at 6pm."
- **Why.**
  - Corteiz locks its site and sends passwords by email at drop time, so signing up is the only way in ([Grow Your Clothing Brand](https://growyourclothingbrand.com/blog/case-studies/corteiz/), [Undiscovered](https://www.undiscoveredmag.com/post/is-the-password-method-dead)). Its list is reported at about **1.7M** addresses (claim via [Growthcurve](https://growthcurve.co/corteiz-growth-playbook-how-crtz-turned-drops-stunts-and-owned-distribution-into-a-repeatable-attention-system); strength C).
  - Unknown London sent "Early Access Code"; Represent sent "THE VAULT IS NOW OPEN".
  - SKIMS gave restock-waitlist sign-ups an hour's early access ([Opensend](https://www.opensend.com/post/skims-marketing-strategy)).
- **Strength: B.**
- **SANTO.** Access is a certain benefit. "First 10 orders free" is a lottery that most readers assume they will lose. Stacked codes (FIVER + GLFS, 0.71%) also underperformed.

### 7. Treat restocks and reloads as events of their own.
- **What to do.**
  - Send "RESTOCK" or "BACK" emails for the pieces now selling: waffle-knit sweatshirt, graffiti sweatshirt, washed zip hoodie.
  - Send them first to people who viewed or carted those pieces, then to everyone.
  - Switch on a back-in-stock flow with a size selector on the product page.
- **Why.**
  - Unknown London: "BLACK ZIP TRACKIE RESTOCK", "CHIEF KEEF X ED HARDY RELOAD".
  - SKIMS restocked bras after a waitlist of 35,000+ ([E! Online](https://www.eonline.com/news/1367816/kim-kardashians-skims-restocks-bras-after-35-000-customer-waitlist)).
  - Represent collects email or phone per size for back-in-stock alerts ([Represent](https://representclo.com/pages/about)).
  - A restock is proof of demand. No discount is needed.
- **Strength: B.**

### 8. Autumn emails name the season, the year and one hero piece. Never "Fall Essentials".
- **What to do.**
  - Subject pattern: "AUTUMN '26 / THE WAFFLE-KNIT SWEATSHIRT" or "KNITS, LAYERS, ONE JACKET".
  - Lead image: one piece worn outside, "caught, not staged".
  - Open with 3–4 pieces the customer is already buying (sweatshirts, the fur-lined denim jacket), not an 80%-off grid.
- **Why.**
  - ALD: "FALL / WINTER 2023 ALD GARDEN MULE".
  - Kith: "A Closer Look at Kith Fall 1", an editorial preview sent **before** product goes live ([Kith Fall 2025 editorial](https://kith.com/blogs/discover/a-closer-look-at-kith-fall-2025)).
  - Represent emailed "Explore the complete Fall Winter '22 collection online now" (6 Nov 2022, from a search snippet of Milled).
  - Stüssy: "Fall '25 Collection" with a date and time.
  - Unknown London: "CLUB KNITS + MORE".
  - None of them lead with a price. The season is framed as a new chapter, not a clearance.
- **Strength: B.**
- **SANTO.** Directly replaces the losing "🍂 Fall Essentials – Up to 80% Off" (0.28%).

### 9. When you do sell on price, keep it flat and factual.
- **What to do.** Name the event, not the %: "END OF SEASON SALE", "ARCHIVE SALE", "SALE ENDS SUNDAY, 23:59". Put the depth in the preview or body. Use one code only, never stacked.
- **Why.**
  - ALD's sale subjects contain no numbers ("END OF SEASON ARCHIVE SALE").
  - Represent: "THE BLACK FRIDAY SALE - NOW LIVE".
  - Corteiz's deadline email is 4 words plus ⏳.
  - SKIMS runs "Bi-Annual Sale Ends Tomorrow" / "Last Chance" ([Opensend](https://www.opensend.com/post/skims-marketing-strategy)). SANTO's "Last chance" got 0.27%, so the difference is the brand heat behind the sale, not the wording.
- **Strength: B.**
- **SANTO.** Signal Red is for price and urgency only. Use it on the deadline, not on "80%".

### 10. Personalise with a fact (size, credit, held item), not just a first name.
- **What to do.**
  - Use `{first_name}` only when a concrete personal object follows it ("{first_name}, your size M is back").
  - Build size segments from order history and send "In your size" versions of sale and restock emails.
- **Why.**
  - Gymshark sends "Shop your size in the Winter Sale" and "On Sale - And In Your Size" ([Milled](https://milled.com/gymshark-eu/on-sale-and-in-your-size-F3jjg7DsXorpuIjF)).
  - Klaviyo: "Using first names alone has limited impact… pair… with dynamic variables like product names, behaviors" ([Klaviyo](https://www.klaviyo.com/blog/subject-lines-best-practices)).
  - SANTO's first-name winners all attached a real object (£9.34 credit, a held hat).
- **Strength: B.**

### 11. Culture and community emails sit between the sell emails.
- **What to do.**
  - About 1 in 4 sends has no product ask. Options: a behind-the-slogan story (who says "I THINK ABOUT YOU BUT I DON'T WANT TO"), a customer photo set, an event.
  - One link at most.
- **Why.**
  - Kith sends "This Week at Kith" and "KITH NYC: Weekly Newsletter".
  - ALD sends "CAFÉ LEON DORE" and "GROTESK FOR AIMÉ LEON DORE" (a typeface and artist story).
  - Unknown London sends "THE UNKNOWN CYPHER THIS THURSDAY" (a music event).
  - Represent runs a "Behind the Brand" series ([Represent](https://representclo.com/blogs/behind-the-brand/reintroducing-owners-club-with-george-heaton)).
  - The InboxNewsletter clothing case used 3–4 emails a week split across "sales, product launches, and brand storytelling" to reach $75k/month ([InboxNewsletter](https://www.inboxnewsletter.com/p/case-study-how-we-took-a-clothing-brand-from-15k-email-revenue-to-75k-month-in-60-days)).
- **Strength: B.**

### 12. Plainer emails usually win clicks. Test a plain "note" format on existing buyers.
- **What to do.**
  - Split-test a text-led email: one image max, 60–120 words, one link, signed by a person.
  - Test it against the image grid on the **customer** segment first.
  - Keep image-led layouts for new-collection reveals.
- **Why.**
  - **HubSpot A/B tests:** the plainer version won every test. HTML with images had 21% lower CTR and 51% fewer total clicks; the GIF version got 42% fewer clicks than plain text ([HubSpot](https://blog.hubspot.com/marketing/plain-text-vs-html-emails-data)).
  - **Litmus A/B test:** plain text converted better with existing customers (63%) and made no difference with non-customers ([Litmus](https://www.litmus.com/blog/the-results-are-in-a-b-testing-html-vs-plain-text-emails)).
  - **Counter-evidence:** these lists are B2B, and some ecommerce tests find HTML wins ([Stripo roundup](https://stripo.email/blog/plain-text-vs-html-email-statistics-benchmarks-and-what-the-data-shows/)).
- **Strength: B** (credible tests, but not in fashion).
- **SANTO.** The store-credit and free-gift winners read like personal notices. Test this for real.

### 13. One hero product, a few supporting pieces, one CTA verb.
- **What to do.**
  - Structure: 1 hero piece full-width, then up to 3 supporting pieces, then a single CTA.
  - CTA wording: "Shop the sweatshirt", "See the drop", "Use your credit".
  - Test 1 product against 4–6 products.
- **Why.** The subjects of the top brands are overwhelmingly single-product or single-collection ("THE VIRTUS SNEAKER", "ALD PÁPIA MOC BOOT", "BLACK ZIP TRACKIE RESTOCK"). Single-offer emails avoid "cognitive overload" ([ConvertCart](https://www.convertcart.com/blog/email-a-b-testing-elements)). I found **no published fashion A/B test on product count**.
- **Strength: C.** Pattern-based. Test it.

### 14. Subject length: aim for under ~30 characters and 3–6 words.
- **What to do.** Keep the product name and status word inside ~30 characters so nothing gets cut off on mobile.
- **Why.**
  - Gymshark averages 27 characters ([Enrich Labs](https://www.enrichlabs.ai/case-study/gymshark-email-marketing)); SKIMS about 29 ([Opensend](https://www.opensend.com/post/skims-marketing-strategy)); the core-streetwear median in my sample is 25.
  - Klaviyo's average is about 7 words ([Klaviyo](https://www.klaviyo.com/blog/subject-lines-best-practices)).
  - SANTO's longest winner (about 70 characters) worked because the number came first, so front-load the number.
- **Strength: B.**

### 15. Flows earn far more per recipient than campaigns. Build the drop-related flows.
- **What to do.** Before adding campaign volume, build or repair:
  - back-in-stock (by size)
  - browse abandonment (no discount, scarcity line)
  - store-credit expiry at 7 days and 48 hours (this is what the winners were, run as one-offs)
  - welcome that explains the drop slot
- **Why.**
  - Omnisend: automated emails produce **22x more revenue per email** than campaigns ([Omnisend](https://www.omnisend.com/blog/email-marketing-statistics/)).
  - Club L: the welcome and abandoned-cart flows made up two-thirds of its 33% email/SMS revenue share ([Klaviyo Club L](https://www.klaviyo.com/customers/case-studies/fashion-ecommerce-brand-drives-revenue-with-automation)).
  - Kerrits: automated emails convert at 21.7% vs 5.6% for campaigns ([Omnisend Kerrits](https://www.omnisend.com/resources/customers/kerrits/)).
  - InboxNewsletter clothing case: flows were $45k of $75k/month.
- **Strength: A.**

### 16. Frequency: send on a steady rhythm to an engaged segment, not blasts to 40k.
- **What to do.**
  - Send 1–2 emails a week on fixed days to people who clicked in the last 90 days.
  - Send to the full list only for the fixed drop slot and big moments.
  - Never go quiet and then burst.
- **Why.**
  - Salesforce (19B sends): 5+ emails a week gave 0.58% unsubscribes; 1–2 a week gave 0.07%.
  - MailerLite: brands sending irregularly had 0.9% unsubscribes vs about 0.4% for regular senders ([Opensend summary](https://www.opensend.com/post/email-unsubscribe-rate-statistics-ecommerce)).
  - SKIMS gets away with about 5 a week because every email is news ([Opensend](https://www.opensend.com/post/skims-marketing-strategy)).
  - Kith, Supreme and Palace are weekly.
- **Strength: A/B.**
- **SANTO.** 47 campaigns a year is about 1 a week, yet unsubscribes run 0.4–1.1%. That is more like the irregular-sender figure than the volume figure. Fix relevance and regularity before cutting sends.

### 17. Use GIFs only when motion shows something a still cannot.
- **What to do.** One short (<4 s) GIF where it earns its place: the fur lining showing as the jacket opens, or a waffle-knit texture close-up. No decorative GIFs.
- **Why.**
  - Dell's product-motion GIF gave +42% click, +103% conversion, +109% revenue. It was measured **against previous campaigns, not A/B** ([MarketingSherpa](https://marketingsherpa.com/article/case-study/gif-centric-email-campaign)).
  - HubSpot's A/B test had the GIF version losing 42% of clicks.
- **Strength: C** (mixed evidence).

### 18. Measure clicks and orders per recipient, not opens.
- **What to do.**
  - Judge every test on click rate and revenue per recipient.
  - Exclude Apple MPP opens in Klaviyo's custom reports.
  - Trigger follow-ups on clicks, not opens.
- **Why.** Apple Mail Privacy Protection auto-opens emails, which inflates open rates. Clicks are unaffected ([Klaviyo Help](https://help.klaviyo.com/hc/en-us/articles/4416791883163), [Klaviyo blog](https://www.klaviyo.com/blog/7-ways-to-use-email-open-rate)).
  - Benchmark to beat, clothing & accessories on Klaviyo: **1.83% campaign click, 33.1% open**. Top-10% placed-order rate across industries is 0.36% ([Klaviyo benchmarks](https://www.klaviyo.com/products/email-marketing/benchmarks)).
- **Strength: A.**

### 19. Collab and culture tags do a lot of work in the subject line.
- **What to do.** When a piece has a story (artist, graffiti writer, a slogan's origin), name it in the subject, e.g. "THE GRAFFITI SWEATSHIRT / BY [ARTIST]", using a "/" or "X".
- **Why.** Collab formatting is the single most common subject structure in the sample: "Stüssy / Harris Tweed", "REPRESENT X MEGADETH - LIVE NOW", "UNKNOWN X RIZLA ONLINE NOW", "ALD / NEW YORK METS COLLECTION". The name borrows attention from the partner.
- **Strength: B.**

---

## Do / Don't for SANTO's next email (autumn, sweatshirts, Friday payday)

**Do**
- Subject: product + status, ≤30 characters, no emoji, no "!". Examples: "THE WAFFLE-KNIT SWEATSHIRT. BACK." or "AUTUMN '26: KNITS + THE FUR-LINED JACKET".
- Preview: one new fact. Examples: "Sizes S–XL. Restocked this morning." / "Payday. No code needed."
- One hero image of a worn piece ("caught, not staged"), up to 3 supporting sweatshirts, one CTA ("Shop the sweatshirt").
- Announce a fixed drop slot (e.g. "Every Thursday, 6pm") and keep it.
- Put the `[Account notice]` credit/gift format into flows (7-day and 48-hour expiry).
- Build size segments and send "in your size" restock and sale versions.
- Send to recent clickers first; judge on click and revenue per recipient.

**Don't**
- Seasonal clichés with discounts ("🍂 Fall Essentials – Up to 80% Off").
- Stacked codes, "first 10 orders free" lotteries, generic "Last chance".
- Fake notices: use the bracket tags only for real account, order or restock facts.
- Decorative GIFs, 12-product grids, several competing CTAs.
- Banned words: "game day", "join the team", "for the win", "unleash", "streetwear redefined". Also "exclusive" (Klaviyo flagged it as part of the off-brand voice).

## Open questions
1. **What is inside the emails?** Milled bodies were unreachable, so product count and CTA count per email are unconfirmed. Next step: open Milled on a normal connection for Represent, Unknown London and ALD and count products, CTAs and word counts.
2. **Represent's Klaviyo case study** exists at https://www.klaviyo.com/customers/case-studies/represent but the proxy blocked it. It is worth reading for UK-streetwear drop numbers.
3. **Trapstar, Broken Planet, Hellstar, Sp5der, Minus Two**: no indexed archive of their own emails was found. They may lean on SMS and Instagram, or use password pages like Corteiz (unconfirmed).
4. **Does plain text beat image-led for SANTO's list?** Needs an A/B test on buyers vs non-buyers (Finding 12).
5. **Which drop slot is best?** Thursday evening vs Friday payday: test announce-then-live on two consecutive weeks.
