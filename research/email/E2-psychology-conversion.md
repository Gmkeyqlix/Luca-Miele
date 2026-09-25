# E2 — Why SANTO's winners won, and how to repeat it honestly

Researcher angle: psychology and conversion mechanics. Date: 2026-09-25 (Friday, UK payday).
Method: about 58 web searches. WebFetch was blocked (egress proxy), so every figure below comes from search-result summaries of the cited pages. Where a figure could not be checked against its original source, the grade says so. Grades: **A** = peer-reviewed, official or a large dataset, or several sources agree; **B** = one credible source; **C** = a vendor or aggregator claim, or an unverified figure.

---

## 0. Diagnosis in one paragraph

SANTO's three winners (5.05%, 4.15% and 3.11% click, against a 0.25–0.6% norm) share six traits that none of the losers have:
1. **The customer already owns something.** "£9.34 is on your account" and "we are holding a hat for you" are endowment, not a discount.
2. **The number is exact and odd.** £9.34 reads as a computed balance, not a marketing number.
3. **The loss is real and dated.** "Expires in 7 days" and "49 hours".
4. **Friction is removed.** "No minimum spend" and "Shipping is covered too."
5. **The copy is plain.** No emoji, no exclamation marks, no "exclusive", and a clear subject line rather than a clever one.
6. **There is one job.** Use the credit, or claim the gift.

The losers are the opposite: percentage-off noise ("Up to 80% Off"), emoji, caps and exclamation, stacked codes, and generic "Last chance" urgency. The research below explains why each trait works, and where the line between persuasion and deception sits under UK law.

---

## Findings

### F1. "Money already in your account" works because of loss aversion and endowment. Frame the credit as something the customer owns and could lose, not as something to gain.
- **Do:** Write "£X is on your account" or "your £X credit", never "get £X off". Put the expiry beside the amount: "£10 on your account. It ends Sunday 23:59."
- **Why:**
  - A 2024 meta-analysis of 607 estimates from 150 papers puts the loss-aversion coefficient at **1.955** (95% CI 1.82–2.10). Losses weigh about twice as much as equal gains. ([Brown et al., JEL / AEA](https://www.aeaweb.org/articles?id=10.1257%2Fjel.20221698); [working-paper PDF](https://economics.appstate.edu/sites/default/files/loss_aversion_meta-analysis_1.pdf))
  - Honest caveat: a 2025 re-meta-analysis argues loss aversion is less robust than claimed ([Yechiam & Zeif 2025](https://www.sciencedirect.com/science/article/abs/pii/S0167487025000133)).
  - The practitioner pattern: give the credit first, then ask the customer to act to keep it ([AB Tasty on loss aversion](https://www.abtasty.com/blog/loss-aversion/)).
- **Strength:** A for the mechanism (with the caveat above). SANTO's own data is the strongest local evidence: the credit email is 17% of the year's campaign revenue from a single send.
- **SANTO:** Keep the ownership frame in the next email. The subject leads with the balance, the preview gives the deadline and the absence of conditions.

### F2. Credit and gift-card balances are spent as "windfall" money, and people overspend them. That is why an £9.34 credit produced orders worth far more than £9.34.
- **Do:** Set the credit below the price of the cheapest hero product, so every redemption needs a top-up. SANTO's range starts around £33, so £10 credit means the customer pays £23 or more. Show a "£45 → £35 with your credit" price line on one or two products.
- **Why:**
  - The UK Gift Card & Voucher Association reports **68%** of redeemers spend more than the card value.
  - First Data puts it at **75%** overspending ([Digital Transactions](https://www.digitaltransactions.net/with-gift-cards-consumers-are-spending-much-more-than-the-gift-amount/); [Northstar / First Data](https://www.northstarmeetingsgroup.com/Incentive/Corporate-Gifts/First-Data-Study-Consumers-Spend-Beyond-Gift-Card-Value); [PaymentsJournal](https://www.paymentsjournal.com/gift-cards-lead-to-even-more-consumer-spending/)).
  - Store-credit vendor Rise.ai claims **+37% AOV** when credit is in the cart, and a Dr. Squatch credit campaign returning $197K on $287K issued ([Rise.ai customers](https://rise.ai/customers/)). This is a vendor claim.
- **Strength:** B for the overspend surveys; C for the Rise.ai figures.
- **SANTO:** The £1,230 from 39 orders is an average of about £31.50 per order, which fits "credit plus top-up". A £10 credit on a £45–£55 sweatshirt is the right shape.

### F3. A short, real deadline beats a long one. Redemption spikes just before expiry.
- **Do:**
  - Give the credit a 5–7 day life.
  - Send once at issue and once about 48 hours before expiry. This is the pattern already proven: 5.05%, then 3.11%.
  - Name a day and time ("ends Sunday 23:59"), not "soon".
- **Why:**
  - In a field test, **31%** (10/32) of people given a 3-week gift certificate used it, against **6%** (2/32) given 2 months. Longer deadlines invite procrastination ([Shu & Gneezy 2010, JMR](https://journals.sagepub.com/doi/abs/10.1509/jmkr.47.5.933); [PDF](https://anderson-review.ucla.edu/wp-content/uploads/2021/03/Shu-Gneezy_ProcrastinationofEnjoyable_2010.pdf)).
  - Coupon redemption is highest right after issue, dips, then rises again just before expiry, which the authors explain by anticipated regret ([Inman & McAlister 1994, JMR](https://journals.sagepub.com/doi/abs/10.1177/002224379403100310)).
- **Strength:** A (two peer-reviewed studies, one of them a small sample).
- **SANTO:** Two sends per credit, no more. A third "final hours" send would be over-exposure (see F14).

### F4. The endowed-progress effect: people finish what they have already started. A credit or gift "already held for you" is a head start.
- **Do:** Use the exact language of holding and reserving: "We're holding a hat in your size", "Your £10 is already applied at checkout". Only say this if it is literally true (see F12).
- **Why:** In a car-wash loyalty field experiment, **34%** of customers given a 10-stamp card with 2 stamps pre-filled completed it, against **19%** given an empty 8-stamp card. The required effort was the same ([Nunes & Drèze summary, Coglode](https://www.coglode.com/nuggets/endowed-progress-effect); [Silicon Canals](https://siliconcanals.com/t-car-wash-loyalty-cards-endowed-progress/)).
- **Strength:** A (widely replicated, peer-reviewed field experiment).
- **SANTO:** This is why "you forgot your free gift" (4.15%) worked: it implies the gift is already yours. The honest version keeps the "holding" frame and drops the implied "you forgot" if the recipient never claimed anything.

### F5. "Free" is a special price. A free gift can outpull a bigger percentage discount, but name the gift's value or it gets devalued.
- **Do:**
  - Make the offer one concrete object ("a free SANTO beanie, worth £18") rather than "free gift".
  - Pair it with free delivery.
  - Put the gift's real retail value in the body.
- **Why:**
  - Zero-price effect: people pick an inferior item because it is free, and value free items above a pure cost-benefit calculation ([Shampanier, Mazar & Ariely 2007, Marketing Science](https://pubsonline.informs.org/doi/10.1287/mksc.1060.0254); [PDF](https://people.duke.edu/~dandan/webfiles/PapersPI/Zero%20as%20a%20Special%20Price.pdf)).
  - A gift is an "incommensurate resource", so it is not mentally netted off the price the way money is ([Nunes & Park 2003, JMR](https://www.researchgate.net/publication/229023926_Incommensurate_Resources_Not_Just_More_of_the_Same)).
  - Risk: value discounting. People will pay less for an item they have seen given away free, especially with cheaper products. The effect weakens when alternative price information is shown ([Raghubir 2004, JCP](https://myscp.onlinelibrary.wiley.com/doi/abs/10.1207/s15327663jcp1401&2_20)).
  - Adestra, 2.2bn emails: "free" alone scored below average, while "free delivery" scored **+35.9% opens and +81.3% clicks** in retail ([Marketing Charts](https://www.marketingcharts.com/featured-57539); [Econsultancy](https://econsultancy.com/six-case-studies-and-an-infographic-on-how-to-write-effective-email-subject-lines/)). The data is from 2013.
- **Strength:** A for the psychology; B for the Adestra keyword data (old).
- **SANTO:** "FREE hat + shipping covered" was the right combination. Next time, name the item and show its value so a SANTO beanie is not read as a cheap throwaway.

### F6. Percentage discounts, especially deep and repeated ones, train established customers to wait and lower their long-term value.
- **Do:**
  - No "up to X% off" campaigns for the next 6–8 weeks.
  - Use a fixed-£ credit or a gift instead.
  - Never stack codes.
- **Why:**
  - Deeper discounts raise future purchases by *first-time* customers but reduce future purchases by *established* customers, across three field studies ([Anderson & Simester 2004, Marketing Science](https://pubsonline.informs.org/doi/10.1287/mksc.1030.0040)).
  - A 35% acquisition discount produced customers worth **about half** the long-term value of non-promo customers ([Lewis 2006, JMR](https://journals.sagepub.com/doi/10.1509/jmkr.43.2.195)).
  - Over the long run, promotions make consumers more price-sensitive ([Mela, Gupta & Lehmann 1997, JMR](https://journals.sagepub.com/doi/10.1177/002224379703400205)).
- **Strength:** A (three peer-reviewed longitudinal or field studies).
- **SANTO:** "🍂 Fall Essentials – Up to 80% Off" at 0.28% and "FIVER + GLFS" at 0.71% show a list already numbed to percentages. A credit tied to the account behaves differently from a public sale, which is exactly what the winners show.

### F7. Clear subject lines beat clever ones. All of SANTO's winners were literal.
- **Do:** State the thing: amount, object, deadline. No puns, no teasers. Keep to about 40–60 characters so the amount and deadline survive mobile truncation.
- **Why:**
  - AWeber tested 20 subject-line pairs on more than 45,000 subscribers. Clear lines beat creative ones on every channel measured, averaging **541% more response** ([MarketingSherpa](https://sherpablog.marketingsherpa.com/email-marketing/aweber-subject-line-test/)).
  - In an academic field test, a blank "curiosity" subject line did not raise response over informative or provocative lines, and produced more active refusals ([Int. J. Social Research Methodology](https://www.tandfonline.com/doi/full/10.1080/13645579.2015.1078596)).
- **Strength:** B for AWeber (one large test, older, not ecommerce). SANTO's own winners and losers point the same way.
- **SANTO:** "{first_name}, your £10 SANTO credit ends Sunday" beats anything clever.

### F8. First-name personalisation gives a real but modest lift. Behaviour and account data lift far more, which is what the credit email actually had.
- **Do:**
  - Keep {first_name}, with a clean fallback: no "Hi ,". Use no name rather than a broken one.
  - The real lift comes from account-specific facts: the balance, the last product viewed or bought, or size.
- **Why:**
  - In randomised field experiments sent to millions of recipients, adding the recipient's name to the subject raised opens **20%** (9.05% → 10.80%), leads **31%**, and **cut unsubscribes 17%** ([Sahni, Wheeler & Chintagunta 2018, Marketing Science](https://pubsonline.informs.org/doi/abs/10.1287/mksc.2017.1066); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2725251)).
  - Experian: personalised subject lines had +26% unique opens, and personalised promotional mailings had +41% unique clicks ([Experian press release](https://www.experianplc.com/newsroom/press-releases/2014/experian-marketing-services-study-finds-personalized-emails-generate-six); [MarTech](https://martech.org/study-70-brands-personalizing-emails-missing-higher-transaction-rates-revenue/)).
  - Klaviyo's own guidance says first name alone "won't do much". Behavioural personalisation is where the lift is ([Klaviyo subject lines](https://www.klaviyo.com/blog/subject-lines-best-practices)).
- **Strength:** A for the name effect (randomised); B for Experian.
- **SANTO:** The unsubscribe reduction matters most. SANTO's unsubscribe rate (0.4–1.1%) is two to five times the benchmark.

### F9. Behaviour-triggered emails earn 10–20x more per recipient than broadcasts. The "account notice" felt triggered, which is part of why it worked.
- **Do:** Turn the credit mechanic into a standing Klaviyo flow as well as a campaign. Examples: an expiring-credit reminder, browse-abandon on sweatshirts, back-in-stock on sold-out sizes.
- **Why:**
  - Klaviyo benchmarks: browse abandonment earns about **$1.95** per recipient (for $100–200 AOV), back-in-stock about **$9.14**, abandoned cart about **$3.65**, against about **$0.11** for a typical campaign ([Klaviyo benchmarks](https://www.klaviyo.com/marketing-resources/ecommerce-benchmarks), via [GOSH Digital](https://www.goshdigital.co/blog/klaviyo-benchmarks-by-industry)).
  - Omnisend (150k brands): automations were **2% of sends and 30% of revenue**, about 16x more per send than campaigns ([Omnisend 2026 report](https://www.omnisend.com/resources/reports/2026-ecommerce-marketing-report/)).
- **Strength:** A (two platforms with very large datasets agree).
- **SANTO:** SANTO's year averaged £0.0064 per recipient, well under Klaviyo's campaign average. Flows are the structural fix; the next campaign is the tactical one.

### F10. Simpler, "personal-looking" emails usually win on clicks, but test it. Evidence is strongest in B2B and weaker in fashion, where the product image matters.
- **Do:**
  - Build the next email as a "letter plus one image": Bone background, Inter Tight body text, the balance in Space Mono, one real ("caught, not staged") photo of the waffle-knit sweatshirt, and one button.
  - A/B test it against the usual designed template, split 50/50 on 20% of the list, winner by click rate.
- **Why:**
  - HubSpot A/B tests: plainer variants won every test with significance.
    - An HTML template cut opens 25%.
    - Plain text got **51% more clicks** than HTML with images.
    - A simple HTML template got **30% more clicks** than a heavy one.
    ([HubSpot](https://blog.hubspot.com/marketing/plain-text-vs-html-emails-data))
  - Litmus found results split by audience: customers and non-customers responded differently ([Litmus](https://www.litmus.com/blog/the-results-are-in-a-b-testing-html-vs-plain-text-emails)).
  - Klaviyo's help centre says text-only emails "often see higher click rates" ([Klaviyo help](https://help.klaviyo.com/hc/en-us/articles/12415384810651)).
- **Strength:** B. The evidence is consistent in direction, but most tests are B2B or content emails, not apparel.
- **SANTO:** The winners read like service messages. Keep that look without pretending to be a service message (see F12).

### F11. Fewer products and one primary action. There is a sweet spot of about 2–5 links, and choice overload after that.
- **Do:** One hero product, at most three supporting products, and one primary CTA ("Use my £10") repeated at most twice, plus a text link. Remove the multi-link nav bar from this email.
- **Why:**
  - MailerLite analysed 317,000 campaigns and 2.9bn emails. Emails with **2–5 links** had the highest conversion (0.56%, **75% above average**) and the best click rate. Emails with more than 20 links had the lowest open rate ([MailerLite](https://www.mailerlite.com/blog/how-many-links-in-email)).
  - A field experiment on 1.6M shoppers found purchase likelihood rises and then falls as the number of recommended products grows. About 64% of the drop comes from people not clicking at all ([Long et al., MSOM](https://pubsonline.informs.org/doi/10.1287/msom.2022.0659)).
  - Whirlpool cutting CTAs from four to one gave **+42% clicks** ([WiserReview roundup](https://wiserreview.com/blog/call-to-action-statistics/)). This is one case.
  - The much-quoted "single CTA = +371% clicks, +1,617% sales" (attributed to Campaign Monitor/WordStream) has no traceable method. Do not rely on it.
- **Strength:** A for 2–5 links and choice overload; B for Whirlpool; C for the 371% figure.
- **SANTO:** The credit email had one job. Keep it that way.

### F12. The honesty line. What is legal and durable, and what could get SANTO flagged by the ASA or CMA.
- **Do:**
  - Every credit, gift and deadline must be real. Credit is actually issued to that customer's account (or code), it actually stops working at the stated time, and it is not re-issued at once with a new deadline.
  - Drop the bracketed "[Account notice]" prefix, or use it only for genuinely transactional mail.
  - If a gift needs a purchase, say so in the subject or preview.
  - If gift stock is limited, give the number.
- **Why:**
  - **CAP Code 2.1:** marketing emails must be "obviously identifiable" as marketing, including from the subject line, without being opened ([ASA rule 2.1](https://www.asa.org.uk/type/capcode/code_rule/2.1.html?_vhid=8269FB3E13235026022973A998FC8FB2); [Pinsent Masons on email and the CAP Code](https://www.pinsentmasons.com/out-law/guides/the-cap-code)).
  - In the US, the FTC fined Experian **$650,000** in 2023 for marketing emails dressed as "important information about your account" ([Validity](https://www.validity.com/blog/the-dangers-of-misleading-subject-lines/)).
  - The ASA treats "gift" as meaning "free". Conditions must be clear, and limited quantities must be flagged "at each stage" ([ASA: use of free](https://www.asa.org.uk/advice-online/use-of-free.html); [ASA: gifts v prizes](https://www.asa.org.uk/advice-online/promotional-marketing-gifts-v-prizes.html)).
  - Under the **DMCC Act** (in force since 6 April 2025), the CMA can fine directly, up to **10% of global turnover** ([Cooley](https://www.cooley.com/news/insight/2025/2025-04-14-new-uk-consumer-law-regime-comes-into-force)).
  - CMA guidance (CMA207): a timer or deadline is misleading if "a near-identical promotion starts shortly afterwards" ([CMS Law-Now](https://cms-lawnow.com/en/ealerts/2025/03/tangled-web-uk-regulators-crack-down-on-harmful-online-choice-architecture); [Macfarlanes](https://www.macfarlanes.com/insights/102ic7m/the-cmas-increasing-scrutiny-of-online-businesses-use-of-urgency-claims/)).
- **Strength:** A (regulator texts and legal-firm summaries).
- **SANTO:** The *mechanics* of the winners (a real balance, a real deadline, a plain look) are fully legal. The *packaging* has two risks: "[Account notice]" and "you forgot your free gift" (if nobody forgot anything). Keep the mechanics and change the packaging. Suggested replacement prefix: "{first_name}, your SANTO credit: £10, ends Sunday".

### F13. Real urgency lifts results. Fake or recycled urgency teaches the list to ignore you, and now carries legal risk.
- **Do:**
  - At most one deadline per email, and at most one deadline campaign in any 7-day window.
  - Use specific dates ("ends Sunday 23:59"), never "Last chance!" with no date.
  - If a countdown GIF is used, it must match a real, enforced end time.
- **Why:**
  - Real deadlines raise redemption (F3).
  - The CMA acted against Emma Sleep and Wowcher over countdown clocks that did not mean what they said ([Travers Smith](https://www.traverssmith.com/knowledge/knowledge-container/online-sales-do-countdown-timers-break-consumer-law-cma-investigates-emma-sleep/); [Bird & Bird](https://www.twobirds.com/en/insights/2023/uk/taking-the-pressure-off)).
  - An aggregator review of 18 ecommerce timer tests reports a median **+9.1%** conversion for genuine deadlines and **−3.2%** for fake or resetting timers ([LiquidBoost](https://liquidboost.app/blog/countdown-timer-conversion-data)). It also notes that few of the tests publish sample sizes.
- **Strength:** A for the law; C for the timer lift figures.
- **SANTO:** "Last chance" (0.27%) and "ITS LIVE, FIRST 10 ORDERS ARE FREE!" (0.24–0.27%) are what urgency fatigue looks like. The "49 hours" clone worked because the deadline was real and specific.

### F14. SANTO's unsubscribe rate is the hidden cost of volume and hype. Frequency is the top reason people unsubscribe.
- **Do:**
  - Send the next credit email only to people engaged in the last 90 days (clicked, bought or viewed a product), plus all purchasers from the last 12 months.
  - Suppress chronic non-clickers.
  - Target unsubscribe below 0.3% on this send.
- **Why:**
  - "Too many emails" is the top unsubscribe reason: 26% per MarketingSherpa's survey ([MarketingSherpa chart](https://marketingsherpa.com/article/chart/why-consumers-unsubscribe)).
  - Since February 2024, Gmail and Yahoo require bulk senders to keep spam complaints under 0.3% (Google advises under 0.1%) and to support one-click unsubscribe ([Google sender FAQ](https://support.google.com/mail/answer/14229414?hl=en)).
- **Strength:** A for the Gmail/Yahoo rules; B for the survey.
- **SANTO:** At 0.4–1.1% unsubscribes per send, list erosion wipes out most of the value of low-click campaigns. Fewer, better emails is the fix.

### F15. Judge on clicks, not opens. Apple Mail Privacy Protection inflates opens, so a curiosity line that "wins on opens" can lose on revenue.
- **Do:** Pick A/B winners on click rate or revenue per recipient (Klaviyo's "placed order" metric), never on open rate. Exclude MPP opens from engagement segments.
- **Why:** Apple Mail accounts for over half of opens and MPP pre-loads pixels, inflating open rates ([Klaviyo help on MPP](https://help.klaviyo.com/hc/en-us/articles/4416791883163); [Klaviyo blog](https://www.klaviyo.com/blog/7-ways-to-use-email-open-rate)). The figure of about 58% of opens comes from a secondary source ([Geysera](https://www.geysera.com/blog/email-marketing/email-marketing-benchmarks-2026-open-rates-ctr-and-why-half-your-data-is-wrong)).
- **Strength:** A for the mechanism; C for the exact share.
- **SANTO:** SANTO already ranks campaigns by click. Keep doing that.

### F16. Emoji and exclamation marks: the evidence is mixed at best. SANTO's own data and brand rules both say drop them.
- **Do:** Use no emoji and no exclamation marks in subjects and previews. This overrides Klaviyo's auto-detected voice.
- **Why:** Studies conflict: some report open-rate lifts, others about 6% lower opens. Phrasee's benchmark concluded emoji "magnify what's already true", so a weak line fails harder ([Search Engine Journal](https://www.searchenginejournal.com/emojis-in-subject-lines/378280/); [Mailmend roundup](https://mailmend.io/blogs/subject-line-effectiveness-statistics)).
- **Strength:** C for the external data. SANTO's internal data is more telling: all three winners had zero emoji, and the worst performers had 🍂, caps and "!".
- **SANTO:** Brand voice and performance agree here.

### F17. Payday timing: most UK workers are paid monthly, around the 25th or the last working day. Spending jumps on payday itself.
- **Do:**
  - Launch credit or gift emails on a payday Friday at 07:00–08:00 UK time.
  - Upcoming payday Fridays:
    - **Fri 25 Sep 2026** (today; the 25th and the last Friday coincide).
    - **Fri 23 Oct** (25 Oct is a Sunday, so 25th payers are paid early).
    - **Fri 30 Oct** (last working day of October).
    - **Fri 27 Nov** (last Friday; Black Friday also falls on 27 Nov 2026).
  - For October, a credit issued Fri 23 Oct and expiring Sun 1 Nov covers both payday groups inside a 9-day window.
- **Why:**
  - More than three-quarters of UK employees are paid monthly. The most common paydays are the 25th or the last working day, and when payday falls on a weekend it moves to the preceding Friday ([CashLady](https://www.cashlady.com/info/getting-paid-uk); [CIPP](https://www.cipp.org.uk/resources/news/rp-normal-payday-falls-on-non-banking-day.html)).
  - InMarket found consumer spending rises **33% on payday** and stays high for one more day ([LSN](https://www.lsnglobal.com/article/view/31006)). This is likely US data.
  - UK footfall data linked a late-September lift to the payday weekend ([FashionNetwork](https://uk.fashionnetwork.com/news/Uk-retail-footfall-ends-september-on-a-high-note,1768694.html)).
- **Strength:** B for the UK pay-date pattern; C for the 33% figure (US data).
- **SANTO:** With about 73% of sessions from the UK, schedule on UK time. Do not write "payday" in the subject every month; that becomes its own fatigue. Use the timing silently.

### F18. The weather: the Met Office says this autumn is 1.5–2x more likely than normal to be warm and wet. Sell "layering for rain", not "the first cold snap". Keep a cold trigger ready for when it comes.
- **Do:**
  - The late-Sept/Oct creative angle is **rain and layers**: the washed zip hoodie over a tee, the fur-lined denim jacket, "sweatshirt weather". No coats-and-frost imagery yet.
  - Set a trigger: when the London/Manchester forecast minimum first falls below about 8–10°C for 2+ days, send a pre-built "It's turned" email featuring the waffle-knit sweatshirt and fur-lined jacket.
- **Why:**
  - Met Office: chances of a **warm and wet autumn are 1.5–2x higher than normal** (El Niño). October is likely to be above average, turning more unsettled mid-month ([Met Office blog 2026](https://www.metoffice.gov.uk/blog/2026/what-does-the-latest-long-range-forecast-tell-us-and-what-role-could-el-nio-play-this-autumn); [Met Office long-range](https://weather.metoffice.gov.uk/long-range-forecast)).
  - Warm autumns delay knitwear and coat demand. Search demand for coats slowed sharply in an October that ran 1.8°C above average ([Econsultancy / Pi Datametrics](https://econsultancy.com/clothing-retailers-must-adapt-to-weather-driven-changes-in-search-behaviour/)).
  - The Japan Meteorological Agency's apparel analysis shows temperature thresholds for coats and knitwear demand ([JMA apparel](https://www.data.jma.go.jp/risk/en/apparel.html)).
  - When cold does arrive it moves sales: Kantar found men's knitwear **+9.7% YoY** in a cold autumn window ([Drapers](https://www.drapersonline.com/insight/analysis/which-winter-warmers-are-selling-for-fashion-retailers)). A cold snap made independents' coat demand "go crazy" ([Drapers](https://www.drapersonline.com/news/cold-snap-impacts-sales-for-indies)).
  - Wet days lift online browsing. WeatherAds reports **+12% site traffic** for clothing retailers on wet or cold days, and light rain lifts online spend up to about 4.4% ([WeatherAds](https://www.weatherads.io/blog/weather-and-ecommerce-how-weather-impacts-retail-website-traffic-and-online-sales); [Retail Tech Innovation Hub](https://retailtechinnovationhub.com/home/2023/9/1/rainy-days-miserable-weather-set-to-boost-brits-online-spending-by-650-million-in-2023)).
  - Weather-triggered campaigns: La Redoute reported +17% sales, and George at ASDA brought AW forward on temperature drops ([WeatherAds case studies](https://www.weatherads.io/blog/how-effective-is-weather-based-marketing-4-case-studies-with-roi-stats)). These are vendor-reported.
- **Strength:**
  - A: Met Office outlook, and the direction of the weather-to-demand link.
  - B: Drapers/Kantar.
  - C: the WeatherAds uplift figures.
- **SANTO:** Shopify already shows sweatshirts overtaking shorts, so demand is turning. Rain is the likelier trigger this year, and rainy evenings are when people browse.

### F19. Benchmarks to judge the next email against.
- **Do:** Treat a click rate of **≥2.5%** as success for a credit or gift email to an engaged segment, **≥1.5%** for a product-led email, and anything under 1% as a failed format. Watch unsubscribes (<0.3%) and orders per 1,000 recipients.
- **Why:**
  - Klaviyo's 2026 benchmarks put clothing and accessories campaign click rate at about **1.83%**, with open rate about 33% ([Klaviyo UK industry benchmarks](https://www.klaviyo.com/uk/marketing-resources/email-benchmarks-by-industry)). A second search summary quoted 5.54% for the same page, so the exact figure is unconfirmed.
  - The brief's working figure is 1–1.5% average.
- **Strength:** B (one platform, and the exact figure is in doubt).
- **SANTO:** The credit email at 5.05% was top-decile. Most other campaigns sit at a fifth to a third of the industry average.

### F20. A person's name as sender can lift opens. Test it, but it is secondary.
- **Do:** A/B test the sender name "SANTO" against "[Founder first name] at SANTO" on the next send, split 50/50 and judged on clicks. Only use a real person who could plausibly reply, and make sure replies reach someone.
- **Why:** Practitioner tests report open lifts of roughly 19–27% for a person-plus-brand sender over the brand alone, with the caveat that the higher-open version sometimes has lower click-to-open ([Benchmark Email](https://www.benchmarkemail.com/blog/email-sender-name-person-or-brand/)).
- **Strength:** C.
- **SANTO:** This fits the "personal email" look of F10 and the honesty rule of F12: it is a real person, not a disguise.

---

## How to build the next email on the same mechanics, honestly (applied)

**Option 1: Autumn credit (recommended for Fri 23 Oct or Fri 30 Oct; or this weekend if credit can be issued today)**
- Mechanic: issue a real £10 Shopify store credit, or a unique single-use £10 code, to engaged profiles (F14). It expires in 7 days at 23:59 on a named day. Use a different amount from the £9.34 run and give it a stated reason, so it is not a "near-identical promotion" (F12).
- Subject (A): `{first_name}, £10 is on your SANTO account` / Preview: `It ends Sunday at midnight. No minimum spend.`
- Subject (B, test): `Your £10 SANTO credit ends Sunday` / Preview: `Use it on the sweatshirt everyone is buying.`
- Body: letter format.
  - "We've put £10 on your account for the turn of the season. No minimum spend. It stops working Sunday 23:59."
  - Then one hero image of the waffle-knit slogan sweatshirt with "£X → £X−10 with your credit".
  - Then 3 supporting products: graffiti sweatshirt, washed zip hoodie, fur-lined denim jacket.
  - One button: "Use my £10".
- Reminder: 48h before expiry, to non-purchasers only. `{first_name}, your £10 ends in 48 hours` / `Still on your account. Sunday 23:59.`
- Why it should work: F1–F4, F7, F8, F11, F17.

**Option 2: Gift with purchase (for a later date, so the two mechanics don't collide)**
- Mechanic: a free named item (beanie or cap, actual retail value stated) with any sweatshirt or hoodie, plus free UK delivery. State a real stock limit if there is one.
- Subject: `A free SANTO beanie with any sweatshirt` / Preview: `Worth £18. Delivery covered. 250 set aside, until Sunday.`
- Why: F5, F12, F13. The honest version of "you forgot your free gift" is "we set one aside for you". Only use "you forgot" in a real abandoned-cart flow where the gift was in their cart.

**Weather standby (F18):** Pre-build the "It's turned" email (sweatshirt and fur-lined jacket, no discount) and send it the first time the forecast minimum stays under about 8–10°C for 2+ days. Full price is appropriate here, because demand is doing the work.

---

## Do / Don't

**Do**
- Lead with something the customer already owns: an exact £ balance, or a named item held for them.
- Use a real deadline with a day and time (5–7 days), and send twice at most: at issue and about 48h before expiry.
- Say "No minimum spend" and "Delivery covered" when true. Removing friction is part of why the winners won.
- Set credit below the cheapest hero price, so redemption means a top-up of about £20–40.
- Keep subjects literal: amount, object, deadline. No emoji, no "!".
- Use one hero product plus at most three others, 2–5 links in total, and one CTA.
- Use a plain, letter-like layout with one "caught, not staged" photo, and A/B test it against the designed template on clicks.
- Send on payday Fridays (23 Oct, 30 Oct, 27 Nov) at around 07:30 UK time, to engaged plus purchaser segments only.
- Sell rain and layering now; keep the cold-snap email ready for when the forecast turns.
- Move credit expiry, browse abandonment and back-in-stock into flows; that is where revenue per recipient is 10–20x higher.

**Don't**
- Don't send "[Account notice]" style prefixes on marketing email (CAP 2.1; the FTC/Experian precedent).
- Don't write "you forgot…" when nobody forgot anything.
- Don't re-issue the same credit or gift with a fresh deadline right after the old one ends (CMA207, DMCC fines up to 10% of turnover).
- Don't use "Up to X% off", stacked codes, "FIRST 10 ORDERS FREE", or undated "Last chance" (all losers; they train discount-waiting).
- Don't call something a free gift without stating the purchase condition and any quantity limit up front.
- Don't pick A/B winners on opens (MPP).
- Don't mention "payday" in every subject; use the timing, not the word.
- Don't send coat and frost creative into a warm, wet October.

---

## Open questions (need SANTO data or a decision)
1. Was the £9.34 credit real and on every recipient's account, and did it actually expire? If it was not, the winning email's result carries compliance risk and should not be repeated as-is.
2. Who received the 49-hour clone: everyone, or only non-clickers? This determines whether the 3.11% shows decay or a good second touch.
3. Orders per click: the credit email converted 39 orders from about 5% clicks. What was the list size and the redemption rate of the credit itself?
4. How much margin can a £10 credit or £18-value gift cost? And what is the landed cost of the hat or beanie, to set the gift's stated value honestly?
5. Can Shopify issue native store credit to customer accounts at scale, or will it be unique Klaviyo coupon codes? Codes are fine, but the copy must then say "code", not "on your account".
6. Is there a real founder or person who can sign the emails and read replies (F20)?
7. What share of the list is non-UK? US recipients convert 7x worse and are not on UK paydays. Should they be excluded, or sent to on US timing?
8. Can SANTO add a weather data source (a Klaviyo integration, or a simple manual check of the Met Office forecast) to fire the cold-snap email?

*Limitations: WebFetch was blocked, so no page was read in full. Figures come from search-result summaries of the linked pages. Numbers graded C should be treated as directional only.*
