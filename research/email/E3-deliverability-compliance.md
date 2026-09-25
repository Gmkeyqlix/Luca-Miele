# E3 — Deliverability, list health and UK promo-email law (SANTO)

Researched 2026-09-25. About 55 web searches plus read-only checks in SANTO's Klaviyo account. WebFetch was blocked for help.klaviyo.com, klaviyo.com, legislation.gov.uk and assets.publishing.service.gov.uk, so statutory and guidance wording below comes from search-result extracts of those pages and from law-firm summaries. Nothing here is legal advice. Anything that relies on the "[Account notice]" framing should be checked with a UK consumer lawyer before it is used again.

Strength key: **A** = official source, a large dataset, or several independent sources agree · **B** = one credible source · **C** = claim or practitioner opinion.

---

## 0. What SANTO's Klaviyo account shows (read-only checks today)

- **Branded sending domain exists and is active:** `send.santo.clothing`, purpose marketing, status active. SPF/DKIM on a branded domain is therefore probably in place. DMARC record and alignment were not checked and should be confirmed in Postmaster Tools v2 (see F3).
- **The "engaged" segment is inflated by machine opens.** Segment `4. [NEW] Engaged Non-Purchasers (90d)` (id WRjMzP) = **31,774 profiles**, defined as "opened OR clicked in last 90 days" **with no machine-open or bot-click filter**. On a 36–43k list, that treats about 80% of the list as "engaged" while campaign click rates are 0.25–0.6%. Most of those "opens" are almost certainly Apple MPP or other machine opens.
- The Aug-2026 wallet segment (R7dsU8) *does* filter correctly (`machine_open = false`, `Bot Click = false`). Its "engaged in 90d and did not open the wallet email" branch holds **3,643 profiles**. So human-engaged profiles number in the low thousands to high single thousands, not ~32k.
- A segment named `DIAG - Past customers, no email consent (soft opt-in pool)` exists. See F17 before anyone emails it.
- The segment name `Wallet Credit £9.34` suggests one flat credit amount was sent to thousands of people. That matters legally (F14).

**Diagnosis in one line:** SANTO is mailing ~36–43k people when only a few thousand are real humans who engage. The unengaged majority produce the unsubscribes and spam complaints, and they drag down inbox placement for everyone else. The 5% click on the credit email partly reflects a sharper offer and partly a subject line that looked like a service notice. That second part carries legal risk (F13–F15).

---

## PART A — Deliverability and list health

### F1. Treat Gmail/Yahoo/Microsoft rules as a pass/fail gate: one-click unsubscribe, authentication, spam rate under 0.1% (never 0.3%)
- **Do:** Confirm all four:
  1. SPF, DKIM and DMARC pass with the From domain aligned.
  2. RFC 8058 `List-Unsubscribe` plus `List-Unsubscribe-Post` headers are present, and a visible unsubscribe link sits in the body.
  3. Opt-outs are processed within 2 days.
  4. Gmail user-reported spam stays **under 0.10%** and never reaches **0.30%**.
- **Why:**
  - Google says rates above 0.1% hurt inbox placement. At 0.3% or more a sender loses mitigation support until the rate stays under 0.3% for 7 consecutive days. Since November 2025 Gmail rejects non-compliant mail (temporary or permanent 550 errors) instead of only filtering it ([Gmail sender FAQ](https://support.google.com/a/answer/14229414?hl=en); [Spam Resource, Nov 2025](https://www.spamresource.com/2025/11/google-warns-sender-requirements.html); [Red Sift](https://redsift.com/blog/gmails-enforcement-ramps-up-what-bulk-senders-need-to-know); [DMARCPal](https://dmarcpal.com/learn/google-enforcement-after-november-2025-bulk-sender-rejections)).
  - Yahoo requires one-click unsubscribe (RFC 8058 preferred), a visible body link, and processing within 2 days ([Yahoo Sender Hub](https://senders.yahooinc.com/best-practices/); [Valimail](https://www.valimail.com/blog/one-click-unsubscribe/)).
  - Microsoft began rejecting non-compliant high-volume senders (5,000+/day) with `550 5.7.15` from 5 May 2025. It requires SPF, DKIM and DMARC at p=none or stricter, aligned ([Microsoft Tech Community](https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730); [dmarcian](https://dmarcian.com/microsoft-enforces-spf-dkim-dmarc/)).
- **Strength:** A
- **For SANTO:** A 40k send can cross 5,000/day to Gmail. Set up Google Postmaster Tools v2 for `santo.clothing` today (F3). Remove the stated 0.4–1.1% unsubscribe rate as a risk by cutting send volume to unengaged profiles (F4, F5). Each unsubscribe is a person who might otherwise have pressed "spam".

### F2. Stop using opens to decide who is "engaged". Apple MPP makes opens meaningless
- **Do:** Rebuild every engaged segment as follows:
  - **Clicked email (Bot Click = false)** in the window, OR
  - **Opened email where Apple Privacy Open = false / machine_open = false**, OR
  - Placed order in the window, OR
  - Subscribed in the last 15 days.

  Report clicks and revenue per recipient, not opens.
- **Why:**
  - Klaviyo tags every open with `Apple Privacy Open` true/false and tells users to filter on false. It keeps an "OR clicked" branch so MPP users who really click stay included ([Klaviyo Help – MPP opens](https://help.klaviyo.com/hc/en-us/articles/4416791883163)).
  - Klaviyo also separates MPP opens from other machine opens made by security scanners ([Klaviyo Community](https://community.klaviyo.com/marketing-30/machine-opens-vs-apple-mpp-opens-10474)).
  - Apple Mail accounts for about 49–50% of all opens in Litmus data, and 50–65% for mobile-first B2C audiences ([Litmus market share](https://www.litmus.com/email-client-market-share); [Sender.net](https://www.sender.net/blog/apple-mail-privacy-protection/)).
- **Strength:** A
- **For SANTO:** Segment WRjMzP (31,774) counts machine opens. Duplicate it with the machine-open and bot-click filters and compare counts. Expect a large drop, probably to under 10k given the 3,643 figure above.

### F3. Monitor reputation in Postmaster Tools v2, not only in Klaviyo
- **Do:**
  - Verify `santo.clothing` in Google Postmaster Tools v2.
  - Check the **Compliance status** page, which shows pass/fail for each sender requirement.
  - Check the **user-reported spam rate** weekly.
  - Also watch Klaviyo's deliverability score: aim for 75 or above, 90 or above is excellent. It needs at least 1,000 sends in 30 days to show.
- **Why:**
  - Google retired Postmaster v1 in Sept–Oct 2025, including the domain and IP reputation dashboards.
  - v2 adds a Compliance Status dashboard. Its spam rate counts only mail that reached the **inbox** and was then reported. So spam-foldered mail hides the problem ([Braze](https://www.braze.com/resources/articles/google-postmaster-tools-v1-interface-retirement); [Suped](https://www.suped.com/blog/understanding-google-postmaster-tools-v2-spam-rate-dashboard)).
  - Klaviyo score ranges are from [Klaviyo deliverability FAQ](https://help.klaviyo.com/hc/en-us/articles/16425927010075) and [Klaviyo – understanding deliverability](https://help.klaviyo.com/hc/en-us/articles/115005247008), via search extracts.
- **Strength:** A (Google) / B (Klaviyo score bands)
- **For SANTO:** A low spam rate in v2 while clicks are 0.3% can mean mail is going to spam. It is not proof of good health.

### F4. Send campaigns to a 30/60/90-day engaged segment by default. Mail the full list rarely or never
- **Do:**
  - **Default audience:** clicked or real-opened in 60 days, OR ordered in 90 days, OR subscribed in 15 days.
  - **High-value or credit emails:** 90 days.
  - **Daily or near-daily sends:** 30 days only.
  - **180-day engaged:** at most once a week.
  - **Full list:** never, except inside a planned re-engagement test.
- **Why:**
  - Klaviyo recommends 30/60/90-day engaged segments. Its cadence guidance is: 30-day daily, 60–90-day three times a week, 180-day weekly.
  - Daily senders should use 30-day criteria; weekly or monthly senders can widen to 60–90 days ([Klaviyo glossary](https://www.klaviyo.com/glossary/what-is-an-engaged-segment); [Klaviyo Academy](https://academy.klaviyo.com/en-us/certificates/deliverability-certificate/courses/strengthen-your-sender-reputation/lessons/build-your-engaged-segments); [Klaviyo Help](https://help.klaviyo.com/hc/en-us/articles/115000200072)).
- **Strength:** A (vendor guidance, widely repeated)
- **For SANTO:** Next campaign goes to engaged-60d (MPP-filtered) plus ordered-90d plus new-15d only. Expected results: sends fall from ~40k to perhaps 5–12k, click rate rises, and unsubscribe and complaint rates fall. Revenue per recipient is the KPI.

### F5. Run a sunset flow, then suppress
- **Do:** Build a sunset flow with these steps:
  1. **Entry:** on list at least 120 days, no human open or click in 90 days, no order in 180 days.
  2. **Emails:** 2 emails, 4–5 days apart. The first is a plain-text "Still want these?" with a one-tap "Keep me on". The second is the best real offer.
  3. **After:** set `Unengaged = true` 14 days after email 2. Exclude those profiles from all campaigns, or suppress them.
- **Why:**
  - Klaviyo's own sunset guidance and several agencies describe 90–180-day inactivity triggers, a 2–3 email last-chance sequence, then suppression ([Klaviyo blog – sunset flow](https://www.klaviyo.com/blog/sunset-flow); [Klaviyo Help – list cleaning](https://help.klaviyo.com/hc/en-us/articles/360044054732); [Sweat Pants Agency](https://www.sweatpantsagency.com/blog/klaviyo-sunset-flow)).
  - Klaviyo's reputation-repair process also removes unengaged profiles automatically ([Klaviyo reputation repair AI](https://help.klaviyo.com/hc/en-us/articles/28311927819163)).
- **Strength:** A/B
- **For SANTO:** It also cuts Klaviyo profile costs. Suppressed profiles can still enter the SMS and retargeting audiences they consented to.

### F6. If placement is already damaged, use a structured recovery: 30-day engaged for about 2 weeks, then widen
- **Do:**
  - **Weeks 1–2:** send only to clicked in 30 days OR subscribed in 15 days.
  - **Weeks 3–4:** widen to 60 days if the score is at least 75 and click rates hold.
  - **Later:** widen to 90 days.
  - Throughout: never jump back to the full list.
- **Why:** This is the recovery Klaviyo documents. Campaigns go only to engaged segments and the criteria widen as the 30-day deliverability score recovers above 75. It recommends two weeks on 30-day engaged before broadening ([Klaviyo reputation repair](https://help.klaviyo.com/hc/en-us/articles/8983758025883); [Klaviyo reputation repair AI](https://help.klaviyo.com/hc/en-us/articles/28311927819163)).
- **Strength:** A (vendor process)
- **For SANTO:** Use this if Postmaster v2 shows spam above 0.1% or the Klaviyo score is under 75.

### F7. The unsubscribe rate is partly a Gmail artefact, but still a real signal
- **Do:**
  - Measure **unique** unsubscribes by mailbox provider.
  - Keep the target at **0.3% or less per campaign** (Klaviyo's guidance) and aim for about 0.2% (benchmark).
  - Do not panic over Gmail spikes from July to August 2025 onward.
- **Why:**
  - Gmail's "Manage subscriptions" (from 8 July 2025) put bulk unsubscribe one tap away. Senders saw unsubscribe rates up 50–300%.
  - Part of this is inflated because Gmail can fire several unsubscribe requests per click. Unique unsubscribes rose only modestly ([Google Workspace Updates](https://workspaceupdates.googleblog.com/2025/07/manage-email-subscriptions-in-gmail.html); [emailexpert](https://emailexpert.com/gmails-new-subscription-management-feature-a-deep-dive-into-its-rollout-and-impact-on-marketer-unsubscribe-rates/); [MarTech](https://martech.org/email-retention-after-gmails-manage-subscriptions-rollout/)).
  - Klaviyo's target is an unsubscribe rate under 0.3% per campaign, because mailbox providers read high unsubscribes as unwanted mail ([Klaviyo anti-abuse](https://help.klaviyo.com/hc/en-us/articles/115000308972)).
  - Industry average is about 0.2% unsubscribe and about 0.02% spam ([GOSH Digital](https://www.goshdigital.co/blog/klaviyo-benchmarks-by-industry); [Threadpoint](https://www.threadpoint.agency/blogs/learn-e-mail-marketing/whats-a-good-email-open-rate-for-ecommerce-2026-benchmarks)).
- **Strength:** A (Gmail feature) / B (size of inflation)
- **For SANTO:** Even allowing for inflation, 0.4–1.1% on 40k sends means 160–440 opt-outs per email. That is list decay of roughly 10–20% a year at the current cadence. Segmenting (F4) is the fix, not wording.

### F8. Frequency: keep Smart Sending on and do not stack sends
- **Do:**
  - Keep Klaviyo Smart Sending **on** for campaigns (default window 16 hours).
  - Consider raising it to 24–48h while the list is recovering.
  - Keep the drop-day series to 2 emails to the full engaged audience, with further emails to clickers or non-buyers only.
  - Never send 4-part series to everyone.
- **Why:**
  - Smart Sending skips anyone emailed within the window (default 16h). Skipped people are not rescheduled ([Klaviyo Smart Sending](https://help.klaviyo.com/hc/en-us/articles/115002779311)).
  - Frequency data from clothing retailers:
    - Complaints climb fast above about 5 emails a week ([Zettasphere](https://www.zettasphere.com/email-frequency-send-sweet-spot-is-6-emails-per-week/)).
    - An apparel case that went from 2 a week to daily saw unsubscribes rise from under 0.3% to over 1.2% and clicks per send halve within 6 weeks ([Bulk Email Checker](https://bulkemailchecker.com/blog/email-sending-frequency-guide/)).
- **Strength:** A (Smart Sending) / C (the case studies)
- **For SANTO:** The "DROP DAY 1/4" naming suggests 4 sends per drop. Cut to 2 plus behaviour-triggered follow-ups (clicked, did not buy).

### F9. Send time for UK: Thursday or Friday mid-morning to lunchtime, then test with Smart Send Time
- **Do:**
  - Default **Thursday or Friday, 11:00–12:30 UK time**.
  - Payday timing: today, 25 Sept, is a Friday payday. Send before lunch.
  - Once a campaign audience is at least 12,000, run Klaviyo Smart Send Time. Below 12k it is not available, so A/B test by hand (e.g. 11:00 vs 19:30).
- **Why:**
  - Klaviyo's data shows Wednesday and Thursday strongest overall, and Thursday highest on revenue despite lower opens.
  - It recommends Friday mid-morning for weekend-planning shoppers ([Klaviyo UK – best send times](https://www.klaviyo.com/uk/blog/best-email-send-times); [Klaviyo – best day](https://www.klaviyo.com/blog/best-day-to-send-emails)).
  - Smart Send Time needs at least 12,000 recipients ([Klaviyo Help – Smart Send Time](https://help.klaviyo.com/hc/en-us/articles/360029794371)).
  - Payday is a hypothesis, not a proven effect.
- **Strength:** B (day/time) / C (payday)
- **For SANTO:** Once sends move to engaged-only (F4), the audience may fall below 12k. Hand-test then.

### F10. Spam trigger words are mostly a myth, but keep the brand's no-shouting rule anyway
- **Do:**
  - Do not waste time scrubbing words like "free".
  - Do avoid what gets people to press "spam": misleading subject lines, all-caps, "!!!", and emoji stacks.
- **Why:** Litmus and others show modern filters work mainly on reputation, authentication and engagement, not keyword lists. A strong sender can write "FREE!!!" and land in the inbox, while a burned sender goes to spam whatever the copy ([Litmus](https://www.litmus.com/blog/why-spam-trigger-words-are-a-thing-of-the-past); [MailTester](https://mailtester.com/blog/spam-trigger-word-myths-debunked-deliverability-data/)).
- **Strength:** A
- **For SANTO:** The brand rules (plain English, no hype) are right for a different reason: they reduce complaints and help "look like a person", which lifts engagement. "ITS LIVE, FIRST 10 ORDERS ARE FREE!" underperformed because of who it went to and what it said, not because of banned words.

### F11. No all-image emails: live text for headline, offer and CTA; stay under ~90KB
- **Do:**
  - Headline, offer line, price and CTA button in **live HTML text**. Images for product shots only. Alt text on every image.
  - Keep total HTML **under 90KB** (Gmail clips at about 102KB).
  - Put the unsubscribe link and legal footer inside the unclipped area. Run a Klaviyo preview size check.
- **Why:**
  - The 60/40 ratio is outdated. Single-image emails with no live text are the real problem for filters and screen readers ([Email on Acid](https://www.emailonacid.com/blog/article/email-deliverability/does-text-to-image-ratio-affect-deliverability/); [Mailflow Authority](https://mailflowauthority.com/email-content/image-to-text-ratio)).
  - Gmail clips HTML over about 102KB and hides the rest behind "View entire message". That can hide the tracking pixel and the footer, including the unsubscribe link ([Klaviyo – clipping](https://help.klaviyo.com/hc/en-us/articles/115000591251); [Email on Acid](https://www.emailonacid.com/blog/article/email-development/gmail-email-clipping/)).
  - A hidden unsubscribe link pushes people to the "spam" button instead.
- **Strength:** A
- **For SANTO:** The build pipeline (`build_emails.py`) should print the final HTML size and fail above 90KB.

### F12. Dark mode: plan for it with SANTO's Ink/Bone palette
- **Do:**
  - Use Ink `#0A0A0B` and Bone `#F3F0EA` rather than pure #000/#FFF.
  - Use transparent PNG logos with a thin Bone or Ink stroke or glow so they survive colour inversion.
  - Never put text inside images on a light background.
  - Test in Apple Mail, Gmail app and Outlook dark mode.
  - Signal Red `#E10600` stays legible on both.
- **Why:**
  - Clients either leave colours alone, partly invert or fully invert. Dark logos vanish.
  - Guidance is to avoid pure black and white, add strokes to logos, and avoid single-image emails.
  - Litmus-cited data says more than 80% of people use dark mode on at least one device ([Litmus dark mode guide](https://www.litmus.com/blog/the-ultimate-guide-to-dark-mode-for-email-marketers); [Customer.io](https://customer.io/learn/message-composing/email-dark-mode); [Email on Acid](https://www.emailonacid.com/blog/article/email-development/dark-mode-for-email/)).
- **Strength:** B
- **For SANTO:** The brand palette is already close to dark-safe. The main risk is the black wordmark on transparent PNG.

---

## PART B — UK law for promo emails (2026)

### F13. The regulator now fines directly: CMA up to 10% of global turnover (DMCC Act, since 6 April 2025), and it is using the power
- **What:**
  - From 6 April 2025 the CMA can decide for itself that consumer law was broken and fine up to **£300,000 or 10% of global turnover, whichever is higher**, without going to court.
  - **Banned practices** (Schedule 20, 32 items) and **omissions** are unlawful whether or not they change consumer behaviour.
  - Misleading actions are judged against the "average consumer" and a "transactional decision". That decision can be as small as **clicking** ([Shoosmiths](https://www.shoosmiths.com/insights/articles/dmcc-new-consumer-enforcement-powers-are-now-in-force); [Linklaters](https://www.linklaters.com/en/insights/blogs/linkingcompetition/2025/april/consumer-deep-dive---understanding-unfair-commercial-practices-under-the-dmcc); [Baker Botts](https://www.bakerbotts.com/thought-leadership/publications/2025/april/new-cma-consumer-protection-comes-into-force)).
- **Enforcement so far:**
  - Nov 2025: 8 investigations, covering drip pricing, **false time-limited sales claims** (Wayfair, Appliances Direct) and default opt-ins. Warning letters went to 100 firms ([GOV.UK press release](https://www.gov.uk/government/news/cma-launches-major-consumer-protection-drive-focused-on-online-pricing-practices); [TLT](https://www.tlt.com/insights-and-events/insight/eight-enforcement-cases-and-a-hundred-warnings)).
  - June 2026: Marks Electrical fined £720k for opt-in charges ([Mondaq](https://www.mondaq.com/uk/consumer-law/1808790/cma-consumer-protection-enforcement-in-2026-the-cma-flexes-its-new-powers)).
  - June 2026: StubHub fined £889,200 (about £900k) plus £590k in refunds for drip pricing ([TLT](https://www.tlt.com/insights-and-events/insight/dmcca-penalty-3-cma-fines-stubhub-over-drip-pricing); [Music Ally](https://musically.com/2026/06/24/uk-competition-watchdog-levies-900k-fine-on-stubhub-uk-and-orders-additional-590k-refund-to-customers/)).
  - 22 May 2026: High Court consent order in which Emma Sleep agreed to stop misleading countdown timers and "high demand" claims ([GOV.UK](https://www.gov.uk/government/news/court-endorses-cma-action-as-emma-sleep-agrees-to-change-sales-practices); [Lewis Silkin](https://www.lewissilkin.com/insights/2026/05/29/uk-consumer-law-revolution-emma-sleep-case-is-partly-settled-but-the-other-part-102mx9f)).
- **Strength:** A
- **For SANTO:** The CMA targets big firms first. Trading Standards and the ASA handle small brands, so the practical risks are an ASA ruling, a Trading Standards letter or a platform complaint. The legal standard is the same, though, and the £300k floor exists.

### F14. "Expires in 7 days" / "expires in 49 hours" is lawful only if literally true for that person and it really ends
- **Rule:**
  - DMCC Sch. 20 para 7 bans **falsely stating that a product, or particular terms, will only be available for a limited time** in order to force an immediate decision. The old word "very" was dropped, so any false time limit is caught ([search extract of legislation.gov.uk Sch. 20](https://www.legislation.gov.uk/ukpga/2024/13/schedule/20); [Lexology](https://www.lexology.com/library/detail.aspx?g=1ae20289-db05-4cb8-9ebb-0a4f9c4ff7b5)).
  - CMA207 (final, 18 Nov 2025) says a trader using a countdown must be able to **substantiate** it. It is misleading if the timer hits zero and nothing changes, or if a near-identical offer starts soon after ([CMA207 on GOV.UK](https://www.gov.uk/government/publications/unfair-commercial-practices-cma207/unfair-commercial-practices); [Ashurst](https://www.ashurstperkinscoie.com/en/insights/mind-the-nudge-the-dmccs-crackdown-on-manipulative-online-design/)).
  - The CMA's 2023 urgency principles also say that when a countdown ends, the offer must end, with no comparable offer shortly after ([Travers Smith](https://www.traverssmith.com/knowledge/knowledge-container/cma-warns-online-b2c-businesses-against-misleading-urgency-and-pricing-claims/); [Bird & Bird](https://www.twobirds.com/en/insights/2023/uk/taking-the-pressure-off)).
  - ASA 2025: a countdown was ruled misleading because it implied the "up to 40% off" sale ended with the "extra 5%" when the sale actually ran another week ([Lewis Silkin, Oct 2025](https://www.lewissilkin.com/en/insights/2025/10/13/times-up-asa-rules-on-countdown-timers-and-pricing-claims-102lp6g)).
- **Allowed:** A real credit with a real expiry, e.g. a credit issued on 20 Sept that is voided at 23:59 on 27 Sept, stated as "Expires Sat 27 Sept, 23:59".
- **Not allowed:**
  - Sending the same £9.34 "expires" email again next month.
  - Extending it quietly.
  - A "49 hours" countdown that restarts.
- **Strength:** A
- **For SANTO:** Before any expiry email, write down the voiding date and have Shopify or Klaviyo actually void the code or credit then. Do not reissue an identical £9.34 credit within about 30 days. Put the exact date and time in the body, which is also a CAP 8.17 significant condition (F19).

### F15. "[Account notice]" subject lines are the biggest legal risk in SANTO's best-performing email
- **Rules:**
  - **CAP Code 10.6 and 2.1:** marketing must be obviously identifiable as marketing, and unsolicited marketing emails must be identifiable as marketing **without being opened** ([CAP Code section 2](https://www.asa.org.uk/type/non_broadcast/code_section/02.html); [Pinsent Masons – CAP Code for email](https://www.pinsentmasons.com/out-law/guides/the-cap-code)).
  - **CAP 3.1 / DMCC misleading action:** a subject line that makes people think this is a service message about their account, when it is a promotion, is likely to mislead them into the "transactional decision" of opening or clicking (F13).
  - **ICO/PECR:** marketing dressed as a service message is still marketing. The ICO fined Flybe £70k for "Are your details correct?" emails sent to opted-out customers. A service message stops being one once it contains significant promotional content ([Hogan Lovells](https://www.hldataprotection.com/2017/03/articles/international-eu-privacy/ico-issues-fine-for-marketing-emails-disguised-as-service-messages/); [ICO – identify direct marketing](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/direct-marketing-guidance/identify-direct-marketing/)).
  - **DMCC Sch. 20 para 24** bans marketing that includes an invoice-like document giving the impression the consumer already ordered. This is a related "fake transactional" ban, but it does not fit SANTO's email exactly ([search extract of Sch. 20](https://www.legislation.gov.uk/ukpga/2024/13/schedule/20)).
  - The ASA has also upheld against an ad that looked like an invoice (Worldwide Trademarks, March 2024) ([Taylor Wessing Q1 2025](https://www.taylorwessing.com/en/insights-and-events/insights/2025/03/aq-top-10-asa-rulings-q1-2025)).
- **Allowed:** Telling someone they have credit, **if the credit really exists on their account or as a unique code issued to them**, in a subject line that still reads as a brand message. Examples:
  - "Your £9.34 SANTO credit ends Sunday"
  - "{first_name}, £9.34 off — yours until Sun 23:59"
- **Risky:**
  - A "[Account notice]" prefix. It copies the format of security or billing emails and adds nothing except disguise.
  - "Active on your account now" when there is no account balance (e.g. one shared discount code).
- **Strength:** A for the rules. There is **no** specific ASA ruling on an "[Account notice]" email subject; that was searched for and not found. The risk rating comes from applying the rules, not from precedent.
- **For SANTO:**
  - Drop the "[Account notice]" prefix.
  - Keep the parts that worked: the name, an exact £ amount, a real deadline, "no minimum spend".
  - The Aug-2026 segment is named "Wallet Credit £9.34". If every recipient got the same flat £9.34, make sure it is a real per-customer credit or unique code before calling it "your credit" or "on your account". If it isn't, call it an offer: "£9.34 off, no minimum, ends Sunday".
  - Inbox placement reason too: making promotions look transactional erodes trust, and Apple's iOS 18 categories and Gmail tabs classify by content anyway ([Apple Support – Mail categories](https://support.apple.com/guide/iphone/use-categories-iphfe4a36baf/ios)).

### F16. "Free gift" / "you forgot your free gift": allowed only under strict conditions
- **Rules:**
  - DMCC Sch. 20 bans describing something as **"free", "gratis" or "without charge"** if the consumer must pay anything beyond the unavoidable cost of responding and collecting or delivery.
  - It also bans creating the **false impression** that the consumer has already won or will win a prize or benefit, or must pay to claim it ([Business Companion](https://www.businesscompanion.info/en/quick-guides/fair-trading/protection-from-unfair-trading-from-april-2025); [Sch. 20 extract](https://www.legislation.gov.uk/ukpga/2024/13/schedule/20)).
  - CAP allows "free with purchase" only if the gift is genuinely extra: the paid item's price is not inflated and its quality is not reduced to cover the gift ([ASA – use of "free"](https://www.asa.org.uk/advice-online/use-of-free.html); [CAP free guidance](https://www.asa.org.uk/resource/free-claims.html)).
  - Any purchase requirement is a **significant condition** and must appear in the email itself, not only in the T&Cs (F19).
- **Allowed:**
  - "Free hat with any order over £X — ends Sun 23:59", with the minimum spend in the preview or first lines.
  - "We are holding a free hat for you", only if a hat really is reserved.
- **Not allowed:**
  - "You forgot your free gift" when the person never claimed or triggered one. That implies a benefit already won.
  - "Free" when the hat needs a purchase that is not stated up front.
  - "Shipping is covered" if a minimum spend applies and is not stated.
- **Strength:** A
- **For SANTO:** The 4.15%-click "free gift" email should say the qualifying condition within the first screen. Only use "forgot" if a cart or claim event exists (e.g. an abandoned-cart flow that already showed the gift).

### F17. PECR consent and soft opt-in: whose inbox you may email
- **Rules:**
  - Unsolicited marketing email to individuals needs **consent** or the **soft opt-in**. Soft opt-in covers existing customers, with details collected during a sale or sale negotiation, for similar products, **and** an opt-out offered at collection and in every message ([ICO – electronic mail marketing](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/); [ICO – how to comply](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/how-do-we-comply-with-the-pecr-electronic-mail-marketing-rules/)).
  - PECR reg. 23: the sender must not be disguised, and a valid opt-out address is required ([Better Regulation – reg 23](https://service.betterregulation.com/document/244592)).
  - An email asking for marketing consent is itself marketing (Flybe/Honda fines, 2017) ([RPC](https://www.rpclegal.com/snapshots/data-protection/ico-issues-fines-for-emails-seeking-consent-to-marketing/)).
  - **Penalties:** since 5 Feb 2026 (Data (Use and Access) Act 2025) maximum PECR fines rose from £500k to **£17.5m or 4% of global turnover** ([Clifford Chance](https://www.cliffordchance.com/insights/resources/blogs/talking-tech/en/articles/2026/02/key-aspects-of-the-data--use-and-access--act-take-effect.html); [MFMac](https://www.mfmac.com/insights/data-protection/data-use-and-access-act-2025-increased-maximum-fines-for-cookies-and-direct-marketing-practices/)).
- **Strength:** A
- **For SANTO:** Emailing the `DIAG - Past customers, no email consent (soft opt-in pool)` segment is lawful **only if** checkout clearly offered an opt-out when the email was collected. If Shopify checkout had no clear opt-out, those people cannot be emailed. You cannot send them a "do you want our emails?" email either. Also check this pool is not used for the drop-day or credit blasts by accident.

### F18. Price claims in subject lines: "Up to 80% off" needs a real share of stock at 80%, and "was" prices must be genuine
- **Rules:**
  - ASA/CTSI: an "up to X% off" claim needs a **significant proportion**, around 10% as a rule of thumb, of sale items at the maximum discount.
  - An "up to 70% + extra 10%" claim was upheld when only 8.63% of items reached the maximum ([ASA – promotional savings](https://www.asa.org.uk/advice-online/promotional-savings-claims.html); [ASA – prices general](https://www.asa.org.uk/advice-online/prices-general.html); [CTSI pricing guidance, Aug 2025](https://www.businesscompanion.info/en/guidance-for-traders-on-pricing-practices)).
  - Reference ("was") prices must be genuine. On 30 July 2026 the High Court rejected the CMA's fixed 1:2 volume test (*CMA v Emma*), but traders must still substantiate that the "was" price was real ([HSF Kramer](https://www.hsfkramer.com/notes/crt/2026-07/high-court-rejects-cmas-fixed-volume-requirement-for-reference-pricing-in-emma-matratzencase); [Stephenson Harwood](https://www.shlegal.com/insights/discount-claims-after-emma-sleep-what-this-means-for-your-business/)).
  - Drip pricing ban (DMCC): the headline price must include all mandatory charges ([Linklaters](https://www.linklaters.com/en/insights/blogs/linkingcompetition/2025/june/consumer-deep-dive_understanding-drip-pricing-under-the-dmcc)). Shipping is fine to show separately if it is optional or chosen, but "£33" must not become £33 plus a mandatory "service fee".
- **Strength:** A
- **For SANTO:** The loser "🍂 Fall Essentials – Up to 80% Off" was also a legal risk unless at least ~10% of lines were really 80% off. Prefer a single true number: "£20 off hoodies".

### F19. Every promotion email must carry its significant conditions itself
- **Rule:** CAP 8.17 requires all significant conditions in the ad itself: closing date, minimum spend, eligibility, and number of gifts or winners. A closing date only in separate T&Cs is unlikely to be acceptable ([ASA – closing dates](https://www.asa.org.uk/advice-online/promotional-marketing-closing-dates.html); [ASA – T&Cs and significant conditions](https://www.asa.org.uk/advice-online/promotional-marketing-terms-and-conditions-tcs.html); [CAP section 8](https://www.asa.org.uk/type/non_broadcast/code_section/08.html)).
- **Strength:** A
- **For SANTO:** Every email needs a one-line conditions strip under the CTA, in Space Mono, e.g. "£9.34 off, no minimum. One use. Ends Sun 28 Sept 23:59 BST. UK & intl." For "FIRST 10 ORDERS ARE FREE!" the email must say how the 10 are chosen and how people know if they won. Otherwise it breaks the prize or instant-win rules.

### F20. Urgency and scarcity copy that is still allowed
- **Allowed if true and substantiated:**
  - "Ends Sunday 23:59" when the price actually reverts.
  - "Last 14 in size M" when stock data shows it.
  - "Restock not planned" only when that is true.
  - "Drop closes at midnight" when the collection really comes down.
- **Not allowed:**
  - "Only 5 left" when stock can be replenished.
  - "10 people viewing".
  - Reopening a "last chance" offer.
  - Several urgency claims stacked together, which the CMA says is more likely to be treated as unfair ([CMA207 summary via search](https://www.gov.uk/government/publications/unfair-commercial-practices-cma207/unfair-commercial-practices); [Travers Smith](https://www.traverssmith.com/knowledge/knowledge-container/cma-warns-online-b2c-businesses-against-misleading-urgency-and-pricing-claims/)).
- **Strength:** A
- **For SANTO:** "Last chance" (0.27% click) failed commercially anyway. Replace it with one precise, true deadline.

### F21. US subscribers: Washington State CEMA makes a false subject line a $500-per-email claim
- **What:** *Brown v. Old Navy* (Wash. Sup. Ct., 17 Apr 2025) held that **any** false or misleading information in a subject line sent to a Washington resident breaches CEMA, with $500 statutory damages per email. Class actions followed over "today only", "last chance" and "ends tonight" ([Justia – opinion](https://law.justia.com/cases/washington/supreme-court/2025/102-592-1.html); [K&L Gates](https://www.klgates.com/Washington-Supreme-Court-Increases-Risks-of-Lawsuits-for-False-or-Misleading-Email-Subject-Lines-8-7-2025); [Ballard Spahr, Apr 2026](https://www.ballardspahr.com/insights/alerts-and-articles/2026/04/cema-ingly-endless-litigation-brown-v-old-navy-turns-1-year-old)).
- **Strength:** A
- **For SANTO:** The US is the 2nd market. Either exclude US profiles from urgency or credit-expiry sends (they also convert 7x worse), or make sure every subject-line deadline is literally true.

---

## Do / Don't (next email)

**Do**
- Send to MPP-filtered engaged-60d + ordered-90d + subscribed-15d. Exclude `Unengaged = true` and the soft opt-in pool unless its consent is verified.
- Use a subject that reads as SANTO, not as a system alert, e.g. "{first_name}, your £9.34 ends Sunday" or "Sweatshirt weather. £9.34 off, no minimum."
- Put the exact deadline in the body ("Ends Sun 28 Sept, 23:59 BST") and void the credit then.
- Add a one-line conditions strip under the CTA (CAP 8.17).
- Use live-text headline and CTA, HTML under 90KB, dark-mode-safe logo, unsubscribe link visible and unclipped.
- Send Friday 11:00–12:30 UK. Keep Smart Sending on.
- Track click rate, revenue per recipient, unique unsubscribes and Postmaster v2 spam rate. Ignore open rate.

**Don't**
- Don't use an "[Account notice]" or other system-alert prefix.
- Don't say "on your account" unless a real balance or unique code exists for that person.
- Don't reuse an "expires in 49 hours" clone, or reissue the same £9.34 "expiring" credit within about 30 days.
- Don't write "You forgot your free gift" without a real claim event, or "free" without stating the purchase condition up front.
- Don't claim "Up to 80% off" unless at least ~10% of items are at 80%. Don't use "Only X left" without stock data.
- Don't send full-list blasts or 4-email drop series to everyone.
- Don't send urgency subject lines to US (Washington) profiles unless they are literally true.

## Open questions

1. Is the £9.34 a real per-customer Shopify store credit or gift card balance, a unique discount code, or one shared code? This decides whether "your credit" / "on your account" wording is lawful (F15).
2. Was the credit actually voided at the stated expiry? Was it reissued, and when? (F14)
3. What does Postmaster Tools v2 show for `santo.clothing`: compliance status, spam rate, and DMARC policy and alignment? (F1, F3) Not checked. It needs Google account access.
4. How many profiles are in engaged-60d with MPP and bot filters, versus the 31,774 in WRjMzP? (F2)
5. How was consent collected for `DIAG - Past customers, no email consent (soft opt-in pool)`? Did checkout offer an opt-out? (F17)
6. What is Klaviyo's current deliverability score, and which inbox providers have the highest unsubscribe or complaint rates? (F3, F7)
7. How many US (especially Washington) profiles receive urgency emails? (F21)
