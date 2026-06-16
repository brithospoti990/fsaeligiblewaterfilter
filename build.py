#!/usr/bin/env python3
# Builds fsaeligiblewaterfilter.com — static, SEO-first, Vercel-ready.
import os, json, html

SITE = "https://fsaeligiblewaterfilter.com"
NAME = "FSA Eligible Water Filter"
AUTHOR = "Stephen Evangelista"
TODAY = "June 16, 2026"
FOUNDER_IMG = "https://bestwellwaterironfilter.com/wp-content/uploads/2026/06/Brian-Campbell.png"
EMAIL = "Stephen@fsaeligiblewaterfilter.com"
ROOT = "/home/claude/site"
URLS = []  # collected for sitemap generation

# SpringWell product URLs (used as the real href; rewritten by /js/affiliate.js if you add tracking links)
P = {
  "whole-house": "https://www.springwellwater.com/product/water-filters/whole-house-water-filters/",
  "filter-softener-combo": "https://www.springwellwater.com/product/dual-systems/water-filter-salt-softener/",
  "salt-free-combo": "https://www.springwellwater.com/product/dual-systems/water-filter-salt-free-conditioner/",
  "well-water": "https://www.springwellwater.com/product/well-water/whole-house-iron-filter/",
  "lead-cyst": "https://www.springwellwater.com/product/truemed-eligible-water-filters/whole-house-lead-cyst-removal-system/",
  "cartridge": "https://www.springwellwater.com/product/promotion/whole-house-cartridge-system/",
  "2in1-combo": "https://www.springwellwater.com/product/dual-systems/2-in-1-filter-salt-softener-combo-system/",
  "uv": "https://www.springwellwater.com/product/uv-systems/uv-water-purification-system/",
  "moen-ro": "https://www.springwellwater.com/product/under-sink-filtration/moen-reverse-osmosis-water-filtration-system/",
  "tannin": "https://www.springwellwater.com/product/water-filters/tannin-softener-system/",
  "truemed-eligible-category": "https://www.springwellwater.com/product-category/truemed-eligible-water-filters/",
  "truemed-how-it-works": "https://www.springwellwater.com/about/springwell-truemed-hsa-fsa-water-filters/",
}

# Real affiliate tracking links (Everflow, affid=40). Used to build cloaked /go/ redirects in vercel.json.
LINKS = {
  "whole-house": "https://www.springwellwater.com/product/water-filters/whole-house-water-filters/?oid=1&affid=40",
  "filter-softener-combo": "https://www.springwellwater.com/product/dual-systems/water-filter-salt-softener/?oid=10&affid=40",
  "salt-free-combo": "https://www.springwellwater.com/product/dual-systems/water-filter-salt-free-softener/?oid=4&affid=40",
  "well-water": "https://www.springwellwater.com/product/well-water/whole-house-iron-filter/?oid=3&affid=40",
  "lead-cyst": "https://www.springwellwater.com/product/water-filters/whole-house-lead-cyst-removal-system/?oid=7&affid=40",
  "cartridge": "https://www.springwellwater.com/product/water-filters/whole-house-cartridge-system/?oid=27&affid=40",
  "2in1-combo": "https://www.springwellwater.com/product/dual-systems/2-in-1-filter-salt-softener-combo-system/?oid=21&affid=40",
  "uv": "https://www.springwellwater.com/product/uv-systems/uv-water-purification/?oid=12&affid=40",
  "moen-ro": "https://www.springwellwater.com/product/under-sink-filtration/moen-reverse-osmosis-water-filtration-system/?oid=34&affid=40",
  "tannin": "https://www.springwellwater.com/product/water-filters/tannin-softener-system/?oid=20&affid=40",
  "test-kit": "https://www.springwellwater.com/product/water-testing/water-test-kit/?oid=8&affid=40",
  "pfas": "https://www.springwellwater.com/product/water-filters/whole-home-pfas-filter/?oid=37&affid=40",
  # Not in the affiliate feed; destination kept with affid for attribution. Replace with a dedicated Everflow offer link if available.
  "truemed-eligible-category": "https://www.springwellwater.com/product-category/truemed-eligible-water-filters/?affid=40",
  "truemed-how-it-works": "https://www.springwellwater.com/about/springwell-truemed-hsa-fsa-water-filters/?affid=40",
}

def aff(key, label, cls="btn"):
    # Cloaked link: points to /go/<key> on this domain; Vercel redirects to the real tracking URL.
    return (f'<a class="{cls}" data-aff="{key}" rel="sponsored nofollow noopener" '
            f'target="_blank" href="/go/{key}">{label} <span class="arr">&rarr;</span></a>')

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

def head(title, desc, path, schema_blocks=None, depth=0):
    pre = "../" * depth
    canonical = f"{SITE}/{path}".rstrip("/") if path else SITE
    if path == "":
        canonical = SITE + "/"
    schema_html = ""
    if schema_blocks:
        for b in schema_blocks:
            schema_html += f'\n<script type="application/ld+json">{json.dumps(b)}</script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,560;0,6..72,600;1,6..72,400&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}css/style.css">{schema_html}
</head>
<body>
{header(depth)}
<main>"""

def header(depth=0):
    pre = "../" * depth
    return f"""<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Primary">
      <a class="brand" href="{pre}index.html">
        <span class="seal">{CHECK}</span>
        <span><b>FSA Eligible Water Filter</b><small>Eligibility &amp; reviews</small></span>
      </a>
      <button class="nav-toggle" aria-label="Menu" aria-expanded="false">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
      <div class="nav-links">
        <a href="{pre}index.html">Eligibility guide</a>
        <a href="{pre}best-fsa-hsa-eligible-water-filters.html">Best systems</a>
        <a href="{pre}guides/letter-of-medical-necessity-water-filter.html">How to buy</a>
        <a href="{pre}reviews/springwell-whole-house-water-filter-review.html">Reviews</a>
        <a href="{pre}about.html">About</a>
        <a class="nav-cta" data-aff="truemed-eligible-category" rel="sponsored nofollow noopener" target="_blank" href="/go/truemed-eligible-category">Shop eligible systems</a>
      </div>
    </nav>
  </div>
</header>"""

def footer(depth=0):
    pre = "../" * depth
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <b>FSA Eligible Water Filter</b>
        <p>An independent resource explaining when water filtration qualifies as an HSA/FSA medical expense — and how to buy it with pre-tax dollars.</p>
        <address class="foot-contact">
          90 Madison St, 3rd Floor, Ste 306<br>Denver, CO 80206<br>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </address>
      </div>
      <div>
        <h5>Guides</h5>
        <ul>
          <li><a href="{pre}index.html">Are water filters eligible?</a></li>
          <li><a href="{pre}guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a></li>
          <li><a href="{pre}index.html#savings">Tax-savings math</a></li>
          <li><a href="{pre}index.html#how">How to buy with HSA/FSA</a></li>
        </ul>
      </div>
      <div>
        <h5>Reviews</h5>
        <ul>
          <li><a href="{pre}best-fsa-hsa-eligible-water-filters.html">Best eligible systems</a></li>
          <li><a href="{pre}reviews/springwell-whole-house-water-filter-review.html">SpringWell Whole House</a></li>
          <li><a href="{pre}reviews/springwell-filter-softener-combo-review.html">SpringWell Filter + Softener</a></li>
        </ul>
      </div>
      <div>
        <h5>Site</h5>
        <ul>
          <li><a href="{pre}about.html">About us</a></li>
          <li><a href="{pre}editorial-policy.html">Editorial &amp; eligibility policy</a></li>
          <li><a href="{pre}contact.html">Contact us</a></li>
          <li><a href="{pre}sitemap.html">Sitemap</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 2026 FSA Eligible Water Filter. Not tax, legal, or medical advice.</span>
      <span>Independent &middot; reader-supported via affiliate links</span>
    </div>
    <nav class="foot-legal" aria-label="Legal and policies">
      <a href="{pre}privacy-policy.html">Privacy Policy</a>
      <a href="{pre}terms-of-use.html">Terms of Use</a>
      <a href="{pre}cookie-policy.html">Cookie Policy</a>
      <a href="{pre}affiliate-disclosure.html">Affiliate Disclosure</a>
      <a href="{pre}disclaimer.html">Disclaimer</a>
      <a href="{pre}accessibility.html">Accessibility</a>
    </nav>
  </div>
</footer>
<script src="{pre}js/affiliate.js"></script>
<script src="{pre}js/main.js"></script>
</body>
</html>"""

DISCLOSURE = ('<div class="disclosure"><b>Disclosure:</b> This page contains affiliate links. '
              'If you buy through them we may earn a commission at no extra cost to you. We only '
              'recommend systems we believe are a genuine fit. See our '
              '<a href="{pre}affiliate-disclosure.html">affiliate disclosure</a>.</div>')

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(full) else None
    with open(full, "w") as f:
        f.write(content)
    if path.endswith(".html") and path != "404.html":
        URLS.append(path)
    # crude word count of body text for the long pages
    import re
    txt = re.sub(r"<[^>]+>", " ", content)
    words = len(txt.split())
    print(f"  {path}  (~{words} words incl. nav/footer)")

print("Building pages:")

def disc(depth=0):
    pre = "../" * depth
    return ('<div class="disclosure"><b>Disclosure:</b> This page contains affiliate links. '
            'If you buy through them we may earn a commission at no extra cost to you. We only '
            'recommend systems we believe are a genuine fit. See our '
            f'<a href="{pre}affiliate-disclosure.html">affiliate disclosure</a>.</div>')

def byline(depth=0):
    pre = "../" * depth
    return (f'<div class="byline"><div class="av"><img src="{FOUNDER_IMG}" alt="{AUTHOR}" width="46" height="46" loading="lazy"></div><div class="who">'
            f'<b>By {AUTHOR}</b><span>Water-treatment researcher &middot; '
            f'<a href="{pre}editorial-policy.html">How we verify eligibility</a> &middot; Updated {TODAY}</span></div></div>')

# ============================ HOMEPAGE / PILLAR ============================
faq_items = [
 ("Are water filters FSA or HSA eligible?",
  "Sometimes. A water filter is not automatically eligible the way bandages or contact-lens solution are. It can be paid for with HSA or FSA funds when it is used to treat, mitigate, or prevent a specific health condition and you have a Letter of Medical Necessity (LMN) from a licensed provider. Without an LMN, the IRS treats a filter as a personal expense."),
 ("What is a Letter of Medical Necessity?",
  "An LMN is a short document from a licensed provider stating that a product is needed to treat or prevent a medical condition. It turns an otherwise personal purchase into a qualified medical expense under IRS rules, similar to how a prescription qualifies a medicine. Services like TrueMed collect a brief health survey and have a provider issue the LMN."),
 ("How do I buy a SpringWell system with HSA/FSA money?",
  "At checkout you choose the TrueMed option, answer a short health questionnaire, and a licensed provider reviews it. If you qualify, you receive an LMN (often within a few hours) and pay with your HSA or FSA card. If your balance is short, you can split the payment with a regular card and submit the rest for reimbursement."),
 ("How much can I actually save?",
  "Because HSA/FSA money is set aside before income tax, you avoid paying tax on the dollars you spend. The effective discount equals your marginal tax rate, commonly 20-37%. On a $2,000 system, that can mean several hundred dollars back. Your exact savings depend on your bracket and plan."),
 ("Will my claim get denied?",
  "The most common reasons for denial are missing documentation and timing. The health survey/LMN must be dated on or before your purchase, you cannot apply an LMN retroactively, and you should keep the LMN and itemized receipt for your administrator. Confirm specifics with your plan administrator."),
 ("Can I use my FSA before the year-end deadline?",
  "Yes, and you usually should. Most FSA balances follow a use-it-or-lose-it rule and expire on December 31 (some plans offer a short grace period or small carryover). A qualifying water filter is a legitimate way to spend a balance you would otherwise forfeit."),
 ("Are replacement filter cartridges eligible too?",
  "They can be, on the same basis as the system: an LMN supports the medical necessity, and ongoing replacements may need to show the continued need. Keep receipts for each replacement and check your plan's documentation rules."),
 ("Is TrueMed available outside the United States?",
  "No. TrueMed and U.S. HSA/FSA accounts are available in the United States only."),
]

def faq_schema(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}

home_article_schema = {
  "@context":"https://schema.org","@type":"Article",
  "headline":"Are Water Filters FSA/HSA Eligible? The Complete 2026 Guide",
  "description":"Water filters can be HSA/FSA eligible with a Letter of Medical Necessity. Here is how eligibility works, how to buy with pre-tax dollars, and the best eligible systems for 2026.",
  "author":{"@type":"Person","name":AUTHOR},
  "publisher":{"@type":"Organization","name":NAME},
  "dateModified":"2026-06-16","mainEntityOfPage":SITE+"/"
}

faq_html = '<div class="faq">'
for q,a in faq_items:
    faq_html += f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>'
faq_html += '</div>'

home = head(
  "Are Water Filters FSA/HSA Eligible? 2026 Guide & Picks",
  "Water filters can be FSA/HSA eligible with a Letter of Medical Necessity. See how eligibility works, how to pay pre-tax, and the best systems for 2026.",
  "", [home_article_schema, faq_schema(faq_items)], depth=0)

home += f"""
<div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> &rsaquo; FSA/HSA eligibility guide</div>
<article class="hero">
  <span class="eyebrow">{CHECK} 2026 eligibility guide</span>
  <h1 class="prose">Are water filters FSA/HSA eligible?</h1>
  <p class="lede prose">Short answer: yes &mdash; but not automatically. A water filter becomes a qualified HSA or FSA medical expense when it is used to treat or prevent a health condition and you hold a <strong>Letter of Medical Necessity</strong>. This guide explains exactly how that works, how to pay with pre-tax dollars, and which systems qualify.</p>
  <div class="meta">
    <span>{CHECK} Reviewed against IRS Pub. 502 &amp; 969</span>
    <span>&middot; {AUTHOR}</span>
    <span>&middot; Updated {TODAY}</span>
    <span>&middot; 12 min read</span>
  </div>
</article>

<figure class="hero-figure" data-reveal>
  <img src="assets/water-filter-fsa-eligible.png" alt="A homeowner reviews a Letter of Medical Necessity and water test results at her kitchen counter, with a whole-house water softener and UV filter behind her, while planning an HSA/FSA-eligible water filter purchase." width="700" height="500" fetchpriority="high">
</figure>

<div class="prose">
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Eligibility ruling</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> Household water filters are treated as a personal expense by default. With an LMN tied to a health condition, they qualify for HSA/FSA reimbursement.</p>
  </div>

  {disc(0)}

  <div class="toc">
    <p class="lab">What this guide covers</p>
    <ol>
      <li><a href="#eligibility">The honest eligibility rule</a></li>
      <li><a href="#accounts">HSA vs FSA vs HRA vs LPFSA</a></li>
      <li><a href="#medical-necessity">What makes a filter "medically necessary"</a></li>
      <li><a href="#not-sure">Not sure you qualify?</a></li>
      <li><a href="#water-type">City water vs well water</a></li>
      <li><a href="#how">How to buy with pre-tax dollars</a></li>
      <li><a href="#savings">The tax-savings math</a></li>
      <li><a href="#best">Best eligible systems for 2026</a></li>
      <li><a href="#situations">Three situations like yours</a></li>
      <li><a href="#choose">How to choose the right one</a></li>
      <li><a href="#checklist">Before-you-buy checklist</a></li>
      <li><a href="#denied">Avoiding a denied claim</a></li>
      <li><a href="#myths">Five common myths</a></li>
      <li><a href="#faq">Frequently asked questions</a></li>
    </ol>
  </div>
</div>

<div class="prose">
  <h2 id="eligibility">The honest answer: eligible, with one condition</h2>
  <p>If you have searched for an "FSA eligible water filter," you have probably seen pages that shout a confident <em>"yes!"</em> The accurate answer is more useful: a water filter is not on the automatic eligibility list the way thermometers, bandages, or contact-lens solution are. The IRS treats ordinary household filtration &mdash; the kind you buy for better-tasting water &mdash; as a <strong>personal expense</strong>, which is not reimbursable.</p>
  <p>What changes the picture is <strong>medical necessity</strong>. Under IRS rules, an expense becomes a qualified medical expense when it is used primarily to <strong>treat, mitigate, or prevent a specific medical condition</strong>, and a licensed provider documents that need. For a water filter, that documentation is a <strong>Letter of Medical Necessity (LMN)</strong>. With one, the same filter that was a personal purchase yesterday becomes a qualified medical expense today &mdash; in the same category as a doctor visit or a prescription.</p>
  <div class="note key"><span class="lab">The rule in one sentence</span>A water filter is HSA/FSA eligible when it is bought to address a diagnosed or preventable health condition and is backed by a Letter of Medical Necessity from a licensed provider.</div>
  <p>This nuance is not a technicality to skim past &mdash; it is the whole game. Getting it right protects your tax advantage, keeps your claim from being denied, and tells you exactly what to do next. The rest of this guide walks through each step.</p>

  <h2 id="accounts">HSA vs FSA vs HRA vs LPFSA for a water filter</h2>
  <p>All four are tax-advantaged accounts, but they behave differently when you buy a filter. The table below summarizes what matters for this specific purchase, drawing on <a href="https://www.irs.gov/publications/p502" target="_blank" rel="noopener">IRS Publication 502</a> and <a href="https://www.irs.gov/publications/p969" target="_blank" rel="noopener">Publication 969</a>. Always confirm the details with your own plan administrator, because employer plans vary.</p>
</div>

<div class="prose tbl-scroll">
  <table class="data">
    <thead><tr><th>Account</th><th>Filter eligible?</th><th>Needs LMN?</th><th>Deadline / rollover</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td><strong>HSA</strong></td><td class="yes">Yes</td><td>Yes</td><td>Funds roll over &mdash; no expiry</td><td>Best for larger whole-house systems; balance can exceed one year of contributions.</td></tr>
      <tr><td><strong>FSA</strong></td><td class="yes">Yes</td><td>Yes</td><td>Often expires Dec 31 (use-it-or-lose-it)</td><td>Great for spending a balance before year-end. Some plans allow a small carryover or grace period.</td></tr>
      <tr><td><strong>HRA</strong></td><td>Maybe</td><td>Usually</td><td>Set by employer</td><td>Employer-funded; eligible expenses are defined by the plan &mdash; check first.</td></tr>
      <tr><td><strong>LPFSA</strong></td><td class="no">Limited</td><td>n/a</td><td>Like FSA</td><td>Usually restricted to dental and vision; a whole-house filter typically does not qualify.</td></tr>
    </tbody>
  </table>
</div>

<div class="prose">
  <p>The practical takeaway: an <strong>HSA</strong> is ideal for a multi-thousand-dollar whole-house system because the funds accumulate and never expire &mdash; you can save across two or three years and pay for a large system outright, and the account is yours even if you change jobs. An <strong>FSA</strong> is perfect if you have a balance that expires on December 31 and want to convert it into something durable instead of forfeiting it. If you have both, a common strategy is to spend the expiring FSA money first and reserve the HSA for the larger balance. Either way, the eligibility rule is the same: the filter needs a Letter of Medical Necessity to qualify.</p>

  <h2 id="medical-necessity">What makes a water filter "medically necessary"</h2>
  <p>Because eligibility hinges on a health condition, it helps to understand what a provider is looking for. A Letter of Medical Necessity connects a contaminant or water-quality problem to a condition it can cause or worsen. Common, well-documented examples include:</p>
  <ul>
    <li><strong>Lead exposure</strong> &mdash; the EPA states there is <a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">no safe level of lead</a> in drinking water, and the risk is highest for children and during pregnancy. Lead-reducing filtration is a textbook preventive measure.</li>
    <li><strong>PFAS ("forever chemicals")</strong> &mdash; linked to a range of health concerns; the <a href="https://www.epa.gov/pfas" target="_blank" rel="noopener">EPA</a> has tightened federal attention on PFAS in drinking water.</li>
    <li><strong>Nitrates</strong> &mdash; a particular concern for infants and pregnant women in well-water households.</li>
    <li><strong>Microbial risk for immunocompromised households</strong> &mdash; people undergoing chemotherapy or living with certain conditions are more vulnerable to waterborne pathogens.</li>
    <li><strong>Gastrointestinal and skin conditions</strong> that a provider links to water quality.</li>
  </ul>
  <p>You do not need to self-diagnose or guess. With a service like TrueMed, you complete a short, confidential health survey and a licensed provider determines whether your situation supports an LMN. The point of understanding the conditions above is simply to see <em>why</em> the rule exists &mdash; filtration that genuinely reduces a health risk is what the IRS framework is designed to cover.</p>
  <div class="note tip"><span class="lab">Start with a water test</span>Knowing what is actually in your water (a <a data-aff="test-kit" rel="sponsored nofollow noopener" target="_blank" href="/go/test-kit">water test kit</a> or your utility's annual Consumer Confidence Report) both guides which system you need and strengthens the documentation behind your purchase.</div>
  <p>It is worth dwelling on why testing matters so much here. The medical-necessity standard is about a <em>specific</em> problem, not a general wish for "better water." A lab report or utility disclosure that shows, say, elevated lead at the tap or a PFAS detection turns an abstract preference into a concrete, documentable reason to filter. That same evidence helps you and the provider agree on the right system rather than over- or under-buying. So the sequence is always: test or pull your report first, identify the contaminant, then match a system to it &mdash; and keep that paperwork with your purchase records.</p>

  <h2 id="not-sure">Not sure you have a "qualifying condition"?</h2>
  <p>This is the hesitation that stops most people, and it usually comes from picturing the wrong thing. You do not need a dramatic diagnosis or a thick medical file. The standard is whether filtration helps treat, mitigate, or <em>prevent</em> a condition &mdash; and prevention counts. A documented contaminant in your water combined with a household that includes children, someone pregnant, an older adult, or anyone with a weakened immune system is exactly the situation the rule was built for.</p>
  <p>You also are not the one making the medical judgment. On the TrueMed route, a licensed provider reviews your short questionnaire and decides whether your circumstances support a letter. If they do, you proceed; if they do not, you have lost nothing but a couple of minutes. So the honest answer to "do I qualify?" is usually: complete the survey and let the provider tell you, rather than talking yourself out of it in advance. Just hold onto the one firm rule &mdash; the letter has to come <em>before</em> you buy, never after. If you want to see exactly what that letter is and how it is issued, our <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity guide</a> walks through it.</p>

  <h2 id="water-type">City water vs well water: which system you need</h2>
  <p>Your water source shapes both the contaminants you face and the system that qualifies. Treating the two the same way is one of the most common &mdash; and expensive &mdash; mistakes buyers make.</p>
  <p><strong>City (municipal) water</strong> is treated before it reaches you, usually with chlorine or chloramine as a disinfectant. The trade-off is that you are drinking disinfection by-products and whatever the pipes between the plant and your home add &mdash; lead being the classic example in older service lines. For most city-water homes, a whole-house carbon filter (like SpringWell's flagship system) addresses chlorine, chloramine, taste, and odor, while a dedicated lead-and-cyst system is the move where lead is a documented concern.</p>
  <p><strong>Well water</strong> has no central treatment, so you own the entire problem: iron and manganese (staining and metallic taste), hydrogen sulfide (rotten-egg smell), sediment, hardness, and &mdash; importantly for the medical case &mdash; potential bacteria and nitrates. Well households often need a sequence: a well-water filter for iron and sulfur, frequently paired with UV purification for microbes, and sometimes a softener for hardness. Because the health risks in untreated well water are more direct, the medical-necessity argument is often clearer, but it also means you should test thoroughly before buying.</p>
  <p>The practical rule: on city water, start with whole-house carbon and add a targeted system for any specific contaminant; on well water, test for the full panel and build a treatment train that matches it.</p>

  <h2 id="how">How to buy a water filter with pre-tax dollars</h2>
  <p>Here is the part most guides skip. The reason "FSA eligible" feels confusing is that you cannot simply walk into a store and swipe an FSA card for a whole-house filter the way you would for cough syrup. You need the LMN in hand. The cleanest path is to buy from a retailer that builds the LMN process into checkout. SpringWell does this through a partnership with <strong>TrueMed</strong>:</p>
  <ol class="steps">
    <li><h4>Complete a short health survey</h4><p>At checkout, choose the TrueMed / "Pay with HSA/FSA" option and answer a confidential questionnaire. It takes a couple of minutes.</p></li>
    <li><h4>A licensed provider reviews it</h4><p>If you qualify, a provider issues your Letter of Medical Necessity &mdash; often within a few hours.</p></li>
    <li><h4>Pay with your HSA or FSA card</h4><p>Enter your HSA/FSA card like any debit card. Short on funds? Split the payment with a regular card and submit the remainder for reimbursement.</p></li>
    <li><h4>Keep your LMN and itemized receipt</h4><p>Store both in case your plan administrator requests documentation. That is your proof the purchase was a qualified medical expense.</p></li>
  </ol>
  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Ready to check eligibility</span>
    <h3>See SpringWell's HSA/FSA-eligible systems</h3>
    <p>SpringWell's whole-house filters, softener combos, and well-water systems all run through the TrueMed LMN process at checkout. You can confirm your eligibility in minutes.</p>
    {aff("truemed-eligible-category", "Shop eligible systems", "btn")}
    &nbsp;{aff("truemed-how-it-works", "See how it works", "btn ghost")}
  </div>

  <h2 id="savings">The tax-savings math</h2>
  <p>The reason this is worth the paperwork: HSA/FSA dollars are set aside <em>before</em> income tax. When you spend them, you skip the tax you would otherwise have paid on that money. Your effective discount is your marginal tax rate &mdash; commonly 20&ndash;37% depending on your bracket and state.</p>
</div>

<div class="prose">
  <div class="math" data-reveal>
    <div>
      <div class="head">Paying from your bank account</div>
      <div class="row"><span>Earned (pre-tax)</span><span>$100</span></div>
      <div class="row"><span>Income tax (~30%)</span><span>&minus;$30</span></div>
      <div class="row"><span>Left to spend</span><span>$70</span></div>
    </div>
    <div class="savings-col">
      <div class="head">Paying from HSA / FSA</div>
      <div class="row"><span>Set aside (pre-tax)</span><span>$100</span></div>
      <div class="row"><span>Income tax</span><span>$0</span></div>
      <div class="row"><span>Left to spend</span><span class="big">$100</span></div>
    </div>
  </div>
  <p>Scaled up, a <strong>$2,000 whole-house system</strong> bought with pre-tax dollars at a 24% marginal rate effectively costs around <strong>$1,520</strong> &mdash; roughly <strong>$480 in tax savings</strong>. At higher brackets the saving is larger. Exact figures depend on your tax situation, so treat this as illustration, not a guarantee.</p>
  <div class="note warn"><span class="lab">A realistic note on price</span>Whole-house systems run from about $1,100 to over $4,000, which can exceed a single year's FSA contribution limit. That is fine: pay what your balance covers with the HSA/FSA card and split the rest onto a normal card. HSAs (which roll over and have higher limits) are well suited to the larger systems.</div>

  <h2 id="best">Best HSA/FSA-eligible water systems for 2026</h2>
  <p>SpringWell is the clearest fit for the LMN route because its whole-house and well-water systems &mdash; the category where filtration is most defensible as a health investment &mdash; are built into the TrueMed checkout. Below are the picks we recommend most often. Full hands-on write-ups are linked from each.</p>
</div>

<div class="prose cards">
  <div class="card" data-reveal>
    <span class="tag">Editor's pick</span>
    <h3>SpringWell Whole House Filter</h3>
    <p>Point-of-entry filtration for the whole home: reduces chlorine, chloramine, and a broad range of contaminants with very low maintenance and a lifetime warranty. The strongest all-round LMN purchase.</p>
    <p class="price">From ~$1,170</p>
    {aff("whole-house", "Check price", "btn")}
    <p style="margin:.7rem 0 0"><a class="more" href="reviews/springwell-whole-house-water-filter-review.html">Read the full review &rarr;</a></p>
  </div>
  <div class="card" data-reveal>
    <span class="tag">Best for hard water</span>
    <h3>Filter + Softener Combo</h3>
    <p>Pairs whole-house filtration with softening, so you address both contaminants and scale in one eligible purchase. Available salt-based or salt-free.</p>
    <p class="price">From ~$2,250</p>
    {aff("filter-softener-combo", "Check price", "btn")}
    <p style="margin:.7rem 0 0"><a class="more" href="reviews/springwell-filter-softener-combo-review.html">Read the full review &rarr;</a></p>
  </div>
  <div class="card" data-reveal>
    <span class="tag">Best on a budget</span>
    <h3>Moen Reverse Osmosis (under-sink)</h3>
    <p>If you only need clean drinking and cooking water, this point-of-use RO system is the lowest-cost eligible option &mdash; ideal for renters and smaller budgets.</p>
    <p class="price">~$399</p>
    {aff("moen-ro", "Check price", "btn")}
    <p style="margin:.7rem 0 0"><a class="more" href="best-fsa-hsa-eligible-water-filters.html">Compare all picks &rarr;</a></p>
  </div>
</div>

<div class="prose">
  <p>Pitcher and faucet filters from brands like Clearly Filtered can also qualify through similar LMN services, and they are fine for renters or single-tap needs. But if your goal is to convert pre-tax dollars into a durable reduction in household contaminant exposure &mdash; the strongest version of the medical-necessity case &mdash; a point-of-entry SpringWell system treats every tap and shower, not just one. <a href="best-fsa-hsa-eligible-water-filters.html">See the full comparison &rarr;</a></p>

  <h2 id="situations">Will this work for someone like you? Three situations</h2>
  <p>Eligibility rules stay abstract until you see your own life in them. Here are three situations where buying a filter with HSA/FSA dollars makes the most sense &mdash; one of them probably looks familiar.</p>
  <h3>1. New parents in an older home</h3>
  <p>If your house predates the 1986 lead-pipe ban and you have a baby or young children, lead is the worry that keeps you up at night &mdash; reasonably so, given the EPA's position that <a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">no level of lead is safe</a> for children. For you, a whole-house system or a dedicated lead-and-cyst system is the textbook medical-necessity purchase: you are reducing a documented risk to the most vulnerable members of your household. Pull your utility's report, test at the tap, and let that evidence support the letter. Our <a href="best-fsa-hsa-eligible-water-filters.html">comparison</a> shows which SpringWell systems target lead specifically.</p>
  <h3>2. The well-water homeowner</h3>
  <p>No one treats your water but you. If you are dealing with rusty staining, a sulfur smell, or you have simply never tested for bacteria and nitrates, yours is the situation where the health case is often clearest &mdash; and where doing nothing carries the most real-world risk. A well-water filter, frequently paired with UV for microbes, handles the contaminants municipal users never think about. The <a href="reviews/springwell-whole-house-water-filter-review.html">whole-house review</a> explains how point-of-entry treatment works before you match a system to your test results.</p>
  <h3>3. The December FSA scramble</h3>
  <p>You log in to your benefits portal in late November and realize a few hundred &mdash; or a few thousand &mdash; dollars vanish on December 31. Spending it on co-pays you do not need is wasteful; forfeiting it is worse. A qualifying water filter converts money you would lose into a durable upgrade that keeps paying off for years. If this is you, start the <a href="guides/letter-of-medical-necessity-water-filter.html">LMN process</a> early in December so the paperwork clears before the cutoff.</p>

  <h2 id="choose">How to choose the right system</h2>
  <p>Once you know a filter can be eligible, the question becomes which one. The biggest budget mistake is buying more or less system than your water actually calls for. Work through these in order, and let your water test &mdash; not marketing &mdash; drive the decision:</p>
  <ul>
    <li><strong>Test first.</strong> Identify your actual contaminants before buying. City water? Read your utility's annual report. Well water? Use a certified lab or a comprehensive test kit so you catch bacteria and nitrates, not just the obvious taste and odor issues.</li>
    <li><strong>Point-of-entry vs point-of-use.</strong> Whole-house (POE) treats every tap, shower, and appliance; under-sink or RO (POU) treats one fixture. POE makes the broadest medical-necessity case because it reduces exposure everywhere; POU is the budget-friendly, renter-friendly route when only drinking water matters.</li>
    <li><strong>Match the contaminant to the system.</strong> Chlorine and general taste point to whole-house carbon; lead and cysts, PFAS, iron and sulfur (well), or hardness each point to a specific system or combo.</li>
    <li><strong>Flow rate and household size.</strong> A system that throttles flow when two showers run at once is a daily annoyance. Size for your peak simultaneous demand, not your average.</li>
    <li><strong>Maintenance and warranty.</strong> Factor replacement cartridge cost and lifespan into the true price. A low-maintenance system with a strong warranty often costs less over five years than a cheap one that needs frequent consumables &mdash; and it is simpler to document for ongoing reimbursement.</li>
  </ul>
  <p>If you weigh those factors and still land between two options, default to the one with the broadest coverage and lowest upkeep. That is usually the choice you will be happiest with years later, and it is the easiest to justify as a genuine health investment.</p>

  <h2 id="checklist">Your before-you-buy checklist</h2>
  <p>When you are ready to move, work through this in order. It keeps your money, your timing, and your documentation all pointing the same direction:</p>
  <ul>
    <li><strong>Check your balance and deadline.</strong> Log in to your HSA/FSA portal and note how much you have and whether it expires (FSA) or rolls over (HSA).</li>
    <li><strong>Find out what is in your water.</strong> City users: read the annual Consumer Confidence Report. Well users: order a lab test. This both picks your system and supports your claim.</li>
    <li><strong>Match a system to the result.</strong> Use our <a href="best-fsa-hsa-eligible-water-filters.html">comparison of eligible systems</a> to align the contaminant with the right unit.</li>
    <li><strong>Use the built-in LMN route.</strong> Buying where the letter is issued at checkout keeps your timing automatically correct.</li>
    <li><strong>Plan the payment.</strong> If the system costs more than your balance, decide upfront how you will split it between your HSA/FSA card and a regular card.</li>
    <li><strong>Save everything.</strong> Download the letter and itemized receipt into one folder the day you buy.</li>
  </ul>

  <h2 id="denied">Avoiding a denied claim</h2>
  <p>Most denials come down to documentation and timing, not the product. Protect yourself:</p>
  <ul>
    <li><strong>Get the LMN on or before your purchase date.</strong> You generally cannot apply an LMN to a past purchase retroactively.</li>
    <li><strong>Keep the LMN and an itemized receipt.</strong> Save them in a dedicated folder in case your administrator asks.</li>
    <li><strong>Document ongoing replacements.</strong> If you reimburse replacement cartridges, be ready to show the continued medical need.</li>
    <li><strong>Confirm with your administrator.</strong> Plans differ; a two-minute check avoids surprises.</li>
  </ul>
  <h3>Questions worth asking your plan administrator</h3>
  <p>Two minutes with your administrator removes almost all the uncertainty. Ask:</p>
  <ul>
    <li>Do you accept a Letter of Medical Necessity for a water filtration system?</li>
    <li>Do you need the letter and receipt submitted upfront, or only if I am audited?</li>
    <li>For my FSA, what is the exact deadline, and is there a grace period or carryover?</li>
    <li>If I split the cost across two cards, how should I submit the medical portion?</li>
    <li>Do replacement filter cartridges need a new or renewed letter?</li>
  </ul>
  <p>Whatever they tell you beats any blog's general answer &mdash; including ours &mdash; because your plan's specific rules are what actually govern your reimbursement.</p>
  <div class="note key"><span class="lab">Not advice</span>This guide is educational and is not tax, legal, or medical advice. Eligibility depends on your specific plan and health situation. Confirm with your plan administrator and a qualified professional.</div>

  <h2 id="myths">Five myths about FSA-eligible water filters</h2>
  <p>Because the topic is muddled online, it is worth clearing up the claims that lead people astray:</p>
  <ul>
    <li><strong>Myth: "Water filters are on the FSA eligible list, so I can just swipe my card."</strong> Reality: ordinary filters are not automatically eligible. The card may decline, or the expense may be clawed back later, without an LMN on file.</li>
    <li><strong>Myth: "I can buy now and get the doctor's note later."</strong> Reality: the LMN should be dated on or before the purchase. Retroactive letters are typically rejected.</li>
    <li><strong>Myth: "An LMN means a real doctor's appointment and out-of-pocket fees."</strong> Reality: services like TrueMed have a licensed provider review a short survey, usually at no cost to you when you buy from a partner retailer.</li>
    <li><strong>Myth: "Only the system qualifies, not the filters."</strong> Reality: replacement cartridges can qualify on the same medical-necessity basis &mdash; keep receipts and document the continued need.</li>
    <li><strong>Myth: "It's basically free because it's pre-tax."</strong> Reality: you save your tax rate (often 20&ndash;37%), not 100%. It is a meaningful discount, not a giveaway.</li>
  </ul>

  <h2 id="faq">Frequently asked questions</h2>
  {faq_html}

  <hr class="rule">
  <h2 class="mt0">The verdict</h2>
  <p>Water filters sit in the "eligible with a Letter of Medical Necessity" category &mdash; not the automatic list, but absolutely reachable. If you have HSA or FSA funds (especially an FSA balance approaching its year-end deadline), a qualifying SpringWell system lets you turn pre-tax dollars into cleaner water at every tap, often at an effective 20&ndash;37% discount. The simplest route is the built-in TrueMed checkout, which handles the LMN for you.</p>
  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Next step</span>
    <h3>Check your eligibility in minutes</h3>
    <p>Browse SpringWell's HSA/FSA-eligible systems and complete the short TrueMed survey to see whether you qualify for a Letter of Medical Necessity.</p>
    {aff("truemed-eligible-category", "Shop eligible systems", "btn")}
  </div>
  {byline(0)}

  <div class="sources">
    <p><strong>Sources &amp; further reading</strong></p>
    <ol>
      <li><a href="https://www.irs.gov/publications/p502" target="_blank" rel="noopener">IRS Publication 502</a>, Medical and Dental Expenses.</li>
      <li><a href="https://www.irs.gov/publications/p969" target="_blank" rel="noopener">IRS Publication 969</a>, Health Savings Accounts and Other Tax-Favored Health Plans.</li>
      <li>SpringWell &times; TrueMed HSA/FSA program &mdash; <a data-aff="truemed-how-it-works" rel="sponsored nofollow noopener" target="_blank" href="/go/truemed-how-it-works">how it works</a>.</li>
      <li>U.S. EPA &mdash; <a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">lead in drinking water</a> and <a href="https://www.epa.gov/pfas" target="_blank" rel="noopener">PFAS</a> guidance.</li>
    </ol>
  </div>
</div>
</div>
"""
home += footer(0)
write("index.html", home)

# ============================ REVIEW: WHOLE HOUSE ============================
wh_schema = {
  "@context":"https://schema.org","@type":"Review",
  "itemReviewed":{"@type":"Product","name":"SpringWell Whole House Water Filter System","brand":{"@type":"Brand","name":"SpringWell"}},
  "author":{"@type":"Person","name":AUTHOR},
  "reviewRating":{"@type":"Rating","ratingValue":"4.7","bestRating":"5"},
  "publisher":{"@type":"Organization","name":NAME}
}
r1 = head("SpringWell Whole House Water Filter Review (2026) — HSA/FSA Eligible",
  "Hands-on review of the SpringWell whole house water filter: performance, contaminant reduction, maintenance, price, and how to buy it with HSA/FSA dollars via TrueMed.",
  "reviews/springwell-whole-house-water-filter-review.html", [wh_schema], depth=1)
r1 += f"""
<div class="wrap">
<div class="crumbs"><a href="../index.html">Home</a> &rsaquo; <a href="../best-fsa-hsa-eligible-water-filters.html">Reviews</a> &rsaquo; SpringWell Whole House</div>
<article class="hero">
  <span class="eyebrow">{CHECK} Product review &middot; Editor's pick</span>
  <h1 class="prose">SpringWell Whole House Water Filter review (2026)</h1>
  <p class="lede prose">SpringWell's flagship point-of-entry filter is our top recommendation for buyers using HSA/FSA dollars: broad contaminant reduction, almost no maintenance, a lifetime warranty, and a built-in TrueMed checkout that handles the Letter of Medical Necessity.</p>
  <div class="rating"><span class="score">4.7</span><span class="out">/ 5</span><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span></div>
</article>
<div class="prose">
  {disc(1)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Eligibility ruling</p>
    <p class="ruling"><b>HSA/FSA eligible via TrueMed.</b> Qualifies as a medical expense with a Letter of Medical Necessity, issued through SpringWell's checkout.</p>
  </div>
  <div class="cta-box" data-reveal>
    <span class="kicker">At a glance</span>
    <h3>SpringWell Whole House Filter</h3>
    <p class="price"><s>List varies</s> From ~$1,170&ndash;$2,160 &middot; lifetime warranty &middot; free shipping</p>
    {aff("whole-house", "Check current price", "btn")}
  </div>

  <h2>Who it is for</h2>
  <p>This is a whole-house, point-of-entry system: it treats water where it enters your home, so every tap, shower, and appliance gets filtered water. That breadth is exactly what makes it the strongest <em>medical-necessity</em> case among filtration options &mdash; you are reducing contaminant exposure across the entire household, not at a single faucet. If your goal is to put HSA/FSA dollars toward a durable reduction in something like chlorine, chloramine, or a documented contaminant concern, this is the system we point people to first.</p>

  <h2>Performance and what it removes</h2>
  <p>SpringWell's whole-house filter uses a multi-stage media bed (including catalytic and activated carbon) to reduce chlorine, chloramine, and a broad range of taste-, odor-, and health-related contaminants on city water. It is designed for high flow so multiple fixtures can run at once without a pressure drop you would notice. For homes that need more &mdash; lead and cysts, PFAS, or well-water issues like iron and sulfur &mdash; SpringWell offers dedicated systems (covered in our <a href="../best-fsa-hsa-eligible-water-filters.html">comparison</a>) that are also TrueMed-eligible.</p>

  <h2>Maintenance and running cost</h2>
  <p>This is where the system shines. There are no cartridges to swap on the main carbon tank for years of normal use; the only routine task is replacing an inexpensive sediment pre-filter periodically. Over a multi-year horizon that keeps the true cost of ownership low &mdash; a point worth remembering when you document ongoing medical necessity, since you are not constantly re-buying consumables.</p>

  <h2>Installation</h2>
  <p>It installs at your main water line. Handy homeowners with basic plumbing experience can do it; others will want a plumber for a few hundred dollars. SpringWell includes the fittings and provides clear guidance, and the system has a bypass for easy servicing.</p>

  <div class="proscons">
    <div class="pro"><h4>What we like</h4><ul>
      <li>Whole-home coverage &mdash; the strongest LMN case</li>
      <li>Very low maintenance; no frequent cartridge changes</li>
      <li>Lifetime warranty and free shipping</li>
      <li>Built-in TrueMed HSA/FSA checkout</li>
      <li>High flow rate; no noticeable pressure loss</li>
    </ul></div>
    <div class="con"><h4>Keep in mind</h4><ul>
      <li>Upfront cost is higher than a pitcher or faucet filter</li>
      <li>May exceed one year's FSA limit (split payment or use an HSA)</li>
      <li>Best installed at point-of-entry &mdash; less ideal for renters</li>
      <li>For lead/PFAS/well issues you may want a dedicated SpringWell system</li>
    </ul></div>
  </div>

  <h2>What it removes, in detail</h2>
  <p>The core media bed combines catalytic and activated carbon. Activated carbon is the workhorse for chlorine, taste, and odor; <strong>catalytic</strong> carbon adds the ability to tackle <strong>chloramine</strong>, the more stable disinfectant many utilities now use and which ordinary carbon struggles with. A sediment pre-filter protects the bed from grit. Together these address the most common city-water complaints &mdash; the chlorinated taste and smell, and the disinfection by-products some households want reduced.</p>
  <p>What it is <em>not</em> built to do alone is remove <a href="../lead-in-drinking-water-fsa-eligible-filtration.html">lead</a>, <a href="../pfas-tap-water-filtration-hsa-fsa.html">PFAS</a>, or treat <a href="../iron-manganese-sulfur-well-water-treatment.html">well-water</a> iron and sulfur &mdash; SpringWell sells dedicated systems for those, and you should match the system to a <a href="../are-water-test-kits-fsa-hsa-eligible.html">water test</a>. Check current NSF/ANSI certifications on the product page for the specific claims that matter to you.</p>

  <h2>Flow rate and sizing</h2>
  <p>A whole-house filter has to keep up with your home's peak demand &mdash; several fixtures running at once &mdash; without a pressure drop you would feel in the shower. SpringWell sizes its systems by household size (broadly, by number of bathrooms), so the key is to pick the model rated for your home rather than the smallest one. An undersized system restricts flow; a correctly sized one is invisible in daily use.</p>

  <h2>Lifespan and the warranty</h2>
  <p>The main carbon media is designed to last years of normal household use before it needs attention, which is what keeps maintenance and running cost so low. The lifetime warranty on core systems is a genuine differentiator in this category &mdash; it signals confidence in the tanks and valves, and it removes a worry from a several-hundred-to-thousand-dollar purchase. Confirm what the warranty covers (typically the tanks and key components) on the current product page.</p>

  <h2>Who should consider a different system</h2>
  <p>This is our top pick for most homeowners, but it is not for everyone. <strong>Renters</strong> usually cannot install a point-of-entry system &mdash; a <a href="../water-filters-renters-hsa-fsa-no-installation.html">point-of-use option</a> fits better. <strong>Well owners</strong> with iron, sulfur, or bacteria need a <a href="../springwell-well-water-filter-system-review.html">dedicated well system</a> (often with UV). If your only concern is <strong>drinking-water lead or nitrates</strong>, an affordable under-sink <a href="../is-reverse-osmosis-fsa-hsa-eligible.html">RO</a> unit may be all you need.</p>

  <h2>How it stacks up against alternatives</h2>
  <p>Against a point-of-use filter, the whole-house system wins on coverage and on the strength of the medical-necessity case, at a higher upfront cost &mdash; see <a href="../whole-house-vs-under-sink-water-filter-hsa-fsa.html">whole-house vs under-sink</a>. Against other whole-house brands, SpringWell's edge is its low-maintenance media, lifetime warranty, and built-in HSA/FSA checkout; we compare it directly with <a href="../springwell-vs-aquasana-hsa-fsa.html">Aquasana</a> and <a href="../springwell-vs-culligan-fsa-hsa.html">Culligan</a>.</p>

  <h2>Real-world ownership</h2>
  <p>What owners notice first is what they stop noticing: the chlorine smell at the kitchen tap and in the shower fades, glassware and skin can feel different, and there are no cartridges to remember to change for years. The trade-off they accept is the upfront cost and a one-time install. For a household putting pre-tax dollars toward a durable improvement, that profile &mdash; high value, low ongoing effort &mdash; is exactly why it documents well as a lasting medical-necessity purchase rather than a recurring expense.</p>

  <h2>Setup and the first week</h2>
  <p>After install, SpringWell systems are typically flushed to condition the media, then they simply run. There is a bypass valve for servicing, and the sediment pre-filter is the one inexpensive consumable to check periodically. There is no programming or salt for the filter itself (softening, if you add it, is a separate stage). Most owners interact with it only when the pre-filter needs a change.</p>

  <h2>How to buy it with HSA/FSA</h2>
  <p>Add the system to your cart, choose the TrueMed / "Pay with HSA/FSA" option at checkout, complete the short health survey, and &mdash; if you qualify &mdash; receive your Letter of Medical Necessity (often within hours). Pay with your HSA/FSA card, or split with a regular card if your balance is short. Keep the LMN and itemized receipt. For the full walkthrough, see our <a href="../guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity guide</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Bottom line</span>
    <h3>Our top pick for HSA/FSA buyers</h3>
    <p>If you want one durable, low-maintenance purchase that puts pre-tax dollars to work across your whole home, the SpringWell Whole House filter is the system we recommend most.</p>
    {aff("whole-house", "Check price &amp; eligibility", "btn")}
  </div>
  {byline(1)}
</div>
</div>
"""
r1 += footer(1)
write("reviews/springwell-whole-house-water-filter-review.html", r1)

# ============================ REVIEW: COMBO ============================
r2_schema = {
  "@context":"https://schema.org","@type":"Review",
  "itemReviewed":{"@type":"Product","name":"SpringWell Water Filter and Softener Combo","brand":{"@type":"Brand","name":"SpringWell"}},
  "author":{"@type":"Person","name":AUTHOR},
  "reviewRating":{"@type":"Rating","ratingValue":"4.6","bestRating":"5"},
  "publisher":{"@type":"Organization","name":NAME}
}
r2 = head("SpringWell Filter + Softener Combo Review (2026) — HSA/FSA Eligible",
  "Review of SpringWell's whole-house water filter and softener combo systems (salt-based and salt-free): performance on hard water, cost, and HSA/FSA eligibility via TrueMed.",
  "reviews/springwell-filter-softener-combo-review.html", [r2_schema], depth=1)
r2 += f"""
<div class="wrap">
<div class="crumbs"><a href="../index.html">Home</a> &rsaquo; <a href="../best-fsa-hsa-eligible-water-filters.html">Reviews</a> &rsaquo; Filter + Softener Combo</div>
<article class="hero">
  <span class="eyebrow">{CHECK} Product review &middot; Best for hard water</span>
  <h1 class="prose">SpringWell Filter + Softener Combo review (2026)</h1>
  <p class="lede prose">If you have hard water <em>and</em> want filtration, the combo solves both in one HSA/FSA-eligible purchase &mdash; available salt-based (true softening) or salt-free (scale control without sodium).</p>
  <div class="rating"><span class="score">4.6</span><span class="out">/ 5</span><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span></div>
</article>
<div class="prose">
  {disc(1)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Eligibility ruling</p>
    <p class="ruling"><b>HSA/FSA eligible via TrueMed</b> with a Letter of Medical Necessity, like the rest of SpringWell's whole-house range.</p>
  </div>
  <div class="cta-box" data-reveal>
    <span class="kicker">At a glance</span>
    <h3>Filter + Softener Combo</h3>
    <p class="price">Salt-based from ~$2,250 &middot; salt-free from ~$2,340 &middot; lifetime warranty</p>
    {aff("filter-softener-combo", "Check salt-based price", "btn")}
    &nbsp;{aff("salt-free-combo", "Check salt-free price", "btn ghost")}
  </div>

  <h2>Salt-based vs salt-free: which to choose</h2>
  <p>The combo pairs SpringWell's whole-house filter with one of two approaches to hardness:</p>
  <ul>
    <li><strong>Salt-based softener</strong> &mdash; true ion-exchange softening that removes calcium and magnesium. Best if you want classic "soft water" feel, spotless glassware, and maximum scale protection. Requires salt top-ups and a drain line.</li>
    <li><strong>Salt-free conditioner (FutureSoft)</strong> &mdash; conditions minerals so they do not form scale, without adding sodium and with no salt, electricity, or wastewater. Best for low-maintenance, eco-minded, or low-sodium households.</li>
  </ul>

  <h2>Why a combo can be the smarter eligible purchase</h2>
  <p>Hard water is not just an appliance nuisance &mdash; for some households a provider may connect water quality to skin or other conditions, and the filtration half of the system reduces contaminant exposure across every tap. Bundling filter and softener means a single LMN purchase covers both needs, and you avoid buying and documenting two separate systems.</p>

  <div class="proscons">
    <div class="pro"><h4>What we like</h4><ul>
      <li>Filtration + softening in one eligible system</li>
      <li>Choice of salt-based or salt-free</li>
      <li>Salt-free option: no sodium, no electricity, no wastewater</li>
      <li>Lifetime warranty; whole-home coverage</li>
    </ul></div>
    <div class="con"><h4>Keep in mind</h4><ul>
      <li>Higher upfront cost than a filter alone</li>
      <li>Salt-based needs ongoing salt and a drain line</li>
      <li>Likely exceeds one year's FSA limit &mdash; plan with an HSA or split payment</li>
    </ul></div>
  </div>

  <h2>What the filter half does</h2>
  <p>It is easy to focus on softening, but the filtration half is what carries the health rationale. The combo includes SpringWell's whole-house carbon filtration &mdash; catalytic and activated carbon that reduce chlorine, chloramine, taste, and odor across every tap. So you are not just softening water; you are reducing contaminant exposure at the same time, which is the part a provider can connect to a <a href="../guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>How much softening do you need?</h2>
  <p>Salt-based softeners are sized by grain capacity to match your water's hardness and your household's water use. The harder your water and the more people in the home, the more capacity you need; an undersized unit regenerates too often and wastes salt, while an oversized one ties up money. Check your hardness on your <a href="../how-to-read-water-quality-report-ccr.html">water report</a> or with a test before choosing.</p>

  <h2>Salt-based: what to expect</h2>
  <p>True ion exchange delivers the classic soft-water feel &mdash; better lather, spotless glassware, and maximum scale protection. In return you top up salt periodically and need a drain line for the regeneration cycle. If you want the most thorough hardness removal and do not mind the upkeep, this is the option.</p>

  <h2>Salt-free: what to expect</h2>
  <p>The FutureSoft conditioner does not remove minerals; it transforms them so they will not stick as scale. That means <strong>no added sodium, no salt to buy, no electricity, and no wastewater</strong> &mdash; very low maintenance, and the better choice if a low-sodium need is documented. The trade-off is that you do not get the slippery "soft" feel of ion exchange, since the minerals are still present, just neutralized.</p>

  <h2>Maintenance and cost over time</h2>
  <p>Both options share the low-maintenance carbon filtration; the difference is the softening stage. Salt-based adds the recurring cost and chore of salt; salt-free is essentially set-and-forget. For an HSA/FSA buyer, fewer consumables means less recurring documentation &mdash; a quiet advantage of the salt-free route, balanced against salt-based's stronger scale control.</p>

  <h2>Installation and footprint</h2>
  <p>A combo is two stages (filter plus softener), so it needs more space at the point of entry than a filter alone, and salt-based versions need a nearby drain. Plan the location accordingly &mdash; many buyers use a plumber for the combo given the extra plumbing. Once in, it runs quietly in the background with a bypass for servicing.</p>

  <h2>Who it's for &mdash; and who can skip it</h2>
  <p>Choose the combo if your water is <em>both</em> hard <em>and</em> you want filtration &mdash; common on <a href="../city-water-vs-well-water-filter-eligible.html">well water</a> and in hard-water city areas. If your water is not hard, a <a href="../reviews/springwell-whole-house-water-filter-review.html">filter alone</a> is enough; if you only want softening with no contaminant concern, be aware a standalone softener is harder to make eligible &mdash; see <a href="../need-water-softener-and-filter-hsa-fsa.html">do you need both?</a></p>

  <h2>How to buy with HSA/FSA</h2>
  <p>Same TrueMed flow as the rest of the range: select the HSA/FSA option at checkout, complete the survey, get your LMN if you qualify, and pay with your account card. Our <a href="../guides/letter-of-medical-necessity-water-filter.html">LMN guide</a> covers the details and how to keep your documentation.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Bottom line</span>
    <h3>The hard-water buyer's best eligible option</h3>
    <p>One purchase, both problems solved &mdash; with the same pre-tax savings as a standalone filter.</p>
    {aff("filter-softener-combo", "Check price &amp; eligibility", "btn")}
  </div>
  {byline(1)}
</div>
</div>
"""
r2 += footer(1)
write("reviews/springwell-filter-softener-combo-review.html", r2)

# ============================ BEST / ROUNDUP ============================
best = head("Best HSA/FSA-Eligible Water Filters (2026) — Compared & Reviewed",
  "The best HSA/FSA-eligible water filters for 2026, compared: whole-house, filter-softener combos, well-water, and budget RO. How each qualifies via a Letter of Medical Necessity.",
  "best-fsa-hsa-eligible-water-filters.html", depth=0)
best += f"""
<div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> &rsaquo; Best eligible systems</div>
<article class="hero">
  <span class="eyebrow">{CHECK} 2026 buyer's guide</span>
  <h1 class="prose">Best HSA/FSA-eligible water filters for 2026</h1>
  <p class="lede prose">Every system below qualifies as a medical expense with a Letter of Medical Necessity through SpringWell's TrueMed checkout. We have matched each to the buyer it fits best.</p>
</article>
<div class="prose">
  {disc(0)}
  <div class="note key"><span class="lab">How we picked</span>We prioritized whole-home contaminant reduction (the strongest medical-necessity case), low maintenance, warranty, and a built-in HSA/FSA checkout. See our <a href="editorial-policy.html">editorial &amp; eligibility policy</a>.</div>
</div>

<div class="prose tbl-scroll">
  <table class="data">
    <thead><tr><th>System</th><th>Best for</th><th>Type</th><th>Price (approx.)</th><th>HSA/FSA</th></tr></thead>
    <tbody>
      <tr><td><strong>Whole House Filter</strong></td><td>All-round / city water</td><td>Point-of-entry</td><td>$1,170&ndash;$2,160</td><td class="yes">With LMN</td></tr>
      <tr><td><strong>Filter + Softener Combo</strong></td><td>Hard water</td><td>Point-of-entry</td><td>$2,250&ndash;$4,320</td><td class="yes">With LMN</td></tr>
      <tr><td><strong>Well Water Filter</strong></td><td>Iron / sulfur / well</td><td>Point-of-entry</td><td>$2,250&ndash;$2,700</td><td class="yes">With LMN</td></tr>
      <tr><td><strong>Lead &amp; Cyst Removal</strong></td><td>Lead concerns, families</td><td>Point-of-entry</td><td>~$1,554</td><td class="yes">With LMN</td></tr>
      <tr><td><strong>Whole House Cartridge</strong></td><td>Smaller homes / budget POE</td><td>Point-of-entry</td><td>$660&ndash;$1,116</td><td class="yes">With LMN</td></tr>
      <tr><td><strong>Moen Reverse Osmosis</strong></td><td>Drinking water only / renters</td><td>Point-of-use</td><td>~$399</td><td class="yes">With LMN</td></tr>
      <tr><td><strong>UV Purification</strong></td><td>Bacteria (often well)</td><td>Add-on</td><td>~$1,089</td><td class="yes">With LMN</td></tr>
    </tbody>
  </table>
</div>

<div class="prose cards">
  <div class="card" data-reveal>
    <span class="tag">Editor's pick</span>
    <h3>SpringWell Whole House</h3>
    <p>Best all-round choice on city water. Broad contaminant reduction, lifetime warranty, almost no maintenance.</p>
    <p class="price">From ~$1,170</p>
    {aff("whole-house", "Check price", "btn")}
    <p style="margin:.7rem 0 0"><a class="more" href="reviews/springwell-whole-house-water-filter-review.html">Full review &rarr;</a></p>
  </div>
  <div class="card" data-reveal>
    <span class="tag">Best for hard water</span>
    <h3>Filter + Softener Combo</h3>
    <p>Filtration plus softening in one eligible system. Salt-based or salt-free.</p>
    <p class="price">From ~$2,250</p>
    {aff("filter-softener-combo", "Check price", "btn")}
    <p style="margin:.7rem 0 0"><a class="more" href="reviews/springwell-filter-softener-combo-review.html">Full review &rarr;</a></p>
  </div>
  <div class="card" data-reveal>
    <span class="tag">Best for well water</span>
    <h3>Well Water Filter</h3>
    <p>Targets iron, sulfur, and sediment common in well supplies. Pairs well with UV for bacteria.</p>
    <p class="price">From ~$2,250</p>
    {aff("well-water", "Check price", "btn")}
  </div>
  <div class="card" data-reveal>
    <span class="tag">Best for lead concerns</span>
    <h3>Lead &amp; Cyst Removal</h3>
    <p>Dedicated lead and cyst reduction &mdash; a strong fit for families with young children.</p>
    <p class="price">~$1,554</p>
    {aff("lead-cyst", "Check price", "btn")}
  </div>
  <div class="card" data-reveal>
    <span class="tag">Best budget / POU</span>
    <h3>Moen Reverse Osmosis</h3>
    <p>Under-sink RO for drinking and cooking water. Lowest-cost eligible option; renter-friendly.</p>
    <p class="price">~$399</p>
    {aff("moen-ro", "Check price", "btn")}
  </div>
  <div class="card" data-reveal>
    <span class="tag">Bacteria / well add-on</span>
    <h3>UV Purification</h3>
    <p>Inactivates bacteria and other microbes &mdash; often paired with a well-water filter.</p>
    <p class="price">~$1,089</p>
    {aff("uv", "Check price", "btn")}
  </div>
</div>

<div class="prose">
  <h2>How to choose the right system</h2>
  <p>The "best" system is the one that matches your situation, not the most expensive one. A quick way to narrow it down:</p>
  <ul>
    <li><strong>City water, general improvement</strong> &rarr; the <a href="whole-house-water-filtration-hsa-fsa-eligible.html">Whole House Filter</a> for chlorine, taste, and odor at every tap.</li>
    <li><strong>Hard water too</strong> &rarr; the <a href="reviews/springwell-filter-softener-combo-review.html">Filter + Softener Combo</a>.</li>
    <li><strong>Private well</strong> (iron, sulfur, bacteria) &rarr; the <a href="springwell-well-water-filter-system-review.html">Well Water Filter</a>, often with UV.</li>
    <li><strong>Lead concern / young children</strong> &rarr; the <a href="lead-in-drinking-water-fsa-eligible-filtration.html">Lead &amp; Cyst</a> system.</li>
    <li><strong>Drinking water only / renting / budget</strong> &rarr; <a href="is-reverse-osmosis-fsa-hsa-eligible.html">Moen Reverse Osmosis</a>.</li>
    <li><strong>Bacteria</strong> &rarr; add <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV purification</a>.</li>
  </ul>

  <h2>Match the system to your water</h2>
  <p>Before buying anything, find out what is actually in your water. City users can start with the annual <a href="how-to-read-water-quality-report-ccr.html">Consumer Confidence Report</a>; everyone &mdash; especially well owners &mdash; should confirm with a <a href="are-water-test-kits-fsa-hsa-eligible.html">home test</a>, since lead and other tap-specific issues will not show on a utility report. The result both tells you which system to buy and becomes documentation for your Letter of Medical Necessity. If you are unsure whether you are on city or well water, read <a href="city-water-vs-well-water-filter-eligible.html">city vs well</a>.</p>

  <h2>What "eligible" really means here</h2>
  <p>None of these systems is <em>automatically</em> FSA/HSA eligible. Each qualifies as a medical expense when a licensed provider documents the need with a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> &mdash; which SpringWell's TrueMed checkout issues at purchase. We are upfront about this throughout the site because the accuracy is what protects you if a claim is ever <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">reviewed</a>.</p>

  <h2>Don't overlook replacement filters</h2>
  <p>Whatever you choose, the <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement filters</a> are eligible on the same basis &mdash; so keep documenting them. This is one reason low-maintenance systems are attractive: fewer cartridge swaps mean lower recurring cost and less paperwork over the years.</p>

  <h2>Remember the pre-tax discount</h2>
  <p>Whichever system you pick, buying with HSA/FSA dollars effectively discounts it by your tax rate &mdash; commonly 20&ndash;37%. On a $2,000 system that is roughly $400&ndash;$740 back. See <a href="how-much-save-water-filter-hsa-fsa.html">how much you can save</a>, and if you have an expiring <a href="fsa-deadline-water-filter-use-it-or-lose-it.html">FSA balance</a>, a qualifying system is one of the best ways to use it before year-end.</p>

  <h2>How we evaluate</h2>
  <p>Our picks weight whole-home contaminant reduction (the strongest medical-necessity case), low maintenance, warranty, certifications, and a working HSA/FSA path. We focus on SpringWell because its range covers the main needs and builds the TrueMed letter into checkout, but we are clear about where a point-of-use or competitor option fits better &mdash; see our comparisons with <a href="springwell-vs-clearly-filtered-fsa-eligible.html">Clearly Filtered</a>, <a href="springwell-vs-aquasana-hsa-fsa.html">Aquasana</a>, and <a href="springwell-vs-culligan-fsa-hsa.html">Culligan</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Check eligibility</span>
    <h3>See all eligible systems and confirm your eligibility</h3>
    <p>Browse SpringWell's full HSA/FSA-eligible range and complete the short TrueMed survey at checkout.</p>
    {aff("truemed-eligible-category", "Shop eligible systems", "btn")}
  </div>
  {byline(0)}
</div>
</div>
"""
best += footer(0)
write("best-fsa-hsa-eligible-water-filters.html", best)

# ============================ GUIDE: LMN ============================
lmn_faq = [
 ("Who can write a Letter of Medical Necessity?","A licensed healthcare provider. With TrueMed, a licensed provider reviews your health survey and issues the LMN if you qualify, so you do not need a separate doctor's appointment."),
 ("How long is an LMN valid?","Often up to 12 months for the same product category, depending on the issuer and your plan, after which you may need to renew. Keep the dated letter with your records."),
 ("Can I get an LMN after I already bought the filter?","Generally no. The LMN should be dated on or before your purchase. Retroactive letters are typically not accepted, which is why buying through a checkout that issues the LMN at purchase is the safest route."),
]
lmn_schema = {"@context":"https://schema.org","@type":"Article","headline":"Letter of Medical Necessity for a Water Filter: How It Works","author":{"@type":"Person","name":AUTHOR},"publisher":{"@type":"Organization","name":NAME},"dateModified":"2026-06-16"}
lmn = head("Letter of Medical Necessity for a Water Filter (2026 Guide)",
  "What a Letter of Medical Necessity is, why a water filter needs one for HSA/FSA, and the exact step-by-step process to get one and buy with pre-tax dollars.",
  "guides/letter-of-medical-necessity-water-filter.html", [lmn_schema, faq_schema(lmn_faq)], depth=1)
lmn_faq_html = '<div class="faq">'
for q,a in lmn_faq:
    lmn_faq_html += f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>'
lmn_faq_html += '</div>'
lmn += f"""
<div class="wrap">
<div class="crumbs"><a href="../index.html">Home</a> &rsaquo; Guides &rsaquo; Letter of Medical Necessity</div>
<article class="hero">
  <span class="eyebrow">{CHECK} How-to guide</span>
  <h1 class="prose">The Letter of Medical Necessity, explained</h1>
  <p class="lede prose">An LMN is the single document that turns a water filter from a personal expense into a qualified HSA/FSA medical expense. Here is what it is, why you need it, and how to get one without a separate doctor's visit.</p>
</article>
<div class="prose">
  {disc(1)}
  <h2>What an LMN is</h2>
  <p>A Letter of Medical Necessity is a short statement from a licensed provider confirming that a product is needed to treat, mitigate, or prevent a specific medical condition. It does for a water filter what a prescription does for a medicine: it satisfies the IRS requirement that an expense be <em>medical</em> rather than personal. The framework comes from IRS Publications 502 and 969.</p>

  <h2>Why a water filter needs one</h2>
  <p>Ordinary filtration is considered a personal, general-health expense &mdash; not reimbursable on its own. The LMN supplies the missing link: it documents that your filter addresses a health condition (for example, reducing exposure to lead, PFAS, or nitrates, or protecting an immunocompromised household). With that documentation, the purchase qualifies.</p>

  <h2>How to get one (the easy way)</h2>
  <p>You do not need to book an appointment and explain water chemistry to your doctor. Retailers partnered with services like <strong>TrueMed</strong> build the process into checkout:</p>
  <ol class="steps">
    <li><h4>Choose "Pay with HSA/FSA" at checkout</h4><p>On an eligible SpringWell system, select the TrueMed option.</p></li>
    <li><h4>Answer a short health survey</h4><p>A couple of minutes, confidential. A licensed provider reviews your responses.</p></li>
    <li><h4>Receive your LMN</h4><p>If you qualify, the letter is issued &mdash; commonly within a few hours.</p></li>
    <li><h4>Pay and keep records</h4><p>Use your HSA/FSA card (split with a regular card if needed) and store the LMN and itemized receipt.</p></li>
  </ol>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Try it</span>
    <h3>Start the eligibility check</h3>
    <p>SpringWell's eligible systems issue the LMN through TrueMed at checkout &mdash; the cleanest way to keep your timing and documentation correct.</p>
    {aff("truemed-how-it-works", "See how it works", "btn")}
    &nbsp;{aff("truemed-eligible-category", "Shop eligible systems", "btn ghost")}
  </div>

  <h2>What a Letter of Medical Necessity must include</h2>
  <p>A valid LMN is short but specific. Whether a provider writes it directly or a service like TrueMed issues it, it should contain:</p>
  <ul>
    <li><strong>Patient information</strong> &mdash; the person whose condition justifies the purchase.</li>
    <li><strong>The diagnosed or preventable condition</strong> &mdash; what the filter is meant to treat, mitigate, or prevent.</li>
    <li><strong>The recommended item</strong> &mdash; the water filtration system or device, described generally (a specific brand is not required).</li>
    <li><strong>The medical rationale</strong> &mdash; a sentence or two linking the condition to the need for filtration.</li>
    <li><strong>Duration</strong> &mdash; how long the recommendation applies (often up to 12 months), which matters for replacement cartridges.</li>
    <li><strong>Provider details and signature</strong> &mdash; name, credentials, and date. The date must be on or before your purchase.</li>
  </ul>

  <h2>Letter of Medical Necessity template</h2>
  <p>Here is a simple template containing those elements. If you obtain your letter through TrueMed at checkout, you do not need to write anything &mdash; the provider produces it for you. This is for reference, or for readers working with their own physician.</p>
  <div class="lmn-template">
    <h4>Sample LMN &mdash; for reference only</h4>
    <p>Date: <span class="blank">[on or before purchase date]</span></p>
    <p>To the Plan Administrator:</p>
    <p>I am the treating provider for <span class="blank">[patient name]</span>. Based on <span class="blank">[diagnosis or documented condition &mdash; e.g., elevated blood lead level, eczema, immunocompromised status]</span>, I recommend a <span class="blank">[whole-house water filtration system / reverse osmosis system / UV purifier]</span> as medically necessary to <span class="blank">[treat / mitigate / prevent]</span> this condition by reducing exposure to <span class="blank">[lead / PFAS / nitrates / waterborne pathogens]</span> in the patient's household water supply.</p>
    <p>This recommendation is valid for <span class="blank">[duration, e.g., 12 months]</span>, including replacement filters required to maintain the system.</p>
    <p>Sincerely,<br><span class="blank">[Provider name, credentials, license number, signature]</span></p>
  </div>
  <div class="note warn"><span class="lab">Important</span>This sample is illustrative only &mdash; it is not a letter you can self-sign. An LMN must be issued and signed by a licensed provider; self-written letters are not valid.</div>

  <h2>Example: how a real case maps to the template</h2>
  <p>Suppose a family in a pre-1986 home tests their tap water and finds lead above the <a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">EPA action level</a>, and they have a toddler. Their provider documents the elevated-lead concern, recommends a lead-reducing whole-house system to prevent ongoing exposure to a vulnerable child, and notes the recommendation covers replacement filters for 12 months. That letter, dated before the purchase, turns the system into a qualified medical expense. See <a href="../how-to-get-letter-of-medical-necessity.html">how to get a letter and what providers look for</a>.</p>

  <h2>When you need to renew your letter</h2>
  <p>An LMN is typically valid for up to 12 months for the same product category. That window matters most for <a href="../water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridges</a>: if you reimburse ongoing replacements, you may need a renewed letter once the original lapses. Set a reminder, keep each letter with the matching receipts, and see <a href="../how-to-get-reimbursed-water-filter-fsa-hsa.html">how reimbursement works</a> for submission details. When you are ready to buy, our <a href="../how-to-buy-water-filter-with-hsa-fsa.html">step-by-step purchase guide</a> walks through the whole flow.</p>

  <h2>Keep your claim clean</h2>
  <ul>
    <li>Get the LMN dated <strong>on or before</strong> the purchase &mdash; no retroactive letters.</li>
    <li>Keep the LMN <strong>and</strong> an itemized receipt together.</li>
    <li>Renew when required (often annually) if you reimburse replacement cartridges.</li>
    <li>When in doubt, confirm specifics with your plan administrator.</li>
  </ul>
  <div class="note key"><span class="lab">Not advice</span>Educational only &mdash; not tax, legal, or medical advice. Eligibility depends on your plan and health situation.</div>

  <h2>Who can issue a Letter of Medical Necessity?</h2>
  <p>Any licensed healthcare provider acting within their scope can issue an LMN &mdash; physicians (MD/DO), nurse practitioners, and physician assistants are common examples. With a checkout service, an independent licensed provider reviews your survey, so you do not need an existing relationship. If you go through your own clinic, your treating provider is the natural choice because they already know your history.</p>

  <h2>How an LMN differs from a prescription</h2>
  <p>People often ask whether they need a "prescription" for a water filter. Not exactly. A prescription orders a specific medication or therapy; a Letter of Medical Necessity explains <em>why</em> a product or piece of equipment is needed to treat or prevent a condition. For durable items like water filters, the LMN is the right instrument, and it is what FSA/HSA administrators expect for equipment.</p>

  <h2>If your plan asks for more</h2>
  <p>Some administrators occasionally request additional detail &mdash; a diagnosis code, a longer rationale, or a renewal. This is routine. Keep your provider's contact handy, respond promptly, and retain every version of the letter. Because requirements vary between employers and plans, a quick call to your administrator before a large purchase can save back-and-forth later. See <a href="../how-to-get-reimbursed-water-filter-fsa-hsa.html">how reimbursement works</a> for submission specifics.</p>

  <h2>Make the letter specific</h2>
  <p>The strongest letters are specific rather than generic. A letter that names the documented contaminant (say, lead above the action level) and ties it to a vulnerable household member is more durable than one that vaguely cites "water quality." If you work with your own provider, share your <a href="../are-water-test-kits-fsa-hsa-eligible.html">water test results</a> and point them to the template above so the rationale is concrete.</p>

  <h2>FAQ</h2>
  {lmn_faq_html}
  {byline(1)}
</div>
</div>
"""
lmn += footer(1)
write("guides/letter-of-medical-necessity-water-filter.html", lmn)

def simple_page(path, title, desc, h1, body_html, depth=0):
    pre = "../"*depth
    p = head(title, desc, path, depth=depth)
    p += f"""
<div class="wrap">
<div class="crumbs"><a href="{pre}index.html">Home</a> &rsaquo; {h1}</div>
<article class="hero"><h1 class="prose">{h1}</h1></article>
<div class="prose">
{body_html}
{byline(depth)}
</div>
</div>
"""
    p += footer(depth)
    write(path, p)

# ABOUT
simple_page("about.html","About Us — FSA Eligible Water Filter","Meet Stephen Evangelista, founder of FSA Eligible Water Filter, and how our research-first, primary-source approach to HSA/FSA water-filter eligibility earns your trust.","About Us", f"""
<div class="founder">
  <img src="{FOUNDER_IMG}" alt="{AUTHOR}, founder of {NAME}">
  <div>
    <p class="fname">{AUTHOR}</p>
    <p class="frole">Founder &amp; Lead Water-Treatment Researcher &middot; {NAME}</p>
  </div>
</div>

<p class="lede">{NAME} exists to answer one deceptively hard question accurately: <em>when can a home water filter be paid for with HSA or FSA dollars &mdash; and how do you do it correctly?</em> We pair real water-quality knowledge with a precise reading of the tax rules, so the guidance you get is both health-smart and money-smart.</p>

<div class="smap-stats">
  <div class="stat"><span class="num">60+</span><span class="lbl">In-depth guides &amp; reviews</span></div>
  <div class="stat"><span class="num">4</span><span class="lbl">Primary-source bodies (IRS, EPA, CDC, NSF)</span></div>
  <div class="stat"><span class="num">100%</span><span class="lbl">Independent &amp; reader-first</span></div>
</div>

<h2>Meet Stephen Evangelista</h2>
<p>{AUTHOR} is the founder and lead researcher behind {NAME}. His work sits at the intersection of two subjects most resources treat separately: <strong>residential water quality</strong> &mdash; contaminants, treatment technologies, and certifications &mdash; and the <strong>rules that decide whether the equipment to address them qualifies as a medical expense</strong> under U.S. HSA and FSA accounts.</p>
<p>He built this site after watching how much conflicting, often inaccurate information surrounds a simple search like &ldquo;are water filters FSA eligible?&rdquo; Too many pages shout a confident <em>yes</em> and skip the one detail that actually matters &mdash; the Letter of Medical Necessity. Stephen's approach is the opposite: research-first, source-led, and honest about the limits. Every eligibility claim is traced back to IRS guidance, and every health or contaminant claim to authorities such as the EPA, CDC, and NSF.</p>

<h2>Areas of expertise</h2>
<ul>
  <li><strong>Water contaminants &amp; health</strong> &mdash; lead, PFAS, nitrates, chlorine and chloramine, bacteria, microplastics, iron, manganese, and sulfur, and what each means for a household.</li>
  <li><strong>Filtration &amp; treatment technology</strong> &mdash; whole-house carbon and catalytic carbon, reverse osmosis, UV purification, air-injection iron systems, and salt-based vs salt-free softening.</li>
  <li><strong>HSA / FSA eligibility</strong> &mdash; how a Letter of Medical Necessity turns a personal purchase into a qualified medical expense, and how the TrueMed checkout works.</li>
  <li><strong>Tax &amp; reimbursement rules</strong> &mdash; IRS Publications 502 and 969, documentation, claim denials, year-end deadlines, and the pre-tax savings math.</li>
  <li><strong>Buying &amp; product evaluation</strong> &mdash; matching a system to a verified water problem, reading certifications, and weighing cost of ownership.</li>
</ul>

<h2>Why you can trust this site</h2>
<p>The clearest measure of expertise is the work itself. {NAME} covers the full landscape &mdash; from the core eligibility question to contaminant-by-contaminant guides, system reviews, brand comparisons, and the exact reimbursement process &mdash; with each page grounded in primary sources rather than repackaged marketing. We are deliberately precise where it counts: we never say a filter is &ldquo;automatically&rdquo; eligible, we frame tax figures as current-year and &ldquo;verify for your plan,&rdquo; and we present honest trade-offs, including who a product is <em>not</em> for.</p>
<p>This is a Your-Money-Your-Life topic, so accuracy is not optional. When the rules are nuanced or evolving &mdash; as with recent EPA contaminant standards &mdash; we say so and point you to the source rather than pretending the answer is simpler than it is.</p>

<h2>How we research and review</h2>
<p>We ground eligibility statements in <strong>IRS Publication 502</strong> (Medical and Dental Expenses) and <strong>IRS Publication 969</strong> (HSAs and other tax-favored plans), and health and contaminant statements in the <strong>EPA</strong>, <strong>CDC</strong>, and <strong>NSF</strong>. Products are judged on contaminant reduction, maintenance and running cost, flow rate, warranty, certifications, and how the HSA/FSA purchase actually works. Full details are in our <a href="editorial-policy.html">editorial &amp; eligibility policy</a>.</p>

<h2>Our editorial independence</h2>
<p>{NAME} is reader-supported. Some links are affiliate links &mdash; if you buy through them we may earn a commission at <strong>no additional cost to you</strong>. Affiliate relationships never determine our recommendations or ratings; we recommend what genuinely fits a reader's situation and describe the limitations honestly. We are independent and not operated by any manufacturer. See our <a href="affiliate-disclosure.html">affiliate disclosure</a>.</p>

<h2>Sources we rely on</h2>
<ul>
  <li><strong>IRS</strong> &mdash; Publications 502 and 969 for medical-expense and HSA/FSA rules.</li>
  <li><strong>U.S. EPA</strong> &mdash; drinking-water standards and contaminant guidance.</li>
  <li><strong>CDC</strong> &mdash; private-well safety and waterborne-health guidance.</li>
  <li><strong>NSF</strong> &mdash; product certification standards such as NSF/ANSI 53 and 58.</li>
</ul>

<h2>Contact</h2>
<address class="contact-block">
  {NAME}<br>
  90 Madison St, 3rd Floor, Ste 306<br>
  Denver, CO 80206<br>
  <a href="mailto:{EMAIL}">{EMAIL}</a>
</address>
<p>Spot something that could be clearer or more accurate? <a href="contact.html">Tell us</a> &mdash; we update content when rules, prices, or products change.</p>

<div class="note key"><span class="lab">Not professional advice</span>Our content is educational and is not tax, legal, or medical advice. Eligibility depends on your specific plan and health situation; always confirm with your plan administrator and a qualified professional.</div>

<script type="application/ld+json">{{"@context":"https://schema.org","@type":"AboutPage","name":"About {NAME}","url":"{SITE}/about","mainEntity":{{"@type":"Person","name":"{AUTHOR}","jobTitle":"Founder & Lead Water-Treatment Researcher","image":"{FOUNDER_IMG}","url":"{SITE}/about","worksFor":{{"@type":"Organization","name":"{NAME}","url":"{SITE}"}},"knowsAbout":["Water filtration","Drinking water contaminants","Reverse osmosis","Whole-house water treatment","Water softeners","UV water purification","HSA and FSA eligibility","Letter of Medical Necessity","TrueMed","IRS Publication 502","IRS Publication 969","Water quality testing"]}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"{NAME}","url":"{SITE}","email":"{EMAIL}","founder":{{"@type":"Person","name":"{AUTHOR}"}},"address":{{"@type":"PostalAddress","streetAddress":"90 Madison St, 3rd Floor, Ste 306","addressLocality":"Denver","addressRegion":"CO","postalCode":"80206","addressCountry":"US"}}}}</script>
""", depth=0)

# EDITORIAL POLICY
simple_page("editorial-policy.html","Editorial & Eligibility Policy","How we research, verify, and update content about HSA/FSA water-filter eligibility, including our sources and review process.","Editorial &amp; eligibility policy", f"""
<p>This page explains how we produce and check our content &mdash; the foundation of trust on a topic that touches both health and money.</p>
<h2>How we verify eligibility claims</h2>
<ul>
  <li>We ground eligibility statements in primary sources: <strong>IRS Publication 502</strong> (Medical and Dental Expenses) and <strong>IRS Publication 969</strong> (HSA and other tax-favored plans).</li>
  <li>We describe the <strong>Letter of Medical Necessity</strong> mechanism accurately and never claim a filter is "automatically" eligible.</li>
  <li>For product and program details (e.g. TrueMed), we link to the official source so you can verify.</li>
  <li>Tax and contribution figures change yearly; we flag them as current-year and "verify for your plan."</li>
</ul>
<h2>How we review products</h2>
<p>We weigh contaminant reduction, maintenance and running cost, flow rate, warranty, and how the HSA/FSA purchase actually works. We state who a product is <em>not</em> for, and we present honest trade-offs rather than only positives.</p>
<h2>Corrections &amp; updates</h2>
<p>We date our pages and update them when rules, prices, or products change. Spot an error? <a href="contact.html">Tell us</a> and we will fix it.</p>
<h2>Not professional advice</h2>
<p>Our content is educational and is not tax, legal, or medical advice. Eligibility depends on your specific plan and health situation; confirm with your plan administrator and a qualified professional.</p>
""", depth=0)

# AFFILIATE DISCLOSURE
simple_page("affiliate-disclosure.html","Affiliate Disclosure","Our FTC affiliate disclosure: how FSA Eligible Water Filter earns commissions and why it does not affect our recommendations.","Affiliate disclosure", """
<p>In line with U.S. Federal Trade Commission guidelines, we want to be clear about how this site is funded.</p>
<p><strong>FSA Eligible Water Filter is reader-supported.</strong> Some links on this site are affiliate links, including links to SpringWell Water products. If you click one and make a purchase, we may earn a commission &mdash; <strong>at no additional cost to you</strong>. The price you pay is the same.</p>
<p>Affiliate relationships never determine our recommendations or ratings. We recommend systems we believe are a genuine fit for the reader's situation, and we describe trade-offs and limitations honestly. Affiliate links are marked as sponsored where they appear.</p>
<p>This site is independent and is not operated by SpringWell, TrueMed, or any manufacturer. Product names and brands are the property of their respective owners.</p>
<p>Questions? <a href="contact.html">Contact us</a>.</p>
""", depth=0)

# PRIVACY
simple_page("privacy-policy.html","Privacy Policy","How FSA Eligible Water Filter handles data, cookies, and third-party links.","Privacy policy", """
<p>This policy explains how FSA Eligible Water Filter ("we") handles information when you visit this website.</p>
<h2>Information we collect</h2>
<p>We do not require you to create an account or submit personal information to read this site. If we add contact forms or newsletters, any details you provide are used only to respond to you or send what you requested.</p>
<h2>Cookies &amp; analytics</h2>
<p>We may use privacy-respecting analytics to understand aggregate, anonymized traffic (for example, which guides are most read). These do not identify you personally. You can block cookies in your browser settings. See our <a href="cookie-policy.html">Cookie Policy</a> for details.</p>
<h2>Affiliate &amp; third-party links</h2>
<p>This site links to third parties such as SpringWell and TrueMed. When you follow those links, the destination site's own privacy policy governs any data it collects. We are not responsible for third-party practices.</p>
<h2>Your choices</h2>
<p>You can browse without providing personal data, decline cookies, and contact us to ask about anything we hold relating to you.</p>
<h2>Contact</h2>
<p>Questions about this policy? Reach us via our <a href="contact.html">contact page</a>. We may update this policy and will revise the date below when we do.</p>
<p class="updated">Last updated: June 16, 2026.</p>
""", depth=0)

# TERMS OF USE
simple_page("terms-of-use.html","Terms of Use — FSA Eligible Water Filter","The terms governing use of FSA Eligible Water Filter: acceptable use, intellectual property, affiliate links, disclaimers, liability, and governing law.","Terms of Use", f"""
<p class="updated">Last updated: {TODAY}</p>
<p>These Terms of Use (&ldquo;Terms&rdquo;) govern your access to and use of {NAME} (the &ldquo;Site&rdquo;), available at {SITE}. By using the Site, you agree to these Terms. If you do not agree, please do not use the Site.</p>

<h2>1. About the Site</h2>
<p>{NAME} is an independent, educational resource about home water filtration and when it may qualify as an HSA/FSA medical expense. Content is provided for general informational purposes only and is not professional advice &mdash; see our <a href="disclaimer.html">Disclaimer</a>.</p>

<h2>2. Use license</h2>
<p>You may view, download, and print pages for your own personal, non-commercial use. You may not republish, sell, or systematically copy our content, or use automated means to scrape it, without our prior written permission. Trademarks and brand names referenced on the Site are the property of their respective owners.</p>

<h2>3. Acceptable use</h2>
<p>You agree not to use the Site in any way that is unlawful, infringing, or harmful; to interfere with its operation or security; or to misrepresent your affiliation with us. We may suspend or restrict access for conduct that violates these Terms.</p>

<h2>4. Affiliate links and third-party products</h2>
<p>The Site contains affiliate links, including to SpringWell Water products. If you purchase through them we may earn a commission at no additional cost to you (see our <a href="affiliate-disclosure.html">Affiliate Disclosure</a>). We are not the seller of any product, do not fulfill orders, and are not responsible for products, prices, availability, warranties, or customer service provided by third parties. Your purchase is governed by the seller's own terms.</p>

<h2>5. Third-party links</h2>
<p>The Site links to third-party websites, such as government and certification sources and merchants. We provide these for convenience and do not control or endorse their content; we are not responsible for third-party sites or their policies.</p>

<h2>6. No professional advice</h2>
<p>Nothing on the Site is tax, legal, medical, or financial advice, and no professional relationship is created by your use of it. HSA/FSA eligibility depends on your specific plan and circumstances; always confirm with your plan administrator and a qualified professional. See our <a href="disclaimer.html">Disclaimer</a>.</p>

<h2>7. Disclaimer of warranties</h2>
<p>The Site and its content are provided &ldquo;as is&rdquo; and &ldquo;as available,&rdquo; without warranties of any kind, express or implied, including accuracy, completeness, fitness for a particular purpose, or non-infringement. We do not warrant that the Site will be uninterrupted, error-free, or current.</p>

<h2>8. Limitation of liability</h2>
<p>To the fullest extent permitted by law, {NAME}, its owner, and contributors will not be liable for any indirect, incidental, consequential, or special damages, or for any loss arising from your use of (or inability to use) the Site or reliance on its content, even if advised of the possibility of such damages.</p>

<h2>9. Indemnification</h2>
<p>You agree to indemnify and hold harmless {NAME} and its owner from any claims, losses, or expenses arising out of your misuse of the Site or violation of these Terms.</p>

<h2>10. Governing law</h2>
<p>These Terms are governed by the laws of the State of Colorado, United States, without regard to its conflict-of-laws rules. Any dispute will be subject to the exclusive jurisdiction of the state and federal courts located in Colorado.</p>

<h2>11. Changes to these Terms</h2>
<p>We may update these Terms from time to time. Changes take effect when posted, and the &ldquo;last updated&rdquo; date above will reflect the revision. Your continued use of the Site means you accept the updated Terms.</p>

<h2>12. Contact</h2>
<address class="contact-block">{NAME}<br>90 Madison St, 3rd Floor, Ste 306<br>Denver, CO 80206<br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
""", depth=0)

# DISCLAIMER
simple_page("disclaimer.html","Disclaimer — FSA Eligible Water Filter","Important disclaimer: FSA Eligible Water Filter provides general educational information only — not medical, tax, legal, or financial advice.","Disclaimer", f"""
<p class="updated">Last updated: {TODAY}</p>
<p>The information on {NAME} (the &ldquo;Site&rdquo;) is provided for general educational purposes only. By using the Site you acknowledge and agree to the points below.</p>

<div class="note warn"><span class="lab">In short</span>This Site does not provide medical, tax, legal, or financial advice and does not create any professional relationship. Always confirm your situation with your plan administrator and a qualified professional before acting.</div>

<h2>Not medical or health advice</h2>
<p>Content about contaminants, water quality, and health is general information, not medical advice, diagnosis, or treatment, and is not a substitute for guidance from a licensed healthcare provider. Never disregard or delay professional medical advice because of something you read here. Decisions about your health &mdash; including whether water treatment is appropriate for a condition &mdash; should be made with a qualified clinician.</p>

<h2>Not tax, legal, or financial advice</h2>
<p>We explain how HSA/FSA eligibility and the Letter of Medical Necessity generally work, but we are not tax advisors, attorneys, or financial advisors, and nothing here is individualized advice. Tax rules, contribution limits, and plan terms change and vary by plan. <strong>Eligibility is ultimately determined by your plan administrator and the IRS rules that apply to your situation.</strong> Confirm with your plan administrator and a qualified tax professional before purchasing or filing a claim.</p>

<h2>Accuracy and no guarantees</h2>
<p>We work hard to keep content accurate and current and to cite primary sources, but we make no guarantee that information is complete, current, or error-free. Regulations (for example, EPA contaminant standards) and product prices and specifications change; verify details against the original source and the manufacturer before relying on them.</p>

<h2>Results and examples</h2>
<p>Any examples, scenarios, or savings figures are illustrative only and are not a promise of any particular outcome, eligibility result, or savings. Your results depend on your plan, tax bracket, water, and circumstances.</p>

<h2>Affiliate links</h2>
<p>The Site is reader-supported and contains affiliate links; we may earn a commission at no additional cost to you. This never changes our recommendations. See our <a href="affiliate-disclosure.html">Affiliate Disclosure</a>.</p>

<h2>External links</h2>
<p>Links to third-party sites are provided for convenience. We do not control and are not responsible for their content, accuracy, or policies.</p>

<h2>Use at your own risk</h2>
<p>You use the Site and act on its information at your own risk. To the fullest extent permitted by law, {NAME} and its owner are not liable for any loss or damage arising from your use of the Site. See our <a href="terms-of-use.html">Terms of Use</a>.</p>

<h2>Contact</h2>
<p>Questions about this disclaimer? <a href="contact.html">Contact us</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
""", depth=0)

# COOKIE POLICY
simple_page("cookie-policy.html","Cookie Policy — FSA Eligible Water Filter","How FSA Eligible Water Filter uses cookies and similar technologies, the types of cookies used, and how to control them.","Cookie Policy", f"""
<p class="updated">Last updated: {TODAY}</p>
<p>This Cookie Policy explains how {NAME} (the &ldquo;Site&rdquo;) uses cookies and similar technologies. It should be read alongside our <a href="privacy-policy.html">Privacy Policy</a>.</p>

<h2>What cookies are</h2>
<p>Cookies are small text files stored on your device when you visit a website. They help sites function, remember preferences, and understand how pages are used. Similar technologies include local storage and pixels.</p>

<h2>How we use cookies</h2>
<ul>
  <li><strong>Strictly necessary</strong> &mdash; basic cookies that let the Site load and function correctly.</li>
  <li><strong>Analytics / performance</strong> &mdash; privacy-respecting, aggregated analytics that help us understand which guides are most useful. These do not identify you personally.</li>
  <li><strong>Affiliate / third-party</strong> &mdash; when you click an affiliate link, the destination merchant or its affiliate network may set cookies to attribute a referral. These are governed by those third parties' policies.</li>
</ul>
<p>We do not sell your personal information, and we do not use cookies to build advertising profiles of you on this Site.</p>

<h2>Third-party cookies</h2>
<p>Some cookies are set by third parties (for example, analytics providers or merchants you visit through our links). We do not control these cookies; please review the relevant third party's privacy and cookie policies.</p>

<h2>Managing cookies</h2>
<p>You can control or delete cookies through your browser settings, and set most browsers to refuse cookies or alert you when one is set. Blocking some cookies may affect how parts of the Site work. Your browser may also offer a &ldquo;Do Not Track&rdquo; setting.</p>

<h2>Changes</h2>
<p>We may update this Cookie Policy as our practices or the law change; the &ldquo;last updated&rdquo; date above will reflect any revision.</p>

<h2>Contact</h2>
<p>Questions? <a href="contact.html">Contact us</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
""", depth=0)

# ACCESSIBILITY
simple_page("accessibility.html","Accessibility Statement — FSA Eligible Water Filter","FSA Eligible Water Filter is committed to accessibility — how we work toward WCAG standards and how to give feedback.","Accessibility statement", f"""
<p class="updated">Last updated: {TODAY}</p>
<p>{NAME} is committed to making this Site accessible to as many people as possible, including people who use assistive technologies.</p>

<h2>Our approach</h2>
<p>We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA as a practical standard, and we build the Site to support that goal with:</p>
<ul>
  <li>Semantic HTML structure and a logical heading order.</li>
  <li>Text alternatives for meaningful images.</li>
  <li>Readable typography and color contrast intended to meet AA ratios.</li>
  <li>Keyboard-navigable links and controls, including a contact form with labeled fields.</li>
  <li>Responsive layouts that adapt to different screen sizes and zoom levels.</li>
</ul>

<h2>Known limitations</h2>
<p>Accessibility is an ongoing effort, and some content (for example, third-party embeds or certain interactive elements) may not yet fully conform. We work to identify and fix issues as we find them.</p>

<h2>Feedback</h2>
<p>If you encounter an accessibility barrier on the Site, please tell us so we can fix it. Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use our <a href="contact.html">contact page</a>, and include the page and the problem you experienced. We aim to respond promptly.</p>

<h2>Contact</h2>
<address class="contact-block">{NAME}<br>90 Madison St, 3rd Floor, Ste 306<br>Denver, CO 80206<br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
""", depth=0)

# CONTACT
simple_page("contact.html","Contact Us — FSA Eligible Water Filter","Contact FSA Eligible Water Filter — email, mailing address, and a contact form for questions, corrections, feedback, and partnership inquiries.","Contact us", f"""
<p class="lede">Questions, corrections, or feedback? We read every message. Use the form below, or reach us directly with the details here.</p>

<div class="contact-cards">
  <div class="cc">
    <h3>Email</h3>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="updated">Best for questions, corrections &amp; feedback.</p>
  </div>
  <div class="cc">
    <h3>Mailing address</h3>
    <address class="contact-block">{NAME}<br>90 Madison St, 3rd Floor, Ste 306<br>Denver, CO 80206</address>
  </div>
</div>

<h2>Send us a message</h2>
<p>Fill out the form and it goes straight to our inbox. Please include the page URL if you are reporting a correction.</p>
<form class="cform" action="https://formsubmit.co/{EMAIL}" method="POST">
  <input type="hidden" name="_subject" value="New message from FSA Eligible Water Filter">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="{SITE}/thanks.html">
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="row2">
    <div>
      <label for="cf-name">Your name</label>
      <input id="cf-name" type="text" name="name" required placeholder="Jane Doe">
    </div>
    <div>
      <label for="cf-email">Your email</label>
      <input id="cf-email" type="email" name="email" required placeholder="you@example.com">
    </div>
  </div>
  <div>
    <label for="cf-topic">Topic</label>
    <select id="cf-topic" name="topic">
      <option>General question</option>
      <option>Correction to a page</option>
      <option>Feedback</option>
      <option>Partnership / media</option>
      <option>Other</option>
    </select>
  </div>
  <div>
    <label for="cf-msg">Message</label>
    <textarea id="cf-msg" name="message" required placeholder="How can we help? For corrections, please include the page URL."></textarea>
  </div>
  <button class="btn" type="submit">Send message</button>
</form>

<div class="note key"><span class="lab">Please note</span>We cannot give individual tax, legal, or medical advice, or confirm your specific plan's rules &mdash; your plan administrator is the right source for that. For corrections, include the page and what needs fixing; we update content when rules, prices, or products change.</div>

<h2>Looking for something else?</h2>
<p>Many questions are already answered in our guides. Start with <a href="index.html">Are water filters FSA/HSA eligible?</a>, the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> guide, or browse the full <a href="sitemap.html">sitemap</a>.</p>

<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ContactPage","name":"Contact {NAME}","url":"{SITE}/contact","mainEntity":{{"@type":"Organization","name":"{NAME}","url":"{SITE}","email":"{EMAIL}","contactPoint":{{"@type":"ContactPoint","contactType":"customer support","email":"{EMAIL}"}},"address":{{"@type":"PostalAddress","streetAddress":"90 Madison St, 3rd Floor, Ste 306","addressLocality":"Denver","addressRegion":"CO","postalCode":"80206","addressCountry":"US"}}}}}}</script>
""", depth=0)

# THANK YOU (form redirect target)
simple_page("thanks.html","Thank you — FSA Eligible Water Filter","Thanks for contacting FSA Eligible Water Filter — your message is on its way.","Thank you", """
<p class="lede">Thanks for reaching out &mdash; your message is on its way to us.</p>
<p>We read every message and reply as soon as we can. In the meantime, you might find what you need in our guides.</p>
<p style="margin-top:1.2rem"><a class="btn" href="index.html">Back to the eligibility guide</a> &nbsp; <a class="btn ghost" href="best-fsa-hsa-eligible-water-filters.html">See the best systems</a></p>
""", depth=0)

# 404
nf = head("Page not found — FSA Eligible Water Filter","The page you were looking for could not be found.","404.html", depth=0)
nf += f"""
<div class="wrap">
<article class="hero center" style="padding:5rem 0">
  <span class="eyebrow">404</span>
  <h1>That page isn't here</h1>
  <p class="lede" style="margin:0 auto">The link may be old or mistyped. Try the eligibility guide or browse the best eligible systems.</p>
  <p style="margin-top:1.6rem"><a class="btn" href="index.html">Eligibility guide</a> &nbsp; <a class="btn ghost" href="best-fsa-hsa-eligible-water-filters.html">Best systems</a></p>
</article>
</div>
"""
nf += footer(0)
write("404.html", nf)

# ---- cloaking: write vercel.json with /go/<key> -> tracking link redirects ----
redirects = [{"source": f"/go/{k}", "destination": v, "permanent": False} for k, v in LINKS.items()]
vercel = {
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": True,
  "trailingSlash": False,
  "redirects": redirects,
  "headers": [
    {"source": "/(.*)\\.(css|js|svg)", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400"}]}
  ]
}
with open(os.path.join(ROOT, "vercel.json"), "w") as f:
    json.dump(vercel, f, indent=2)
print(f"  vercel.json  ({len(redirects)} cloaked /go/ redirects)")

# keep cloaked links out of the index
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: https://fsaeligiblewaterfilter.com/sitemap.xml\n")
print("  robots.txt  (Disallow: /go/)")

# (Cluster A articles and sitemap are generated by the appended block below)

# ======================================================================
#  CLUSTER A — Eligibility & Rules (Articles #1-#6)
# ======================================================================
def iaff(key, text):
    return f'<a data-aff="{key}" rel="sponsored nofollow noopener" target="_blank" href="/go/{key}">{text}</a>'

def art_schema(title, desc, path):
    return {"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,
            "author":{"@type":"Person","name":AUTHOR},"publisher":{"@type":"Organization","name":NAME},
            "dateModified":"2026-06-16","mainEntityOfPage":f"{SITE}/{path}"}

def faq_block(items):
    h='<div class="faq">'
    for q,a in items:
        h+=f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>'
    return h+'</div>'

def article(slug,title,desc,crumb,h1,lede,body,faq=None,schema_extra=None):
    schema=[art_schema(title,desc,slug)]
    if schema_extra: schema+=schema_extra
    if faq: schema.append(faq_schema(faq))
    p=head(title,desc,slug,schema,depth=0)
    p+=f'''
<div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> &rsaquo; {crumb}</div>
<article class="hero">
  <span class="eyebrow">{CHECK} Eligibility guide</span>
  <h1 class="prose">{h1}</h1>
  <p class="lede prose">{lede}</p>
  <div class="meta"><span>{CHECK} Reviewed against IRS Pub. 502 &amp; 969</span><span>&middot; {AUTHOR}</span><span>&middot; Updated {TODAY}</span></div>
</article>
<div class="prose">
{disc(0)}
{body}
'''
    if faq:
        p+=f'\n  <h2 id="faq">Frequently asked questions</h2>\n  {faq_block(faq)}\n'
    p+=byline(0)
    p+='</div>\n</div>\n'
    p+=footer(0)
    write(slug,p)

IRS502='<a href="https://www.irs.gov/publications/p502" target="_blank" rel="noopener">IRS Publication 502</a>'
IRS969='<a href="https://www.irs.gov/publications/p969" target="_blank" rel="noopener">IRS Publication 969</a>'
EPALEAD='<a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">EPA</a>'
EPAPFAS='<a href="https://www.epa.gov/pfas" target="_blank" rel="noopener">EPA PFAS</a>'
NSF='<a href="https://www.nsf.org/knowledge-library/standards-water-treatment-systems" target="_blank" rel="noopener">NSF/ANSI standards</a>'
CDC='<a href="https://www.cdc.gov/healthywater/drinking/" target="_blank" rel="noopener">CDC</a>'

# ---------- Article #1 ----------
article(
 "are-water-filters-fsa-eligible.html",
 "Are Water Filters FSA Eligible? Quick Answer + Rules",
 "Yes, water filters can be FSA eligible, but only with a Letter of Medical Necessity. Here is the rule, what qualifies, and how to buy one with FSA funds.",
 "Are water filters FSA eligible?",
 "Are water filters FSA eligible?",
 "Yes, a water filter can be FSA eligible &mdash; but it is not automatic. It qualifies only when it treats or prevents a specific health condition and you hold a Letter of Medical Necessity from a licensed provider. Here is exactly what that means and how to do it.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>FSA eligible &mdash; with a Letter of Medical Necessity (LMN).</b> Ordinary filters bought for taste are a personal expense; with an LMN tying the filter to a health condition, the same purchase qualifies for FSA reimbursement.</p>
  </div>

  <h2>The rule in plain English</h2>
  <p>The IRS does not list household water filters as automatically reimbursable the way it does bandages or thermometers. Under {IRS502}, an expense becomes a <strong>qualified medical expense</strong> only when it is used primarily to treat, mitigate, or prevent a specific medical condition. A filter bought simply for better-tasting water is considered personal &mdash; and personal expenses are not FSA eligible.</p>
  <p>What flips a filter into the eligible column is documentation of <strong>medical necessity</strong>. For equipment like a water filter, that document is a <strong>Letter of Medical Necessity (LMN)</strong> issued by a licensed provider. With it, the filter is treated like any other qualified medical expense. Without it, your FSA administrator can deny or claw back the claim.</p>
  <div class="note key"><span class="lab">One-sentence rule</span>A water filter is FSA eligible when it is bought to address a diagnosed or preventable health condition and is backed by a Letter of Medical Necessity. Our <a href="index.html">complete eligibility guide</a> walks through every detail.</div>

  <h2>What kinds of water filters can qualify?</h2>
  <p>Eligibility follows the health rationale, not the product category, so most filter types can qualify when the medical case is sound:</p>
  <ul>
    <li><strong>Whole-house (point-of-entry) systems</strong> &mdash; the strongest case, because they reduce exposure at every tap. See <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a>.</li>
    <li><strong>Under-sink and reverse osmosis</strong> &mdash; good for drinking-water contaminants like lead or nitrates. See <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</li>
    <li><strong>Replacement cartridges</strong> &mdash; the ongoing consumables can also qualify. See <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridge rules</a>.</li>
  </ul>

  <h2>How to make your water filter FSA eligible (3 steps)</h2>
  <ol class="steps">
    <li><h4>Document the medical need</h4><p>A licensed provider issues the LMN. The easiest route is buying from a retailer that builds this into checkout &mdash; see <a href="guides/letter-of-medical-necessity-water-filter.html">how the LMN works</a>.</p></li>
    <li><h4>Buy and pay with your FSA card</h4><p>Pay at checkout. If your balance is short, split with a regular card and submit the rest for reimbursement.</p></li>
    <li><h4>Keep your LMN and itemized receipt</h4><p>Store both in case your administrator asks for documentation.</p></li>
  </ol>

  <h2>FSA-specific things to know</h2>
  <p>Because most FSAs follow a <strong>use-it-or-lose-it</strong> rule, your balance often expires on December 31 (some plans add a short grace period or small carryover). That deadline makes a qualifying filter a smart way to convert money you would otherwise forfeit into a durable home upgrade. The LMN must be dated on or before your purchase &mdash; retroactive letters are not accepted.</p>
  <p>Systems like {iaff("whole-house","SpringWell's whole-house filter")} qualify through the TrueMed LMN process at checkout. If you are comparing options, see our roundup of the <a href="best-fsa-hsa-eligible-water-filters.html">best FSA/HSA-eligible systems</a>.</p>

  <div class="note tip"><span class="lab">Have an HSA instead?</span>The rule is the same, but HSAs roll over and never expire &mdash; see <a href="are-water-filters-hsa-eligible.html">Are water filters HSA eligible?</a></div>

  <h2>FSA eligible vs HSA eligible: is there a difference?</h2>
  <p>For the filter itself, no &mdash; both accounts use the same definition of a qualified medical expense and both require a Letter of Medical Necessity. The difference is in the account, not the product. An FSA is usually employer-sponsored and follows use-it-or-lose-it, so the money is "now or never." An HSA is yours to keep, rolls over indefinitely, and pairs with a high-deductible health plan. If you are deciding which to use, our <a href="index.html#accounts">account comparison</a> lays out HSA vs FSA vs HRA vs LPFSA side by side, and the <a href="are-water-filters-hsa-eligible.html">HSA guide</a> covers the rollover advantage in detail.</p>

  <h2>How much does FSA eligibility actually save you?</h2>
  <p>Because FSA dollars are set aside before income tax, buying a qualifying filter with them means you never pay tax on that money. Your effective discount equals your marginal tax rate &mdash; commonly 20&ndash;37% depending on your bracket. On a $1,500 system, that is roughly $300&ndash;$555 you keep. The savings are real but not unlimited: you are saving your tax rate, not getting the filter free. Treat any figure as illustrative and verify against your own bracket.</p>

  <h2>Three mistakes that get filter claims denied</h2>
  <ul>
    <li><strong>Buying before the letter.</strong> The Letter of Medical Necessity must be dated on or before your purchase date. Retroactive letters are routinely rejected.</li>
    <li><strong>Keeping only a card statement.</strong> Save the <em>itemized</em> receipt that names the product, not just a bank line item.</li>
    <li><strong>Claiming a comfort upgrade.</strong> Eligibility rests on a health rationale, not better taste. If your only reason is flavor, it is a personal expense &mdash; and over-claiming is what triggers clawbacks.</li>
  </ul>
  <p>For the complete compliance walkthrough, see <a href="index.html#denied">avoiding a denied claim</a>, and to understand the letter itself, read <a href="guides/letter-of-medical-necessity-water-filter.html">what a Letter of Medical Necessity is</a>.</p>

  <h2>Not sure you qualify?</h2>
  <p>You do not decide medical necessity yourself &mdash; a licensed provider does, and prevention counts. A documented contaminant such as lead (which the {EPALEAD} says has no safe level in drinking water) combined with a vulnerable household member is exactly the situation the rule was built for. Services that issue the letter at checkout review a short health survey and tell you whether you qualify, so the practical move is to complete it rather than talk yourself out of it in advance.</p>
''',
 faq=[
  ("Are water filters automatically FSA eligible?","No. Filters bought for taste or convenience are a personal expense. A filter qualifies only when it treats or prevents a health condition and you have a Letter of Medical Necessity from a licensed provider."),
  ("Can I just swipe my FSA card for a water filter?","Not reliably. Without an LMN on file, the charge may be declined or later reversed. The safest route is to get the letter at the time of purchase, then pay with your FSA card."),
  ("How much can I save?","You avoid income tax on the dollars you spend, so the effective discount equals your tax rate &mdash; commonly 20-37%. Exact savings depend on your bracket and plan."),
  ("Does the filter need a prescription?","Not a traditional prescription, but a Letter of Medical Necessity serves the same purpose for equipment like a filter. A licensed provider issues it based on your health situation."),
 ])

# ---------- Article #2 ----------
article(
 "are-water-filters-hsa-eligible.html",
 "Are Water Filters HSA Eligible? 2026 Rules + How-To",
 "Water filters can be HSA eligible with a Letter of Medical Necessity. Learn the HSA rules, the rollover advantage, and how to pay for a filter pre-tax.",
 "Are water filters HSA eligible?",
 "Are water filters HSA eligible?",
 "Yes &mdash; a water filter can be HSA eligible with a Letter of Medical Necessity, and an HSA is often the better account to use because the funds roll over and never expire. Here is how it works.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>HSA eligible &mdash; with a Letter of Medical Necessity.</b> The same medical-necessity rule applies as with an FSA, but your HSA balance carries over year to year, which suits larger systems.</p>
  </div>

  <h2>The HSA rule</h2>
  <p>Health Savings Accounts follow the same definition of a qualified medical expense found in {IRS502} and {IRS969}. A water filter is not automatically eligible; it qualifies when a licensed provider documents that it treats, mitigates, or prevents a specific health condition. That document is a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. The mechanics are identical to the <a href="are-water-filters-fsa-eligible.html">FSA process</a> &mdash; what differs is the account behavior.</p>

  <h2>Why an HSA is often the better choice for a filter</h2>
  <ul>
    <li><strong>Funds roll over.</strong> Unlike most FSAs, an HSA never expires. You can save across two or three years and buy a larger whole-house system outright.</li>
    <li><strong>The account is yours.</strong> It stays with you if you change jobs or retire.</li>
    <li><strong>Triple tax advantage.</strong> Contributions are pre-tax, growth is tax-free, and qualified withdrawals are tax-free.</li>
    <li><strong>Higher effective ceiling.</strong> Because balances accumulate, an HSA comfortably covers multi-thousand-dollar systems that exceed a single year's FSA limit.</li>
  </ul>
  <div class="note tip"><span class="lab">Deciding between accounts?</span>If you have both, a common strategy is to spend an expiring FSA balance first and reserve the HSA for the larger purchase. Our <a href="index.html#accounts">pillar guide compares HSA vs FSA vs HRA vs LPFSA</a>.</div>

  <h2>How to buy a filter with your HSA</h2>
  <ol class="steps">
    <li><h4>Get the Letter of Medical Necessity</h4><p>A provider reviews your situation and issues the LMN &mdash; built into checkout on eligible retailers.</p></li>
    <li><h4>Pay with your HSA card</h4><p>Use it like a debit card. Keep the LMN and itemized receipt.</p></li>
    <li><h4>Save records for the life of the account</h4><p>HSAs can be audited years later, so retain documentation even longer than you would for an FSA.</p></li>
  </ol>
  <p>Because HSAs suit bigger systems, many buyers put the money toward a {iaff("whole-house","whole-house filter")} that treats the entire home. See <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a> or compare the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a>.</p>

  <h2>A worked example: the HSA savings on a water filter</h2>
  <p>Say you are in a combined 30% marginal bracket and buy a $2,000 whole-house system with HSA funds. Because that $2,000 was set aside pre-tax, you avoid roughly $600 in tax you would have paid on the same money earned normally &mdash; an effective cost near $1,400. At a higher bracket the saving is larger; at a lower one, smaller. The mechanism is simple: you are discounting the purchase by your tax rate. Our <a href="index.html#savings">pillar guide shows the pre-tax vs after-tax math</a> in a side-by-side table.</p>

  <h2>Contribution limits and timing (verify for your plan year)</h2>
  <p>HSA contribution limits are set annually by the IRS and differ for individual vs family coverage, with a catch-up amount for those 55 and older. Because a whole-house system can cost more than a single year's contribution, savers often spread contributions across two years and buy once the balance is sufficient &mdash; something an FSA cannot do. Always confirm the current year's limits and your own balance in {IRS969} and your HSA portal before planning a large purchase.</p>

  <h2>What if you don't have enough in your HSA yet?</h2>
  <p>You have two clean options. First, split the payment: cover what your HSA card allows and put the remainder on a regular card, keeping the Letter of Medical Necessity and receipt for the qualified portion. Second, pay out of pocket now and reimburse yourself from the HSA later once funds are available &mdash; permitted as long as the expense was qualified and the letter predates the purchase. Keep documentation either way; HSAs can be reviewed years after the fact.</p>
''',
 faq=[
  ("Is a water filter an HSA qualified medical expense?","It can be. With a Letter of Medical Necessity tying the filter to a health condition, it qualifies under the same IRS rules that govern other HSA medical expenses."),
  ("Does my HSA balance expire if I don't buy this year?","No. HSA funds roll over indefinitely and remain yours, which is why an HSA is well suited to saving for a larger water system."),
  ("Can I reimburse myself later from my HSA?","Generally yes &mdash; if the expense was qualified and the LMN was dated on or before the purchase. Keep documentation, and confirm your administrator's rules."),
 ])

# ---------- Article #3 ----------
article(
 "whole-house-water-filtration-hsa-fsa-eligible.html",
 "Is a Whole-House Water Filter HSA/FSA Eligible? (2026)",
 "A whole-house water filter can be HSA/FSA eligible with a Letter of Medical Necessity. See what qualifies, costs, and the best eligible systems for 2026.",
 "Whole-house system eligibility",
 "Is a whole-house water filtration system HSA/FSA eligible?",
 "Yes &mdash; a whole-house system can be HSA/FSA eligible with a Letter of Medical Necessity, and because it reduces contaminant exposure at every tap, it is often the most defensible filtration purchase of all.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> A point-of-entry system that treats the whole home makes the strongest medical-necessity case, because it reduces exposure everywhere, not at a single faucet.</p>
  </div>

  <h2>Why whole-house systems have the strongest eligibility case</h2>
  <p>Eligibility depends on demonstrating that filtration addresses a health risk. A whole-house, point-of-entry (POE) system does exactly that across every tap and shower &mdash; so the medical-necessity argument is broader and easier to support than for a single-faucet filter. If a provider connects your situation to a contaminant such as lead (which the {EPALEAD} states has no safe level) or to an immunocompromised household, a system that filters all household water is a natural fit.</p>
  <p>The eligibility mechanism is the same as for any filter: a licensed provider issues a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, and you pay with your HSA/FSA card. See the <a href="index.html">full eligibility guide</a> for the underlying IRS framing.</p>

  <h2>What a whole-house system costs &mdash; and which account to use</h2>
  <p>Whole-house systems typically run from about $1,100 to over $4,000 depending on configuration. That range frequently exceeds a single year's FSA contribution limit, which has two practical implications:</p>
  <ul>
    <li><strong>An HSA is often the better fit</strong> because balances roll over &mdash; you can save up and buy outright. See <a href="are-water-filters-hsa-eligible.html">HSA eligibility</a>.</li>
    <li><strong>Split payments work</strong> if your balance is short: pay what your HSA/FSA covers and put the remainder on a regular card.</li>
  </ul>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Editor's pick</span>
    <h3>SpringWell Whole House Filter</h3>
    <p>Broad contaminant reduction, very low maintenance, a lifetime warranty, and a built-in TrueMed HSA/FSA checkout that issues the LMN for you. From ~$1,170.</p>
    {aff("whole-house","Check price &amp; eligibility","btn")}
    &nbsp;<a class="btn ghost" href="reviews/springwell-whole-house-water-filter-review.html">Read our full review &rarr;</a>
  </div>

  <h2>How to choose a whole-house system</h2>
  <p>Match the system to your water: test first (city users can read the annual Consumer Confidence Report; well users should lab-test), then weigh contaminant target, flow rate for your household size, certifications to {NSF}, maintenance cost, and warranty. For a side-by-side, see the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible whole-house systems</a>, and if you are weighing coverage, read <a href="index.html#water-type">city vs well water</a>.</p>

  <h2>Which contaminants justify a whole-house system?</h2>
  <p>The cleanest medical-necessity cases involve contaminants with recognized health effects that reach you through more than just the kitchen tap:</p>
  <ul>
    <li><strong>Lead</strong> &mdash; no safe level per the {EPALEAD}; highest risk for children and during pregnancy.</li>
    <li><strong>PFAS</strong> &mdash; persistent "forever chemicals" under tightening {EPAPFAS} attention.</li>
    <li><strong>Chlorine and chloramine by-products</strong> &mdash; relevant for skin and respiratory sensitivity, and a reason whole-home (including showers) matters.</li>
    <li><strong>Microbial risk in immunocompromised households</strong> &mdash; the {CDC} notes higher vulnerability for some patients, where treating all water is sensible.</li>
  </ul>

  <h2>Whole-house vs point-of-use for eligibility</h2>
  <p>A point-of-use filter (like an under-sink {iaff("moen-ro","reverse osmosis unit")}) treats one tap and is cheaper, while a whole-house system treats every tap and shower. For eligibility, breadth helps: reducing exposure throughout the home is easier to frame as medically necessary than treating a single faucet. If your concern is drinking water only, RO may suffice &mdash; see <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>; if exposure is whole-home (e.g., showering in chlorinated or contaminated water), the whole-house case is stronger.</p>

  <h2>How to document medical necessity for a whole-house system</h2>
  <p>The pattern is the same as any eligible filter, with a little more attention because of the cost: get the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> dated on or before purchase, keep an itemized receipt, and store both. If you split the payment across cards, document the qualified portion clearly. Installation and labor are treated differently by different plans &mdash; ask your administrator how they handle it rather than assuming.</p>
''',
 faq=[
  ("Is a whole-house water filter a qualified medical expense?","It can be, with a Letter of Medical Necessity. Because it reduces exposure throughout the home, it is often the easiest filtration purchase to justify as medically necessary."),
  ("My system costs more than my FSA limit. What now?","Use an HSA (funds roll over) or split the payment between your HSA/FSA card and a regular card. Keep the LMN and receipt for the qualified portion."),
  ("Does installation count toward the eligible expense?","Policies vary by plan. The system itself is the qualified item; ask your plan administrator how they treat installation and labor."),
 ])

# ---------- Article #4 ----------
article(
 "are-water-softeners-fsa-hsa-eligible.html",
 "Are Water Softeners FSA/HSA Eligible? (2026 Guide)",
 "Water softeners are harder to qualify than filters. Learn when a softener is HSA/FSA eligible and which filter + softener combos qualify.",
 "Water softener eligibility",
 "Are water softeners FSA/HSA eligible?",
 "Sometimes &mdash; a water softener is harder to qualify than a filter, because hardness is often a comfort issue rather than a health one. But with a documented medical reason and a Letter of Medical Necessity, a softener (or a filter + softener combo) can be eligible.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Conditionally eligible.</b> A softener alone is harder to justify than a filter. It can qualify with a Letter of Medical Necessity when a provider links water hardness to a health condition &mdash; and combos that include filtration are easier to support.</p>
  </div>

  <h2>Why softeners are a tougher case than filters</h2>
  <p>Eligibility hinges on health, not comfort. Hard water is mostly a nuisance &mdash; scale, spotty dishes, dry-feeling skin &mdash; and "nuisance" is not a medical expense under {IRS502}. So a softener bought purely for convenience is a personal expense.</p>
  <p>Where it can qualify is when a licensed provider documents a genuine health rationale &mdash; for example, a dermatological condition a provider connects to water quality. As always, the provider makes that judgment and issues the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>; you should not assume eligibility on your own.</p>
  <div class="note warn"><span class="lab">Be honest with the rule</span>Do not claim a softener as medical if your reason is purely cosmetic or convenience. Over-claiming is exactly what gets FSA/HSA purchases denied or reversed.</div>

  <h2>The stronger play: a filter + softener combo</h2>
  <p>Because <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house filtration</a> carries a clearer medical-necessity case, a combined system that pairs filtration with softening is generally easier to support than a standalone softener &mdash; the filtration half addresses contaminant exposure across the home, and you solve hardness in the same purchase.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Best for hard water</span>
    <h3>SpringWell Filter + Softener Combo</h3>
    <p>Whole-house filtration plus softening in one eligible system &mdash; available salt-based or salt-free. Runs through the TrueMed LMN checkout.</p>
    {aff("filter-softener-combo","Check price","btn")}
    &nbsp;<a class="btn ghost" href="reviews/springwell-filter-softener-combo-review.html">Read the combo review &rarr;</a>
  </div>

  <h2>Salt-based vs salt-free for a low-sodium household</h2>
  <p>If sodium intake is the documented health concern, a {iaff("salt-free-combo","salt-free conditioner")} (which adds no sodium) may be the more sensible choice than traditional salt-based softening. Discuss your specific situation with your provider, and confirm coverage with your plan administrator before buying.</p>

  <h2>When is a softener actually medically necessary?</h2>
  <p>This is where honesty protects you. A provider is looking for a genuine link between water characteristics and a health condition &mdash; not generalized dislike of hard water. Situations that may support a case include a dermatological condition a clinician connects to water quality, or a documented need to limit sodium that makes a salt-free conditioner preferable to a salt-based unit. In each case the provider makes the determination and issues the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>; you should not self-certify.</p>

  <h2>Hard water and skin: what the evidence actually says</h2>
  <p>Research on hard water and skin conditions such as eczema is mixed and still developing &mdash; some studies suggest an association, others are inconclusive. The practical takeaway: do not overstate the science. If you have a skin condition, the right move is to discuss it with your provider, who can decide whether softening or filtration is a reasonable part of managing it. General consumer-health resources like the {CDC} are a sensible starting point for understanding water quality, but your clinician's judgment is what supports eligibility.</p>

  <h2>How to document a softener (or combo) claim</h2>
  <p>Because softeners draw more scrutiny than filters, tight documentation matters: secure the Letter of Medical Necessity before purchase, keep an itemized receipt, and retain any provider notes that connect the system to your condition. A <a href="reviews/springwell-filter-softener-combo-review.html">filter + softener combo</a> is generally easier to support than a standalone softener because the filtration component has a clearer health rationale &mdash; see also <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a>.</p>
''',
 faq=[
  ("Is a water softener FSA eligible?","Not by default. A softener bought for comfort is a personal expense. It can qualify with a Letter of Medical Necessity when a provider links hard water to a specific health condition."),
  ("Why is a filter easier to qualify than a softener?","Filters reduce exposure to contaminants with recognized health risks (like lead or PFAS), which maps cleanly to medical necessity. Hardness is more often a comfort issue."),
  ("Are filter + softener combos eligible?","The filtration component carries a clear medical-necessity case, so a combo is generally easier to support than a standalone softener &mdash; still with a Letter of Medical Necessity."),
 ])

# ---------- Article #5 ----------
article(
 "is-reverse-osmosis-fsa-hsa-eligible.html",
 "Is Reverse Osmosis (RO) FSA/HSA Eligible? (2026)",
 "Reverse osmosis systems can be FSA/HSA eligible with a Letter of Medical Necessity. Learn what RO removes, who it suits, and eligible under-sink options.",
 "Reverse osmosis eligibility",
 "Is reverse osmosis FSA/HSA eligible?",
 "Yes &mdash; a reverse osmosis (RO) system can be FSA/HSA eligible with a Letter of Medical Necessity. RO is a strong fit when the health concern is in your drinking water specifically, and it is the most affordable eligible route.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> An under-sink RO system qualifies on the same basis as any filter, and is the lowest-cost eligible option for treating drinking and cooking water.</p>
  </div>

  <h2>What reverse osmosis removes &mdash; and why that matters for eligibility</h2>
  <p>RO pushes water through a semipermeable membrane that removes a wide range of dissolved contaminants &mdash; including lead, nitrates, and many that drive medical-necessity cases. Systems certified to {NSF} (notably NSF/ANSI 58 for RO) give you and your provider confidence in what the unit actually reduces, which strengthens the documentation behind your purchase. For contaminant-specific context, see lead concerns at the {EPALEAD} and {EPAPFAS} resources.</p>
  <p>Because the health rationale is about your drinking water, RO maps neatly to medical necessity for households worried about a specific drinking-water contaminant. The eligibility mechanism is unchanged: a provider issues the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, and you pay with your HSA/FSA card.</p>

  <h2>Who reverse osmosis is right for</h2>
  <ul>
    <li><strong>Renters and apartments</strong> &mdash; under-sink RO does not require treating the whole home and can move with you.</li>
    <li><strong>Drinking-water-only concerns</strong> &mdash; if your issue is what you drink and cook with, RO targets exactly that.</li>
    <li><strong>Tight budgets</strong> &mdash; RO is the most affordable eligible category. See <a href="index.html">how the savings math works</a>.</li>
  </ul>
  <p>If your concern is whole-home exposure (showering, every tap), a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> makes a broader case &mdash; many readers weigh the two in our <a href="index.html#water-type">point-of-entry vs point-of-use</a> discussion.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Best budget / point-of-use</span>
    <h3>Moen Reverse Osmosis (under-sink)</h3>
    <p>A compact, renter-friendly RO system for clean drinking and cooking water &mdash; the lowest-cost eligible option, around $399, through the TrueMed checkout.</p>
    {aff("moen-ro","Check price","btn")}
  </div>

  <h2>RO vs whole-house vs pitcher: which is right for you?</h2>
  <p>All three can be eligible with a Letter of Medical Necessity, but they fit different needs. A pitcher filter is cheapest and treats small batches &mdash; fine for a single contaminant and a renter on a budget. Under-sink RO gives stronger, certified contaminant removal at the kitchen tap. A <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> treats every tap and shower and makes the broadest medical-necessity case. If your documented concern is specifically what you drink and cook with, RO is usually the sweet spot of cost and performance.</p>

  <h2>What reverse osmosis does <em>not</em> do</h2>
  <p>RO is thorough, which has two trade-offs worth knowing before you buy. First, it removes beneficial minerals along with contaminants, so some systems add a remineralization stage for taste &mdash; a reasonable feature, not a necessity. Second, RO produces some wastewater and treats water slowly through a storage tank, so it suits drinking and cooking rather than whole-home supply. None of this affects eligibility; it just shapes whether RO or a whole-house system is the better match for your situation.</p>

  <h2>Maintenance, membranes, and documentation</h2>
  <p>RO systems need periodic filter and membrane changes. Those replacements can be eligible on the same basis as the system &mdash; keep itemized receipts and your Letter of Medical Necessity, and see <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridge eligibility</a> for the record-keeping routine. As with any eligible purchase, get the letter dated on or before you buy, and confirm submission rules with your plan administrator.</p>
''',
 faq=[
  ("Is a reverse osmosis system a qualified medical expense?","It can be, with a Letter of Medical Necessity. RO is a good fit when the documented health concern is in your drinking water, such as lead or nitrates."),
  ("Is RO or a whole-house filter better for FSA/HSA?","RO is cheaper and treats one tap; a whole-house system treats every tap and makes a broader medical-necessity case. Choose based on whether your concern is drinking water only or whole-home exposure."),
  ("Do RO replacement membranes qualify too?","They can, on the same medical-necessity basis as the system. Keep itemized receipts for each replacement, and retain your Letter of Medical Necessity."),
 ])

# ---------- Article #6 ----------
article(
 "water-filter-replacement-cartridges-fsa-eligible.html",
 "Are Replacement Water Filter Cartridges FSA Eligible?",
 "Replacement filter cartridges can be FSA/HSA eligible on the same medical-necessity basis as the system. Here is how to document recurring filter purchases.",
 "Replacement cartridge eligibility",
 "Are water filter replacement cartridges FSA eligible?",
 "Yes &mdash; replacement cartridges can be FSA/HSA eligible on the same basis as the filter system itself: they support an ongoing medical need documented by a Letter of Medical Necessity. The key is keeping your paperwork current.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; alongside a qualifying system.</b> Cartridges are the consumable that keeps a medically necessary filter working, so they can be reimbursed on the same Letter of Medical Necessity basis &mdash; with good record-keeping.</p>
  </div>

  <h2>The recurring-expense logic</h2>
  <p>If your filter qualifies as a medical expense, the replacements that keep it functioning follow the same logic under {IRS502}: they are part of maintaining the equipment that treats or prevents your condition. That means routine cartridge purchases can be reimbursable &mdash; but because they recur, documentation matters more than for a one-time buy.</p>

  <h2>How to keep recurring replacements eligible</h2>
  <ul>
    <li><strong>Keep the original Letter of Medical Necessity</strong> and note whether your plan or issuer requires periodic renewal (often annually). See <a href="guides/letter-of-medical-necessity-water-filter.html">how the LMN works</a>.</li>
    <li><strong>Save an itemized receipt for every replacement,</strong> showing it is a filter cartridge for your documented system.</li>
    <li><strong>Be ready to show continued need</strong> if your administrator asks &mdash; the condition that justified the filter should still apply.</li>
    <li><strong>Check submission rules</strong> with your plan; some accept card payments directly, others want receipts submitted. Our <a href="index.html#denied">guide to avoiding denied claims</a> covers the common pitfalls.</li>
  </ul>
  <div class="note tip"><span class="lab">Plan ahead with an HSA</span>Because replacements are ongoing, an <a href="are-water-filters-hsa-eligible.html">HSA</a> (which never expires) makes budgeting for them simpler than an FSA you must spend each year.</div>

  <h2>Lower-maintenance systems mean fewer claims</h2>
  <p>One practical tip: systems with long-life media need replacements far less often, which means less paperwork over time. A {iaff("whole-house","whole-house system")} with multi-year media is simpler to document than a filter needing frequent cartridge swaps. Compare options in our <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a> roundup.</p>

  <h2>How often will you actually replace cartridges?</h2>
  <p>Replacement frequency &mdash; and therefore how many reimbursement claims you file &mdash; depends heavily on the system type:</p>
  <ul>
    <li><strong>Pitcher and faucet filters:</strong> every 1&ndash;3 months. Cheap individually, but the most frequent paperwork.</li>
    <li><strong>Under-sink and RO:</strong> pre/post filters every 6&ndash;12 months; the RO membrane every 2&ndash;3 years.</li>
    <li><strong>Whole-house carbon tanks:</strong> the main media can last several years; often only an inexpensive sediment pre-filter is changed periodically.</li>
  </ul>
  <p>If minimizing both maintenance and claims matters to you, a whole-house tank system is the easiest to live with &mdash; see <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a>.</p>

  <h2>Build a simple documentation routine</h2>
  <p>Make reimbursement painless by treating it like any recurring medical expense. Keep one folder (digital is fine) holding your Letter of Medical Necessity and every itemized cartridge receipt. Note the date you bought each replacement and the system it serves. If your issuer requires periodic renewal of the letter, set a calendar reminder. When your administrator asks for proof &mdash; if they ever do &mdash; everything is in one place. Our guide to <a href="guides/letter-of-medical-necessity-water-filter.html">the Letter of Medical Necessity</a> explains renewal, and <a href="index.html#denied">avoiding a denied claim</a> covers submission rules.</p>

  <h2>FSA vs HSA for ongoing replacements</h2>
  <p>Because cartridges are a recurring cost, an <a href="are-water-filters-hsa-eligible.html">HSA</a> makes budgeting simpler &mdash; the balance never expires, so you can reimburse replacements whenever you buy them. With an <a href="are-water-filters-fsa-eligible.html">FSA</a>, plan to purchase a year's worth of replacements before your December 31 deadline so you do not forfeit funds that could have covered them.</p>
''',
 faq=[
  ("Are replacement filter cartridges FSA eligible?","They can be, on the same medical-necessity basis as the system they serve. Keep the Letter of Medical Necessity and an itemized receipt for each replacement."),
  ("Do I need a new letter for every replacement?","Not usually for each one, but issuers and plans may require periodic renewal (often annually) to confirm the ongoing need. Check your specific plan."),
  ("How do I prove a cartridge purchase is eligible?","Save an itemized receipt identifying the item as a replacement cartridge for your documented system, and retain your Letter of Medical Necessity alongside it."),
 ])

# ======================================================================
#  CLUSTER A (cont.) — Articles #7-#12
# ======================================================================

# ---------- Article #7 ----------
article(
 "are-shower-filters-fsa-hsa-eligible.html",
 "Are Shower Filters FSA/HSA Eligible? (2026 Guide)",
 "Shower filters can be FSA/HSA eligible with a Letter of Medical Necessity. Learn when they qualify, what they remove, and whole-home alternatives.",
 "Shower filter eligibility",
 "Are shower filters FSA/HSA eligible?",
 "Yes &mdash; a shower filter can be FSA/HSA eligible with a Letter of Medical Necessity, most often when a provider links chlorine or chloramine exposure to a skin or respiratory condition. Here is when it qualifies and when a whole-home system is the better buy.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> A shower filter qualifies when it addresses a documented health condition (commonly skin or respiratory sensitivity to disinfection by-products), not simply for softer-feeling water.</p>
  </div>

  <h2>The rule, applied to shower filters</h2>
  <p>Like any filter, a shower filter is not automatically reimbursable. It becomes a qualified medical expense only when a licensed provider documents that it treats, mitigates, or prevents a specific condition &mdash; the same standard described in our <a href="are-water-filters-fsa-eligible.html">FSA eligibility guide</a> and the <a href="index.html">complete pillar guide</a>. The provider issues a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>; you keep it with your receipt.</p>

  <h2>What shower filters actually do</h2>
  <p>Most shower filters target chlorine and, to varying degrees, chloramine and their by-products &mdash; the compounds some people associate with dry, irritated skin and aggravated eczema, and with airway irritation from inhaled steam. Effectiveness varies by media type and contact time, and a shower filter does nothing for what you drink. That is the key limitation that shapes both the health case and the smarter purchase.</p>

  <h2>The skin and respiratory angle</h2>
  <p>If you or a family member has a dermatological or respiratory condition that a clinician connects to chlorinated water, a shower filter is a reasonable, documentable part of managing it. As always, the provider &mdash; not you &mdash; decides medical necessity. General consumer-health context is available from the {CDC}, but eligibility rests on your clinician's judgment, not a blog's.</p>

  <h2>Shower filter vs whole-house: which to buy</h2>
  <p>A shower filter treats one shower head. A {iaff("whole-house","whole-house system")} treats every shower, tap, and appliance &mdash; so if your concern is chlorine exposure throughout the home, the whole-house route both solves the problem more completely and makes the broader medical-necessity case. Many readers find a single whole-house purchase is easier to justify and document than several point-of-use filters. See <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a> or compare the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a>.</p>

  <h2>How to document a shower filter claim</h2>
  <p>Secure the Letter of Medical Necessity dated on or before purchase, keep an itemized receipt, and retain any provider notes linking the filter to your condition. Replacement cartridges can be eligible on the same basis &mdash; see <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridge rules</a>. Confirm submission requirements with your plan administrator.</p>

  <h2>What to look for in a shower filter</h2>
  <p>If a shower filter is the right call, judge it on a few practical points: the media (KDF and catalytic carbon handle chlorine, and some chloramine, better than basic carbon), the flow rate so your pressure holds up, the replacement interval and cartridge cost, and credible testing claims. Be skeptical of vague "removes 99% of impurities" marketing with no specifics &mdash; look for named contaminants and, where possible, certification to recognized {NSF}.</p>

  <h2>Does a shower filter soften water?</h2>
  <p>No &mdash; this is a common mix-up. A shower filter reduces chlorine and some contaminants; it does not remove the calcium and magnesium that make water "hard." If hardness is your real concern, that is a softener question &mdash; see <a href="are-water-softeners-fsa-hsa-eligible.html">are water softeners FSA/HSA eligible?</a> Matching the device to the problem your provider documents keeps you from buying the wrong thing.</p>

  <h2>Shower filter vs whole-house: the cost picture</h2>
  <p>A shower filter is cheap upfront but relies on cartridges that need frequent replacement, and it protects only one shower. Across multiple bathrooms, or where the documented concern is whole-home chlorine exposure, the recurring cartridge cost of several shower filters can approach the price of a single low-maintenance {iaff("whole-house","whole-house system")} that treats every outlet for years. For an FSA/HSA buyer, one documented whole-house purchase is also simpler than repeated small claims.</p>
''',
 faq=[
  ("Is a shower filter a qualified medical expense?","It can be, with a Letter of Medical Necessity. The typical case is a skin or respiratory condition a provider links to chlorine or chloramine in the water supply."),
  ("Do I need a whole-house filter or just a shower filter?","A shower filter treats one shower; a whole-house system treats every tap and shower and makes a broader medical-necessity case. Choose based on whether your concern is one shower or whole-home exposure."),
  ("Are shower filter replacements eligible?","They can be, on the same medical-necessity basis as the filter. Keep an itemized receipt for each replacement and retain your Letter of Medical Necessity."),
 ])

# ---------- Article #8 ----------
article(
 "are-uv-water-purifiers-fsa-hsa-eligible.html",
 "Are UV Water Purifiers FSA/HSA Eligible? (2026)",
 "UV water purifiers can be FSA/HSA eligible with a Letter of Medical Necessity, a strong case for well water and immunocompromised households. Here is how.",
 "UV purifier eligibility",
 "Are UV water purifiers FSA/HSA eligible?",
 "Yes &mdash; a UV water purifier can be FSA/HSA eligible with a Letter of Medical Necessity, and it is one of the strongest medical-necessity cases of all because it targets disease-causing microbes, especially in well water and for immunocompromised households.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> Because UV inactivates bacteria, viruses, and other pathogens, its purpose is inherently health-related &mdash; a clean fit for the medical-necessity standard.</p>
  </div>

  <h2>What a UV purifier does (and doesn't do)</h2>
  <p>A UV system passes water past an ultraviolet lamp that inactivates microorganisms so they cannot reproduce or cause illness. It is highly effective against bacteria, viruses, and protozoa such as those that worry well owners. Crucially, UV does <strong>not</strong> remove chemicals, sediment, or hardness &mdash; so it is normally paired with a filter that clears particles first (UV needs clear water to work). That pairing matters when you plan your purchase and your documentation.</p>

  <h2>Why UV has a strong eligibility case</h2>
  <p>Eligibility hinges on a health rationale, and disinfection is about as health-related as filtration gets. The {CDC} highlights that some people &mdash; including those who are immunocompromised &mdash; face higher risk from waterborne pathogens, and private wells are not treated by any municipal system. For these households, a provider can readily connect UV treatment to preventing illness, which supports the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>Who should consider UV</h2>
  <ul>
    <li><strong>Well-water households</strong> &mdash; no central disinfection means you own microbial safety yourself.</li>
    <li><strong>Immunocompromised members</strong> &mdash; chemotherapy patients, transplant recipients, and others advised to minimize pathogen exposure.</li>
    <li><strong>After a boil-water history or positive bacteria test</strong> &mdash; a documented reason that strengthens the case.</li>
  </ul>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Bacteria / well add-on</span>
    <h3>SpringWell UV Purification System</h3>
    <p>Inactivates bacteria and other microbes &mdash; commonly paired with a well-water filter for complete treatment. Runs through the TrueMed HSA/FSA checkout.</p>
    {aff("uv","Check price","btn")}
  </div>

  <h2>Pair UV with the right pre-filtration</h2>
  <p>Since UV needs clear water, well households usually combine it with a {iaff("well-water","whole-house well filter")} that handles iron, sulfur, and sediment first. You can document both as part of one medically necessary treatment train. For city homes worried about whole-home exposure, see <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a>; for the underlying rules, the <a href="index.html">pillar guide</a> covers everything.</p>

  <h2>Documentation notes</h2>
  <p>Get the Letter of Medical Necessity before purchase, keep itemized receipts (including for replacement UV lamps, which qualify on the same basis &mdash; see <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement eligibility</a>), and confirm your plan's submission rules.</p>

  <h2>UV vs other ways to make water safe</h2>
  <p>Compared with boiling (impractical for whole-home use) or chemical disinfection like chlorine bleach (which adds taste and by-products), UV inactivates pathogens continuously, with no chemicals and no change to taste or odor. That makes it the preferred point-of-entry disinfection method for private wells. It is not a filter, though &mdash; it leaves dissolved chemicals and particles in place, which is why it sits at the end of a treatment train, after sediment and carbon stages.</p>

  <h2>UV maintenance to budget for</h2>
  <p>UV systems are low-effort but not zero: the lamp loses output and is typically replaced about once a year, the quartz sleeve needs occasional cleaning, and the upstream pre-filter must be changed so the water stays clear enough for the light to work. These replacements can be reimbursed on the same medical-necessity basis as the system &mdash; keep itemized receipts and your <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>Do city homes need UV?</h2>
  <p>Usually not for routine disinfection, because municipal utilities already disinfect. UV makes the strongest sense for well water and for immunocompromised households wanting an extra barrier against pathogens. If your concern on city water is chemicals rather than microbes, a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house carbon system</a> or <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> is the better fit. Compare complete configurations in the <a href="best-fsa-hsa-eligible-water-filters.html">eligible systems roundup</a>.</p>
''',
 faq=[
  ("Is a UV water purifier FSA/HSA eligible?","It can be, with a Letter of Medical Necessity. Because UV exists to inactivate disease-causing microbes, it is one of the clearest medical-necessity cases among water-treatment devices."),
  ("Does UV replace a filter?","No. UV disinfects but does not remove chemicals, sediment, or hardness, and it needs clear water to work. It is typically paired with a filter, especially on well water."),
  ("Are replacement UV lamps eligible?","They can be, on the same basis as the system. UV lamps are replaced roughly annually; keep itemized receipts and your Letter of Medical Necessity."),
 ])

# ---------- Article #9 ----------
article(
 "is-bottled-water-fsa-hsa-eligible.html",
 "Is Bottled Water FSA/HSA Eligible? (The Honest Answer)",
 "Bottled water is generally not FSA/HSA eligible; it is a personal expense. A water filter can be, with a Letter of Medical Necessity. Here is the difference.",
 "Bottled water eligibility",
 "Is bottled water FSA/HSA eligible?",
 "Generally no &mdash; everyday bottled water is treated as a personal expense and is not FSA/HSA eligible. But a water filter can be, with a Letter of Medical Necessity &mdash; and over time it is far cheaper. Here is the honest breakdown.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Usually not eligible.</b> Ordinary bottled water is a personal grocery expense. Eligibility would require a narrow, provider-documented medical reason &mdash; and even then, a filter is the more practical, reimbursable solution.</p>
  </div>

  <h2>Why bottled water generally isn't eligible</h2>
  <p>Under {IRS502}, a qualified medical expense must be primarily for treating or preventing a condition &mdash; not a substitute for ordinary food and drink. Bottled water is normally considered a personal expense, like groceries, so it does not qualify on its own. Buying it because you prefer the taste or convenience is precisely the kind of personal spending FSA/HSA rules exclude.</p>

  <h2>The narrow exceptions</h2>
  <p>There are uncommon situations where a provider documents a specific medical need for a particular type of water. These are case-by-case, determined by a licensed provider, and confirmed by your plan administrator &mdash; not something to assume. If you think your situation is unusual, ask your provider directly rather than relying on general guidance.</p>

  <h2>The smarter move: a filter you can actually reimburse</h2>
  <p>Here is the part that helps your wallet. If your concern is contaminants &mdash; lead, PFAS, nitrates &mdash; a filter addresses the same worry that drives people to bottled water, can be <a href="are-water-filters-fsa-eligible.html">FSA/HSA eligible with a Letter of Medical Necessity</a>, and costs dramatically less over time. A household spending $30&ndash;$60 a month on bottled water spends $360&ndash;$720 a year; a one-time filter purchase made with pre-tax dollars often pays for itself quickly while removing the plastic waste.</p>
  <div class="note tip"><span class="lab">Run the numbers</span>Compare your annual bottled-water spend against a one-time, pre-tax filter purchase &mdash; see how the <a href="index.html#savings">tax-savings math</a> works on our main guide.</div>

  <h2>Which filter replaces bottled water best?</h2>
  <p>For drinking and cooking water specifically, an under-sink {iaff("moen-ro","reverse osmosis system")} delivers bottled-quality water at the tap &mdash; see <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>. For whole-home peace of mind, a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> treats every tap. Either is a durable, eligible alternative to an ongoing bottled-water habit.</p>

  <h2>Bottled water vs a filter: the five-year cost</h2>
  <p>The case against bottled water is mostly arithmetic. A household going through a few cases a month commonly spends $360&ndash;$720 a year &mdash; $1,800&ndash;$3,600 over five years &mdash; on water that is often just filtered tap water. A one-time filter purchase, ideally made with pre-tax HSA/FSA dollars, typically costs less than that five-year total and keeps working afterward. You convert a recurring, non-eligible grocery cost into a one-time, potentially eligible medical-device purchase.</p>

  <h2>The practical and environmental downsides</h2>
  <p>Beyond cost, bottled water means hauling, storage, and plastic waste, plus uncertainty about quality &mdash; bottled is not inherently safer than well-chosen home filtration. For most households worried about a specific contaminant, treating water at the source is both more reliable and more economical.</p>

  <h2>When bottled water is a reasonable stopgap</h2>
  <p>There are short-term situations &mdash; a boil-water advisory, a pending well test, or a newly discovered contaminant &mdash; where bottled water bridges the gap until a filter is installed. That is sensible as a temporary measure; it just is not a long-term, FSA/HSA-friendly solution. The durable, eligible answer is a documented filtration device &mdash; see <a href="are-water-filters-fsa-eligible.html">how filters qualify</a>.</p>
''',
 faq=[
  ("Can I use my FSA or HSA to buy bottled water?","Generally no. Everyday bottled water is a personal expense and is not a qualified medical expense. Only a narrow, provider-documented medical situation could change that."),
  ("Is a water filter a better FSA/HSA buy than bottled water?","Usually yes. A filter can be eligible with a Letter of Medical Necessity, costs far less over time than ongoing bottled water, and addresses contaminants at the source."),
  ("What if my doctor recommends a specific water?","Then discuss documentation with your provider and confirm with your plan administrator. Eligibility for any water purchase is determined case-by-case, not assumed."),
 ])

# ---------- Article #10 ----------
article(
 "are-water-test-kits-fsa-hsa-eligible.html",
 "Are Water Test Kits FSA/HSA Eligible? (2026)",
 "Water test kits may be FSA/HSA eligible with a Letter of Medical Necessity, and testing is the smart first step before buying a filter. Here is what to know.",
 "Water test kit eligibility",
 "Are water test kits FSA/HSA eligible?",
 "Possibly &mdash; a water test kit can be FSA/HSA eligible with a Letter of Medical Necessity when it is part of diagnosing a water-related health risk. Either way, testing first is the smartest move you can make before buying any filter.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Potentially eligible &mdash; and strategically essential.</b> A test kit can qualify with a Letter of Medical Necessity as part of identifying a health risk, and the results strengthen the documentation behind whatever filter you buy next.</p>
  </div>

  <h2>Why testing comes first</h2>
  <p>You cannot fix what you have not measured. A water test tells you exactly which contaminants you face &mdash; lead, nitrates, bacteria, hardness, PFAS &mdash; which determines both the right system and the strength of your medical-necessity case. Buying a filter without testing risks over- or under-treating. The {EPALEAD} and your utility's annual Consumer Confidence Report are good starting points for city water; private wells need direct testing because no one tests them for you.</p>

  <h2>The eligibility angle</h2>
  <p>A test kit used to identify a water-related health hazard can fit the medical-necessity framework when a provider documents it, much like other diagnostic items. As with every purchase on this site, a licensed provider issues the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> and your plan administrator confirms coverage. Even where a kit is inexpensive enough that you simply pay out of pocket, the results are valuable: a documented lead or nitrate result is powerful support for the filter purchase that follows.</p>

  <h2>What to test for</h2>
  <ul>
    <li><strong>City water:</strong> lead (especially older homes), chlorine/chloramine by-products, and anything flagged in your CCR.</li>
    <li><strong>Well water:</strong> bacteria and nitrates (health-critical), plus iron, manganese, sulfur, hardness, and pH.</li>
  </ul>
  <p>See <a href="index.html#water-type">city vs well water</a> for how the source changes what you should look for.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Test first</span>
    <h3>SpringWell Water Test Kit</h3>
    <p>Identify what is actually in your water before you buy a system &mdash; the results guide your choice and support your documentation.</p>
    {aff("test-kit","Check the test kit","btn")}
  </div>

  <h2>From results to the right system</h2>
  <p>Once you know your contaminants, match them to a system: lead and cysts or PFAS point to specific <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house options</a>; bacteria points to <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV</a>; drinking-water concerns suit <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a>. Compare everything in the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a> roundup.</p>

  <h2>Types of water test kits</h2>
  <ul>
    <li><strong>Test strips</strong> &mdash; cheapest and fastest for a quick read on hardness, chlorine, pH, nitrates, and lead presence; good for a first screen.</li>
    <li><strong>Mail-in lab tests</strong> &mdash; you collect a sample and a certified lab returns detailed, quantified results; the most reliable, and the most useful for documentation.</li>
    <li><strong>Digital meters</strong> &mdash; handy for ongoing checks of total dissolved solids (TDS) once you know your baseline.</li>
  </ul>
  <p>For a purchase you intend to support with a medical-necessity case, a certified lab result carries the most weight.</p>

  <h2>How to read your results</h2>
  <p>Compare each measured contaminant against recognized limits &mdash; for example, the {EPALEAD} action level for lead, or nitrate limits that matter most for infants and pregnant women. Flag anything at or above a health-based threshold; those are the results that both justify a filter and tell you which system you need.</p>

  <h2>What to do after testing</h2>
  <p>Turn results into action: bring a health-relevant finding to your provider for the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, then match the contaminant to a system. Retest well water at least annually (and after any change in taste, color, or odor, or nearby flooding); city households can lean on the yearly Consumer Confidence Report but should still test at the tap for lead in older homes, since pipes vary house to house.</p>
''',
 faq=[
  ("Are water test kits FSA/HSA eligible?","They can be, with a Letter of Medical Necessity, when used to identify a water-related health risk. Confirm with your plan administrator, as treatment of diagnostic items varies."),
  ("Should I test my water before buying a filter?","Yes. Testing identifies your actual contaminants, which determines the right system and strengthens the medical-necessity documentation for your purchase."),
  ("What should well owners test for?","At minimum bacteria and nitrates, which are health-critical, plus iron, manganese, sulfur, hardness, and pH. Private wells are not tested by any utility."),
 ])

# ---------- Article #11 ----------
article(
 "is-distilled-purified-water-fsa-eligible.html",
 "Is Distilled or Purified Water FSA Eligible? (2026)",
 "Distilled and purified water are usually personal expenses, not FSA eligible. But a water filter can be, with a Letter of Medical Necessity. Here is the rule.",
 "Distilled / purified water eligibility",
 "Is distilled or purified water FSA eligible?",
 "Usually no &mdash; distilled and purified water are generally personal expenses, not FSA eligible, unless a provider documents a specific medical need. A home filtration or reverse-osmosis system, however, can be eligible with a Letter of Medical Necessity.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Generally not eligible.</b> Store-bought distilled or purified water is treated like ordinary bottled water &mdash; a personal expense. A filtration system that produces clean water at home is the eligible route, with a Letter of Medical Necessity.</p>
  </div>

  <h2>Distilled vs purified: a quick definition</h2>
  <p>"Purified" water has been treated to remove contaminants to a defined purity (often by reverse osmosis, deionization, or distillation). "Distilled" water is one type of purified water, boiled to steam and recondensed, leaving minerals behind. Both describe the <em>water</em> &mdash; a consumable &mdash; rather than a medical device.</p>

  <h2>Why they're usually not FSA eligible</h2>
  <p>Because they are consumable drinking water, distilled and purified water sit in the same category as <a href="is-bottled-water-fsa-hsa-eligible.html">bottled water</a>: a personal grocery expense under {IRS502}, not a qualified medical expense. Buying jugs of distilled water for convenience does not qualify. Narrow medical exceptions exist but must be documented by a provider and confirmed by your plan &mdash; never assumed.</p>

  <h2>The eligible alternative: make purified water at home</h2>
  <p>If you want purified water for health reasons, the device that produces it can be the qualified expense. An under-sink {iaff("moen-ro","reverse osmosis system")} produces purified-grade drinking water on demand and can be <a href="is-reverse-osmosis-fsa-hsa-eligible.html">FSA/HSA eligible with a Letter of Medical Necessity</a> &mdash; far cheaper over time than buying jugs, and it removes the recurring cost and plastic waste. For whole-home needs, see <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a>.</p>
  <div class="note tip"><span class="lab">The pattern to remember</span>The <em>water</em> is usually personal; the <em>device</em> that treats it can be medical. That distinction runs through our entire <a href="index.html">eligibility guide</a>.</div>

  <h2>Is distilled water ever medically necessary?</h2>
  <p>Occasionally a provider recommends distilled water for a specific device or condition &mdash; some medical equipment manufacturers specify it, for instance. Whether that makes a purchase reimbursable is a case-by-case determination by your provider and plan administrator, and it does not generalize to everyday drinking water. When in doubt, ask rather than assume.</p>

  <h2>Distilled vs reverse osmosis vs spring water</h2>
  <p>Distillation and reverse osmosis both produce very low-mineral, high-purity water; RO does it on demand at the tap without boiling, which is why a home {iaff("moen-ro","RO system")} is the practical eligible route to purified water. Spring water, by contrast, is simply bottled source water &mdash; a personal expense like any other bottled product.</p>

  <h2>The cost of buying vs making purified water</h2>
  <p>Buying jugs of distilled or purified water is an ongoing, non-eligible cost; an at-home RO system is a one-time, potentially eligible purchase that produces comparable water for pennies per gallon afterward. Over a few years the home system is almost always cheaper &mdash; see the <a href="index.html#savings">savings math</a> and <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</p>

  <h2>The bottom line</h2>
  <p>Treat store-bought distilled or purified water as a personal grocery expense, and treat the device that purifies water at home as the potentially eligible medical purchase. If purity matters for a documented reason, put your pre-tax dollars toward the equipment, not the jugs.</p>
''',
 faq=[
  ("Is distilled water FSA eligible?","Generally no. Distilled water is a consumable personal expense, like bottled water, unless a provider documents a specific medical need and your plan confirms it."),
  ("Is purified water HSA eligible?","Usually not on its own. Purified water is treated as a personal grocery expense. A device that purifies water at home can be eligible with a Letter of Medical Necessity."),
  ("What's the eligible way to get purified water?","A home reverse-osmosis or filtration system can qualify with a Letter of Medical Necessity, produces purified-grade water on demand, and costs far less over time than buying water."),
 ])

# ---------- Article #12 (HUB) ----------
article(
 "fsa-hsa-eligible-water-filters-list.html",
 "FSA/HSA Eligible Water Filters: Complete 2026 List",
 "A complete, honest list of which water filtration items are FSA/HSA eligible, what each requires, and how to buy them with pre-tax dollars.",
 "Eligible water-items list",
 "FSA/HSA eligible water filters: the complete list",
 "Use this master list to see, at a glance, which water-treatment items can be FSA/HSA eligible, which need a Letter of Medical Necessity, and where to learn more about each. The honest one-line summary: most filtration can qualify with an LMN; consumable water generally cannot.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The common thread</p>
    <p class="ruling"><b>Devices that treat water can be eligible; consumable water usually cannot.</b> Nearly every filtration <em>device</em> qualifies with a Letter of Medical Necessity, while bottled, distilled, and purified <em>water</em> are personal expenses.</p>
  </div>

  <p>This page is the quick-reference hub for the whole eligibility cluster. Each row links to a full guide. For the underlying IRS framing &mdash; {IRS502} and {IRS969} &mdash; and the buying process, start with our <a href="index.html">complete eligibility guide</a>.</p>

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Water-related item</th><th>FSA/HSA eligible?</th><th>Needs LMN?</th><th>Learn more</th></tr></thead>
    <tbody>
      <tr><td>Whole-house filtration system</td><td class="yes">Yes</td><td>Yes</td><td><a href="whole-house-water-filtration-hsa-fsa-eligible.html">Whole-house guide</a></td></tr>
      <tr><td>Under-sink / reverse osmosis</td><td class="yes">Yes</td><td>Yes</td><td><a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO guide</a></td></tr>
      <tr><td>UV purifier</td><td class="yes">Yes</td><td>Yes</td><td><a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV guide</a></td></tr>
      <tr><td>Shower filter</td><td class="yes">Yes</td><td>Yes</td><td><a href="are-shower-filters-fsa-hsa-eligible.html">Shower filter guide</a></td></tr>
      <tr><td>Water softener (alone)</td><td>Conditional</td><td>Yes</td><td><a href="are-water-softeners-fsa-hsa-eligible.html">Softener guide</a></td></tr>
      <tr><td>Filter + softener combo</td><td class="yes">Yes</td><td>Yes</td><td><a href="reviews/springwell-filter-softener-combo-review.html">Combo review</a></td></tr>
      <tr><td>Replacement cartridges / membranes</td><td class="yes">Yes</td><td>Yes*</td><td><a href="water-filter-replacement-cartridges-fsa-eligible.html">Replacements guide</a></td></tr>
      <tr><td>Water test kit</td><td>Conditional</td><td>Often</td><td><a href="are-water-test-kits-fsa-hsa-eligible.html">Test kit guide</a></td></tr>
      <tr><td>Bottled water</td><td class="no">Usually no</td><td>n/a</td><td><a href="is-bottled-water-fsa-hsa-eligible.html">Bottled water guide</a></td></tr>
      <tr><td>Distilled / purified water</td><td class="no">Usually no</td><td>n/a</td><td><a href="is-distilled-purified-water-fsa-eligible.html">Distilled water guide</a></td></tr>
    </tbody>
  </table>
  </div>
  <p class="updated">*Replacements use the original system's Letter of Medical Necessity; some plans require periodic renewal.</p>

  <h2>Devices that are eligible (with a Letter of Medical Necessity)</h2>
  <p>The whole category of filtration <strong>equipment</strong> can qualify when a provider documents a health reason. <a href="whole-house-water-filtration-hsa-fsa-eligible.html">Whole-house systems</a> make the broadest case because they reduce exposure everywhere; <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> targets drinking water; <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV</a> handles microbes; and <a href="are-shower-filters-fsa-hsa-eligible.html">shower filters</a> address chlorine for skin and respiratory concerns. The <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems roundup</a> compares the leading options.</p>

  <h2>The conditional cases</h2>
  <p><a href="are-water-softeners-fsa-hsa-eligible.html">Softeners</a> are harder to justify alone because hardness is often a comfort issue, though combos and documented health needs change that. <a href="are-water-test-kits-fsa-hsa-eligible.html">Test kits</a> can qualify as part of identifying a hazard &mdash; and testing first is wise regardless.</p>

  <h2>What's generally not eligible</h2>
  <p>Consumable water &mdash; <a href="is-bottled-water-fsa-hsa-eligible.html">bottled</a>, <a href="is-distilled-purified-water-fsa-eligible.html">distilled, or purified</a> &mdash; is treated as a personal expense. The eligible move is to buy the device that produces clean water at home, not the water itself.</p>

  <h2>The one rule behind every row</h2>
  <p>Eligibility is never automatic. It comes from documented medical necessity &mdash; a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> from a licensed provider &mdash; confirmed by your plan administrator. Whether you use an <a href="are-water-filters-hsa-eligible.html">HSA</a> or an <a href="are-water-filters-fsa-eligible.html">FSA</a>, that is the key that unlocks pre-tax savings. Ready to act? See <a href="index.html#how">how to buy with pre-tax dollars</a>.</p>

  <h2>How to use this list (the buyer's path)</h2>
  <p>The table answers "is it eligible?" but the more useful question is "what do I do?" Here is the path most readers follow, in order:</p>
  <ol class="steps">
    <li><h4>Test your water</h4><p>Identify the actual contaminant before spending anything &mdash; see <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a> and <a href="index.html#water-type">city vs well water</a>.</p></li>
    <li><h4>Match a device to the result</h4><p>Use the table above to pick the system type that targets your contaminant.</p></li>
    <li><h4>Get the Letter of Medical Necessity</h4><p>A licensed provider documents the health need &mdash; see <a href="guides/letter-of-medical-necessity-water-filter.html">how the LMN works</a>.</p></li>
    <li><h4>Buy with your HSA/FSA card and keep records</h4><p>Pay, then store the letter and itemized receipt together.</p></li>
  </ol>

  <h2>How eligibility is actually decided</h2>
  <p>Three parties shape every eligible purchase. A <strong>licensed provider</strong> determines medical necessity and issues the letter. Your <strong>plan administrator</strong> confirms what the plan accepts and how to submit. And the <strong>IRS framework</strong> &mdash; {IRS502} and {IRS969} &mdash; sets the underlying rules. No website replaces those parties, including this one; we explain the pattern so you know what to ask. It is also why over-claiming is risky: an administrator can deny or reverse a purchase that lacks proper documentation.</p>

  <h2>HSA or FSA for these purchases?</h2>
  <p>Either works, with the same medical-necessity requirement. An <a href="are-water-filters-hsa-eligible.html">HSA</a> rolls over and suits larger or recurring purchases; an <a href="are-water-filters-fsa-eligible.html">FSA</a> often expires December 31, which makes a qualifying filter a smart way to use a balance you would otherwise forfeit. The pillar compares <a href="index.html#accounts">all four account types</a>.</p>

  <h2>Which device should most people choose?</h2>
  <p>If you want one recommendation that fits the most situations, a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> treats every tap with the lowest ongoing maintenance and the broadest medical-necessity case. Budget or renting? An under-sink <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> unit is the affordable, drinking-water-focused choice. Well water with bacteria? Add <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV</a>. The <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems roundup</a> compares them head to head.</p>

  <h2>Frequently confused: device vs consumable</h2>
  <p>The single most common eligibility mistake is treating the <em>water</em> and the <em>device</em> the same way. Buying jugs of purified water, cases of bottled water, or refill deliveries is consumable spending &mdash; personal, not medical. Buying equipment that filters, purifies, or disinfects your water can be medical, with documentation. When you scan the table above, that line &mdash; equipment versus consumable &mdash; explains almost every "yes" and "no" on it. Bookmark this page as your starting point; from here you can reach every detailed guide, the buying process, and the product comparisons.</p>
''',
 faq=[
  ("What water items are FSA/HSA eligible?","Most filtration devices can be, with a Letter of Medical Necessity: whole-house, reverse osmosis, UV, shower filters, combos, and their replacement parts. Consumable water (bottled, distilled, purified) generally is not."),
  ("Does everything need a Letter of Medical Necessity?","Eligible devices do. The letter, from a licensed provider, is what turns a personal purchase into a qualified medical expense. Your plan administrator confirms coverage."),
  ("What is never eligible?","Ordinary bottled, distilled, or purified water is treated as a personal expense. Buying the device that treats water at home is the eligible alternative."),
 ])

# ======================================================================
#  CLUSTER B — Process / LMN / TrueMed (Articles #14-#18)
# ======================================================================

# ---------- Article #14 ----------
article(
 "how-to-buy-water-filter-with-hsa-fsa.html",
 "How to Buy a Water Filter With Your HSA/FSA (Step-by-Step)",
 "Step-by-step: how to buy a water filter with HSA/FSA dollars using a Letter of Medical Necessity and TrueMed checkout \u2014 what to prepare, pay, and keep.",
 "How to buy with HSA/FSA",
 "How to buy a water filter with your HSA/FSA",
 "Here is the exact, step-by-step process for buying a water filter with pre-tax HSA or FSA dollars &mdash; from confirming your need to paying at checkout and keeping the right records so the purchase sticks.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The short version</p>
    <p class="ruling"><b>Get a Letter of Medical Necessity, then pay with your HSA/FSA card.</b> The cleanest path is a retailer that issues the letter at checkout &mdash; you answer a short survey, a provider approves it, and you pay. Keep the letter and receipt.</p>
  </div>

  <p>If you have read that water filters are HSA/FSA eligible and wondered "okay, but how do I actually do it?", this is the page for you. The reason it feels confusing is that you cannot simply swipe your benefits card for a whole-house filter the way you would for cough syrup &mdash; you need documentation first. Done in the right order, the whole thing takes minutes. (For the underlying rules, see our <a href="index.html">complete eligibility guide</a>.)</p>

  <h2>Step by step</h2>
  <ol class="steps">
    <li><h4>Test your water (or pull your report)</h4><p>Know what you are treating. City users can read the annual Consumer Confidence Report; well users should lab-test. A documented contaminant strengthens your case &mdash; see <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>.</p></li>
    <li><h4>Choose the right system</h4><p>Match the contaminant to the system: <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house</a> for broad coverage, <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> for drinking water, <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV</a> for bacteria. Compare options in the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a> roundup.</p></li>
    <li><h4>Select "Pay with HSA/FSA" at checkout</h4><p>On an eligible SpringWell system, choose the TrueMed option. This starts the Letter of Medical Necessity process automatically &mdash; see <a href="how-truemed-works-for-water-filters.html">how TrueMed works</a>.</p></li>
    <li><h4>Complete the short health survey</h4><p>A couple of confidential minutes. A licensed provider reviews your answers and, if you qualify, issues your <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> &mdash; often within a few hours.</p></li>
    <li><h4>Pay with your HSA/FSA card</h4><p>Enter your benefits card like a debit card. If your balance is short, split the payment with a regular card (more below).</p></li>
    <li><h4>Save your documentation</h4><p>Download the letter and itemized receipt into one folder in case your administrator asks. That is your proof the purchase qualified.</p></li>
  </ol>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Do it now</span>
    <h3>Start your eligibility check</h3>
    <p>SpringWell's eligible systems run the entire Letter-of-Medical-Necessity step inside checkout through TrueMed &mdash; the simplest way to keep your timing and paperwork correct.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
    &nbsp;{aff("truemed-how-it-works","See how it works","btn ghost")}
  </div>

  <h2>What to have ready before you start</h2>
  <ul>
    <li>Your <strong>HSA/FSA card</strong> (or account login for reimbursement).</li>
    <li>A sense of your <strong>contaminant concern</strong> &mdash; even a general one helps the survey.</li>
    <li>Your <strong>balance and deadline</strong> &mdash; check whether an FSA balance expires this year.</li>
    <li>A <strong>backup card</strong> if the system costs more than your balance.</li>
  </ul>

  <h2>What if you do not have enough in your account?</h2>
  <p>This is common with whole-house systems, which can exceed a single year's FSA limit. You have two clean options: split the payment (pay what your HSA/FSA card covers, put the rest on a regular card), or pay out of pocket and reimburse yourself later from an <a href="are-water-filters-hsa-eligible.html">HSA</a> once funds are available. Either way, keep the qualified portion clearly documented &mdash; see <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">how reimbursement works</a>.</p>

  <h2>Timing and the year-end deadline</h2>
  <p>Two timing rules matter. First, the Letter of Medical Necessity must be dated on or before your purchase &mdash; never after. Second, most <a href="are-water-filters-fsa-eligible.html">FSAs</a> follow use-it-or-lose-it and expire December 31, so if you are spending an FSA balance, do not leave it to the last day; allow time for the survey and letter to process. Worried about rejection? Our guide to <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">avoiding a denied claim</a> covers the pitfalls.</p>

  <h2>A 60-second readiness check</h2>
  <p>Before you start, run through this quickly: Do you know roughly what is in your water? Do you know your balance and whether it expires? Have you picked the system type that matches your concern? Do you have a backup card if the cost exceeds your balance? If you can answer yes to those four, the checkout itself takes only minutes. If not, the slowest part is usually testing &mdash; so order a <a href="are-water-test-kits-fsa-hsa-eligible.html">test kit</a> early.</p>

  <h2>Worked example: buying a whole-house system with an HSA</h2>
  <p>Imagine you are in a 30% combined bracket and choose a $2,000 whole-house system. You select the HSA/FSA option at checkout, complete the survey, and receive your letter within a few hours. You pay the full $2,000 with your HSA card. Because that money was set aside pre-tax, you effectively avoid roughly $600 in tax &mdash; a real cost near $1,400. You download the letter and receipt, and you are done. See the full <a href="index.html#savings">savings math</a> for how the discount scales with your bracket.</p>

  <h2>City water vs well water: what to buy</h2>
  <p>Your source shapes the purchase. On <strong>city water</strong>, a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house carbon system</a> handles chlorine and taste, with a dedicated unit where lead is a concern. On <strong>well water</strong>, you own treatment entirely &mdash; often a well filter for iron and sulfur plus <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV</a> for bacteria. The <a href="index.html#water-type">city vs well</a> section explains how to choose.</p>

  <h2>After you buy: maintenance and replacements</h2>
  <p>Once installed, budget for replacement filters &mdash; which can be reimbursed on the same basis as the system. Keep each receipt and renew your letter when required; see <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridge eligibility</a>. Low-maintenance whole-house systems minimize both upkeep and paperwork over time.</p>
''',
 faq=[
  ("Can I buy a water filter directly with my FSA/HSA card?","Not reliably without a Letter of Medical Necessity. The cleanest method is a checkout that issues the letter first (like SpringWell via TrueMed), then you pay with your card."),
  ("How long does the whole process take?","Often a few hours. The health survey takes minutes; the provider review and Letter of Medical Necessity are commonly issued the same day."),
  ("What if my filter costs more than my balance?","Split the payment between your HSA/FSA card and a regular card, or pay out of pocket and reimburse later from an HSA. Document the qualified portion."),
  ("Do I need to do this every year?","Only if you reimburse recurring replacement filters, which may require a renewed letter. The system purchase itself is a one-time event."),
 ])

# ---------- Article #15 ----------
article(
 "how-truemed-works-for-water-filters.html",
 "How TrueMed Works for Water Filters (Full Walkthrough)",
 "TrueMed lets you buy a water filter with HSA/FSA money via a Letter of Medical Necessity. Here is how it works, what it costs, and whether it is legitimate.",
 "How TrueMed works",
 "How TrueMed works for water filters",
 "TrueMed is the service that turns 'is this eligible?' into 'here is your Letter of Medical Necessity, pay with your card.' This walkthrough explains exactly how it works for a water filter, what it costs you, and why it is a legitimate, compliant process.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">In a sentence</p>
    <p class="ruling"><b>TrueMed connects you to a licensed provider who issues a Letter of Medical Necessity at checkout,</b> so you can pay for an eligible water filter with HSA/FSA funds &mdash; without a separate doctor visit.</p>
  </div>

  <h2>What TrueMed is</h2>
  <p>TrueMed is a health-tech company that partners with retailers to let customers use HSA/FSA dollars on qualifying health-related products. It is not a filter brand and not your bank &mdash; it is the bridge that handles the medical-necessity step the IRS requires. When a retailer like SpringWell offers "Pay with HSA/FSA," TrueMed is usually the mechanism behind it. For the eligibility framework itself, see {IRS502} and {IRS969}.</p>

  <h2>How it works, step by step</h2>
  <ol class="steps">
    <li><h4>You choose the HSA/FSA option at checkout</h4><p>On an eligible product, you select TrueMed instead of a standard payment.</p></li>
    <li><h4>You answer a short health survey</h4><p>A few confidential questions about your situation &mdash; the basis for the medical-necessity determination.</p></li>
    <li><h4>A licensed provider reviews it</h4><p>An independent, licensed provider assesses whether your circumstances support a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p></li>
    <li><h4>You receive the letter and pay</h4><p>If you qualify, the LMN is issued (often within hours) and you pay with your HSA/FSA card. You keep the letter and receipt.</p></li>
  </ol>

  <h2>What it costs you</h2>
  <p>When you buy through a partner retailer, the Letter of Medical Necessity is typically provided at no separate charge to you &mdash; the cost is handled through the retailer relationship. You pay the product's normal price, simply using pre-tax dollars. That is the whole appeal: the same system, discounted by your tax rate, with the paperwork handled.</p>

  <h2>Is TrueMed legitimate and compliant?</h2>
  <p>Yes &mdash; the model is built around the same rules that govern any qualified medical expense. The key compliance points are that a real licensed provider makes the determination, the letter is dated on or before purchase, and you retain documentation for your plan administrator. TrueMed does not override your plan's rules; your administrator still has the final say on reimbursement, which is why keeping records matters. If a claim is ever questioned, see <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">how to avoid (and handle) a denial</a>.</p>
  <div class="note warn"><span class="lab">US only</span>TrueMed and U.S. HSA/FSA accounts are available in the United States only.</div>

  <h2>Which SpringWell products use it</h2>
  <p>SpringWell offers the TrueMed route across its eligible range &mdash; whole-house filters, filter + softener combos, well-water systems, UV, and under-sink reverse osmosis. Match the system to your need using the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a> comparison, then start the process at checkout.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} See it in action</span>
    <h3>Check your eligibility through TrueMed</h3>
    <p>Browse SpringWell's eligible systems and complete the short survey to see whether you qualify for a Letter of Medical Necessity.</p>
    {aff("truemed-how-it-works","See how it works","btn")}
    &nbsp;{aff("truemed-eligible-category","Shop eligible systems","btn ghost")}
  </div>

  <h2>What the health survey asks</h2>
  <p>The survey is short and focuses on whether filtration is reasonably connected to a health need &mdash; for example, questions about household members, relevant conditions, and water-quality concerns. It is not an exhaustive medical exam; it gives the reviewing provider enough to make a determination. Answer honestly and specifically &mdash; a documented contaminant or a vulnerable household member (a child, someone pregnant, an immunocompromised member) makes the case clearer.</p>

  <h2>What happens if you do not qualify</h2>
  <p>If the provider decides your situation does not support a Letter of Medical Necessity, you simply do not use HSA/FSA funds for that purchase &mdash; you can still buy the system with regular money. You have lost nothing but a few minutes, and there is no penalty for completing the survey. This is also why you should never self-certify or overstate your situation: the provider's independent judgment is part of what keeps the process compliant.</p>

  <h2>TrueMed and your privacy</h2>
  <p>Because the survey involves health information, treat it like any other medical interaction: provide accurate details, and keep your issued letter in a secure place with your purchase records. The letter is the document your plan administrator may ask to see, so storing it safely protects both your privacy and your reimbursement.</p>

  <h2>Which account works with TrueMed</h2>
  <p>Both HSAs and FSAs work through the same flow, with the same medical-necessity requirement. An <a href="are-water-filters-hsa-eligible.html">HSA</a> suits larger systems because it rolls over; an <a href="are-water-filters-fsa-eligible.html">FSA</a> is ideal for spending a balance before its year-end deadline. If you are unsure which to use, the pillar compares <a href="index.html#accounts">all four account types</a>.</p>
''',
 faq=[
  ("Is TrueMed legit?","Yes. It connects you to a licensed provider who determines medical necessity and issues a Letter of Medical Necessity, following the same IRS rules that govern other qualified medical expenses."),
  ("Does TrueMed cost extra?","When you buy through a partner retailer, the Letter of Medical Necessity is typically provided at no separate cost to you. You pay the product's normal price with pre-tax dollars."),
  ("Is TrueMed available outside the US?","No. TrueMed and U.S. HSA/FSA accounts are available in the United States only."),
  ("Does TrueMed guarantee my plan will reimburse me?","No service can. Your plan administrator has the final say. TrueMed provides the documentation; you keep it and submit if asked."),
 ])

# ---------- Article #16 ----------
article(
 "how-to-get-letter-of-medical-necessity.html",
 "How to Get a Letter of Medical Necessity (2026)",
 "Two ways to get a Letter of Medical Necessity for a water filter \u2014 via TrueMed or your own doctor \u2014 plus what providers look for and how to prepare.",
 "How to get a letter",
 "How to get a Letter of Medical Necessity (and what doctors look for)",
 "There are two ways to get a Letter of Medical Necessity for a water filter: the built-in checkout route, or asking your own provider. Here is how each works, what providers look for before signing, and how to prepare so you qualify.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Two routes</p>
    <p class="ruling"><b>Get your letter through a checkout that issues it (fast, no appointment) or from your own provider.</b> Either way, a licensed provider must connect your filter to a health condition and sign before you buy.</p>
  </div>

  <h2>Route 1: Through the checkout (fastest)</h2>
  <p>The simplest path is buying from a retailer that issues the letter at purchase. You answer a short health survey, a licensed provider reviews it, and the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> is issued &mdash; often within hours, with no appointment. This is how SpringWell's TrueMed checkout works; see <a href="how-truemed-works-for-water-filters.html">the full walkthrough</a>.</p>

  <h2>Route 2: From your own doctor</h2>
  <p>If you prefer, your treating physician can write the letter. Bring the request to a regular visit, explain the water-quality concern and any test results, and ask them to document the medical necessity. This works well if you already have a relevant diagnosis on file. Use our <a href="guides/letter-of-medical-necessity-water-filter.html">template and example</a> to show your provider exactly what the letter should contain.</p>

  <h2>What providers look for before they sign</h2>
  <p>A provider is making a clinical judgment, so they want to see a genuine link between your water and a health condition. Strong supporting elements include:</p>
  <ul>
    <li><strong>A documented condition</strong> &mdash; diagnosed or a clear prevention rationale (for example, a young child or pregnancy in a home with lead risk per the {EPALEAD}).</li>
    <li><strong>Evidence about your water</strong> &mdash; a test result or your utility report showing the contaminant of concern.</li>
    <li><strong>A logical match</strong> &mdash; the filter type actually addresses that contaminant.</li>
  </ul>
  <p>General consumer-health context from the {CDC} can help you frame the conversation, but the determination is the provider's.</p>

  <h2>How to prepare</h2>
  <ul>
    <li><strong>Test first.</strong> A lab result or CCR is the most persuasive single document &mdash; see <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>.</li>
    <li><strong>Know your household risk factors</strong> &mdash; children, pregnancy, immune status &mdash; which a provider weighs.</li>
    <li><strong>Pick the system</strong> that matches the contaminant so the recommendation is specific.</li>
  </ul>

  <h2>Timing and renewal</h2>
  <p>The letter must be dated on or before your purchase &mdash; retroactive letters are not accepted &mdash; and it is generally valid up to 12 months, which matters for <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridges</a>. After it lapses, renew if you continue reimbursing replacements.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Skip the appointment</span>
    <h3>Get your letter at checkout</h3>
    <p>SpringWell's eligible systems issue the Letter of Medical Necessity through TrueMed during checkout &mdash; the fastest route for most buyers.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>Conditions that commonly support a letter</h2>
  <p>While only a provider can decide, these situations frequently support a medical-necessity case:</p>
  <ul>
    <li><strong>Lead exposure risk</strong> &mdash; older plumbing plus children or pregnancy; the {EPALEAD} notes no safe level of lead.</li>
    <li><strong>PFAS detections</strong> &mdash; documented "forever chemicals" in the supply.</li>
    <li><strong>Nitrates in well water</strong> &mdash; a particular concern for infants and pregnant women.</li>
    <li><strong>Immunocompromised household members</strong> &mdash; higher vulnerability to waterborne pathogens, per the {CDC}.</li>
    <li><strong>Provider-linked skin or GI conditions</strong> &mdash; where a clinician connects symptoms to water quality.</li>
  </ul>

  <h2>What to say to your doctor</h2>
  <p>Keep it concrete: describe the contaminant concern, share any test results, name who in the household is at risk, and ask whether they can document a water filtration system as medically necessary to treat or prevent the condition. Bringing the <a href="guides/letter-of-medical-necessity-water-filter.html">template</a> makes it a two-minute request rather than an open-ended conversation.</p>

  <h2>If your provider is unfamiliar with LMNs</h2>
  <p>Some clinicians have not written one for a water filter before. That is fine &mdash; the concept is standard for durable medical equipment. Show them the template, explain that your FSA/HSA administrator accepts a Letter of Medical Necessity, and offer your test results as support. If it is easier, the checkout route handles the provider step for you.</p>

  <h2>What each route costs</h2>
  <p>Through a partner checkout, the letter is typically provided at no separate cost. Through your own provider, a brief visit may carry a normal copay &mdash; though if you are seeing them anyway, adding the request costs nothing extra. Either way, the letter unlocks tax savings that usually dwarf any small cost to obtain it.</p>
''',
 faq=[
  ("How do I get a Letter of Medical Necessity for a water filter?","Either through a checkout that issues it after a short health survey (fastest), or by asking your own treating provider to write one based on your condition and water-quality concern."),
  ("What do doctors look for?","A genuine link between your water and a health condition: a documented or preventable condition, evidence about your water (a test or utility report), and a filter that actually addresses that contaminant."),
  ("Do I need a water test to get a letter?","Not strictly, but a test result or utility report is the most persuasive supporting document and helps the provider make a specific recommendation."),
  ("How long is the letter valid?","Generally up to 12 months for the same product category. Renew it if you keep reimbursing replacement filters after it lapses."),
 ])

# ---------- Article #17 ----------
article(
 "how-to-get-reimbursed-water-filter-fsa-hsa.html",
 "How to Get Reimbursed for a Water Filter (FSA/HSA)",
 "How to get reimbursed for a water filter from your FSA or HSA: the two payment paths, the documents you need, how to submit a claim, and recurring filters.",
 "How to get reimbursed",
 "How to get reimbursed for a water filter from your FSA/HSA",
 "Whether you paid with your benefits card or out of pocket, here is how to get a water filter properly reimbursed from your FSA or HSA &mdash; the documents to keep, how to submit a claim, and how to handle recurring replacement filters.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The essentials</p>
    <p class="ruling"><b>Keep your Letter of Medical Necessity and itemized receipt, then either pay with your card or submit a claim for reimbursement.</b> Good records are the difference between smooth reimbursement and a denial.</p>
  </div>

  <h2>Two ways to use your funds</h2>
  <p>There are two clean paths, and you can mix them:</p>
  <ul>
    <li><strong>Pay directly with your HSA/FSA card.</strong> The simplest method &mdash; the charge comes straight from your account at checkout. You still keep documentation in case it is requested.</li>
    <li><strong>Pay out of pocket, then reimburse yourself.</strong> Useful if your balance is short now or you used a rewards card. You submit a claim (FSA) or withdraw/reimburse from your HSA, supported by your records.</li>
  </ul>
  <p>For the purchase itself, see the <a href="how-to-buy-water-filter-with-hsa-fsa.html">step-by-step buying guide</a>.</p>

  <h2>The documents you need</h2>
  <ul>
    <li><strong>Letter of Medical Necessity</strong> &mdash; dated on or before purchase. See <a href="guides/letter-of-medical-necessity-water-filter.html">how to get one</a>.</li>
    <li><strong>Itemized receipt</strong> &mdash; showing the product, date, and amount (not just a card statement line).</li>
    <li><strong>Proof of payment</strong> &mdash; in case your administrator wants it.</li>
  </ul>

  <h2>How to submit a reimbursement claim</h2>
  <ol class="steps">
    <li><h4>Log in to your administrator's portal</h4><p>Most FSA/HSA providers have an online claims or "reimburse myself" section.</p></li>
    <li><h4>Enter the expense and upload documents</h4><p>Attach the Letter of Medical Necessity and itemized receipt.</p></li>
    <li><h4>Submit and track</h4><p>Reimbursement timelines vary &mdash; often a few business days to a couple of weeks.</p></li>
    <li><h4>Keep copies</h4><p>Retain everything even after reimbursement; HSAs in particular can be reviewed years later.</p></li>
  </ol>

  <h2>Recurring replacement filters</h2>
  <p>Replacement cartridges can be reimbursed on the same basis as the system &mdash; keep an itemized receipt for each, and note that you may need a renewed letter once the original lapses. See <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridge eligibility</a> for the routine.</p>

  <h2>If something goes wrong</h2>
  <p>If a claim is questioned or denied, it is almost always a documentation or timing issue, not the product. Our guide to <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">avoiding a denied claim</a> covers the common causes and how to respond.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Start clean</span>
    <h3>Buy where the paperwork is handled</h3>
    <p>SpringWell's TrueMed checkout issues the Letter of Medical Necessity at purchase, so your reimbursement records are correct from day one.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>FSA vs HSA: reimbursement differences</h2>
  <p>The documentation is the same, but the mechanics differ. With an <strong>FSA</strong>, you typically submit a claim to your employer's administrator, who reimburses from your pre-funded balance &mdash; and unspent funds usually expire December 31. With an <strong>HSA</strong>, you control the account: you can pay directly, or reimburse yourself at any time (even years later) as long as the expense was qualified and the letter predates it. See <a href="are-water-filters-hsa-eligible.html">HSA eligibility</a> and <a href="are-water-filters-fsa-eligible.html">FSA eligibility</a> for the account-specific rules.</p>

  <h2>Worked example: a split-payment reimbursement</h2>
  <p>Say a $2,400 combo system exceeds your $1,500 FSA balance. You pay $1,500 with your FSA card and $900 on a regular card at checkout. For the $1,500, you keep the letter and itemized receipt; if your plan requires substantiation, you upload both. The $900 remainder is simply a normal purchase. Clean records on the qualified $1,500 are all you need &mdash; see the <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">denial-avoidance guide</a> to keep it smooth.</p>

  <h2>How long to keep records</h2>
  <p>Keep your letter and receipts for as long as the account could be reviewed. For FSAs, retain them at least through the plan year and any run-out period. For HSAs, keep them indefinitely &mdash; you may reimburse yourself far in the future, and HSA records can be examined years after the expense. A single labeled folder (digital is fine) makes this painless.</p>

  <h2>Common reimbursement mistakes</h2>
  <ul>
    <li>Submitting a card statement instead of an <strong>itemized receipt</strong>.</li>
    <li>Missing or late <strong>Letter of Medical Necessity</strong> (it must predate the purchase).</li>
    <li>Forgetting to <strong>renew</strong> the letter for ongoing replacement filters.</li>
    <li>Not checking the <strong>administrator's specific submission rules</strong> before buying.</li>
  </ul>
''',
 faq=[
  ("How do I get reimbursed for a water filter from my FSA?","Keep your Letter of Medical Necessity and itemized receipt, then submit a claim through your administrator's portal with those documents attached, or pay directly with your FSA card."),
  ("What documents do I need?","A Letter of Medical Necessity dated on or before purchase, an itemized receipt showing the product and amount, and proof of payment if requested."),
  ("How long does reimbursement take?","It varies by administrator, commonly a few business days to a couple of weeks after you submit a complete claim."),
  ("Can I reimburse replacement filters too?","Yes, on the same medical-necessity basis. Keep a receipt for each replacement and renew the letter if required once the original lapses."),
 ])

# ---------- Article #18 ----------
article(
 "will-my-fsa-hsa-water-filter-claim-be-denied.html",
 "Will My FSA/HSA Water Filter Claim Be Denied? (Avoid It)",
 "The top reasons FSA/HSA water filter claims get denied \u2014 and exactly how to avoid each one. Plus what to do if your claim is rejected.",
 "Avoiding a denied claim",
 "Will my FSA/HSA water filter claim get denied?",
 "Most denied water-filter claims fail for the same handful of avoidable reasons &mdash; and almost none of them are about the filter itself. Here is what trips people up, how to prevent each issue, and what to do if your claim is rejected.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The pattern</p>
    <p class="ruling"><b>Denials are almost always about documentation and timing, not the product.</b> Get the Letter of Medical Necessity before you buy, keep an itemized receipt, and be honest about the health reason &mdash; and you avoid nearly every denial.</p>
  </div>

  <h2>The top reasons claims get denied</h2>
  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Reason</th><th>Why it happens</th><th>How to avoid it</th></tr></thead>
    <tbody>
      <tr><td>No Letter of Medical Necessity</td><td>Buyer assumed filters are auto-eligible</td><td>Get an <a href="guides/letter-of-medical-necessity-water-filter.html">LMN</a> before purchase</td></tr>
      <tr><td>Letter dated after purchase</td><td>Bought first, documented later</td><td>Secure the letter on or before the buy date</td></tr>
      <tr><td>No itemized receipt</td><td>Only a card statement kept</td><td>Save the receipt naming the product</td></tr>
      <tr><td>Comfort, not health</td><td>Claimed taste/convenience as medical</td><td>Only claim a genuine, documented health need</td></tr>
      <tr><td>Lapsed letter on replacements</td><td>Recurring filters past the 12-month window</td><td>Renew the letter; keep receipts</td></tr>
    </tbody>
  </table>
  </div>

  <h2>How to prevent a denial (the short checklist)</h2>
  <ul>
    <li><strong>Order matters.</strong> Letter first, purchase second. Always.</li>
    <li><strong>Document the why.</strong> A water test result or utility report backing a real health concern &mdash; see <a href="how-to-get-letter-of-medical-necessity.html">what providers look for</a>.</li>
    <li><strong>Keep an itemized receipt</strong> with the letter in one place.</li>
    <li><strong>Be honest.</strong> If the reason is purely taste or convenience, it is a personal expense &mdash; do not claim it.</li>
    <li><strong>Confirm with your administrator</strong> how they want claims submitted &mdash; see <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">how reimbursement works</a>.</li>
  </ul>

  <h2>What to do if your claim is denied</h2>
  <p>A denial is not always final. First, read the reason given &mdash; it usually points to a missing document. If you have the Letter of Medical Necessity and itemized receipt, you can typically resubmit or appeal through your administrator, attaching the documentation. If the letter was missing or dated after the purchase, that specific purchase generally cannot be fixed retroactively, but you can get the documentation right for future purchases and replacements. When in doubt, call your administrator and ask exactly what they need.</p>
  <div class="note key"><span class="lab">Not advice</span>This is general information, not tax or legal advice. Your plan administrator's rules govern your specific claim.</div>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Avoid the pitfalls</span>
    <h3>Buy where timing and documentation are built in</h3>
    <p>SpringWell's TrueMed checkout issues the Letter of Medical Necessity at the moment of purchase, which prevents the two most common denial causes &mdash; missing or late documentation.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>Real-world denial scenarios (and the fix)</h2>
  <ul>
    <li><strong>"I bought it, then asked my doctor."</strong> The letter postdates the purchase, so that buy generally cannot be reimbursed. Fix: from now on, letter first &mdash; and the checkout route enforces this automatically.</li>
    <li><strong>"My card was declined at a hardware store."</strong> General retailers are not set up for the LMN process. Fix: buy from a retailer with a built-in HSA/FSA checkout, or pay out of pocket and reimburse with proper documentation.</li>
    <li><strong>"They asked for a receipt and I only had my statement."</strong> Fix: provide the itemized receipt naming the product; re-upload through your administrator's portal.</li>
    <li><strong>"My replacement-filter claim was rejected."</strong> The original letter likely lapsed. Fix: get a renewed letter and resubmit &mdash; see <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">reimbursement</a>.</li>
  </ul>

  <h2>How to appeal, step by step</h2>
  <ol class="steps">
    <li><h4>Read the denial reason</h4><p>It almost always names a specific missing piece.</p></li>
    <li><h4>Gather the documents</h4><p>Your <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> and itemized receipt.</p></li>
    <li><h4>Resubmit or formally appeal</h4><p>Upload through the portal or follow the administrator's appeal process, attaching everything.</p></li>
    <li><h4>Follow up</h4><p>Confirm receipt and keep a record of the correspondence.</p></li>
  </ol>

  <h2>When to call your administrator</h2>
  <p>If the reason is unclear, the rules seem inconsistent, or a large purchase is involved, a quick call is worth it. Your administrator can tell you exactly what they need and whether a resubmission will be accepted. Because plan rules vary, their answer is more reliable than any general guide &mdash; including this one.</p>
''',
 faq=[
  ("Why would my FSA water filter claim be denied?","Almost always for documentation or timing: no Letter of Medical Necessity, a letter dated after purchase, a missing itemized receipt, or claiming a comfort purchase as medical."),
  ("Can I fix a denied claim?","Often yes, if you have the Letter of Medical Necessity and itemized receipt &mdash; resubmit or appeal with the documents. A missing or late letter usually cannot be fixed retroactively for that purchase."),
  ("How do I make sure my claim is approved?","Get the letter before buying, keep an itemized receipt, claim only a genuine health need, and confirm submission rules with your administrator."),
 ])

# ======================================================================
#  CLUSTER B (cont.) — Articles #19-#21
# ======================================================================

# ---------- Article #19 ----------
article(
 "can-you-use-fsa-hsa-card-for-water-filter.html",
 "Can You Use an FSA/HSA Card for a Water Filter?",
 "Can you swipe your FSA/HSA card directly for a water filter? Usually only with a Letter of Medical Necessity on file. Here is how the card actually works.",
 "Using your card directly",
 "Can you use an FSA/HSA card directly for a water filter?",
 "Sometimes &mdash; but a direct swipe often fails unless a Letter of Medical Necessity supports the purchase. Here is how the card actually works for a water filter, why it can decline, and the clean way to pay.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Often not directly &mdash; not without documentation.</b> Water filters are not auto-approved merchant items, so a plain swipe at a general store may decline or be flagged. With a Letter of Medical Necessity and the right checkout, the card works.</p>
  </div>

  <h2>Why a direct swipe can fail</h2>
  <p>FSA/HSA cards run on a system that auto-approves clearly medical items (think pharmacy SKUs) and flags everything else for substantiation. A water filter from a general retailer is not coded as an auto-approved medical product, so the charge may be declined at the register or later require you to prove it was a qualified expense. That is not the card refusing eligibility &mdash; it is the system asking for the documentation the IRS requires. See the rule in our <a href="are-water-filters-fsa-eligible.html">FSA eligibility guide</a>.</p>

  <h2>How to make the card work</h2>
  <p>Two things turn a water filter into a clean card transaction:</p>
  <ul>
    <li><strong>A Letter of Medical Necessity</strong> dated on or before purchase &mdash; the document that establishes the expense is medical. See <a href="guides/letter-of-medical-necessity-water-filter.html">how to get one</a>.</li>
    <li><strong>A retailer set up for HSA/FSA</strong> &mdash; one that issues the letter and processes the payment correctly, so substantiation is handled.</li>
  </ul>
  <p>SpringWell's TrueMed checkout does both: you complete a short survey, receive the letter, then pay with your card. See the <a href="how-truemed-works-for-water-filters.html">TrueMed walkthrough</a> and the full <a href="how-to-buy-water-filter-with-hsa-fsa.html">step-by-step buying guide</a>.</p>

  <h2>What if the charge is more than my balance?</h2>
  <p>Split it: pay what your card covers and put the rest on a regular card. Or pay out of pocket and reimburse later (especially easy with an HSA). Either way, keep the letter and itemized receipt &mdash; see <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">how reimbursement works</a>.</p>

  <h2>Keep your documentation either way</h2>
  <p>Even when a card payment goes through smoothly, retain your Letter of Medical Necessity and itemized receipt. Administrators can request substantiation after the fact, and HSAs can be reviewed years later. A direct swipe is convenient, but documentation is what makes it stick.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} The clean way to pay</span>
    <h3>Use a checkout built for HSA/FSA</h3>
    <p>SpringWell's TrueMed checkout issues the letter and processes your card correctly, so the payment is substantiated from the start.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>Auto-approved vs flagged: how card systems decide</h2>
  <p>FSA/HSA debit cards run on an approval system that instantly clears items coded as medical &mdash; prescriptions, many over-the-counter health products &mdash; at participating merchants. Anything outside that list, including most water filters at general retailers, is flagged for substantiation: the card may decline, or the charge clears but your administrator later asks for proof. That explains why a filter behaves differently from a pharmacy purchase, and why buying through an HSA/FSA-ready retailer matters.</p>

  <h2>The safer default for larger systems</h2>
  <p>For a multi-thousand-dollar whole-house system, many buyers find it simplest to pay out of pocket and reimburse from an HSA once the letter and receipt are in hand &mdash; it sidesteps card-substantiation hiccups entirely and works even while your balance is still building. See <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">how reimbursement works</a> and the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>
''',
 faq=[
  ("Can I swipe my FSA card for a water filter at any store?","Usually not. General retailers do not code filters as auto-approved medical items, so the charge may decline or require substantiation. A Letter of Medical Necessity and an HSA/FSA-ready checkout fix this."),
  ("Why was my HSA card declined for a filter?","Likely because the item was not recognized as a qualified medical product without documentation. With a Letter of Medical Necessity and the right retailer, it processes correctly."),
  ("Do I still need records if the card works?","Yes. Keep the Letter of Medical Necessity and itemized receipt; administrators can request substantiation later, and HSAs can be reviewed years afterward."),
 ])

# ---------- Article #20 ----------
article(
 "hsa-fsa-water-filter-reimbursement-checklist.html",
 "HSA/FSA Water Filter Reimbursement: Documents Checklist",
 "The exact documents you need to reimburse a water filter from your FSA/HSA \u2014 a simple checklist for the letter, receipt, and records, plus how to submit.",
 "Documents checklist",
 "HSA/FSA water filter reimbursement: documents checklist",
 "Use this checklist to make sure your water-filter reimbursement goes through the first time. It covers exactly what to gather before, during, and after the purchase &mdash; and how to submit it.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The short list</p>
    <p class="ruling"><b>You need three things:</b> a Letter of Medical Necessity dated on or before purchase, an itemized receipt, and proof of payment. Keep them together and you are covered.</p>
  </div>

  <h2>The core documents</h2>
  <ul>
    <li><strong>Letter of Medical Necessity (LMN).</strong> From a licensed provider, dated on or before the purchase, naming the condition and the filtration recommendation. See <a href="guides/letter-of-medical-necessity-water-filter.html">the LMN guide and template</a>.</li>
    <li><strong>Itemized receipt.</strong> Showing the product name, date, and amount &mdash; not just a card statement line.</li>
    <li><strong>Proof of payment.</strong> Card record or order confirmation, in case the administrator asks.</li>
    <li><strong>Renewal letter (for replacements).</strong> If you reimburse ongoing cartridges past the letter's validity window.</li>
  </ul>

  <h2>Checklist: before, during, and after purchase</h2>
  <ol class="steps">
    <li><h4>Before</h4><p>Test your water or pull your report; confirm your balance and any deadline; choose the system that matches your contaminant.</p></li>
    <li><h4>During</h4><p>Obtain the Letter of Medical Necessity (the checkout route issues it automatically); pay with your HSA/FSA card or note the amount for reimbursement.</p></li>
    <li><h4>After</h4><p>Download and file the letter, itemized receipt, and payment proof together; submit a claim if you paid out of pocket.</p></li>
  </ol>

  <h2>How to submit (if reimbursing)</h2>
  <p>Log in to your administrator's portal, open the claims or "reimburse myself" section, enter the expense, and upload the letter and itemized receipt. Track the claim to completion and keep copies. Full detail is in <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">how to get reimbursed</a>.</p>

  <h2>Recurring replacement filters</h2>
  <p>For each replacement, keep an itemized receipt and confirm whether your letter is still within its validity window; renew if needed. See <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement cartridge eligibility</a> for the routine.</p>

  <div class="note key"><span class="lab">One-folder rule</span>Keep everything &mdash; letter, receipts, payment proof &mdash; in a single labeled folder (digital is fine). It turns any future request into a 30-second task and is the simplest way to <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">avoid a denial</a>.</div>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Start with clean records</span>
    <h3>Buy where the letter is issued at checkout</h3>
    <p>SpringWell's TrueMed checkout produces the Letter of Medical Necessity at purchase, so your first and most important document is handled automatically.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>What an itemized receipt must show</h2>
  <p>This is the document people most often get wrong. An acceptable itemized receipt names the <strong>product</strong> (the filtration system or cartridge), the <strong>date</strong>, the <strong>amount</strong>, and ideally the seller. A credit-card statement line showing only a dollar amount and merchant name is not enough on its own. If you buy online, save the order confirmation and invoice, not just the bank charge.</p>

  <h2>Digital vs paper records</h2>
  <p>Either is fine &mdash; what matters is that documents are legible, complete, and kept together. A simple approach: create one folder named for the purchase, drop in the letter, receipt, and payment proof, and back it up. For HSAs especially, you may need these years later, so digital copies with a backup are the safest choice.</p>

  <h2>Keep a copy of this checklist</h2>
  <p>Before any eligible water purchase, run the three-line test: letter dated on or before purchase, itemized receipt in hand, payment proof saved. If all three are yes, you are ready &mdash; and if your administrator ever asks, you can respond in minutes.</p>
''',
 faq=[
  ("What documents do I need to reimburse a water filter?","A Letter of Medical Necessity dated on or before purchase, an itemized receipt showing the product and amount, and proof of payment. Keep a renewal letter for ongoing replacements."),
  ("Is a card statement enough?","No. You need an itemized receipt that names the product, date, and amount. A statement line alone is usually rejected."),
  ("How long should I keep the documents?","Through the plan year and run-out period for an FSA; indefinitely for an HSA, which can be reviewed years later."),
 ])

# ---------- Article #21 ----------
article(
 "do-you-need-prescription-fsa-eligible-water-filter.html",
 "Do You Need a Prescription for an FSA Water Filter?",
 "You don't need a traditional prescription for an FSA/HSA water filter \u2014 you need a Letter of Medical Necessity. Here is the difference and how to get one.",
 "Prescription vs LMN",
 "Do you need a prescription for an FSA-eligible water filter?",
 "Not a traditional prescription &mdash; for a water filter you need a Letter of Medical Necessity, which does the same job for equipment that a prescription does for medication. Here is the difference and how to get the right document.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>No prescription &mdash; you need a Letter of Medical Necessity.</b> For durable equipment like a water filter, the LMN is the correct document and is what FSA/HSA administrators expect.</p>
  </div>

  <h2>Prescription vs Letter of Medical Necessity</h2>
  <p>A prescription is an order for a specific medication or therapy. A Letter of Medical Necessity explains <em>why</em> a product or piece of equipment is needed to treat, mitigate, or prevent a condition. Medicines use prescriptions; durable items like water filters, CPAP supplies, or orthopedic equipment use an LMN. They overlap in spirit &mdash; both are a provider documenting medical need &mdash; but for a filter, the LMN is the instrument that unlocks reimbursement. See <a href="guides/letter-of-medical-necessity-water-filter.html">our LMN guide and template</a>.</p>

  <h2>Why a water filter uses an LMN</h2>
  <p>Because a filter is equipment rather than a dispensed drug, there is nothing for a pharmacy to fill. What your plan needs is documentation that the equipment addresses a health condition &mdash; exactly what an LMN provides. With it, the same rules in {IRS502} and {IRS969} that govern other qualified medical expenses apply to your filter.</p>

  <h2>How to get the right document</h2>
  <p>Two routes, same as any LMN: obtain it through a checkout that issues it after a short survey (fastest, no appointment), or ask your own provider to write one. Either way the letter must be dated on or before purchase. Details are in <a href="how-to-get-letter-of-medical-necessity.html">how to get a Letter of Medical Necessity</a>, and the <a href="how-to-buy-water-filter-with-hsa-fsa.html">buying guide</a> shows where it fits in checkout.</p>

  <h2>When something prescription-like is involved</h2>
  <p>Occasionally a provider documents a specific recommendation that reads like a prescription &mdash; that is fine, and an LMN can incorporate that detail. The key is not the label on the document but that a licensed provider has connected the filter to a medical need and dated it correctly. Your administrator confirms what format they accept.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Get the right document</span>
    <h3>The letter is issued at checkout</h3>
    <p>SpringWell's TrueMed checkout produces your Letter of Medical Necessity after a short survey &mdash; no prescription, no appointment.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>Documents people confuse with an LMN</h2>
  <p>Several documents sound interchangeable but are not. A <strong>prescription</strong> orders a medication. A <strong>doctor's note</strong> might excuse you from work but rarely satisfies a plan administrator. A <strong>Letter of Medical Necessity</strong> is the specific document that ties equipment to a condition and is what administrators want for a filter. When in doubt, ask your provider for "a Letter of Medical Necessity for FSA/HSA purposes" by name.</p>

  <h2>What if my plan says "prescription required"?</h2>
  <p>Some plan language uses "prescription" loosely to mean "provider documentation." If your administrator says a prescription is required, ask whether a Letter of Medical Necessity satisfies it &mdash; for equipment like a filter, it almost always does. Get their answer in writing if you can, and keep it with your records. See <a href="how-to-get-letter-of-medical-necessity.html">how to get the letter</a> and the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>
''',
 faq=[
  ("Do I need a prescription for an FSA water filter?","No. You need a Letter of Medical Necessity, which is the correct document for equipment like a filter and is what FSA/HSA administrators expect."),
  ("What's the difference between a prescription and an LMN?","A prescription orders a medication; a Letter of Medical Necessity explains why a product or equipment is medically needed. Filters use an LMN."),
  ("Can my doctor write the letter?","Yes. Your provider can issue the LMN, or you can get one through a checkout that issues it after a short health survey. It must be dated on or before purchase."),
 ])

# ======================================================================
#  CLUSTER C — Comparisons (Articles #25-#27)
# ======================================================================

# ---------- Article #25 ----------
article(
 "springwell-vs-clearly-filtered-fsa-eligible.html",
 "SpringWell vs Clearly Filtered: FSA-Eligible Filters",
 "SpringWell vs Clearly Filtered for FSA/HSA buyers: whole-house vs pitcher and under-sink, eligibility, cost, and which is the better health investment.",
 "SpringWell vs Clearly Filtered",
 "SpringWell vs Clearly Filtered: which FSA-eligible filter wins?",
 "Both SpringWell and Clearly Filtered can be bought with HSA/FSA dollars through a Letter of Medical Necessity &mdash; but they solve different problems. The short version: Clearly Filtered excels at point-of-use; SpringWell owns whole-home. Here is how to choose.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick verdict</p>
    <p class="ruling"><b>Different tools for different jobs.</b> Choose <b>Clearly Filtered</b> for a renter-friendly pitcher or single-tap filter; choose <b>SpringWell</b> when you want to treat the whole home &mdash; the stronger medical-necessity case for an HSA/FSA purchase.</p>
  </div>

  {disc(0)}

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Factor</th><th>SpringWell</th><th>Clearly Filtered</th></tr></thead>
    <tbody>
      <tr><td>Primary focus</td><td>Whole-house &amp; well systems</td><td>Pitchers &amp; under-sink (point-of-use)</td></tr>
      <tr><td>Coverage</td><td>Every tap and shower</td><td>One pour or one tap</td></tr>
      <tr><td>Best for</td><td>Homeowners, whole-home exposure</td><td>Renters, drinking-water only</td></tr>
      <tr><td>HSA/FSA route</td><td class="yes">LMN via TrueMed</td><td class="yes">LMN services</td></tr>
      <tr><td>Install</td><td>Point-of-entry (DIY or pro)</td><td>None / minimal</td></tr>
    </tbody>
  </table>
  </div>

  <h2>Where Clearly Filtered shines</h2>
  <p>Clearly Filtered built its reputation on point-of-use filtration &mdash; pitchers and under-sink units with strong contaminant-reduction claims. If you rent, want something portable, or only care about the water you drink and cook with, it is a sensible, low-commitment choice. It can also be eligible through a Letter of Medical Necessity, like other qualifying filtration.</p>

  <h2>Where SpringWell wins</h2>
  <p>SpringWell focuses on the category Clearly Filtered does not really serve: whole-house and well systems that treat every outlet &mdash; drinking, cooking, bathing, laundry. For an HSA/FSA buyer, that breadth matters twice over: it reduces exposure across the home, and whole-home reduction is the easier medical-necessity case to document. SpringWell also pairs its systems with a built-in <a href="how-truemed-works-for-water-filters.html">TrueMed checkout</a> and a lifetime warranty on core systems.</p>

  <h2>Cost and value</h2>
  <p>A pitcher or under-sink filter has a low entry price but ongoing cartridge costs and limited scope. A whole-house system costs more upfront but treats everything with low long-term maintenance. Verify current pricing on each brand's site, and remember that buying with pre-tax dollars discounts either choice by your tax rate &mdash; see the <a href="index.html#savings">savings math</a>.</p>

  <h2>Who should choose which</h2>
  <ul>
    <li><strong>Choose Clearly Filtered if:</strong> you rent, want point-of-use only, or have a tight budget for drinking water.</li>
    <li><strong>Choose SpringWell if:</strong> you own your home, want whole-home coverage, or your documented concern (lead, chlorine, well contaminants) affects more than the kitchen tap.</li>
  </ul>

  <h2>Pros and cons at a glance</h2>
  <div class="proscons">
    <div class="pro"><h4>SpringWell strengths</h4><ul>
      <li>Whole-home coverage &mdash; every tap and shower</li>
      <li>Low-maintenance, long-life media</li>
      <li>Lifetime warranty on core systems</li>
      <li>Built-in TrueMed HSA/FSA checkout</li>
      <li>Well-water options Clearly Filtered does not offer</li>
    </ul></div>
    <div class="con"><h4>Clearly Filtered strengths</h4><ul>
      <li>Low entry price; no installation</li>
      <li>Renter- and apartment-friendly</li>
      <li>Strong point-of-use contaminant claims</li>
      <li>Portable; ideal for drinking water only</li>
      <li>Can also qualify via an LMN service</li>
    </ul></div>
  </div>

  <h2>Total cost of ownership</h2>
  <p>Point-of-use filters look cheap until you add years of cartridge replacements for each filtered tap. A whole-house system front-loads the cost but typically uses long-life media, so the five-year picture often favors whole-house for households wanting comprehensive coverage. Run your own numbers against current prices, and remember pre-tax dollars discount either path by your tax rate &mdash; see the <a href="how-to-get-reimbursed-water-filter-fsa-hsa.html">reimbursement basics</a>.</p>

  <h2>The eligibility process for each</h2>
  <p>Both routes require a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. The practical difference is friction: SpringWell issues the letter inside checkout via <a href="how-truemed-works-for-water-filters.html">TrueMed</a>, while a point-of-use purchase through another retailer may route you through a separate LMN service. Either works &mdash; confirm the path before buying and keep your documents per the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">checklist</a>.</p>

  <h2>The honest bottom line</h2>
  <p>These brands are less rivals than answers to different questions. If the question is "how do I get cleaner drinking water in a rental without installing anything?", Clearly Filtered is a fine answer. If it is "how do I reduce a documented contaminant across my whole home with one eligible purchase?", SpringWell is the stronger choice &mdash; and the easier medical-necessity case to make.</p>

  <h2>A closer look at the eligibility question</h2>
  <p>Both brands can be purchased with HSA/FSA dollars, but the path and the strength of the case differ. The eligibility rule is identical &mdash; a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> tying the filter to a health concern. Where they diverge is twofold. First, the <em>case</em>: a whole-house system reduces exposure at every tap, shower, and appliance, which is generally easier for a provider to document as medically necessary than a single pour or one tap. Second, the <em>convenience</em>: SpringWell builds the survey-and-letter step into its checkout via TrueMed, whereas a point-of-use purchase typically means arranging the documentation yourself through an LMN service. Neither is disqualifying &mdash; just be clear on how you will obtain and keep the letter.</p>

  <h2>Which is right for you?</h2>
  <ul>
    <li><strong>Renter or apartment, drinking water only</strong> &rarr; a Clearly Filtered pitcher or under-sink unit is the low-commitment, portable choice. See our <a href="water-filters-renters-hsa-fsa-no-installation.html">renter guidance</a>.</li>
    <li><strong>Homeowner with whole-home concerns</strong> (chlorine on skin and hair, every-tap exposure) &rarr; SpringWell, which actually serves that category.</li>
    <li><strong>Well owner</strong> &rarr; SpringWell, since point-of-use pitchers are not built for iron, sulfur, or whole-well treatment.</li>
    <li><strong>Tight budget, single tap</strong> &rarr; point-of-use is the cheaper entry; weigh ongoing cartridge costs.</li>
  </ul>

  <h2>Can you use both?</h2>
  <p>Yes &mdash; and some households do. A whole-house SpringWell system treats the home while a point-of-use filter adds a final polishing stage at the kitchen tap. Each can be documented on the same medical-necessity basis; keep receipts and the letter for both per the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>

  <h2>The bottom line</h2>
  <p>This is less a head-to-head than a question of scope. For drinking-water-only and portability, Clearly Filtered fits. For whole-home coverage and the stronger HSA/FSA case, SpringWell is the better tool. Match the system to your home and your documented concern &mdash; and compare current pricing and certifications on each brand's own site.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} For whole-home coverage</span>
    <h3>SpringWell Whole House Filter</h3>
    <p>Treats every tap with low maintenance and a built-in HSA/FSA checkout &mdash; the stronger fit for a documented, whole-home health need.</p>
    {aff("whole-house","Check price","btn")}
    &nbsp;<a class="btn ghost" href="reviews/springwell-whole-house-water-filter-review.html">Read the review &rarr;</a>
  </div>
''',
 faq=[
  ("Is SpringWell or Clearly Filtered better for FSA/HSA?","Both can be eligible with a Letter of Medical Necessity. Clearly Filtered suits point-of-use needs; SpringWell suits whole-home coverage, which is the stronger medical-necessity case."),
  ("Can I buy Clearly Filtered with HSA/FSA?","Generally yes, with a Letter of Medical Necessity through an LMN service, like other qualifying filtration. Confirm at checkout and with your plan administrator."),
  ("Which is cheaper?","Point-of-use filters have a lower entry price but recurring cartridge costs; whole-house systems cost more upfront but treat everything with lower long-term maintenance."),
 ])

# ---------- Article #26 ----------
article(
 "springwell-vs-aquasana-hsa-fsa.html",
 "SpringWell vs Aquasana: HSA/FSA Whole-House Compared",
 "SpringWell vs Aquasana whole-house water filters for HSA/FSA buyers: filtration approach, maintenance, warranty, eligibility, and which to choose.",
 "SpringWell vs Aquasana",
 "SpringWell vs Aquasana: HSA/FSA whole-house comparison",
 "SpringWell and Aquasana are two of the better-known direct-to-consumer whole-house brands, and both can be bought with HSA/FSA dollars via a Letter of Medical Necessity. Here is how they compare on the factors that matter for an eligible purchase.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick verdict</p>
    <p class="ruling"><b>Both are credible whole-house options.</b> SpringWell stands out for low-maintenance media, a lifetime warranty on core systems, and a built-in TrueMed HSA/FSA checkout. Compare current specs and pricing before deciding.</p>
  </div>

  {disc(0)}

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Factor</th><th>SpringWell</th><th>Aquasana</th></tr></thead>
    <tbody>
      <tr><td>Category</td><td>Whole-house &amp; well specialist</td><td>Whole-house &amp; under-sink</td></tr>
      <tr><td>Approach</td><td>Multi-stage catalytic + carbon media</td><td>Multi-stage carbon/KDF (verify model)</td></tr>
      <tr><td>Maintenance</td><td>Low; long-life media</td><td>Varies by model</td></tr>
      <tr><td>Warranty</td><td>Lifetime on core systems</td><td>Limited (verify current)</td></tr>
      <tr><td>HSA/FSA route</td><td class="yes">LMN via TrueMed</td><td>LMN where offered</td></tr>
    </tbody>
  </table>
  </div>

  <h2>Filtration approach</h2>
  <p>Both brands use multi-stage carbon-based filtration to reduce chlorine, taste, and odor on city water. SpringWell emphasizes catalytic carbon (helpful for chloramine) and long-life media designed to minimize cartridge swaps. Aquasana offers several whole-house tiers as well. Exact media, capacity, and certifications vary by model, so check each brand's current spec sheet and any {NSF} certifications before buying.</p>

  <h2>Maintenance and warranty</h2>
  <p>For an FSA/HSA buyer, low maintenance is doubly valuable: fewer replacement filters mean less recurring cost and less <a href="water-filter-replacement-cartridges-fsa-eligible.html">documentation</a>. SpringWell's lifetime warranty on core systems is a notable differentiator; confirm Aquasana's current warranty terms, which differ by product line.</p>

  <h2>Eligibility and checkout</h2>
  <p>Both can be eligible through a Letter of Medical Necessity. SpringWell builds the process directly into checkout via <a href="how-truemed-works-for-water-filters.html">TrueMed</a>, which keeps your timing and documentation correct automatically. With any brand, confirm the HSA/FSA path before you buy &mdash; see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>

  <h2>Which should you choose?</h2>
  <p>If warranty, low maintenance, and a frictionless HSA/FSA checkout are priorities &mdash; or you have well water, where SpringWell's specialization helps &mdash; SpringWell is the easy recommendation. If a specific Aquasana model better matches your tested contaminants or budget, it is a reasonable alternative. Either way, <a href="are-water-test-kits-fsa-hsa-eligible.html">test first</a> and match the system to the result.</p>

  <h2>Pros and cons at a glance</h2>
  <div class="proscons">
    <div class="pro"><h4>SpringWell strengths</h4><ul>
      <li>Catalytic carbon (helps with chloramine)</li>
      <li>Long-life media; low maintenance</li>
      <li>Lifetime warranty on core systems</li>
      <li>Well-water specialization</li>
      <li>Built-in TrueMed HSA/FSA checkout</li>
    </ul></div>
    <div class="con"><h4>Aquasana strengths</h4><ul>
      <li>Established brand with multiple tiers</li>
      <li>Whole-house and under-sink options</li>
      <li>Competitive entry pricing on some models</li>
      <li>Can qualify via an LMN where offered</li>
    </ul></div>
  </div>

  <h2>Total cost of ownership</h2>
  <p>Compare not just sticker price but the replacement schedule. A system with longer-life media and a lifetime warranty often costs less over five years than a cheaper unit with frequent cartridge changes &mdash; and fewer replacements means less <a href="water-filter-replacement-cartridges-fsa-eligible.html">reimbursement paperwork</a>. Verify each model's current filter intervals before deciding.</p>

  <h2>The honest bottom line</h2>
  <p>Both can serve you well on city water. SpringWell edges ahead for buyers who value warranty, low upkeep, a seamless HSA/FSA checkout, or who have well water. If a particular Aquasana model matches your tested contaminants and budget better, it is a fair alternative &mdash; just confirm its eligibility path first via <a href="how-to-buy-water-filter-with-hsa-fsa.html">the buying guide</a>.</p>

  <h2>Well water: a key dividing line</h2>
  <p>The clearest practical difference is source. SpringWell offers dedicated <a href="springwell-well-water-filter-system-review.html">well-water systems</a> for iron, manganese, sulfur, and (paired with UV) bacteria &mdash; problems a city-focused carbon filter is not designed to solve. If you are on a private well, that specialization is decisive. If you are on city water and mainly want chlorine, taste, and odor reduced, both brands are credible and the decision comes down to specs, warranty, and price. Confirm each model's media and any NSF/ANSI certifications on the brand's current spec sheet.</p>

  <h2>Total cost of ownership</h2>
  <p>Look past the sticker to the running cost. Whole-house systems with long-life media mean fewer cartridge swaps, which matters twice for an HSA/FSA buyer: lower recurring spend, and fewer <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement claims</a> to document. SpringWell emphasizes low-maintenance media and a lifetime warranty on its core systems; compare that against the specific Aquasana line you are considering, since maintenance cadence and warranty vary by model.</p>

  <h2>Documentation: the quiet advantage</h2>
  <p>For a tax-advantaged purchase, the smoothest experience is one where the price is clear and the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> is handled at purchase. SpringWell's built-in TrueMed flow does exactly that, keeping your timing and paperwork correct automatically. With any brand, confirm the HSA/FSA path before buying &mdash; see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>

  <h2>Which is right for you?</h2>
  <ul>
    <li><strong>City water, chlorine/taste focus</strong> &rarr; either can work; compare current specs, certifications, and price.</li>
    <li><strong>Well water (iron, sulfur, bacteria)</strong> &rarr; SpringWell, for the dedicated well systems.</li>
    <li><strong>Priority on warranty + low upkeep + built-in checkout</strong> &rarr; SpringWell.</li>
    <li><strong>Chloramine in your supply</strong> &rarr; favor catalytic carbon; confirm the model handles it.</li>
  </ul>

  <h2>The bottom line</h2>
  <p>Both are legitimate whole-house brands. For city water it is a close, spec-by-spec call; for well water, or if a lifetime warranty and a frictionless HSA/FSA checkout matter most, SpringWell has the edge. Verify current pricing and certifications before you commit.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Our pick for most buyers</span>
    <h3>SpringWell Whole House Filter</h3>
    <p>Low-maintenance media, lifetime warranty on core systems, and a built-in HSA/FSA checkout.</p>
    {aff("whole-house","Check price","btn")}
    &nbsp;<a class="btn ghost" href="best-fsa-hsa-eligible-water-filters.html">Compare all picks &rarr;</a>
  </div>
''',
 faq=[
  ("Is SpringWell better than Aquasana?","Both are credible whole-house brands. SpringWell stands out for low-maintenance media, a lifetime warranty on core systems, and a built-in HSA/FSA checkout. Compare current model specs before deciding."),
  ("Are both Aquasana and SpringWell HSA/FSA eligible?","Both can be, with a Letter of Medical Necessity. SpringWell integrates the process into checkout via TrueMed; with any brand, confirm the path before buying."),
  ("Which needs less maintenance?","SpringWell emphasizes long-life media to minimize replacements. Aquasana maintenance varies by model, so check the specific system's filter-change schedule."),
 ])

# ---------- Article #27 ----------
article(
 "springwell-vs-culligan-fsa-hsa.html",
 "SpringWell vs Culligan for FSA/HSA Buyers (2026)",
 "SpringWell vs Culligan for FSA/HSA buyers: transparent direct-to-consumer pricing vs the dealer/quote model, eligibility, and which fits your situation.",
 "SpringWell vs Culligan",
 "SpringWell vs Culligan for FSA/HSA buyers",
 "SpringWell and Culligan take very different approaches: SpringWell sells direct with transparent pricing, while Culligan typically works through local dealers with custom quotes. For an HSA/FSA buyer who needs a clear, documentable price, that difference matters.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick verdict</p>
    <p class="ruling"><b>It comes down to model, not just media.</b> SpringWell's transparent direct-to-consumer pricing and built-in HSA/FSA checkout make documentation simple; Culligan's dealer model offers local service but variable, quote-based pricing.</p>
  </div>

  {disc(0)}

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Factor</th><th>SpringWell</th><th>Culligan</th></tr></thead>
    <tbody>
      <tr><td>Sales model</td><td>Direct-to-consumer</td><td>Local dealers / quote-based</td></tr>
      <tr><td>Pricing</td><td>Published, transparent</td><td>Custom quote (varies by dealer)</td></tr>
      <tr><td>Service</td><td>DIY or local pro install</td><td>Dealer install &amp; service</td></tr>
      <tr><td>HSA/FSA route</td><td class="yes">LMN via TrueMed at checkout</td><td>Varies by dealer</td></tr>
      <tr><td>Warranty</td><td>Lifetime on core systems</td><td>Varies by product/dealer</td></tr>
    </tbody>
  </table>
  </div>

  <h2>The big difference: how you buy</h2>
  <p>Culligan is a long-established name that generally operates through local dealers offering installation, service, and sometimes rentals &mdash; with pricing quoted case by case. SpringWell sells directly with published prices and a self- or pro-install model. Neither approach is wrong, but they suit different buyers.</p>

  <h2>Why the model matters for HSA/FSA</h2>
  <p>For a tax-advantaged purchase, you want a clear price and clean paperwork. SpringWell's transparent pricing and built-in <a href="how-truemed-works-for-water-filters.html">TrueMed checkout</a> mean you know the cost upfront and the Letter of Medical Necessity is issued at purchase &mdash; ideal for documentation. With a dealer quote, confirm in advance how the HSA/FSA path and the LMN will be handled, and get an itemized invoice for your records (see <a href="hsa-fsa-water-filter-reimbursement-checklist.html">the documents checklist</a>).</p>

  <h2>Service and support</h2>
  <p>Culligan's strength is local, hands-on service &mdash; valuable if you want a dealer to manage everything. SpringWell offers strong warranties and phone/online support, with installation by you or a local plumber. If you are comfortable coordinating a standard install, the DTC route is usually more economical and easier to document.</p>

  <h2>Which should you choose?</h2>
  <ul>
    <li><strong>Choose SpringWell if:</strong> you want transparent pricing, a simple HSA/FSA checkout, and strong warranties.</li>
    <li><strong>Choose Culligan if:</strong> you prefer a local dealer to handle everything and value in-person service &mdash; just confirm pricing and the LMN process in writing.</li>
  </ul>

  <h2>Pros and cons at a glance</h2>
  <div class="proscons">
    <div class="pro"><h4>SpringWell strengths</h4><ul>
      <li>Published, transparent pricing</li>
      <li>Built-in HSA/FSA checkout (TrueMed)</li>
      <li>Lifetime warranty on core systems</li>
      <li>DIY or local-pro install &mdash; usually lower total cost</li>
    </ul></div>
    <div class="con"><h4>Culligan strengths</h4><ul>
      <li>Local, hands-on dealer service</li>
      <li>Long-established brand and support network</li>
      <li>Custom solutions for complex water problems</li>
      <li>Dealer handles install and maintenance</li>
    </ul></div>
  </div>

  <h2>Documentation: the practical difference</h2>
  <p>For a tax-advantaged purchase, a known price and a clean invoice matter. SpringWell gives you both upfront, with the Letter of Medical Necessity issued at checkout. With a Culligan dealer, ask before signing how the LMN and HSA/FSA payment will work, and insist on an itemized invoice for your records &mdash; see the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>

  <h2>The honest bottom line</h2>
  <p>If you want a transparent price and frictionless documentation, SpringWell's direct model is the easier path for an HSA/FSA buyer. If your water is complex enough to want a local expert on-site &mdash; or you simply prefer dealer service &mdash; Culligan can be worth the quote, provided you nail down pricing and the eligibility process in writing first.</p>

  <h2>What you actually pay</h2>
  <p>The pricing models could hardly be more different. SpringWell publishes its prices, so you know the cost before you commit. Culligan typically quotes through a local dealer, which means the price varies by location, installation complexity, and sometimes whether you buy or rent. For an HSA/FSA buyer this is not a minor detail: you need a clear, itemized cost and a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> for your records. A published price makes that straightforward; a custom quote means asking up front for an itemized invoice and confirming how the LMN will be handled.</p>

  <h2>When Culligan's dealer model is worth it</h2>
  <p>To be fair to the dealer approach: if you have a complicated install, want a local technician to manage everything, prefer ongoing service visits, or like the option to rent, a Culligan dealer can deliver that hands-on experience in a way a direct-to-consumer brand does not. Some buyers value that service relationship enough to accept variable pricing. The trade-off is transparency and, often, cost.</p>

  <h2>Which is right for you?</h2>
  <ul>
    <li><strong>Want a transparent price and clean HSA/FSA paperwork</strong> &rarr; SpringWell's direct model and built-in checkout.</li>
    <li><strong>Want a dealer to handle everything, or have a complex setup</strong> &rarr; a Culligan dealer &mdash; confirm their HSA/FSA path and get an itemized invoice.</li>
    <li><strong>Comfortable coordinating a standard install</strong> &rarr; the direct route is usually more economical and easier to document.</li>
  </ul>

  <h2>The bottom line</h2>
  <p>Both can deliver good water; the question is how you prefer to buy and document it. If price transparency and effortless HSA/FSA paperwork matter most, SpringWell's model fits. If you want local, full-service handling and will manage the documentation with your dealer, Culligan's approach can suit. Either way, get the price and the letter in writing &mdash; see the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Transparent &amp; documentable</span>
    <h3>SpringWell Whole House Filter</h3>
    <p>Published pricing and a built-in HSA/FSA checkout make the tax-advantaged purchase straightforward.</p>
    {aff("whole-house","Check price","btn")}
    &nbsp;{aff("truemed-eligible-category","Shop eligible systems","btn ghost")}
  </div>
''',
 faq=[
  ("Is SpringWell or Culligan better for FSA/HSA?","SpringWell's transparent pricing and built-in TrueMed checkout make the HSA/FSA purchase and documentation simpler. Culligan's dealer model offers local service but variable, quote-based pricing; confirm the LMN process with the dealer."),
  ("Does Culligan accept HSA/FSA?","It can vary by dealer. Because Culligan is sold locally, confirm in advance how the Letter of Medical Necessity and HSA/FSA payment will be handled, and get an itemized invoice."),
  ("Why choose direct-to-consumer for a tax-advantaged purchase?","A published price and a checkout that issues the Letter of Medical Necessity give you a clear, documentable transaction, which simplifies reimbursement and substantiation."),
 ])

# ======================================================================
#  CLUSTER C (cont.) — Review + roundups (Articles #24, #29-#32)
# ======================================================================

# ---------- Article #24 (Well Water Review) ----------
article(
 "springwell-well-water-filter-system-review.html",
 "SpringWell Well Water Filter Review (2026): Worth It?",
 "Hands-on review of the SpringWell well water filter: what it removes (iron, sulfur, sediment), performance, maintenance, price, and HSA/FSA eligibility.",
 "SpringWell Well Water review",
 "SpringWell Well Water Filter System review (2026)",
 "SpringWell's well water system is built for the problems municipal users never face &mdash; iron staining, rotten-egg sulfur smell, and sediment &mdash; and it is HSA/FSA eligible with a Letter of Medical Necessity. Here is how it performs and who should buy it.",
 f'''
  <div class="rating"><span class="score">4.6</span><span class="out">/ 5</span><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span></div>
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Eligibility ruling</p>
    <p class="ruling"><b>HSA/FSA eligible via TrueMed</b> with a Letter of Medical Necessity &mdash; and well water often makes one of the clearest medical-necessity cases, since you own treatment entirely.</p>
  </div>
  <div class="cta-box" data-reveal>
    <span class="kicker">At a glance</span>
    <h3>SpringWell Whole House Well Water Filter</h3>
    <p class="price">From ~$2,250 &middot; targets iron, sulfur &amp; sediment &middot; lifetime warranty</p>
    {aff("well-water","Check current price","btn")}
  </div>

  <h2>Who it is for</h2>
  <p>If you are on a private well, no utility treats your water &mdash; the responsibility is entirely yours. This system is designed for the classic well-water complaints: orange or brown iron staining on fixtures and laundry, a metallic taste, and the unmistakable rotten-egg odor of hydrogen sulfide. If your water also tests positive for bacteria, you will want to pair it with <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV purification</a>, since this filter targets chemistry and sediment, not microbes.</p>

  <h2>What it removes</h2>
  <p>SpringWell's well system uses an air-injection oxidation process: a pocket of air oxidizes dissolved iron, manganese, and hydrogen sulfide so they become filterable and are flushed away on a regular backwash cycle. In practice that means it tackles:</p>
  <ul>
    <li><strong>Iron</strong> &mdash; the cause of rust staining and metallic taste.</li>
    <li><strong>Manganese</strong> &mdash; black staining and bitter taste.</li>
    <li><strong>Hydrogen sulfide</strong> &mdash; the sulfur/rotten-egg smell.</li>
    <li><strong>Sediment</strong> &mdash; with an appropriate pre-filter stage.</li>
  </ul>
  <p>It does not soften hard water or remove bacteria on its own &mdash; those need a softener and UV respectively, which is why SpringWell offers combos (more below). Always <a href="are-water-test-kits-fsa-hsa-eligible.html">test your well</a> first so you treat the right things.</p>

  <h2>Performance and maintenance</h2>
  <p>The air-injection approach is popular for well water because it uses no chemicals and regenerates with air rather than added media, keeping running costs low. The system backwashes automatically on a schedule, and there is no salt to haul for the filter itself. Maintenance is minimal: periodic checks and an occasional sediment pre-filter change. That low upkeep also means fewer <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement claims</a> to document for reimbursement.</p>

  <h2>Installation</h2>
  <p>It installs at the point of entry, after any pressure tank. Experienced DIYers can manage it; many well owners use a local plumber given the plumbing involved. SpringWell provides guidance and a bypass for servicing.</p>

  <h2>Pairing: UV and softening</h2>
  <p>Well water often needs a treatment train rather than a single box. A common eligible setup is: sediment pre-filtration, this iron/sulfur filter, then <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV</a> for bacteria &mdash; and a softener if your water is also hard. SpringWell sells well-plus-softener combos for exactly this. Documented together for a household with a positive bacteria test or a vulnerable member, the whole train is a strong medical-necessity case.</p>

  <div class="proscons">
    <div class="pro"><h4>What we like</h4><ul>
      <li>Targets the core well issues: iron, sulfur, sediment</li>
      <li>Air-injection &mdash; no chemicals, low running cost</li>
      <li>Automatic backwash; minimal maintenance</li>
      <li>Lifetime warranty; built-in TrueMed checkout</li>
      <li>Combos available for hardness and bacteria</li>
    </ul></div>
    <div class="con"><h4>Keep in mind</h4><ul>
      <li>Does not soften water or kill bacteria alone</li>
      <li>Higher upfront cost; likely exceeds an FSA year limit</li>
      <li>Point-of-entry install &mdash; plan for a plumber</li>
      <li>Requires a water test to size and configure correctly</li>
    </ul></div>
  </div>

  <h2>Price and HSA/FSA eligibility</h2>
  <p>The well filter starts around $2,250, with combos higher. Because that exceeds a single year's FSA limit, an <a href="are-water-filters-hsa-eligible.html">HSA</a> (which rolls over) or a split payment is the usual route. It qualifies as a medical expense with a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, issued through the TrueMed checkout &mdash; see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>

  <h2>How it compares to a city whole-house filter</h2>
  <p>If you are on municipal water, you do not need this system &mdash; a <a href="reviews/springwell-whole-house-water-filter-review.html">city whole-house carbon filter</a> is the right tool. The well system exists precisely because untreated well water has different problems. Match the system to your source; our <a href="index.html#water-type">city vs well</a> section explains the split.</p>

  <h2>How to read your well water test</h2>
  <p>A test tells you exactly what to treat. Key numbers: iron above ~0.3 mg/L causes staining; hydrogen sulfide shows up as odor at low levels; manganese above ~0.05 mg/L stains; hardness (grains per gallon) signals whether you also need softening; and a positive bacteria or nitrate result is a health flag that calls for UV and possibly more. Bring these results to your provider for the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, and use them to size the system. See <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>.</p>

  <h2>Matching add-ons to common well problems</h2>
  <ul>
    <li><strong>Rotten-egg smell + staining:</strong> the air-injection iron/sulfur filter is the core fix.</li>
    <li><strong>Positive bacteria test:</strong> add <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV purification</a>.</li>
    <li><strong>Hard water too:</strong> choose a well + softener combo.</li>
    <li><strong>Low pH / acidic water:</strong> a neutralizer stage may be needed (test for pH).</li>
    <li><strong>Yellow tint (tannins):</strong> a tannin system addresses organic discoloration.</li>
  </ul>

  <h2>Five-year cost of ownership</h2>
  <p>The upfront price is the headline, but well systems are cheap to run: air injection uses no chemicals, the filter backwashes itself, and the main media lasts years. Budget mainly for occasional sediment pre-filters and, if you add UV, an annual lamp. Across five years the total cost of ownership stays low &mdash; and because replacements are infrequent, you file fewer <a href="water-filter-replacement-cartridges-fsa-eligible.html">reimbursement claims</a>. Paired with the pre-tax discount, a quality well system is more affordable than its sticker suggests.</p>

  <h2>Well filter vs ULTRA combo systems</h2>
  <p>For heavily contaminated wells, SpringWell offers ULTRA combinations bundling filtration, softening, and sometimes extra stages. If your test shows multiple severe issues at once, a combo can be more cost-effective and simpler to document as a single medically necessary system than buying stages separately. If your well is mainly iron and sulfur, the standalone filter here is the efficient choice.</p>

  <h2>Is it worth it?</h2>
  <p>For a well household battling iron, sulfur, and sediment, yes &mdash; this is a purpose-built, low-maintenance fix with a lifetime warranty, and the well-water context makes the medical-necessity case unusually clear. The honest caveats: it does not soften or disinfect alone, and the upfront cost favors an HSA or split payment. Test first, configure correctly, and it solves the problem for years.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Bottom line</span>
    <h3>The right system for problem well water</h3>
    <p>If iron, sulfur, or sediment are your reality, this is the eligible, low-maintenance fix &mdash; add UV if bacteria is a concern.</p>
    {aff("well-water","Check price &amp; eligibility","btn")}
    &nbsp;{aff("uv","Add UV purification","btn ghost")}
  </div>
''',
 faq=[
  ("Is the SpringWell well water filter HSA/FSA eligible?","Yes, with a Letter of Medical Necessity through the TrueMed checkout. Well water often makes a clear medical-necessity case because no utility treats it."),
  ("Does it remove bacteria?","No. It targets iron, manganese, sulfur, and sediment. For bacteria, pair it with a UV purification system."),
  ("Does it soften hard water?","Not on its own. If your water is also hard, choose a well-plus-softener combo or add a softener stage."),
  ("Do I need a water test first?","Yes. Testing identifies your iron, sulfur, hardness, and bacteria levels so the system is sized and configured correctly."),
 ],
 schema_extra=[{"@context":"https://schema.org","@type":"Review","itemReviewed":{"@type":"Product","name":"SpringWell Whole House Well Water Filter System","brand":{"@type":"Brand","name":"SpringWell"}},"author":{"@type":"Person","name":AUTHOR},"reviewRating":{"@type":"Rating","ratingValue":"4.6","bestRating":"5"},"publisher":{"@type":"Organization","name":NAME}}])

# ---------- Article #29 (Best Softeners) ----------
article(
 "best-hsa-fsa-eligible-water-softeners.html",
 "Best HSA/FSA-Eligible Water Softeners (2026)",
 "The best HSA/FSA-eligible water softeners for 2026 \u2014 salt-based and salt-free combos that qualify with a Letter of Medical Necessity, compared and ranked.",
 "Best eligible softeners",
 "Best HSA/FSA-eligible water softeners for 2026",
 "Softeners are harder to qualify than filters, so the smartest eligible buys are filter + softener combos &mdash; you get a defensible medical-necessity case plus hard-water relief in one system. Here are the best options for 2026.",
 f'''
  {disc(0)}
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Read this first</p>
    <p class="ruling"><b>A softener alone is hard to justify; a filter + softener combo is the eligible play.</b> All picks below qualify with a Letter of Medical Necessity through TrueMed &mdash; see <a href="are-water-softeners-fsa-hsa-eligible.html">why softeners are conditional</a>.</p>
  </div>

  <h2>How we picked</h2>
  <p>We prioritized systems where filtration (the stronger medical-necessity case) is bundled with softening, plus low maintenance, warranty, and a built-in HSA/FSA checkout. For the eligibility nuance, see our guide to <a href="are-water-softeners-fsa-hsa-eligible.html">water softener eligibility</a>.</p>

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>System</th><th>Best for</th><th>Type</th><th>Price (approx.)</th></tr></thead>
    <tbody>
      <tr><td>Filter + Salt-Based Softener</td><td>Maximum scale protection</td><td>Combo</td><td>$2,250&ndash;$4,320</td></tr>
      <tr><td>Filter + Salt-Free (FutureSoft)</td><td>Low-sodium / low-maintenance</td><td>Combo</td><td>$2,340&ndash;$4,050</td></tr>
      <tr><td>2-in-1 Filter + Salt Softener</td><td>Space-saving single unit</td><td>Combo</td><td>$2,263&ndash;$2,804</td></tr>
    </tbody>
  </table>
  </div>

  <div class="cards">
    <div class="card" data-reveal>
      <span class="tag">Editor's pick</span>
      <h3>Filter + Salt-Based Softener</h3>
      <p>True ion-exchange softening plus whole-house filtration &mdash; the most thorough scale protection, ideal for very hard water and spotless fixtures.</p>
      <p class="price">From ~$2,250</p>
      {aff("filter-softener-combo","Check price","btn")}
      <p style="margin:.7rem 0 0"><a class="more" href="reviews/springwell-filter-softener-combo-review.html">Read the review &rarr;</a></p>
    </div>
    <div class="card" data-reveal>
      <span class="tag">Best low-sodium</span>
      <h3>Filter + Salt-Free (FutureSoft)</h3>
      <p>Conditions minerals so they do not scale, with no added sodium, no salt, no electricity, and no wastewater. Great for low-sodium households.</p>
      <p class="price">From ~$2,340</p>
      {aff("salt-free-combo","Check price","btn")}
    </div>
    <div class="card" data-reveal>
      <span class="tag">Space-saving</span>
      <h3>2-in-1 Filter + Softener</h3>
      <p>Filtration and softening in a single combined unit &mdash; a tidy option where space is tight.</p>
      <p class="price">From ~$2,263</p>
      {aff("2in1-combo","Check price","btn")}
    </div>
  </div>

  <h2>Salt-based vs salt-free: which to choose</h2>
  <p><strong>Salt-based</strong> truly removes hardness minerals via ion exchange &mdash; the classic "soft water" feel and maximum scale protection, at the cost of salt top-ups and a drain line. <strong>Salt-free</strong> conditions minerals so they do not form scale, without adding sodium or producing wastewater &mdash; lower maintenance and the better pick if sodium is a documented concern. Our <a href="reviews/springwell-filter-softener-combo-review.html">combo review</a> goes deeper.</p>

  <h2>The eligibility angle</h2>
  <p>Remember the rule: a softener alone is usually a comfort purchase, but the filtration in these combos carries a genuine health rationale, which is what supports the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. Be honest about your reason, and confirm coverage with your administrator. Ready to buy? See <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>

  <h2>What hard water does (and doesn't do) to your health</h2>
  <p>Be clear-eyed: hard water is mostly a household nuisance &mdash; scale, spotty dishes, dry-feeling skin &mdash; not, by itself, a disease. That is exactly why a softener alone is a weak FSA/HSA case. Where a provider may get involved is a documented skin condition they connect to water quality; the evidence is mixed and developing, so let your clinician decide. The filtration in a combo, by contrast, addresses recognized contaminant risks, which is the part that carries the medical-necessity weight.</p>

  <h2>Sizing and maintenance</h2>
  <p>Salt-based softeners are sized by grain capacity to match your hardness and household size; undersized units regenerate too often, oversized ones waste salt. Plan for periodic salt top-ups and a drain line. Salt-free conditioners skip salt, electricity, and wastewater entirely, trading maximum softening for near-zero maintenance. Match the choice to your water and your tolerance for upkeep &mdash; and document the filtration rationale for eligibility per the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Best for hard water</span>
    <h3>Shop eligible filter + softener systems</h3>
    <p>Solve filtration and hardness in one documented, eligible purchase.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("Are water softeners HSA/FSA eligible?","A softener alone is hard to justify because hardness is often a comfort issue. A filter + softener combo is easier to qualify because the filtration component has a clear medical-necessity case &mdash; with a Letter of Medical Necessity."),
  ("Salt-based or salt-free for FSA/HSA?","Either can be eligible in a combo. Choose salt-free if a low-sodium need is documented; choose salt-based for maximum scale protection."),
  ("Why buy a combo instead of a standalone softener?","The filtration half supports the medical-necessity case, making a combo easier to document than a softener bought purely for comfort."),
 ])

# ---------- Article #30 (Best Under-Sink / RO) ----------
article(
 "best-fsa-eligible-under-sink-ro-water-filters.html",
 "Best FSA-Eligible Under-Sink & RO Water Filters (2026)",
 "The best FSA/HSA-eligible under-sink and reverse osmosis water filters for 2026 \u2014 point-of-use systems that qualify with a Letter of Medical Necessity.",
 "Best under-sink / RO",
 "Best FSA-eligible under-sink &amp; RO water filters (2026)",
 "If your concern is the water you drink and cook with &mdash; not the whole house &mdash; an under-sink or reverse osmosis system is the affordable, eligible answer. Here are the best point-of-use picks for 2026.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick take</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> Under-sink and RO systems are the lowest-cost eligible route and the best fit for renters and drinking-water-only concerns. See <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</p>
  </div>

  <h2>How we picked</h2>
  <p>For point-of-use we weighted contaminant reduction (certifications to {NSF}, especially NSF/ANSI 58 for RO), footprint under a sink, filter cost and lifespan, and a working HSA/FSA path. These systems treat one tap rather than the whole home &mdash; if you need whole-home coverage, see the <a href="best-fsa-hsa-eligible-water-filters.html">whole-house roundup</a> instead.</p>

  <div class="cards">
    <div class="card" data-reveal>
      <span class="tag">Editor's pick</span>
      <h3>Moen Reverse Osmosis</h3>
      <p>Compact under-sink RO delivering bottled-quality drinking and cooking water. The lowest-cost eligible option and renter-friendly.</p>
      <p class="price">~$399</p>
      {aff("moen-ro","Check price","btn")}
    </div>
    <div class="card" data-reveal>
      <span class="tag">Why RO</span>
      <h3>Broad contaminant removal</h3>
      <p>RO membranes reduce lead, nitrates, PFAS, and many dissolved contaminants &mdash; the issues that most often drive a medical-necessity case for drinking water.</p>
      <p class="price">Point-of-use</p>
      <p style="margin:.4rem 0 0"><a class="more" href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility &rarr;</a></p>
    </div>
    <div class="card" data-reveal>
      <span class="tag">Renters</span>
      <h3>No-install options</h3>
      <p>Point-of-use systems can move with you and need no whole-home plumbing &mdash; ideal for apartments. See our <a href="index.html">renter-friendly guidance</a>.</p>
      <p class="price">Flexible</p>
    </div>
  </div>

  <h2>Who under-sink / RO suits best</h2>
  <ul>
    <li><strong>Renters and apartments</strong> &mdash; no whole-home install, moves with you.</li>
    <li><strong>Drinking-water-only concerns</strong> &mdash; targets exactly what you consume.</li>
    <li><strong>Tight budgets</strong> &mdash; the cheapest eligible category; see <a href="cheapest-fsa-hsa-eligible-water-filters.html">cheapest eligible options</a>.</li>
  </ul>

  <h2>What to know before buying</h2>
  <p>RO removes minerals along with contaminants, so some units remineralize for taste; it also uses a storage tank and a little wastewater, which is why it suits drinking and cooking rather than whole-home supply. Replacement filters and membranes can be reimbursed on the same basis &mdash; keep receipts per the <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a>.</p>

  <h2>How reverse osmosis works</h2>
  <p>RO forces water through a semipermeable membrane that blocks dissolved contaminants, typically across several stages: sediment and carbon pre-filters, the RO membrane itself, and a final polishing filter (some add remineralization). The result is very low-contaminant water at the tap. Certification to {NSF} NSF/ANSI 58 is the signal that a system's RO claims are independently verified.</p>

  <h2>Maintenance and what to expect</h2>
  <p>Plan on pre/post filter changes every 6&ndash;12 months and a membrane every 2&ndash;3 years &mdash; all reimbursable on the same basis as the system when documented. RO also produces some wastewater and stores treated water in a small tank, so flow is slower than a faucet filter. None of this affects eligibility; it just confirms RO is for drinking and cooking, not whole-home supply. For the bigger picture, weigh it against a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a>.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Best budget / POU</span>
    <h3>Moen Reverse Osmosis</h3>
    <p>Clean drinking water at the tap for around $399 &mdash; the most affordable eligible system, through the TrueMed checkout.</p>
    {aff("moen-ro","Check price","btn")}
  </div>
''',
 faq=[
  ("Are reverse osmosis systems FSA/HSA eligible?","Yes, with a Letter of Medical Necessity. RO is a strong fit when the documented concern is in your drinking water, such as lead or nitrates."),
  ("Is under-sink or whole-house better for FSA/HSA?","Under-sink is cheaper and treats one tap; whole-house treats every tap and makes a broader medical-necessity case. Choose based on whether your concern is drinking water only or whole-home."),
  ("Can renters use these?","Yes. Point-of-use systems need no whole-home plumbing and can move with you, making them ideal for apartments."),
 ])

# ---------- Article #31 (Cheapest) ----------
article(
 "cheapest-fsa-hsa-eligible-water-filters.html",
 "Cheapest FSA/HSA-Eligible Water Filters (2026)",
 "The cheapest FSA/HSA-eligible water filter options for 2026 \u2014 the lowest-cost ways to buy filtration with pre-tax dollars, from under-sink RO to budget systems.",
 "Cheapest eligible options",
 "Cheapest FSA/HSA-eligible water filter options (2026)",
 "You do not need to spend thousands to put pre-tax dollars toward cleaner water. Here are the lowest-cost FSA/HSA-eligible filters for 2026 &mdash; and a reminder that buying pre-tax makes any of them cheaper still.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick take</p>
    <p class="ruling"><b>The cheapest eligible route is point-of-use.</b> An under-sink RO system is the lowest-cost system that qualifies with a Letter of Medical Necessity &mdash; and pre-tax dollars discount it further by your tax rate.</p>
  </div>

  <h2>The lowest-cost eligible options</h2>
  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Option</th><th>Approx. price</th><th>Best for</th><th>Eligible?</th></tr></thead>
    <tbody>
      <tr><td>Under-sink reverse osmosis</td><td>~$399</td><td>Drinking water, renters</td><td class="yes">With LMN</td></tr>
      <tr><td>Whole-house cartridge system</td><td>$660&ndash;$1,116</td><td>Smaller homes, budget POE</td><td class="yes">With LMN</td></tr>
      <tr><td>Point-of-use / pitcher (other brands)</td><td>Lowest</td><td>Single-tap, minimal need</td><td>With LMN service</td></tr>
    </tbody>
  </table>
  </div>

  <div class="cards">
    <div class="card" data-reveal>
      <span class="tag">Cheapest eligible system</span>
      <h3>Moen Reverse Osmosis</h3>
      <p>Around $399 for clean drinking and cooking water at one tap &mdash; the lowest-cost system with a built-in HSA/FSA checkout.</p>
      <p class="price">~$399</p>
      {aff("moen-ro","Check price","btn")}
    </div>
    <div class="card" data-reveal>
      <span class="tag">Budget whole-house</span>
      <h3>Whole House Cartridge System</h3>
      <p>The most affordable way to treat the whole home &mdash; cartridge-based, good for smaller households on a budget.</p>
      <p class="price">From ~$660</p>
      {aff("cartridge","Check price","btn")}
    </div>
  </div>

  <h2>Pre-tax makes "cheap" cheaper</h2>
  <p>Here is the part people miss: because you buy with pre-tax HSA/FSA dollars, you avoid income tax on the purchase &mdash; effectively a 20&ndash;37% discount depending on your bracket. A $399 RO system at a 30% rate effectively costs around $280. See the full <a href="index.html#savings">savings math</a> for how the discount scales.</p>

  <h2>The trade-offs of going cheap</h2>
  <p>Lower-cost point-of-use options treat one tap, not the whole home, and may use more frequent replacement filters. That is fine if your concern is drinking water only; if you need whole-home coverage, weigh a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> against the recurring cost. Either way, the eligibility rule is the same &mdash; a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>Upfront price vs ongoing cost</h2>
  <p>"Cheapest" has two meanings. The lowest <em>upfront</em> price is usually a pitcher or faucet filter; the lowest <em>five-year</em> cost may be a system with longer-life filters and fewer replacements. For drinking water only, under-sink RO hits a sweet spot: modest upfront cost and reasonable filter life. Factor replacement cartridges into any comparison &mdash; and remember each can be reimbursed with documentation.</p>

  <h2>Cheapest by use case</h2>
  <ul>
    <li><strong>Renter, drinking water only:</strong> under-sink RO (~$399).</li>
    <li><strong>Small home, whole-house on a budget:</strong> cartridge system (from ~$660).</li>
    <li><strong>Single tap, minimal need:</strong> a point-of-use pitcher via an LMN service.</li>
  </ul>
  <p>See the <a href="best-fsa-eligible-under-sink-ro-water-filters.html">under-sink &amp; RO roundup</a> for the point-of-use picks in detail.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Lowest-cost eligible</span>
    <h3>Start with under-sink RO</h3>
    <p>The most affordable eligible system &mdash; clean drinking water for around $399, less after the pre-tax discount.</p>
    {aff("moen-ro","Check price","btn")}
  </div>
''',
 faq=[
  ("What is the cheapest FSA/HSA-eligible water filter?","An under-sink reverse osmosis system, around $399, is the lowest-cost system with a built-in HSA/FSA checkout. Pitcher and faucet filters can be cheaper but treat less and use an LMN service."),
  ("Does buying pre-tax actually save money on a cheap filter?","Yes. You avoid income tax on the purchase, an effective 20-37% discount by your bracket, so even an inexpensive system costs less."),
  ("Is a cheap filter worth it?","If your concern is drinking water only, a point-of-use system is a sensible, eligible choice. For whole-home exposure, weigh a whole-house system instead."),
 ])

# ---------- Article #32 (Savings) ----------
article(
 "springwell-truemed-savings-coupons.html",
 "SpringWell Savings: Stack Pre-Tax + Discounts (2026)",
 "How to maximize savings on a SpringWell water filter: stack pre-tax HSA/FSA dollars with current promotions, free shipping, and financing. Here is the playbook.",
 "Maximize your savings",
 "SpringWell savings: stacking pre-tax dollars and discounts",
 "The biggest discount on a water filter is not a coupon &mdash; it is buying with pre-tax HSA/FSA dollars. Here is how to stack that with current promotions, free shipping, and timing to pay the least.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The playbook</p>
    <p class="ruling"><b>Pre-tax is the big lever.</b> Buying with HSA/FSA via a Letter of Medical Necessity effectively discounts the price by your tax rate (20&ndash;37%) &mdash; usually far more than any coupon. Stack promotions on top.</p>
  </div>

  <h2>1. The pre-tax discount (the biggest one)</h2>
  <p>Because HSA/FSA dollars are set aside before income tax, an eligible purchase avoids that tax entirely &mdash; an effective 20&ndash;37% off depending on your bracket. On a $2,000 system at a 30% rate, that is roughly $600 saved. This dwarfs typical coupons, and it is the reason the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> step is worth it. See the <a href="index.html#savings">savings math</a>.</p>

  <h2>2. Watch for current promotions and free shipping</h2>
  <p>SpringWell runs periodic promotions and frequently includes free shipping and a money-back trial window on systems. These change over time, so check the current offers at checkout rather than relying on a stale code. Combine an active promotion with the pre-tax discount and the savings compound.</p>

  <h2>3. Consider financing for cash flow</h2>
  <p>If a whole-house system's upfront cost is a hurdle, financing can spread it out &mdash; useful when you are reimbursing from an HSA over time. Financing does not change eligibility; you still document the purchase normally. See <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a> for split-payment options too.</p>

  <h2>4. Time it around the FSA deadline</h2>
  <p>If you have an <a href="are-water-filters-fsa-eligible.html">FSA</a> balance expiring December 31, spending it on a qualifying system converts money you would forfeit into a durable purchase &mdash; effectively a 100% "discount" on funds that would otherwise vanish. Plan ahead so the letter and payment clear before the deadline.</p>

  <h2>How to stack it all</h2>
  <p>The optimal play: buy an eligible system during an active promotion, pay with pre-tax HSA/FSA dollars via the TrueMed checkout, and time an expiring FSA balance into it. That layers a promotion discount, your tax-rate discount, and zero forfeited funds &mdash; the lowest realistic out-of-pocket cost.</p>

  <h2>A worked savings stack</h2>
  <p>Picture a $2,000 system bought during a promotion that includes free shipping, paid with an expiring $1,500 FSA balance plus $500 from an HSA, at a 30% bracket. The pre-tax treatment saves roughly $600 in tax; the expiring FSA money would otherwise have been forfeited entirely; and free shipping trims a little more. Your effective out-of-pocket lands well below the sticker &mdash; that is the power of stacking.</p>

  <h2>Mistakes that cost you savings</h2>
  <ul>
    <li>Letting an FSA balance expire instead of spending it on a qualifying system.</li>
    <li>Skipping the Letter of Medical Necessity and paying with after-tax money.</li>
    <li>Relying on an old coupon code instead of checking current offers.</li>
    <li>Forgetting that <a href="water-filter-replacement-cartridges-fsa-eligible.html">replacement filters</a> can also be reimbursed.</li>
  </ul>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Stack your savings</span>
    <h3>See current SpringWell systems and offers</h3>
    <p>Check today's promotions, then pay with pre-tax dollars through the TrueMed checkout.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
    &nbsp;{aff("whole-house","See the whole-house filter","btn ghost")}
  </div>
''',
 faq=[
  ("What's the best way to save on a SpringWell water filter?","Buy with pre-tax HSA/FSA dollars via a Letter of Medical Necessity, which effectively discounts the price by your tax rate (20-37%) &mdash; usually more than any coupon. Stack a current promotion on top."),
  ("Does SpringWell offer coupons?","Promotions and free shipping change over time, so check current offers at checkout rather than relying on a fixed code. The pre-tax discount is the larger and more reliable saving."),
  ("Can I combine a discount with pre-tax savings?","Yes. An active promotion plus the pre-tax discount, and timing an expiring FSA balance, gives the lowest out-of-pocket cost."),
 ])

# ======================================================================
#  CLUSTER D — Account types & audiences (Articles #33-#39)
# ======================================================================

# ---------- #33 HSA vs FSA ----------
article(
 "hsa-vs-fsa-water-filter.html",
 "HSA vs FSA for a Water Filter: Which Should You Use?",
 "HSA vs FSA for a water filter: both can be eligible with a Letter of Medical Necessity, but rollover, limits, and deadlines differ. Here is how to choose.",
 "HSA vs FSA",
 "HSA vs FSA for a water filter: which should you use?",
 "Both an HSA and an FSA can pay for an eligible water filter with a Letter of Medical Necessity &mdash; so the choice comes down to how each account behaves. The short rule: use an HSA for larger systems you save toward, and an FSA to spend a balance before it expires.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick decision</p>
    <p class="ruling"><b>HSA for big or future purchases; FSA to beat the year-end deadline.</b> Both require a Letter of Medical Necessity. If you have both accounts, spend the expiring FSA first and reserve the HSA for the larger system.</p>
  </div>

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>Factor</th><th>HSA</th><th>FSA</th></tr></thead>
    <tbody>
      <tr><td>Funds roll over?</td><td class="yes">Yes, indefinitely</td><td class="no">Often expire Dec 31</td></tr>
      <tr><td>Account is yours?</td><td class="yes">Yes (portable)</td><td>Tied to employer</td></tr>
      <tr><td>Requires HDHP?</td><td>Yes</td><td>No</td></tr>
      <tr><td>Best for</td><td>Larger whole-house systems</td><td>Spending a balance now</td></tr>
      <tr><td>Needs LMN for a filter?</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
    </tbody>
  </table>
  </div>

  <h2>When the HSA wins</h2>
  <p>Because HSA funds roll over and the account is yours for life, it is ideal for a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> that costs more than one year of contributions &mdash; save up, then buy. You also get the triple tax advantage (pre-tax in, tax-free growth, tax-free qualified withdrawals). See <a href="are-water-filters-hsa-eligible.html">Are water filters HSA eligible?</a></p>

  <h2>When the FSA wins</h2>
  <p>If you have an <a href="are-water-filters-fsa-eligible.html">FSA</a> balance that disappears on December 31, a qualifying filter is one of the best ways to use it &mdash; you convert "use it or lose it" money into a durable home upgrade. The catch is timing: get the Letter of Medical Necessity and complete the purchase before the deadline.</p>

  <h2>Using both</h2>
  <p>Have an HSA and an FSA (or a limited-purpose FSA)? Spend the expiring FSA money first on the qualified portion, then use the HSA for the remainder or for future replacements. Either way the rule is the same &mdash; the filter needs a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. See the full <a href="index.html#accounts">account comparison</a> on our main guide.</p>

  <h2>The one HSA gotcha: the HDHP requirement</h2>
  <p>You can only contribute to an HSA if you are enrolled in a qualifying high-deductible health plan. An FSA has no such requirement and is offered through an employer. So your eligibility to <em>fund</em> each account may decide the question before preferences do &mdash; if you do not have an HDHP, an FSA (or HRA) is your route. Existing HSA balances remain usable for an eligible filter even in a year you cannot contribute.</p>

  <h2>Which should a first-time buyer pick?</h2>
  <p>If you are buying a one-time whole-house system and have both accounts, the simplest plan is: drain any expiring FSA balance into the purchase first (so none is forfeited), then cover the rest from the HSA, which keeps growing for future replacements. If you only have one account, use it &mdash; both work with the same Letter of Medical Necessity.</p>

  <h2>Contribution limits to keep in mind (verify yearly)</h2>
  <p>Both accounts have annual contribution limits set by the IRS that change each year and differ for individual vs family coverage (HSAs add a catch-up amount at 55+). Because a whole-house system can exceed a single year's FSA limit, savers often lean on an HSA across two years. Check the current year's figures in {IRS969} before planning a large purchase.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Either account works</span>
    <h3>Buy with whichever account fits</h3>
    <p>SpringWell's TrueMed checkout issues the Letter of Medical Necessity and accepts your HSA or FSA card.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("Should I use my HSA or FSA for a water filter?","Use an HSA for larger systems you save toward (funds roll over) and an FSA to spend a balance before it expires. Both require a Letter of Medical Necessity."),
  ("Can I use both an HSA and FSA on one purchase?","Often yes, in sequence. Spend an expiring FSA balance first, then use the HSA for the rest. Document the qualified portion."),
  ("Do both require a Letter of Medical Necessity?","Yes. The filter is not automatically eligible under either account; a licensed provider must document the medical need."),
 ])

# ---------- #34 HRA ----------
article(
 "can-you-use-hra-for-water-filter.html",
 "Can You Use an HRA for a Water Filter? (2026)",
 "Whether you can use an HRA for a water filter depends entirely on your employer's plan. Here is how HRAs differ from HSA/FSA and what to check.",
 "HRA eligibility",
 "Can you use an HRA for a water filter?",
 "Maybe &mdash; an HRA is employer-funded, so what it covers is defined by your specific plan. A water filter can qualify when the plan allows it and you have a Letter of Medical Necessity. Here is what to check.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>It depends on your employer's plan.</b> Unlike HSAs and FSAs, an HRA's eligible expenses are set by the employer. A filter may qualify with a Letter of Medical Necessity if the plan permits it &mdash; always confirm first.</p>
  </div>

  <h2>What an HRA is</h2>
  <p>A Health Reimbursement Arrangement is funded entirely by your employer, who also defines which expenses it reimburses within IRS rules. That is the key difference from an <a href="hsa-vs-fsa-water-filter.html">HSA or FSA</a>: there is more variation, because your plan document &mdash; not just the IRS list &mdash; governs what is covered.</p>

  <h2>Why eligibility varies</h2>
  <p>Some HRAs are broad and cover the same qualified medical expenses an FSA would; others are narrow (for example, limited to specific categories or to post-deductible expenses). A water filter, which already requires a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> to be a qualified medical expense, will only be reimbursable if your particular HRA design allows that category.</p>

  <h2>What to check with your employer or administrator</h2>
  <ul>
    <li>Does the HRA cover general qualified medical expenses, or only specific categories?</li>
    <li>Does it accept a Letter of Medical Necessity for durable medical equipment?</li>
    <li>How do you submit a claim, and what documentation is required?</li>
  </ul>
  <p>Get the answer in writing if you can, and keep it with your records. If your HRA will not cover it, an <a href="are-water-filters-hsa-eligible.html">HSA</a> or <a href="are-water-filters-fsa-eligible.html">FSA</a> may be the better route.</p>

  <h2>HRA types you might have</h2>
  <p>"HRA" covers several designs, and the type shapes what is reimbursable. An <strong>integrated HRA</strong> pairs with a group health plan and often follows broad qualified-expense rules. A <strong>QSEHRA</strong> (small employers) and an <strong>ICHRA</strong> (individual-coverage HRA) reimburse defined expenses and sometimes premiums, with employer-set rules. Knowing which you have tells you where to look: your plan's summary document lists eligible categories, and that is what determines whether a documented water filter qualifies.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} If your plan allows it</span>
    <h3>Eligible SpringWell systems</h3>
    <p>If your HRA covers it (with a Letter of Medical Necessity), SpringWell's eligible systems issue the letter at checkout.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("Can I use an HRA for a water filter?","Possibly. HRAs are employer-defined, so coverage varies. A filter may qualify with a Letter of Medical Necessity if your specific plan allows that category &mdash; confirm with your administrator."),
  ("Why is an HRA different from an FSA?","An HRA is funded and defined by your employer, who sets eligible expenses within IRS rules, so there is more plan-to-plan variation than with an FSA."),
  ("What if my HRA won't cover it?","Consider an HSA or FSA instead, both of which can cover an eligible filter with a Letter of Medical Necessity."),
 ])

# ---------- #35 LPFSA ----------
article(
 "lpfsa-water-filtration-eligible.html",
 "Can You Use an LPFSA for Water Filtration? (2026)",
 "A Limited-Purpose FSA (LPFSA) usually covers only dental and vision, so a water filter typically does not qualify. Here is the nuance and your options.",
 "LPFSA eligibility",
 "Can you use a Limited-Purpose FSA (LPFSA) for water filtration?",
 "Usually not &mdash; a Limited-Purpose FSA is generally restricted to dental and vision expenses, so a whole-house water filter typically does not qualify. Here is why, the narrow exception, and what to use instead.",
 f'''
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Usually no.</b> An LPFSA is limited to dental and vision so you can keep contributing to an HSA. A water filter falls outside that scope &mdash; use your HSA instead.</p>
  </div>

  <h2>What an LPFSA is</h2>
  <p>A Limited-Purpose FSA exists to pair with a Health Savings Account. Because you cannot have a general-purpose FSA and contribute to an HSA at the same time, the LPFSA restricts itself to <strong>dental and vision</strong> expenses, leaving your HSA free for everything else. That restriction is exactly why a water filter usually does not fit.</p>

  <h2>Why a water filter typically doesn't qualify</h2>
  <p>A whole-house or drinking-water filter is general medical equipment, not a dental or vision expense, so it falls outside the LPFSA's purpose. Even with a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, the category is the barrier here, not the documentation.</p>

  <h2>The post-deductible nuance</h2>
  <p>Some LPFSAs expand to cover broader expenses once you meet your health plan's deductible (a "post-deductible" feature). If your plan has this, a filter might become reimbursable later in the year &mdash; but this is plan-specific, so confirm with your administrator before counting on it.</p>

  <h2>What to use instead</h2>
  <p>The natural fit is the <a href="are-water-filters-hsa-eligible.html">HSA</a> the LPFSA is designed to protect &mdash; it covers an eligible filter with a Letter of Medical Necessity and rolls over year to year. See <a href="hsa-vs-fsa-water-filter.html">HSA vs FSA</a> to plan your accounts.</p>

  <h2>LPFSA vs HSA: a quick example</h2>
  <p>Say you fund both an LPFSA and an HSA. You use the LPFSA for a dental crown and new glasses &mdash; exactly what it is for &mdash; which leaves your HSA balance intact. When you later buy an eligible whole-house filter, you draw on the HSA, not the LPFSA. The two accounts are designed to work together this way: the LPFSA handles dental and vision, the HSA handles general qualified medical expenses like a documented water filter. Trying to push the filter through the LPFSA simply will not fit its purpose.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Use your HSA instead</span>
    <h3>Eligible SpringWell systems</h3>
    <p>Pay with your HSA via the TrueMed checkout, which issues the Letter of Medical Necessity at purchase.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("Can I use an LPFSA for a water filter?","Usually not. An LPFSA is limited to dental and vision expenses, so a water filter falls outside its scope. Use the paired HSA instead."),
  ("What is an LPFSA for?","It covers dental and vision so you can keep contributing to an HSA at the same time, since a general-purpose FSA would make you HSA-ineligible."),
  ("Is there any way a filter qualifies under an LPFSA?","Only if your plan has a post-deductible feature that broadens coverage after you meet your deductible. Confirm with your administrator."),
 ])

# ---------- #36 Families with children ----------
article(
 "fsa-eligible-water-filters-families-young-children.html",
 "FSA-Eligible Water Filters for Families With Kids",
 "For families with young children, a water filter can be FSA/HSA eligible with a Letter of Medical Necessity \u2014 especially for lead. Here is what to know.",
 "Families with children",
 "FSA-eligible water filters for families with young children",
 "Young children are more vulnerable to certain water contaminants, which is why filtration for a family home can be a well-supported FSA/HSA purchase with a Letter of Medical Necessity. Here is a calm, practical guide to what matters.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> A household with young children and a documented contaminant concern (lead is the classic example) is exactly the kind of preventive case the medical-necessity rule is built for.</p>
  </div>

  {disc(0)}

  <h2>Why young children change the calculus</h2>
  <p>Children's developing bodies absorb some contaminants more readily than adults, which is why agencies treat them as a priority group. For lead in particular, the <a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">EPA</a> states there is no safe level, and the risk is highest for infants and young children. That makes preventive filtration in a family home a reasonable, documentable health measure &mdash; not just a preference.</p>

  <h2>What to filter for</h2>
  <ul>
    <li><strong>Lead</strong> &mdash; especially in homes built before the 1986 lead-pipe ban.</li>
    <li><strong>Nitrates</strong> &mdash; a particular concern for infants (relevant on well water).</li>
    <li><strong>Bacteria</strong> &mdash; on well water, where a UV stage may be warranted.</li>
    <li><strong>Chlorine by-products</strong> &mdash; for skin-sensitive kids, a whole-home consideration.</li>
  </ul>
  <p>The right first step is a <a href="are-water-test-kits-fsa-hsa-eligible.html">water test</a> &mdash; it identifies the actual risk and strengthens your documentation.</p>

  <h2>Which systems fit a family home</h2>
  <p>For a documented lead concern, a dedicated <a href="best-fsa-hsa-eligible-water-filters.html">lead and cyst system</a> is the targeted choice; for broad coverage across every tap and shower, a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> makes the strongest case. If only drinking water is the concern, an under-sink <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> unit is an affordable option.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} For lead concerns</span>
    <h3>SpringWell Lead &amp; Cyst Removal System</h3>
    <p>Dedicated lead and cyst reduction &mdash; a strong fit for families with young children, eligible via the TrueMed checkout.</p>
    {aff("lead-cyst","Check price","btn")}
  </div>

  <h2>How to make it eligible</h2>
  <p>Bring your water test and your household situation to a provider, who can issue the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> &mdash; or use the checkout route that issues it for you. Then pay with your HSA/FSA card and keep your records. See <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>. This page is educational, not medical advice &mdash; your provider determines what is appropriate for your family.</p>

  <h2>How to talk to your pediatrician</h2>
  <p>If your child's doctor is the one documenting the need, keep it concrete: mention your home's age (lead-pipe risk), share any water test results, and note your child's age. Pediatricians are familiar with lead-exposure prevention, so framing the request around reducing a documented contaminant for a young child is straightforward. Ask specifically for "a Letter of Medical Necessity for FSA/HSA purposes."</p>

  <h2>Renting with young children</h2>
  <p>If you rent and cannot install a whole-house system, a point-of-use <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> unit covers drinking and cooking water without permanent plumbing &mdash; and it moves with you. It can still be eligible with the same documentation, making it a practical choice for families in apartments.</p>

''',
 faq=[
  ("Is a water filter for my kids FSA/HSA eligible?","It can be, with a Letter of Medical Necessity. A household with young children and a documented contaminant concern such as lead is a strong preventive case."),
  ("What should families filter for?","Commonly lead (older homes), nitrates and bacteria (well water), and chlorine by-products. Test your water first to identify the actual risk."),
  ("Which system is best for a family?","A lead and cyst system for documented lead, a whole-house system for broad coverage, or under-sink RO if only drinking water is the concern."),
 ])

# ---------- #37 Pregnancy ----------
article(
 "hsa-fsa-water-filters-pregnancy.html",
 "HSA/FSA Water Filters for Pregnancy: What to Know",
 "During pregnancy, a water filter can be HSA/FSA eligible with a Letter of Medical Necessity \u2014 lead and nitrates are key concerns. A calm, factual guide.",
 "Pregnancy",
 "HSA/FSA water filters for pregnancy: what to know",
 "Pregnancy is a recognized higher-sensitivity window for certain water contaminants, so filtration can be a well-supported HSA/FSA purchase with a Letter of Medical Necessity. Here is a calm, factual overview &mdash; with the reminder that your provider guides what is right for you.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> Pregnancy is widely recognized as a higher-sensitivity period for contaminants like lead and nitrates, which supports a preventive filtration case when documented by a provider.</p>
  </div>

  {disc(0)}

  <h2>Why pregnancy is treated as higher-risk</h2>
  <p>Public-health agencies flag pregnancy as a window when reducing certain exposures matters more. The <a href="https://www.epa.gov/ground-water-and-drinking-water/basic-information-about-lead-drinking-water" target="_blank" rel="noopener">EPA</a> notes lead is especially harmful during pregnancy, and nitrates in water are a recognized concern as well. This is context, not cause for alarm &mdash; most water is fine &mdash; but it is why a documented filtration purchase can be reasonable during this period.</p>

  <h2>What to consider filtering</h2>
  <ul>
    <li><strong>Lead</strong> &mdash; particularly in older homes with legacy plumbing.</li>
    <li><strong>Nitrates</strong> &mdash; chiefly a well-water concern.</li>
    <li><strong>Bacteria</strong> &mdash; on well water, where UV may be appropriate.</li>
  </ul>
  <p>Start with a <a href="are-water-test-kits-fsa-hsa-eligible.html">water test</a> so any decision is based on your actual water, and discuss the results with your provider.</p>

  <h2>Systems that fit</h2>
  <p>For drinking and cooking water, an under-sink <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> system is a focused, affordable option; for whole-home coverage, a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> or a <a href="fsa-eligible-water-filters-families-young-children.html">lead and cyst system</a> may be appropriate &mdash; especially useful to keep in place after the baby arrives.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Talk to your provider</span>
    <h3>Eligible systems for the household</h3>
    <p>If filtration is right for you, SpringWell's eligible systems issue the Letter of Medical Necessity at checkout.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <h2>A note on guidance</h2>
  <p>This page is informational and not medical advice. Your obstetric provider is the right person to decide whether filtration is appropriate for your situation and to issue or support the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. If you have concerns about your water during pregnancy, raise them at your next visit.</p>

  <h2>Questions to ask at your prenatal visit</h2>
  <p>If you want to raise it with your provider, a few focused questions help: Given my home's age and water source, is reducing lead or nitrate exposure worth addressing? Would you support a Letter of Medical Necessity for a water filtration system? Are there specific contaminants you would want me to test for? Bringing a <a href="are-water-test-kits-fsa-hsa-eligible.html">water test</a> to the conversation makes it concrete and quick.</p>

  <h2>City vs well water during pregnancy</h2>
  <p>On <strong>city water</strong>, the main question is usually lead from household plumbing, addressed by a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house</a> or under-sink system. On <strong>well water</strong>, nitrates and bacteria matter more, since no utility treats your supply &mdash; testing is essential, and UV may be appropriate. Match the response to your source rather than guessing.</p>

''',
 faq=[
  ("Can I buy a water filter with HSA/FSA during pregnancy?","Yes, with a Letter of Medical Necessity. Pregnancy is recognized as a higher-sensitivity period for contaminants like lead and nitrates, which supports a documented filtration case."),
  ("What should I filter for during pregnancy?","Commonly lead and, on well water, nitrates and bacteria. Test your water first and discuss the results with your provider."),
  ("Should I be worried about my tap water?","Most tap water is fine. This is about reasonable, documented precaution for specific contaminants, not alarm. Your provider can advise based on your water and health."),
 ])

# ---------- #38 Immunocompromised ----------
article(
 "fsa-hsa-water-filtration-immunocompromised.html",
 "FSA/HSA Water Filtration for Immunocompromised Homes",
 "For immunocompromised households, water filtration and UV can be HSA/FSA eligible with a Letter of Medical Necessity \u2014 one of the clearest cases. Here is how.",
 "Immunocompromised households",
 "FSA/HSA water filtration for immunocompromised households",
 "For households with an immunocompromised member, reducing exposure to waterborne pathogens is a recognized health priority &mdash; which makes filtration and UV one of the clearest HSA/FSA medical-necessity cases, with a Letter of Medical Necessity.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; and a strong case.</b> Because immunocompromised people face higher risk from waterborne pathogens, provider-documented filtration and UV map cleanly to medical necessity.</p>
  </div>

  {disc(0)}

  <h2>Why immunocompromised households are different</h2>
  <p>People with weakened immune systems &mdash; for example, those undergoing chemotherapy, transplant recipients, or others advised by their care team &mdash; can be more vulnerable to pathogens that healthier people tolerate. The <a href="https://www.cdc.gov/healthywater/drinking/" target="_blank" rel="noopener">CDC</a> notes this heightened vulnerability and the value of extra precautions around water for some patients. That clinical context is what makes a documented water-treatment purchase a strong medical-necessity case.</p>

  <h2>What to use</h2>
  <ul>
    <li><strong>UV purification</strong> &mdash; inactivates bacteria, viruses, and protozoa; the most direct pathogen barrier. See <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV eligibility</a>.</li>
    <li><strong>Whole-house filtration</strong> &mdash; reduces contaminants across every tap; pairs with UV (which needs clear water to work).</li>
    <li><strong>Reverse osmosis</strong> &mdash; for high-purity drinking and cooking water at the tap.</li>
  </ul>

  <h2>City vs well water</h2>
  <p>On <strong>well water</strong>, where there is no central disinfection, UV plus filtration is especially sensible. On <strong>city water</strong>, the utility already disinfects, so the focus is usually contaminant reduction and a possible extra barrier on the advice of a care team. Either way, <a href="are-water-test-kits-fsa-hsa-eligible.html">test first</a> and follow your provider's guidance.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Pathogen protection</span>
    <h3>UV + whole-house filtration</h3>
    <p>A UV stage paired with whole-house filtration is the recognized setup &mdash; both eligible via the TrueMed checkout.</p>
    {aff("uv","See UV purification","btn")}
    &nbsp;{aff("whole-house","See whole-house filter","btn ghost")}
  </div>

  <h2>How to make it eligible</h2>
  <p>Because the health rationale is clear, documentation is usually straightforward: your care team can support the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, and you keep it with your receipt. This page is informational, not medical advice &mdash; decisions about water precautions for an immunocompromised person should be made with the treating care team.</p>

  <h2>Pathogens of particular concern</h2>
  <p>Care teams sometimes flag organisms like <em>Cryptosporidium</em> and <em>Giardia</em> &mdash; chlorine-tolerant protozoa &mdash; as relevant for severely immunocompromised patients, along with certain bacteria. UV is effective against a broad range of these, and a fine filtration stage helps with the larger cysts. The point is not to catalog every microbe but to understand why a disinfection step is recommended for some patients: it adds a barrier the body might otherwise have to handle alone.</p>

  <h2>Layering protection sensibly</h2>
  <p>For the highest-risk situations, care teams may suggest a belt-and-suspenders approach: filtration to clear particles and contaminants, UV to inactivate pathogens, and sometimes point-of-use <a href="is-reverse-osmosis-fsa-hsa-eligible.html">reverse osmosis</a> for drinking water. You do not need to over-build &mdash; follow your team's guidance &mdash; but each layer can be documented as part of one medically necessary setup.</p>

''',
 faq=[
  ("Is water filtration HSA/FSA eligible for immunocompromised people?","Yes, with a Letter of Medical Necessity, and it is one of the clearest medical-necessity cases because immunocompromised people face higher risk from waterborne pathogens."),
  ("What's best for pathogen protection?","UV purification inactivates microbes and is the most direct barrier, usually paired with filtration so the water is clear enough for UV to work."),
  ("Does it matter if I'm on city or well water?","Yes. Well water has no central disinfection, so UV plus filtration is especially sensible. On city water, focus on contaminant reduction and follow your care team's advice."),
 ])

# ---------- #39 Self-employed ----------
article(
 "self-employed-hsa-home-water-filtration.html",
 "Self-Employed? Use an HSA for Home Water Filtration",
 "Self-employed with an HSA? Here is how to use it for an eligible home water filter \u2014 the rules, the tax advantage, and record-keeping for your situation.",
 "Self-employed",
 "Self-employed? How to use an HSA for home water filtration",
 "If you are self-employed with a high-deductible health plan, your HSA is a powerful, flexible way to pay for an eligible home water filter with pre-tax dollars. Here is how it works and what to keep for your records.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Quick answer</p>
    <p class="ruling"><b>Eligible &mdash; with a Letter of Medical Necessity.</b> A self-employed HSA holder can buy an eligible filter with pre-tax dollars, and the HSA's rollover and portability suit a larger one-time purchase well.</p>
  </div>

  <h2>HSA basics for the self-employed</h2>
  <p>If you carry your own qualifying high-deductible health plan (HDHP), you can open and fund an HSA &mdash; no employer required. Contributions are deductible (an above-the-line deduction on your return), the balance rolls over indefinitely, and the account is entirely yours. That flexibility makes the HSA the natural vehicle for a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> you might save toward across the year. See <a href="are-water-filters-hsa-eligible.html">Are water filters HSA eligible?</a></p>

  <h2>The tax advantage</h2>
  <p>For the self-employed, every pre-tax dollar matters. Using HSA funds for an eligible filter means you never pay income tax on that money &mdash; an effective discount equal to your marginal rate. Because you also deduct HSA contributions, the benefit is built in at both ends. As always, treat figures as illustrative and confirm with a tax professional; this is not tax advice.</p>

  <h2>Eligibility and the LMN</h2>
  <p>The rule is the same as for anyone: the filter needs a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> tying it to a health condition. The <a href="how-truemed-works-for-water-filters.html">TrueMed checkout</a> issues it without an appointment &mdash; convenient if your schedule is your own. See <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>

  <h2>Record-keeping matters more for you</h2>
  <p>Self-employed taxpayers should be especially tidy with documentation. Keep the Letter of Medical Necessity, itemized receipt, and proof of payment together, and retain them for years &mdash; HSAs can be reviewed well after the fact. Our <a href="hsa-fsa-water-filter-reimbursement-checklist.html">documents checklist</a> makes this simple.</p>

  <h2>Coverage tier and contribution limits</h2>
  <p>Your HSA contribution limit depends on whether your HDHP covers just you or your family, with an extra catch-up amount once you turn 55. If you are saving toward a larger <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a>, family-tier limits make it easier to accumulate enough in a single year. Limits change annually, so verify the current figures before you plan &mdash; see {IRS969}.</p>

  <h2>Don't forget state taxes</h2>
  <p>Most states follow the federal treatment, so HSA contributions and qualified withdrawals are tax-advantaged at the state level too &mdash; but a few states treat HSAs differently. Since the self-employed feel every tax dollar directly, it is worth confirming your state's rules (or asking your tax professional) so you know the full size of the discount on an eligible filter.</p>


  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Put your HSA to work</span>
    <h3>Eligible SpringWell systems</h3>
    <p>The TrueMed checkout issues your Letter of Medical Necessity and accepts your HSA card &mdash; no appointment needed.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("Can a self-employed person use an HSA for a water filter?","Yes, if you have a qualifying high-deductible health plan and an HSA. The filter needs a Letter of Medical Necessity, like any eligible buyer."),
  ("What's the tax benefit for the self-employed?","HSA contributions are deductible and qualified withdrawals are tax-free, so an eligible filter is effectively discounted by your marginal rate. Confirm specifics with a tax professional."),
  ("Do I need to keep extra records?","It is wise. Keep the Letter of Medical Necessity, itemized receipt, and payment proof for years, since HSAs can be reviewed long after the purchase."),
 ])

# ======================================================================
#  CLUSTER E — Condition / Contaminant bridge (Articles #40-#48)
# ======================================================================
EPAWATER='<a href="https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations" target="_blank" rel="noopener">EPA drinking water standards</a>'
EPACCR='<a href="https://www.epa.gov/ccr" target="_blank" rel="noopener">EPA Consumer Confidence Report guide</a>'

# ---------- #40 Lead ----------
article(
 "lead-in-drinking-water-fsa-eligible-filtration.html",
 "Lead in Drinking Water: Risks & FSA-Eligible Filters",
 "Lead in drinking water has no safe level. Learn the health risks, how to test, which filters remove lead, and how they qualify for FSA/HSA with an LMN.",
 "Lead in drinking water",
 "Lead in drinking water: health risks and FSA-eligible filtration",
 "Lead is the contaminant that most clearly justifies water filtration as a health measure &mdash; there is no safe level, and the risk falls hardest on children and during pregnancy. Here is where lead comes from, how to test, what removes it, and how a lead filter qualifies for FSA/HSA.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Why it matters</p>
    <p class="ruling"><b>No safe level &mdash; and a strong eligibility case.</b> Because the {EPALEAD} states there is no safe level of lead in drinking water, reducing it is a textbook medical-necessity reason for a filter, with a Letter of Medical Necessity.</p>
  </div>

  <h2>Where lead in water comes from</h2>
  <p>Lead rarely originates at the treatment plant; it usually enters water from the plumbing between the main and your tap &mdash; lead service lines, older brass fixtures, and lead solder, common in homes built before the 1986 lead-pipe ban. Because the source is your own plumbing, two homes on the same street can have very different lead levels, which is why testing at <em>your</em> tap matters.</p>

  <h2>The health risks</h2>
  <p>Lead is a cumulative toxin. The {EPALEAD} and {CDC} are clear that infants, young children, and pregnant women are most vulnerable, with effects on development at low exposures. This is the basis for treating lead reduction as preventive care rather than a comfort upgrade &mdash; see our guidance for <a href="fsa-eligible-water-filters-families-young-children.html">families with children</a> and <a href="hsa-fsa-water-filters-pregnancy.html">pregnancy</a>.</p>

  <h2>How to test for lead</h2>
  <p>Your utility's <a href="how-to-read-water-quality-report-ccr.html">annual report</a> reflects water at the plant, not your tap, so for lead you should test at home with a certified kit or lab &mdash; see <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>. A documented result is also the strongest support for your Letter of Medical Necessity.</p>

  <h2>What removes lead</h2>
  <ul>
    <li><strong>Reverse osmosis</strong> &mdash; highly effective for drinking-water lead; see <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</li>
    <li><strong>Lead-certified filters</strong> &mdash; look for certification to {NSF} (NSF/ANSI 53 for lead).</li>
    <li><strong>Whole-house lead &amp; cyst systems</strong> &mdash; for reduction at every tap.</li>
  </ul>

  <h2>What the numbers actually mean</h2>
  <p>Lead regulation uses a few terms worth understanding. The EPA's <strong>maximum contaminant level goal (MCLG)</strong> for lead is <strong>zero</strong> &mdash; the level with no known safe exposure. Separately, utilities are judged against an <strong>action level</strong>, historically <strong>15 parts per billion (ppb)</strong>. Under the 2024 Lead and Copper Rule Improvements, that action level drops to <strong>10 ppb</strong>, with most water systems transitioning by the November 2027 compliance date, alongside mandatory lead service line inventories and replacement.</p>
  <p>Here is the crucial part: the action level is a <em>treatment trigger</em> that measures whether a utility's corrosion control is working &mdash; it is not a safety threshold for your glass. A system can be "in compliance" while lead still enters water from the plumbing inside <em>your</em> home. That gap is exactly why point-of-use or whole-house filtration matters even on a compliant supply.</p>

  <h2>How lead gets into your water</h2>
  <p>Lead is picked up as water sits in contact with lead service lines, lead solder, or older brass fixtures &mdash; so levels rise the longer water stagnates and tend to be higher with hot water. Two homes on the same main can differ enormously depending on their internal plumbing and how recently the tap was used.</p>

  <h2>Steps you can take today</h2>
  <ul>
    <li><strong>Run the cold tap</strong> for 30&ndash;120 seconds before drinking if water has sat for hours.</li>
    <li><strong>Use cold water</strong> for drinking, cooking, and especially infant formula &mdash; hot water leaches more lead.</li>
    <li><strong>Clean faucet aerators</strong> periodically, where lead particles collect.</li>
  </ul>
  <p>These reduce exposure but do not remove lead reliably &mdash; a certified filter is the dependable fix, and the documented health rationale is what supports eligibility.</p>

  <h2>Choosing a lead-certified filter</h2>
  <p>Match the certification to the claim: look for <strong>NSF/ANSI 53</strong> (lead reduction) on carbon-block filters and <strong>NSF/ANSI 58</strong> for reverse osmosis. Certification to {NSF} confirms the system was independently tested to reduce lead specifically &mdash; not just "filtered water" in general.</p>

  <h2>Lead on well water</h2>
  <p>Wells are not immune: lead can come from older well components, pumps, or household plumbing, and there is no utility monitoring at all. Well owners should include lead in periodic <a href="are-water-test-kits-fsa-hsa-eligible.html">testing</a> and treat accordingly.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Targeted lead reduction</span>
    <h3>SpringWell Lead &amp; Cyst Removal System</h3>
    <p>Dedicated lead and cyst reduction, eligible via the TrueMed checkout with a Letter of Medical Necessity.</p>
    {aff("lead-cyst","Check price","btn")}
  </div>

  <h2>How lead filtration qualifies for FSA/HSA</h2>
  <p>Because lead has recognized health effects, a provider can readily connect a lead-reducing filter to preventing harm &mdash; the essence of the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. Test, document, and buy through a checkout that issues the letter; see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>. This page is educational, not medical advice.</p>
''',
 faq=[
  ("Is a lead water filter FSA/HSA eligible?","Yes, with a Letter of Medical Necessity. Because there is no safe level of lead, reducing it is a strong medical-necessity case."),
  ("What filter removes lead best?","Reverse osmosis is highly effective for drinking-water lead; lead-certified filters (NSF/ANSI 53) and whole-house lead and cyst systems also work. Match the choice to whether you need one tap or every tap."),
  ("Do I need to test for lead?","Yes. Lead usually comes from household plumbing, so test at your own tap rather than relying on the utility's plant-level report."),
 ])

# ---------- #41 PFAS ----------
article(
 "pfas-tap-water-filtration-hsa-fsa.html",
 "PFAS in Tap Water: Filtration & HSA/FSA Coverage",
 "PFAS 'forever chemicals' are a growing tap-water concern. Learn the health risks, which filters remove PFAS, and how filtration qualifies for HSA/FSA.",
 "PFAS forever chemicals",
 "PFAS 'forever chemicals' in tap water: filtration and HSA/FSA coverage",
 "PFAS are persistent industrial chemicals increasingly detected in drinking water, and federal attention is rising fast. Here is what PFAS are, the health concerns, which filters actually reduce them, and how PFAS filtration qualifies for HSA/FSA.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Why it matters</p>
    <p class="ruling"><b>A rising, documentable concern.</b> With the {EPAPFAS} tightening federal limits, a documented PFAS detection is a solid basis for medically necessary filtration &mdash; with a Letter of Medical Necessity.</p>
  </div>

  <h2>What PFAS are</h2>
  <p>PFAS (per- and polyfluoroalkyl substances) are a large family of synthetic chemicals used in nonstick, waterproof, and stain-resistant products. They are nicknamed "forever chemicals" because they resist breaking down and accumulate in the environment and the body. They reach drinking water through industrial discharge, firefighting foam, and contaminated groundwater.</p>

  <h2>The health concerns and the regulatory shift</h2>
  <p>Regulators have linked PFAS exposure to a range of health concerns, and the {EPAPFAS} has moved to set enforceable limits for certain PFAS in public water systems &mdash; a significant change that has put PFAS firmly on the public agenda. For an HSA/FSA buyer, a documented PFAS result turns filtration into a defensible preventive measure.</p>

  <h2>What removes PFAS</h2>
  <ul>
    <li><strong>Reverse osmosis</strong> &mdash; among the most effective for PFAS at the drinking tap.</li>
    <li><strong>Activated carbon</strong> &mdash; effective for many PFAS, especially high-quality carbon with adequate contact time.</li>
    <li><strong>Specialized PFAS systems</strong> &mdash; designed and tested specifically for PFAS reduction.</li>
  </ul>
  <p>Look for certification covering PFAS reduction, and confirm the specific compounds addressed.</p>

  <h2>Where the PFAS rules stand (2026)</h2>
  <p>In April 2024 the EPA finalized the first national drinking water limits for six PFAS, setting enforceable maximum contaminant levels for PFOA and PFOS at 4 parts per trillion each. As of 2026 the picture is evolving: the EPA has moved to <em>keep</em> the 4 ppt PFOA/PFOS limits while proposing to extend utility compliance deadlines to 2031, and has separately proposed rescinding the limits for four other PFAS. Because this is actively changing &mdash; and subject to litigation &mdash; check the {EPAPFAS} for the current standard rather than relying on a fixed figure.</p>
  <p>What does not change for you: a documented PFAS detection in your water supports filtration as a reasonable health measure regardless of where the rulemaking lands.</p>

  <h2>How to find out if you have PFAS</h2>
  <p>Start with your utility &mdash; many now publish PFAS monitoring results, and federal testing of public systems has expanded. For a private well, or to confirm your own tap, use a certified laboratory test, since PFAS require specialized lab analysis rather than a strip test. A before/after test also tells you whether your filter is working.</p>

  <h2>What removes PFAS &mdash; and what doesn't</h2>
  <ul>
    <li><strong>Reverse osmosis</strong> &mdash; among the most effective for PFAS at the drinking tap.</li>
    <li><strong>High-quality activated carbon</strong> &mdash; effective for many PFAS, especially longer-chain compounds, with adequate carbon and contact time.</li>
    <li><strong>Anion exchange</strong> &mdash; used in some specialized PFAS systems.</li>
  </ul>
  <p>Note what does <em>not</em> work: <strong>boiling concentrates PFAS rather than removing them</strong>, and standard sediment filters do nothing for them. Look for certification (such as NSF/ANSI 53 for PFOA/PFOS, or 58 for RO) confirming the specific compounds addressed.</p>

  <h2>Whole-house or point-of-use for PFAS?</h2>
  <p>Because the main PFAS exposure route from water is drinking and cooking, a point-of-use RO system covers the priority efficiently. A whole-house approach adds coverage where PFAS is widespread in the supply or where you want every tap addressed; the right answer depends on your test results and budget &mdash; see <a href="whole-house-vs-under-sink-water-filter-hsa-fsa.html">whole-house vs under-sink</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} PFAS reduction</span>
    <h3>SpringWell PFAS &amp; whole-house options</h3>
    <p>Address PFAS across the home or at the tap &mdash; eligible via the TrueMed checkout with a Letter of Medical Necessity.</p>
    {aff("pfas","See PFAS system","btn")}
    &nbsp;{aff("whole-house","See whole-house filter","btn ghost")}
  </div>

  <h2>How PFAS filtration qualifies</h2>
  <p>The pattern is the same as any contaminant: a provider documents the need based on your situation and a detection, issuing the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. Test first &mdash; see <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a> &mdash; then buy through a checkout that issues the letter. Educational only, not medical advice.</p>
''',
 faq=[
  ("Is a PFAS water filter HSA/FSA eligible?","Yes, with a Letter of Medical Necessity. A documented PFAS detection supports filtration as a preventive health measure."),
  ("What removes PFAS from water?","Reverse osmosis and high-quality activated carbon are effective for many PFAS, as are systems designed specifically for PFAS. Check certification for the specific compounds."),
  ("Are PFAS regulated?","The EPA has moved to set enforceable limits for certain PFAS in public water systems. Check the EPA's PFAS resources for current standards."),
 ])

# ---------- #42 Nitrates ----------
article(
 "nitrates-well-water-filtration.html",
 "Nitrates in Well Water: Risks & Eligible Filtration",
 "Nitrates in well water are a serious concern for infants and pregnancy. Learn the risks, how to test, what removes nitrates, and HSA/FSA eligibility.",
 "Nitrates in well water",
 "Nitrates in well water: risks and medically-necessary filtration",
 "Nitrates are one of the most health-significant well-water contaminants, especially for infants and during pregnancy. Here is where they come from, why they matter, how to test, what actually removes them, and how nitrate filtration qualifies for HSA/FSA.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Why it matters</p>
    <p class="ruling"><b>A genuine health risk, not a nuisance.</b> Nitrates are regulated under {EPAWATER} because of real infant risk &mdash; which makes nitrate filtration a clear medical-necessity case with a Letter of Medical Necessity.</p>
  </div>

  <h2>Where nitrates come from</h2>
  <p>Nitrates enter groundwater mainly from agricultural fertilizer, manure, and septic systems, so private wells in farming areas are most at risk. Because nitrates are colorless, odorless, and tasteless, you cannot detect them without testing.</p>

  <h2>The health risk</h2>
  <p>High nitrate levels are most dangerous for infants under six months, in whom they can interfere with the blood's ability to carry oxygen (sometimes called "blue baby syndrome"). Pregnant women are also advised to limit exposure. The {CDC} and EPA treat nitrates as a priority contaminant, which is why a documented result strongly supports filtration as preventive care &mdash; relevant for <a href="hsa-fsa-water-filters-pregnancy.html">pregnancy</a> and <a href="fsa-eligible-water-filters-families-young-children.html">families with young children</a>.</p>

  <h2>How to test</h2>
  <p>Well owners should test for nitrates at least annually, and immediately if there is an infant in the home. See <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>; a quantified result is also key documentation for your Letter of Medical Necessity.</p>

  <h2>What removes nitrates</h2>
  <p>This is important: carbon filters do <strong>not</strong> remove nitrates. Effective options are <strong>reverse osmosis</strong> (for drinking water) and <strong>anion-exchange</strong> systems. Match the method to the need &mdash; for an infant's drinking water, RO at the kitchen tap is often the practical choice; see <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</p>

  <h2>The number that matters: 10 mg/L</h2>
  <p>The EPA's maximum contaminant level for nitrate is <strong>10 mg/L</strong> (measured as nitrogen), set specifically to protect infants. Below that, public water is considered compliant &mdash; but private wells are not monitored by anyone, so a well can exceed it without warning. Because nitrate is colorless, odorless, and tasteless, testing is the only way to know your level.</p>

  <h2>Why testing and timing matter</h2>
  <p>Nitrate levels in wells can rise seasonally &mdash; after heavy rain, snowmelt, or fertilizer application &mdash; so a single clean test is not a permanent all-clear. Health agencies advise testing wells for nitrate at least annually, and promptly if you are pregnant or have an infant in the home. A quantified, dated result is also the documentation a provider needs for your <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>What removes nitrates (and a safety warning)</h2>
  <p>This bears repeating because it is widely misunderstood: <strong>carbon filters and standard softeners do not remove nitrate</strong>, and <strong>boiling makes it worse</strong> by concentrating it. The methods that work are <strong>reverse osmosis</strong>, <strong>anion exchange</strong>, and <strong>distillation</strong>. For an infant's drinking water, RO at the kitchen tap is usually the practical, eligible choice; for whole-home nitrate, anion exchange is used.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} For well households</span>
    <h3>SpringWell well water systems</h3>
    <p>Address well-water contaminants with eligible systems &mdash; pair with RO for drinking-water nitrates. Letter of Medical Necessity via the TrueMed checkout.</p>
    {aff("well-water","See well water systems","btn")}
    &nbsp;{aff("moen-ro","See RO system","btn ghost")}
  </div>

  <h2>Eligibility</h2>
  <p>Because nitrates carry recognized infant and pregnancy risk, a provider can readily document medical necessity. Test, get the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, and buy through the checkout that issues it. Educational only, not medical advice.</p>
''',
 faq=[
  ("Is a nitrate water filter FSA/HSA eligible?","Yes, with a Letter of Medical Necessity. Nitrates carry recognized infant and pregnancy risk, making filtration a clear medical-necessity case."),
  ("What removes nitrates from water?","Reverse osmosis and anion-exchange systems remove nitrates. Carbon filters do not, so do not rely on a standard carbon filter for nitrate reduction."),
  ("Who is most at risk from nitrates?","Infants under six months are most vulnerable, and pregnant women are advised to limit exposure. Well households should test, especially with an infant at home."),
 ])

# ---------- #43 Chlorine & Chloramine ----------
article(
 "chlorine-chloramine-health-filtration.html",
 "Chlorine & Chloramine in Tap Water: Filtration Options",
 "Chlorine and chloramine disinfect city water but affect taste, skin, and more. Learn the differences, health context, and filters that reduce them.",
 "Chlorine &amp; chloramine",
 "Chlorine and chloramine: health concerns and filtration options",
 "Chlorine and chloramine keep municipal water safe from microbes, but many people want to reduce them for taste, skin comfort, or disinfection-byproduct concerns. Here is the difference between the two, the health context, and which filters actually reduce them.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The balance</p>
    <p class="ruling"><b>Useful at the plant, often unwanted at the tap.</b> Disinfectants protect the supply, but reducing them at home can be reasonable &mdash; and with a documented health rationale, a whole-house filter qualifies for HSA/FSA.</p>
  </div>

  <h2>Why utilities use them</h2>
  <p>Chlorine and chloramine (chlorine combined with ammonia) are disinfectants that keep pathogens at bay as water travels to your home &mdash; a genuine public-health success. The trade-off is that you receive residual disinfectant and its by-products at the tap. Standards for these are set under {EPAWATER}.</p>

  <h2>Chlorine vs chloramine</h2>
  <p>The practical difference matters for filtration: <strong>chlorine</strong> dissipates and is relatively easy to filter with standard carbon; <strong>chloramine</strong> is more stable and harder to remove, requiring <em>catalytic</em> carbon and adequate contact time. Many utilities have switched to chloramine, so check what yours uses on your <a href="how-to-read-water-quality-report-ccr.html">annual report</a>.</p>

  <h2>Health and comfort context</h2>
  <p>For most people, disinfectant residual is about taste, odor, and skin/hair comfort rather than acute danger. Some report skin irritation, and disinfection by-products are an area of ongoing study. Where a provider connects a skin or respiratory condition to chlorinated water, reduction becomes a documentable health measure &mdash; see <a href="hard-water-health-skin-softening.html">hard water and skin</a> and <a href="are-shower-filters-fsa-hsa-eligible.html">shower filters</a>.</p>

  <h2>What removes them</h2>
  <p>A whole-house <strong>catalytic carbon</strong> filter reduces both chlorine and chloramine across every tap and shower &mdash; the most complete approach. Point-of-use carbon works for drinking water. For chloramine specifically, confirm the system is rated for it.</p>

  <h2>How much is in your water</h2>
  <p>The EPA sets a maximum residual disinfectant level of <strong>4 mg/L</strong> for chlorine and chloramine &mdash; enough to keep the supply safe all the way to the tap. Your <a href="how-to-read-water-quality-report-ccr.html">annual report</a> lists the disinfectant used and typical levels, which tells you both what to expect and which filter media you need.</p>

  <h2>Disinfection by-products: the bigger reason some filter</h2>
  <p>When chlorine reacts with natural organic matter in water, it forms <strong>disinfection by-products</strong> such as trihalomethanes (TTHMs) and haloacetic acids (HAA5), which the EPA regulates under {EPAWATER}. For some households this &mdash; more than the disinfectant itself &mdash; is the motivation to filter. Activated carbon reduces both the residual disinfectant and many of these by-products.</p>

  <h2>Where to filter: whole-house, shower, or tap</h2>
  <p>A <strong>whole-house catalytic carbon</strong> filter addresses chlorine and chloramine everywhere, including the <a href="are-shower-filters-fsa-hsa-eligible.html">shower</a>, where inhalation and skin contact occur. A point-of-use carbon filter handles drinking water only. For chloramine specifically, confirm the system uses catalytic carbon and provides enough contact time &mdash; ordinary carbon struggles with it.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Whole-home reduction</span>
    <h3>SpringWell Whole House Filter</h3>
    <p>Catalytic carbon reduces chlorine and chloramine at every tap &mdash; eligible via the TrueMed checkout with a Letter of Medical Necessity.</p>
    {aff("whole-house","Check price","btn")}
  </div>

  <h2>Eligibility</h2>
  <p>Taste alone is a personal preference; a documented health reason is what supports a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. Be honest about your reason and confirm with your administrator. Educational only, not medical advice.</p>
''',
 faq=[
  ("What's the difference between chlorine and chloramine?","Chlorine dissipates and is easy to filter with standard carbon; chloramine (chlorine plus ammonia) is more stable and needs catalytic carbon to remove effectively."),
  ("Is a chlorine filter FSA/HSA eligible?","It can be, with a Letter of Medical Necessity, when a provider connects reduction to a health condition such as a skin or respiratory issue. Taste alone is a personal preference."),
  ("How do I know if my water has chloramine?","Check your utility's annual Consumer Confidence Report, which states the disinfectant used. Many utilities have switched from chlorine to chloramine."),
 ])

# ---------- #44 Hard water & skin ----------
article(
 "hard-water-health-skin-softening.html",
 "Hard Water and Your Skin: When Softening Is Justified",
 "Is hard water bad for your health or skin? Here's what the evidence says, when softening is medically justified, and how eligible combos work.",
 "Hard water &amp; skin",
 "Hard water and your health/skin: when softening is justified",
 "Hard water is mostly a household nuisance, but many people ask whether it affects their skin or health. Here is an honest look at what the evidence says, when a provider might consider softening medically justified, and how eligible filter + softener combos work.",
 f'''
  {disc(0)}
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The honest take</p>
    <p class="ruling"><b>Mostly a nuisance, sometimes a documented health factor.</b> Hard water alone rarely qualifies; a provider-documented skin condition, or the filtration in a combo system, is what supports a Letter of Medical Necessity.</p>
  </div>

  <h2>What hard water is</h2>
  <p>Hard water simply contains higher levels of dissolved calcium and magnesium. It causes scale on fixtures, spotty dishes, reduced soap lather, and a "dry" feel on skin and hair. None of these are diseases, which is the crux of the eligibility question.</p>

  <h2>What the evidence says about skin</h2>
  <p>Research on hard water and skin conditions such as eczema is mixed and still developing &mdash; some studies suggest an association, particularly in early childhood, while others are inconclusive. The honest position is that hard water may aggravate some sensitive skin but is not established as a cause of disease. That is why claims here should be modest and a clinician's judgment should drive any medical-necessity case. General context is available from the {CDC}.</p>

  <h2>When softening may be justified</h2>
  <p>A standalone softener bought for comfort is a personal expense. Where it can be different is a documented dermatological condition a provider connects to water quality, or a low-sodium need that makes a salt-free conditioner preferable. The provider decides &mdash; see <a href="are-water-softeners-fsa-hsa-eligible.html">water softener eligibility</a>.</p>

  <h2>Salt-based vs salt-free</h2>
  <p>Salt-based softeners remove hardness via ion exchange (maximum scale protection, needs salt and a drain). Salt-free conditioners prevent scale without adding sodium (lower maintenance, better for low-sodium households). Pairing either with filtration creates a combo whose filtration half carries the clearer health rationale.</p>

  <h2>How hard is your water?</h2>
  <p>Hardness is measured in grains per gallon (gpg) or mg/L. As a rough guide: under 1 gpg is soft, 3.5&ndash;7 gpg is moderately hard, 7&ndash;10.5 gpg is hard, and above 10.5 gpg is very hard. Your <a href="how-to-read-water-quality-report-ccr.html">water report</a> or a simple test tells you where you fall &mdash; useful for sizing a softener and for deciding whether you need one at all.</p>

  <h2>What the research actually shows</h2>
  <p>The honest summary: studies exploring hard water and skin conditions like eczema are <em>mixed</em>. Some observational research links harder water to a higher rate of eczema, particularly in infants, but controlled trials of water softeners have not clearly demonstrated benefit, and the mechanism is not established. So hard water may aggravate some sensitive skin, but it is not proven to cause disease. General health context is available from the {CDC}. This is why any medical-necessity claim here should rest on a clinician's judgment, not marketing.</p>

  <h2>What softening changes &mdash; and what it doesn't</h2>
  <p>Softening reliably reduces scale, improves soap lather, and extends appliance life &mdash; real quality-of-life benefits. What it does not do is remove contaminants or treat a medical condition on its own. That distinction is the heart of why a standalone softener is hard to make eligible, while the filtration in a <a href="reviews/springwell-filter-softener-combo-review.html">combo</a> carries the health rationale.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Filtration + softening</span>
    <h3>SpringWell Filter + Softener Combo</h3>
    <p>Solve filtration and hardness in one eligible system &mdash; salt-based or salt-free, via the TrueMed checkout.</p>
    {aff("filter-softener-combo","Check price","btn")}
    &nbsp;{aff("salt-free-combo","See salt-free","btn ghost")}
  </div>

  <h2>Eligibility</h2>
  <p>Be honest about your reason: comfort is personal, a documented condition is medical. A provider issues the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>; combos are easier to support than standalone softeners. Educational only, not medical advice.</p>
''',
 faq=[
  ("Is hard water bad for your health?","Hard water is mostly a nuisance rather than a health hazard. Evidence on skin conditions like eczema is mixed; it may aggravate some sensitive skin but is not established as a cause of disease."),
  ("Is a water softener FSA/HSA eligible?","A softener alone is hard to justify because hardness is usually a comfort issue. With a documented health condition, or as part of a filter + softener combo, it can qualify with a Letter of Medical Necessity."),
  ("Salt-based or salt-free for skin concerns?","Either can help with scale; salt-free avoids adding sodium. Discuss with your provider, who determines whether softening is appropriate for a documented condition."),
 ])

# ---------- #45 Bacteria ----------
article(
 "bacteria-well-water-uv-filtration.html",
 "Bacteria in Well Water: UV Purification & Filtration",
 "Bacteria and pathogens in well water are a real health risk. Learn how to test, how UV and filtration work, and HSA/FSA eligibility for treatment.",
 "Bacteria in well water",
 "Bacteria and pathogens in well water: UV and filtration",
 "Private wells have no central disinfection, so bacteria and other pathogens are a genuine, sometimes serious risk. Here is how to test for them, why UV paired with filtration is the standard answer, and how treatment qualifies for HSA/FSA.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Why it matters</p>
    <p class="ruling"><b>A clear health risk on wells &mdash; and a strong eligibility case.</b> Because no utility disinfects your well, provider-documented UV and filtration map cleanly to medical necessity.</p>
  </div>

  <h2>Why wells are different</h2>
  <p>City water is disinfected before it reaches you; well water is not. That means microbial safety is entirely your responsibility. Contamination can come from surface runoff, septic systems, flooding, or a compromised well cap, and it often gives no taste or smell warning &mdash; testing is the only way to know.</p>

  <h2>Pathogens of concern</h2>
  <p>Routine well testing looks for <strong>total coliform</strong> and <strong>E. coli</strong> as indicators that disease-causing organisms may be present. Protozoa such as <em>Giardia</em> and <em>Cryptosporidium</em>, and various bacteria and viruses, can also occur. The {CDC} provides guidance on private-well safety and testing frequency.</p>

  <h2>How to test</h2>
  <p>Test at least annually, and after flooding, repairs, or any change in taste or odor &mdash; immediately if anyone in the home is <a href="fsa-hsa-water-filtration-immunocompromised.html">immunocompromised</a>. See <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>; a positive result is strong documentation for your Letter of Medical Necessity.</p>

  <h2>UV plus filtration: the standard answer</h2>
  <p><strong>UV purification</strong> inactivates bacteria, viruses, and protozoa without chemicals, and is the most direct microbial barrier &mdash; but it needs clear water to work, so it follows sediment and carbon <strong>filtration</strong>. Together they form a complete treatment train. See <a href="are-uv-water-purifiers-fsa-hsa-eligible.html">UV eligibility</a>.</p>

  <h2>What to test for, and how often</h2>
  <p>For wells, test for <strong>total coliform</strong> and <strong>E. coli</strong> at least once a year, and immediately after flooding, well repairs, or any change in taste, color, or odor. The {CDC} recommends nitrate testing periodically as well. Total coliform is an indicator: its presence signals that disease-causing organisms <em>could</em> get in, prompting further action.</p>

  <h2>How UV purification works</h2>
  <p>A UV system passes water under an ultraviolet-C lamp whose dose (measured in mJ/cm&sup2;) scrambles the DNA of bacteria, viruses, and protozoa so they cannot reproduce or infect &mdash; without adding any chemicals or taste. Two conditions make it work: the water must be <strong>clear</strong> (UV cannot penetrate cloudy water, so sediment and carbon pre-filtration come first), and the <strong>lamp is replaced annually</strong> as its output fades.</p>

  <h2>If a test comes back positive</h2>
  <p>A positive bacteria result usually calls for disinfecting the well (often shock chlorination), fixing the entry point if one is found, and retesting &mdash; then installing UV for ongoing protection. For an <a href="fsa-hsa-water-filtration-immunocompromised.html">immunocompromised</a> household, treat a positive result as urgent and follow your provider's guidance.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Pathogen protection</span>
    <h3>SpringWell UV + well filtration</h3>
    <p>UV inactivates microbes; pair it with well filtration so the water is clear enough for UV to work. Eligible via the TrueMed checkout.</p>
    {aff("uv","See UV purification","btn")}
    &nbsp;{aff("well-water","See well filtration","btn ghost")}
  </div>

  <h2>Eligibility</h2>
  <p>Disinfection is inherently health-related, so a provider can readily document the need &mdash; see the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> guide. Educational only, not medical advice.</p>
''',
 faq=[
  ("Is UV water treatment FSA/HSA eligible?","Yes, with a Letter of Medical Necessity. Because UV exists to inactivate disease-causing microbes, it is one of the clearest medical-necessity cases, especially on well water."),
  ("How do I know if my well has bacteria?","Test for total coliform and E. coli, which indicate possible contamination. Bacteria often give no taste or smell warning, so annual testing is recommended."),
  ("Does UV replace filtration?","No. UV disinfects but does not remove particles or chemicals and needs clear water to work, so it is paired with sediment and carbon filtration."),
 ])

# ---------- #46 Microplastics ----------
article(
 "microplastics-drinking-water-filters.html",
 "Microplastics in Drinking Water: What Filters Remove Them",
 "Microplastics are increasingly found in tap water. Learn what they are, the health questions, and which filters (RO, fine filtration) actually remove them.",
 "Microplastics",
 "Microplastics in drinking water: what filters actually remove them",
 "Microplastics are turning up in tap water worldwide, and many people want them out. Here is what microplastics are, what science does and does not yet know about the health effects, and which filters genuinely reduce them.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The honest status</p>
    <p class="ruling"><b>Widespread, with health effects still being studied.</b> The science is evolving, so we avoid overstating risk &mdash; but reducing microplastics is reasonable, and filtration can qualify with a Letter of Medical Necessity where a provider supports it.</p>
  </div>

  <h2>What microplastics are</h2>
  <p>Microplastics are tiny plastic particles &mdash; from larger plastics breaking down, synthetic fibers, and manufacturing &mdash; now detected in oceans, soil, food, and drinking water. Sizes vary widely, from visible specks down to particles far smaller than a human hair.</p>

  <h2>What we do and don't know about health</h2>
  <p>This is an area of active research. Microplastics are widely present, and scientists are studying potential effects, but the health consequences of typical drinking-water exposure are not yet well established. We think the honest framing matters: reducing exposure is a reasonable precaution, not a proven medical necessity for most people. A provider decides whether your specific situation supports a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>What actually removes microplastics</h2>
  <ul>
    <li><strong>Reverse osmosis</strong> &mdash; its fine membrane is highly effective at capturing microplastic particles in drinking water.</li>
    <li><strong>Fine mechanical filtration</strong> &mdash; sub-micron filters capture larger particles; effectiveness depends on pore size.</li>
    <li><strong>Whole-house systems with adequate filtration stages</strong> &mdash; reduce particles across the home.</li>
  </ul>
  <p>Pore size is the key spec &mdash; the smaller the rated micron level, the more it captures.</p>

  <h2>How they get into tap water &mdash; and how much</h2>
  <p>Microplastics enter water from degrading plastic waste, synthetic textile fibers, tire wear, and manufacturing, and have been detected in tap and bottled water worldwide. Reported concentrations vary widely between studies because measurement methods are still being standardized &mdash; there is, as yet, <strong>no federal drinking-water limit</strong> for microplastics, though some regulators (California among the first) have begun developing measurement requirements.</p>

  <h2>What the science says, honestly</h2>
  <p>Major reviews to date conclude there is not yet enough evidence to say whether microplastics in drinking water harm health at the levels typically found, while emphasizing that research is ongoing and gaps remain. We think that warrants measured language: reducing exposure is a reasonable precaution, not an established medical necessity for most people. A provider decides whether your specific situation supports a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>The filter spec that matters: pore size</h2>
  <p>Removal comes down to how fine the filter is. A <strong>reverse osmosis</strong> membrane has openings far smaller than the smallest measured microplastics, making it highly effective at the drinking tap. <strong>Sub-micron mechanical filters</strong> capture larger particles; the lower the micron rating, the more they catch. Whole-house filtration with adequate stages reduces particles across the home, though independent certification specifically for microplastics is still emerging.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Fine filtration</span>
    <h3>RO or whole-house filtration</h3>
    <p>Reverse osmosis is the most effective at the drinking tap; whole-house adds coverage everywhere. Eligible via the TrueMed checkout.</p>
    {aff("moen-ro","See RO system","btn")}
    &nbsp;{aff("whole-house","See whole-house filter","btn ghost")}
  </div>

  <h2>Eligibility</h2>
  <p>Because the health case is still emerging, be measured: a provider determines whether filtration is medically necessary for you. If it is, the usual <a href="how-to-buy-water-filter-with-hsa-fsa.html">process</a> applies. Educational only, not medical advice.</p>
''',
 faq=[
  ("Do water filters remove microplastics?","Reverse osmosis is highly effective at the drinking tap, and fine sub-micron mechanical filtration captures larger particles. Pore size determines how much is removed."),
  ("Are microplastics dangerous in drinking water?","The science is still developing. Microplastics are widespread, but the health effects of typical drinking-water exposure are not yet well established, so reducing them is a reasonable precaution rather than a proven necessity."),
  ("Is microplastic filtration FSA/HSA eligible?","It can be, with a Letter of Medical Necessity, if a provider supports it for your situation. Given the evolving science, the determination is the provider's."),
 ])

# ---------- #47 Iron, Manganese & Sulfur ----------
article(
 "iron-manganese-sulfur-well-water-treatment.html",
 "Iron, Manganese & Sulfur in Well Water: Treatment Guide",
 "Iron staining, manganese, and rotten-egg sulfur smell are classic well-water problems. Learn what causes them and which systems treat each.",
 "Iron, manganese &amp; sulfur",
 "Iron, manganese &amp; sulfur in well water: a treatment guide",
 "Orange staining, black specks, and a rotten-egg smell are the signatures of iron, manganese, and hydrogen sulfide in well water. Here is what causes each, how to test, which systems treat them, and how that fits HSA/FSA eligibility.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The well-water trio</p>
    <p class="ruling"><b>Mostly aesthetic, but worth treating &mdash; and eligible where documented.</b> These are classic well problems; the well filter that treats them is eligible with a Letter of Medical Necessity, especially alongside health-relevant contaminants.</p>
  </div>

  <h2>The three problems and their signs</h2>
  <ul>
    <li><strong>Iron</strong> &mdash; orange/brown staining on fixtures and laundry, metallic taste.</li>
    <li><strong>Manganese</strong> &mdash; black or dark staining and a bitter taste; often appears with iron.</li>
    <li><strong>Hydrogen sulfide</strong> &mdash; the unmistakable rotten-egg odor.</li>
  </ul>
  <p>These are largely aesthetic and nuisance issues rather than acute health hazards, though they often accompany contaminants that <em>are</em> health-relevant &mdash; another reason to <a href="are-water-test-kits-fsa-hsa-eligible.html">test thoroughly</a>.</p>

  <h2>What causes them</h2>
  <p>Iron and manganese dissolve into groundwater from soil and rock; hydrogen sulfide is often produced by bacteria or geology underground. Levels vary well to well and season to season, which is why testing guides the right configuration.</p>

  <h2>How they're treated</h2>
  <p>The common solution is an <strong>air-injection oxidation</strong> filter: it oxidizes dissolved iron, manganese, and sulfide so they become filterable and are flushed on a backwash cycle &mdash; no chemicals required. For organic discoloration (a yellow-brown tint from <strong>tannins</strong>), a dedicated tannin system is used. See our <a href="springwell-well-water-filter-system-review.html">well water filter review</a> for how this works in practice.</p>

  <h2>The standards and health context</h2>
  <p>Iron and sulfur are governed mainly by the EPA's <strong>secondary</strong> (aesthetic) standards &mdash; iron at 0.3 mg/L and manganese at 0.05 mg/L &mdash; meaning they affect taste, color, and staining rather than posing acute danger at typical levels. Manganese is the exception worth noting: at higher concentrations it carries a health advisory, particularly for infants, so a high manganese result is worth discussing with a provider.</p>

  <h2>Test before you treat</h2>
  <p>Effective treatment depends on specifics a <a href="are-water-test-kits-fsa-hsa-eligible.html">water test</a> reveals: how much iron and of what form (dissolved "ferrous" vs already-oxidized "ferric"), manganese and sulfide levels, pH (which affects oxidation), and whether iron bacteria are present. Configuring a system without testing is guesswork.</p>

  <h2>Treatment options compared</h2>
  <p><strong>Air-injection oxidation (AIO)</strong> is the common chemical-free solution for iron, manganese, and hydrogen sulfide &mdash; it oxidizes them so they filter out and backwash away. Heavy or bacterial cases may need additional steps; organic discoloration from <strong>tannins</strong> (a yellow-brown tint) needs a dedicated tannin system; and hardness or bacteria are handled by adding a <a href="need-water-softener-and-filter-hsa-fsa.html">softener</a> or <a href="bacteria-well-water-uv-filtration.html">UV</a>. The right train is matched to your test.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Well water treatment</span>
    <h3>SpringWell well &amp; tannin systems</h3>
    <p>Air-injection filtration for iron, manganese, and sulfur; a tannin system for organic discoloration. Eligible via the TrueMed checkout.</p>
    {aff("well-water","See well filter","btn")}
    &nbsp;{aff("tannin","See tannin system","btn ghost")}
  </div>

  <h2>Eligibility</h2>
  <p>Aesthetic improvement alone is a personal expense, but a well system documented for a genuine health reason &mdash; or bundled with treatment for bacteria or other contaminants &mdash; can qualify with a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. Educational only, not medical advice.</p>
''',
 faq=[
  ("What causes rotten-egg smell in well water?","Hydrogen sulfide gas, often produced by bacteria or geology underground. An air-injection oxidation filter is the common treatment."),
  ("How do I remove iron from well water?","An air-injection oxidation filter oxidizes dissolved iron so it can be filtered out and flushed on a backwash cycle, with no chemicals needed."),
  ("Is well water treatment FSA/HSA eligible?","Iron, manganese, and sulfur are mainly aesthetic, but a well system documented for a genuine health reason, or bundled with treatment for health-relevant contaminants, can qualify with a Letter of Medical Necessity."),
 ])

# ---------- #48 CCR ----------
article(
 "how-to-read-water-quality-report-ccr.html",
 "How to Read Your Water Quality Report (CCR) (2026)",
 "Your annual Consumer Confidence Report (CCR) tells you what's in your city water. Here's how to read it, what to flag, and when to filter or test further.",
 "Reading your water report",
 "How to read your water quality report (CCR) before buying a filter",
 "If you are on city water, your utility sends an annual Consumer Confidence Report (CCR) listing what is in your water. Knowing how to read it tells you what to filter for &mdash; and where the report falls short, so you know when to test your own tap.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Start here</p>
    <p class="ruling"><b>Read the report, then test what it can't tell you.</b> A CCR reveals what is in your supply at the plant; for lead and other tap-specific issues, you still test at home before buying a filter.</p>
  </div>

  <h2>What a CCR is and how to get one</h2>
  <p>Community water systems must publish an annual Consumer Confidence Report summarizing detected contaminants and how they compare to federal limits. Utilities typically mail it or post it online by July each year; you can also find guidance at the {EPACCR}. If you cannot find yours, call your water provider.</p>

  <h2>How to read the numbers</h2>
  <p>Two columns matter most: the <strong>level detected</strong> in your water and the <strong>MCL</strong> (Maximum Contaminant Level), the legal limit under {EPAWATER}. A detection below the MCL meets federal standards; a detection at or near it deserves attention. Also note the <strong>disinfectant used</strong> (chlorine vs <a href="chlorine-chloramine-health-filtration.html">chloramine</a>), which determines the right filter media.</p>

  <h2>Key things to look for</h2>
  <ul>
    <li><strong>Disinfection by-products</strong> &mdash; if elevated, a carbon filter helps.</li>
    <li><strong>Hardness</strong> &mdash; signals whether you might want softening.</li>
    <li><strong>Any contaminant near its MCL</strong> &mdash; worth targeting with the right system.</li>
  </ul>

  <h2>The big limitation: it's the plant, not your tap</h2>
  <p>A CCR reflects water as it leaves the treatment plant and the distribution system &mdash; not after it travels through <em>your</em> home's plumbing. That is why <a href="lead-in-drinking-water-fsa-eligible-filtration.html">lead</a>, which usually comes from household pipes, will not show up accurately in a CCR. For lead and other tap-specific concerns, test at home &mdash; see <a href="are-water-test-kits-fsa-hsa-eligible.html">water test kits</a>.</p>

  <h2>When and where to get it</h2>
  <p>Community water systems must make the Consumer Confidence Report available by <strong>July 1</strong> each year, covering the prior year's water quality. Many utilities mail it, post it online, or include a link on your bill; if you cannot find yours, call the utility or check the {EPACCR}. Apartment dwellers can request it from the building or the local water provider.</p>

  <h2>Decoding the table</h2>
  <p>A few terms unlock the report. <strong>MCL</strong> is the legal maximum; <strong>MCLG</strong> is the health-based goal (often lower, sometimes zero); an <strong>action level (AL)</strong> applies to lead and copper. Levels appear in <strong>ppm</strong> (parts per million) or <strong>ppb</strong> (parts per billion), and the table usually shows both the range and the average detected. "ND" means not detected. A dedicated <strong>violations</strong> section flags anything that exceeded a standard during the year.</p>

  <h2>Red flags worth acting on</h2>
  <ul>
    <li>Any listed <strong>violation</strong>, or a contaminant detected near its MCL.</li>
    <li>The <strong>disinfectant</strong> used &mdash; chlorine vs <a href="chlorine-chloramine-health-filtration.html">chloramine</a> changes the filter you need.</li>
    <li><strong>Hardness</strong>, if listed &mdash; signals whether softening is worth considering.</li>
    <li>The note on <strong>lead</strong> &mdash; a reminder to <a href="lead-in-drinking-water-fsa-eligible-filtration.html">test your own tap</a>, since the CCR cannot measure your plumbing.</li>
  </ul>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Test what the report can't</span>
    <h3>SpringWell Water Test Kit</h3>
    <p>Confirm what is actually at your tap &mdash; the results guide your system choice and support your Letter of Medical Necessity.</p>
    {aff("test-kit","Check the test kit","btn")}
  </div>

  <h2>From report to the right filter</h2>
  <p>Combine your CCR with a home test, then match contaminants to a system: a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house filter</a> for chlorine and broad coverage, <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO</a> for drinking-water specifics, and so on. The result is also documentation for your <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>
''',
 faq=[
  ("What is a Consumer Confidence Report (CCR)?","An annual report community water systems must publish, listing detected contaminants and how they compare to federal limits. Utilities usually issue it by July each year."),
  ("Does my CCR show lead at my tap?","Not accurately. A CCR reflects water at the plant and distribution system, while lead usually comes from household plumbing. Test at your own tap for lead."),
  ("How do I use my CCR to pick a filter?","Note any contaminant near its limit and the disinfectant used, combine that with a home test, then match the contaminants to the right system."),
 ])

# ======================================================================
#  CLUSTER F — Money / Tax / Seasonal (Articles #49-#53)
# ======================================================================

# ---------- #49 FSA Deadline ----------
article(
 "fsa-deadline-water-filter-use-it-or-lose-it.html",
 "FSA Deadline 2026: Use It or Lose It on a Water Filter",
 "Your FSA likely expires December 31. Here is how to use it on a qualifying water filter before the deadline \u2014 and avoid forfeiting your balance.",
 "FSA deadline",
 "FSA deadline 2026: use it or lose it on a water filter",
 "If you have money sitting in an FSA, the clock is real: most balances vanish on December 31. A qualifying water filter is one of the best ways to turn that expiring money into something durable. Here is how to do it in time.",
 f'''
  {disc(0)}
  <div class="verdict caution" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The deadline</p>
    <p class="ruling"><b>Most FSA balances expire December 31.</b> A qualifying water filter &mdash; bought with a Letter of Medical Necessity &mdash; converts money you would otherwise forfeit into a lasting home upgrade. Start early; the letter takes time.</p>
  </div>

  <h2>The use-it-or-lose-it rule</h2>
  <p>Flexible Spending Accounts are "use it or lose it": funds you do not spend by your plan's deadline are generally forfeited. For most plans that deadline is <strong>December 31</strong>, though some employers offer a short <strong>grace period</strong> (often into mid-March) or a small <strong>carryover</strong> of unused funds. Check which your plan has &mdash; but never assume; many plans have neither.</p>

  <h2>Why a water filter is a smart year-end use</h2>
  <p>Faced with forfeiting money, people often buy random eligible odds and ends. A qualifying <a href="whole-house-water-filtration-hsa-fsa-eligible.html">water filter</a> is different: it is durable, genuinely useful, and (with documentation) addresses a real health concern. Instead of spending the balance on things you do not need, you convert it into cleaner water for years &mdash; effectively a 100% "discount" on funds that would otherwise vanish, on top of the usual pre-tax saving. See <a href="end-of-year-hsa-fsa-spending-water-filter.html">end-of-year spending ideas</a>.</p>

  <h2>Mind the timing</h2>
  <p>This is the part people get wrong. A filter needs a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> dated on or before purchase, and the survey-and-review step takes a little time. Do not wait until December 31 &mdash; start in early December so the letter is issued and the purchase clears before your deadline.</p>

  <h2>What to do now (before the deadline)</h2>
  <ol class="steps">
    <li><h4>Check your balance and deadline</h4><p>Log in to your FSA portal; note the exact cutoff and any grace period or carryover.</p></li>
    <li><h4>Pick a qualifying system</h4><p>Match it to your water concern &mdash; see the <a href="best-fsa-hsa-eligible-water-filters.html">best eligible systems</a>.</p></li>
    <li><h4>Buy through a checkout that issues the letter</h4><p>The TrueMed flow handles the Letter of Medical Necessity at purchase.</p></li>
    <li><h4>Keep your documentation</h4><p>Save the letter and itemized receipt for your administrator.</p></li>
  </ol>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Beat the deadline</span>
    <h3>Use your FSA before it expires</h3>
    <p>SpringWell's eligible systems issue the Letter of Medical Necessity at checkout &mdash; start now so it clears before December 31.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <p class="updated">Tip: if your balance is larger than a single year's filter purchase, remember replacement filters and combos can use eligible funds too &mdash; see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>
''',
 faq=[
  ("When does my FSA expire?","Most FSA balances expire December 31, though some plans offer a short grace period or a small carryover. Check your specific plan, and do not assume you have either."),
  ("Can I use my FSA on a water filter before year-end?","Yes, with a Letter of Medical Necessity. Start in early December so the letter is issued and the purchase clears before your deadline."),
  ("Is buying a water filter better than forfeiting FSA money?","Almost always. You convert money you would lose into a durable, eligible purchase, on top of the usual pre-tax saving."),
 ])

# ---------- #50 Savings math ----------
article(
 "how-much-save-water-filter-hsa-fsa.html",
 "How Much Can You Save on a Water Filter With HSA/FSA?",
 "How much do you really save buying a water filter with HSA/FSA? The pre-tax math by bracket, worked examples, and what affects your actual savings.",
 "How much you save",
 "How much can you actually save buying a water filter with HSA/FSA?",
 "Buying a water filter with HSA/FSA dollars discounts it by your tax rate &mdash; commonly 20 to 37%. Here is exactly how the math works, worked examples at different prices and brackets, and what changes your real savings.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The short answer</p>
    <p class="ruling"><b>You save your marginal tax rate &mdash; typically 20&ndash;37%.</b> Because HSA/FSA dollars are pre-tax, an eligible filter effectively costs that much less. On a $2,000 system, that is roughly $400&ndash;$740 back.</p>
  </div>

  <h2>Why pre-tax means a discount</h2>
  <p>Money you put into an HSA or FSA is set aside before income tax. When you spend it on a qualified expense, you never pay tax on those dollars &mdash; so the effective price drops by your marginal rate. It is not free; you save your tax rate, not 100%. But on a multi-hundred or multi-thousand-dollar purchase, that adds up fast.</p>

  <div class="math" data-reveal>
    <div>
      <div class="head">Paying from your bank account</div>
      <div class="row"><span>Earned (pre-tax)</span><span>$100</span></div>
      <div class="row"><span>Income tax (~30%)</span><span>&minus;$30</span></div>
      <div class="row"><span>Left to spend</span><span>$70</span></div>
    </div>
    <div class="savings-col">
      <div class="head">Paying from HSA / FSA</div>
      <div class="row"><span>Set aside (pre-tax)</span><span>$100</span></div>
      <div class="row"><span>Income tax</span><span>$0</span></div>
      <div class="row"><span>Left to spend</span><span class="big">$100</span></div>
    </div>
  </div>

  <h2>Worked examples</h2>
  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th>System price</th><th>At 22%</th><th>At 30%</th><th>At 37%</th></tr></thead>
    <tbody>
      <tr><td>$399 (under-sink RO)</td><td>~$88 saved</td><td>~$120 saved</td><td>~$148 saved</td></tr>
      <tr><td>$1,170 (whole house)</td><td>~$257 saved</td><td>~$351 saved</td><td>~$433 saved</td></tr>
      <tr><td>$2,000 (combo)</td><td>~$440 saved</td><td>~$600 saved</td><td>~$740 saved</td></tr>
    </tbody>
  </table>
  </div>
  <p class="updated">Illustrative only &mdash; your actual saving depends on your bracket and is not a guarantee.</p>

  <h2>What affects your actual savings</h2>
  <ul>
    <li><strong>Your marginal tax bracket</strong> &mdash; the single biggest factor.</li>
    <li><strong>State income tax</strong> &mdash; HSA/FSA savings often apply at the state level too, increasing the discount.</li>
    <li><strong>FICA on FSA</strong> &mdash; FSA contributions can also avoid payroll tax, adding to the benefit.</li>
    <li><strong>Forfeiture avoided</strong> &mdash; spending an expiring <a href="fsa-deadline-water-filter-use-it-or-lose-it.html">FSA balance</a> effectively saves 100% of money you would have lost.</li>
  </ul>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Put it to work</span>
    <h3>See eligible systems and your savings</h3>
    <p>Pick a system, then pay pre-tax via the TrueMed checkout to capture the discount.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <p>This is not tax advice &mdash; confirm your bracket and situation with a professional. For how to actually buy, see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>
''',
 faq=[
  ("How much do you save on a water filter with HSA/FSA?","You save your marginal tax rate, commonly 20-37%. On a $2,000 system that is roughly $400-$740, depending on your bracket and state."),
  ("Is the filter free if I use FSA money?","No. You save your tax rate, not the full price. The exception is spending an expiring FSA balance you would otherwise forfeit, which effectively saves 100% of that money."),
  ("Does state tax change the savings?","Often yes. HSA/FSA savings frequently apply at the state level too, and FSA contributions can also avoid payroll tax, increasing the total discount."),
 ])

# ---------- #51 Open enrollment ----------
article(
 "hsa-fsa-open-enrollment-water-filter.html",
 "HSA/FSA Open Enrollment: Plan a Water Filter Purchase",
 "Open enrollment is the time to plan an HSA/FSA water filter purchase. Here is how to set contributions and time your buy for maximum pre-tax savings.",
 "Open enrollment planning",
 "HSA/FSA open enrollment: planning for a water filtration purchase",
 "Open enrollment is your once-a-year chance to set up the accounts that pay for an eligible water filter. A little planning now means the funds are there when you buy. Here is how to plan contributions and time the purchase.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Plan ahead</p>
    <p class="ruling"><b>Use open enrollment to fund the purchase deliberately.</b> Decide whether an HSA or FSA fits, set contributions with a water filter in mind, and you will have pre-tax dollars ready when you buy.</p>
  </div>

  <h2>What open enrollment is</h2>
  <p>Open enrollment is the annual window (commonly autumn, for coverage starting January 1) when you choose your health plan and elect HSA or FSA contributions for the year ahead. It is the main chance to set those elections, so it is worth a few minutes of planning if a water filter is on your list.</p>

  <h2>HSA or FSA: choose the right vehicle</h2>
  <p>If you are enrolling in a qualifying high-deductible plan, an <a href="are-water-filters-hsa-eligible.html">HSA</a> lets you build a balance toward a larger <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house system</a> over time. If not, an <a href="are-water-filters-fsa-eligible.html">FSA</a> still works, but plan its annual election carefully. Our <a href="hsa-vs-fsa-water-filter.html">HSA vs FSA guide</a> walks through the choice.</p>

  <h2>Setting contributions with a filter in mind</h2>
  <p>If you intend to buy this year, factor the system's cost (and any replacement filters) into your election. For an FSA, be realistic: elect enough to cover the purchase, but avoid over-electing money you cannot use before the <a href="fsa-deadline-water-filter-use-it-or-lose-it.html">year-end deadline</a>. For an HSA, contributions roll over, so there is less risk in funding ahead.</p>

  <h2>Timing the purchase</h2>
  <p>With an FSA, funds are typically available up to your full annual election early in the year, so you can buy sooner rather than later. With an HSA, you may prefer to wait until your balance is sufficient, or use a split payment. Either way, remember the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> requirement.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} When you're ready</span>
    <h3>Eligible systems for your plan year</h3>
    <p>Once your account is funded, SpringWell's eligible systems issue the Letter of Medical Necessity at checkout.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("Should I plan a water filter purchase during open enrollment?","Yes, if you intend to buy. Choosing the right account and setting contributions with the system's cost in mind means the pre-tax funds are ready when you purchase."),
  ("How much should I contribute for a water filter?","Enough to cover the system and any replacement filters. For an FSA, avoid over-electing money you cannot spend before the year-end deadline; HSA funds roll over."),
  ("Can I buy early in the year with an FSA?","Often yes. FSA funds are typically available up to your full annual election early in the plan year, so you can purchase sooner."),
 ])

# ---------- #52 End-of-year spending ----------
article(
 "end-of-year-hsa-fsa-spending-water-filter.html",
 "End-of-Year HSA/FSA Spending: Why a Water Filter Fits",
 "Scrambling to spend an FSA before year-end? A water filter is a durable, high-value way to use HSA/FSA funds. Here is why it beats last-minute buys.",
 "End-of-year spending",
 "End-of-year HSA/FSA spending ideas: why a water filter makes sense",
 "Every December, people scramble to spend FSA money before it disappears &mdash; often on things they do not need. A qualifying water filter is a smarter use: durable, genuinely valuable, and eligible with a Letter of Medical Necessity. Here is why it makes sense.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">A better year-end buy</p>
    <p class="ruling"><b>Convert expiring funds into something durable.</b> Rather than stockpiling odds and ends, a qualifying water filter turns a year-end FSA balance into cleaner water for years &mdash; with a Letter of Medical Necessity.</p>
  </div>

  <h2>The year-end scramble</h2>
  <p>As December closes in, anyone with an unspent FSA faces a choice: spend it or forfeit it. The common reflex is to grab whatever qualifies &mdash; extra supplies you may never use. That spends the money, but it does not get you much. A bigger, durable purchase puts the funds to better work. (Check your <a href="fsa-deadline-water-filter-use-it-or-lose-it.html">deadline and any grace period</a> first.)</p>

  <h2>Why a water filter beats stockpiling</h2>
  <ul>
    <li><strong>Durable value</strong> &mdash; a system serves your household for years, not a season.</li>
    <li><strong>Genuine health benefit</strong> &mdash; with documentation, it addresses a real concern, not a checkbox.</li>
    <li><strong>Uses a larger balance</strong> &mdash; if you have a substantial amount to spend, a system absorbs it meaningfully.</li>
    <li><strong>Keeps giving</strong> &mdash; replacement filters can use future eligible funds too.</li>
  </ul>

  <h2>How to do it in time</h2>
  <p>Because a filter needs a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, start in early December rather than on the 31st. Pick a <a href="best-fsa-hsa-eligible-water-filters.html">qualifying system</a>, buy through the checkout that issues the letter, and keep your documentation. See <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>.</p>

  <h2>Other eligible year-end ideas</h2>
  <p>If you have funds left over after a filter, common eligible items include things like first-aid and many over-the-counter health products &mdash; but confirm each against your plan. The point is to spend deliberately on things you will use, with the durable water system as the anchor purchase.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Spend it well</span>
    <h3>Turn year-end funds into cleaner water</h3>
    <p>SpringWell's eligible systems issue the Letter of Medical Necessity at checkout &mdash; start early so it clears in time.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>
''',
 faq=[
  ("What's a good way to spend FSA money at year-end?","A durable, qualifying purchase like a water filter is often better than stockpiling small items. It uses a larger balance and provides lasting value, with a Letter of Medical Necessity."),
  ("Can I buy a water filter at the last minute?","Allow time. Because a Letter of Medical Necessity is required, start in early December so the letter and purchase clear before your deadline."),
  ("What if I have money left after a filter?","Confirm other eligible items against your plan. Spend deliberately on things you will actually use, with the water system as the anchor purchase."),
 ])

# ---------- #53 Tax-deductible beyond FSA/HSA ----------
article(
 "water-filter-tax-deductible-medical-expense.html",
 "Is a Water Filter a Tax-Deductible Medical Expense?",
 "Beyond FSA/HSA, can you deduct a water filter on your taxes? The Schedule A medical-expense rules, the 7.5% AGI threshold, and what to know.",
 "Tax-deductible medical expense",
 "Is a water filter a tax-deductible medical expense (beyond FSA/HSA)?",
 "Even without an FSA or HSA, a medically necessary water filter may count toward the itemized medical-expense deduction on your taxes. Here is how that works, the thresholds involved, and why most people still prefer the pre-tax route.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">The other route</p>
    <p class="ruling"><b>Possibly &mdash; via the itemized medical deduction.</b> With a Letter of Medical Necessity, a water filter can count toward medical expenses on Schedule A, but only the portion above 7.5% of your income, and only if you itemize.</p>
  </div>

  <h2>How the medical-expense deduction works</h2>
  <p>Separate from FSA/HSA accounts, the IRS allows an itemized deduction for qualified medical expenses on Schedule A. Under {IRS502}, a water filter can be a qualified medical expense when it is needed to treat or prevent a condition &mdash; the same medical-necessity standard, supported by a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>.</p>

  <h2>The two big catches</h2>
  <ul>
    <li><strong>The 7.5% AGI threshold.</strong> You can only deduct total medical expenses that exceed 7.5% of your adjusted gross income. If your AGI is $80,000, only expenses above $6,000 count &mdash; so a single filter rarely clears the bar on its own.</li>
    <li><strong>You must itemize.</strong> The deduction only helps if your itemized deductions beat the standard deduction, which many people do not exceed.</li>
  </ul>

  <h2>Who actually benefits</h2>
  <p>This route mainly helps people who already have high medical expenses in a year &mdash; where a filter adds to a total that already clears the threshold &mdash; and who itemize. For most others, the pre-tax <a href="how-much-save-water-filter-hsa-fsa.html">HSA/FSA route</a> is simpler and captures the saving regardless of the threshold.</p>

  <h2>You can't double-dip</h2>
  <p>Important: you cannot deduct expenses you already paid with pre-tax HSA/FSA funds &mdash; that would be a double tax benefit. Choose one route per dollar. For most buyers, paying with an HSA or FSA is the easier win; the Schedule A deduction is a fallback for those with high itemized medical costs.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} The simpler route</span>
    <h3>Most buyers use pre-tax HSA/FSA</h3>
    <p>It captures the saving without the AGI threshold. Eligible systems issue the Letter of Medical Necessity at checkout.</p>
    {aff("truemed-eligible-category","Shop eligible systems","btn")}
  </div>

  <p>This is general information, not tax advice. Confirm your situation with a tax professional and see {IRS502} for the rules.</p>
''',
 faq=[
  ("Is a water filter tax-deductible?","It can count toward the itemized medical-expense deduction on Schedule A with a Letter of Medical Necessity, but only the portion of total medical expenses above 7.5% of your AGI, and only if you itemize."),
  ("Should I deduct it or use my HSA/FSA?","For most people the pre-tax HSA/FSA route is simpler and captures the saving regardless of the AGI threshold. The deduction mainly helps those with high itemized medical expenses."),
  ("Can I do both?","No. You cannot deduct expenses paid with pre-tax HSA/FSA funds, since that would be a double tax benefit. Choose one route per dollar."),
 ])

# ======================================================================
#  CLUSTER G — Water type / Use case (Articles #54-#57)
# ======================================================================

# ---------- #54 City vs Well ----------
article(
 "city-water-vs-well-water-filter-eligible.html",
 "City Water vs Well Water: Which Filter Do You Need?",
 "City water vs well water need very different filters. Here is how to tell which you have, what each requires, and how either qualifies for HSA/FSA.",
 "City vs well water",
 "City water vs well water: which filter do you need (and is it eligible)?",
 "The single biggest factor in choosing a water filter is your source. City water is already disinfected; well water is not &mdash; so they need very different systems. Here is how to tell what you have, what each requires, and how either qualifies for HSA/FSA.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Start with your source</p>
    <p class="ruling"><b>Match the filter to the source.</b> City water needs disinfectant and lead reduction; well water needs iron, sulfur, bacteria, and nitrate treatment. Either qualifies for HSA/FSA with a Letter of Medical Necessity.</p>
  </div>

  <h2>The fundamental difference</h2>
  <p>If you are on <strong>city (municipal) water</strong>, a utility treats and disinfects it before it reaches you, then monitors it &mdash; your concerns are mostly residual disinfectant, disinfection by-products, and lead from household plumbing. If you are on a <strong>private well</strong>, nobody treats your water; everything is your responsibility, from bacteria to iron to nitrates. This split drives every other decision. (Our pillar covers it too &mdash; see <a href="index.html#water-type">city vs well</a>.)</p>

  <h2>What city water typically needs</h2>
  <ul>
    <li><strong>Chlorine or chloramine reduction</strong> &mdash; for taste and comfort; see <a href="chlorine-chloramine-health-filtration.html">chlorine &amp; chloramine</a>.</li>
    <li><strong>Lead reduction</strong> &mdash; from older home plumbing; see <a href="lead-in-drinking-water-fsa-eligible-filtration.html">lead</a>.</li>
    <li><strong>Broad carbon filtration</strong> &mdash; a <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house carbon system</a> covers most city needs.</li>
  </ul>

  <h2>What well water typically needs</h2>
  <ul>
    <li><strong>Iron, manganese, sulfur</strong> &mdash; staining and odor; see <a href="iron-manganese-sulfur-well-water-treatment.html">the treatment guide</a>.</li>
    <li><strong>Bacteria</strong> &mdash; no central disinfection, so <a href="bacteria-well-water-uv-filtration.html">UV</a> may be needed.</li>
    <li><strong>Nitrates</strong> &mdash; especially with infants; see <a href="nitrates-well-water-filtration.html">nitrates</a>.</li>
    <li><strong>Hardness</strong> &mdash; common on wells; may warrant softening.</li>
  </ul>

  <h2>How to know which you have</h2>
  <p>If you receive a monthly water bill from a utility and an annual <a href="how-to-read-water-quality-report-ccr.html">Consumer Confidence Report</a>, you are on city water. If you have a well on your property and no water bill, you are on well water &mdash; and you should <a href="are-water-test-kits-fsa-hsa-eligible.html">test regularly</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Match your source</span>
    <h3>City and well systems</h3>
    <p>Whole-house carbon for city water; air-injection filtration (plus UV) for wells. Both eligible via the TrueMed checkout.</p>
    {aff("whole-house","City whole-house filter","btn")}
    &nbsp;{aff("well-water","Well water system","btn ghost")}
  </div>

  <h2>Eligibility is the same either way</h2>
  <p>Whichever source you have, the rule is identical: a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> tied to a documented concern. Test, document, and buy through a checkout that issues the letter. This page is educational, not medical advice.</p>
''',
 faq=[
  ("How do I know if I have city or well water?","If you get a water bill and an annual Consumer Confidence Report from a utility, you are on city water. If you have a well and no water bill, you are on well water and should test regularly."),
  ("Do city and well water need different filters?","Yes. City water needs disinfectant and lead reduction (whole-house carbon); well water needs iron, sulfur, bacteria, and nitrate treatment (air-injection filtration plus possibly UV)."),
  ("Is filtration eligible for both?","Yes, with a Letter of Medical Necessity tied to a documented concern. The eligibility rule is the same regardless of your water source."),
 ])

# ---------- #55 Whole-house vs under-sink ----------
article(
 "whole-house-vs-under-sink-water-filter-hsa-fsa.html",
 "Whole-House vs Under-Sink Filter: Which for HSA/FSA?",
 "Whole-house or under-sink water filter for HSA/FSA? Compare coverage, cost, installation, and which makes the stronger medical-necessity case.",
 "Whole-house vs under-sink",
 "Whole-house vs under-sink water filter: which for HSA/FSA?",
 "Whole-house and under-sink filters solve different problems. One treats every tap; the other treats your drinking water affordably. Here is how they compare on coverage, cost, and installation &mdash; and which makes the stronger HSA/FSA case.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Coverage vs cost</p>
    <p class="ruling"><b>Whole-house for every tap; under-sink for affordable drinking water.</b> Whole-house makes the broader medical-necessity case; under-sink is the budget and renter-friendly choice. Both eligible with a Letter of Medical Necessity.</p>
  </div>

  <h2>The core difference</h2>
  <p>A <strong>whole-house</strong> system (point-of-entry) treats water where it enters your home, so every tap, shower, and appliance gets filtered water. An <strong>under-sink</strong> system (point-of-use) treats one tap &mdash; usually the kitchen &mdash; for drinking and cooking. The right choice depends on whether your concern is the whole home or just what you drink.</p>

  <div class="tbl-scroll">
  <table class="data">
    <thead><tr><th></th><th>Whole-house</th><th>Under-sink</th></tr></thead>
    <tbody>
      <tr><td>Coverage</td><td class="yes">Every tap &amp; shower</td><td>One tap</td></tr>
      <tr><td>Typical cost</td><td>Higher (from ~$1,000+)</td><td class="yes">Lower (~$399)</td></tr>
      <tr><td>Installation</td><td>Point of entry (plumber common)</td><td class="yes">Under one sink</td></tr>
      <tr><td>Renter-friendly</td><td>No</td><td class="yes">Yes</td></tr>
      <tr><td>Medical-necessity scope</td><td class="yes">Broad (e.g. showering, skin)</td><td>Drinking water</td></tr>
    </tbody>
  </table>
  </div>

  <h2>When whole-house wins</h2>
  <p>Choose whole-house if your concern reaches beyond drinking water &mdash; chlorine on skin and hair, a household member with a <a href="fsa-hsa-water-filtration-immunocompromised.html">heightened vulnerability</a>, or whole-home contaminant exposure. It also makes the strongest <a href="guides/letter-of-medical-necessity-water-filter.html">medical-necessity</a> case because it addresses every point of contact. See <a href="whole-house-water-filtration-hsa-fsa-eligible.html">whole-house eligibility</a>.</p>

  <h2>When under-sink wins</h2>
  <p>Choose under-sink if your concern is specifically your drinking and cooking water (lead, nitrates, taste), if budget matters, or if you <a href="water-filters-renters-hsa-fsa-no-installation.html">rent</a>. It is the lowest-cost eligible route &mdash; see <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Pick your coverage</span>
    <h3>Whole-house or under-sink</h3>
    <p>Every tap, or just the kitchen &mdash; both eligible via the TrueMed checkout with a Letter of Medical Necessity.</p>
    {aff("whole-house","Whole-house filter","btn")}
    &nbsp;{aff("moen-ro","Under-sink RO","btn ghost")}
  </div>
''',
 faq=[
  ("Whole-house or under-sink for HSA/FSA?","Whole-house treats every tap and makes the broader medical-necessity case; under-sink treats drinking water affordably and suits renters. Choose based on whether your concern is whole-home or drinking-water only."),
  ("Which is cheaper?","Under-sink, typically around $399 versus $1,000+ for whole-house. The pre-tax discount applies to either."),
  ("Which makes a stronger eligibility case?","Whole-house, because it addresses every point of contact including showering. But under-sink is fully eligible too with a Letter of Medical Necessity."),
 ])

# ---------- #56 Renters ----------
article(
 "water-filters-renters-hsa-fsa-no-installation.html",
 "Water Filters for Renters: HSA/FSA Options, No Install",
 "Renting? You can still buy an HSA/FSA-eligible water filter. Here are point-of-use options that need no permanent installation and move with you.",
 "Renters",
 "Water filters for renters: HSA/FSA-eligible options without installation",
 "Renting does not mean settling for unfiltered water. Point-of-use systems are HSA/FSA-eligible, need no permanent plumbing changes, and move with you when you go. Here are the best no-install options and how they qualify.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Renter-friendly</p>
    <p class="ruling"><b>Eligible and install-free.</b> Point-of-use systems qualify with a Letter of Medical Necessity, need no permanent changes, and come with you when you move &mdash; ideal for rentals.</p>
  </div>

  <h2>The renter's challenge</h2>
  <p>A whole-house system installs at the point of entry, which usually is not an option in a rental &mdash; and you would not want to leave it behind anyway. The solution is point-of-use: systems that treat one tap and attach without permanent plumbing work.</p>

  <h2>No-install eligible options</h2>
  <ul>
    <li><strong>Under-sink reverse osmosis</strong> &mdash; connects to the existing kitchen supply and can be removed when you leave; the most thorough option. See <a href="is-reverse-osmosis-fsa-hsa-eligible.html">RO eligibility</a>.</li>
    <li><strong>Countertop and faucet filters</strong> &mdash; the simplest, fully renter-friendly, lower cost.</li>
  </ul>
  <p>All of these can be eligible with a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, the same as larger systems.</p>

  <h2>What to avoid as a renter</h2>
  <p>Skip anything requiring permanent plumbing modification or landlord approval. The whole point is a system that works in your unit today and moves with you tomorrow &mdash; protecting both your water and your deposit.</p>

  <h2>It moves with you</h2>
  <p>Because point-of-use systems are not built into the home, they are a portable investment: buy once with pre-tax dollars, take it to your next place. Replacement filters can use future eligible funds too.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Best for rentals</span>
    <h3>Under-sink reverse osmosis</h3>
    <p>Clean drinking water with no permanent install &mdash; around $399, eligible via the TrueMed checkout.</p>
    {aff("moen-ro","Check price","btn")}
  </div>

  <h2>How to buy</h2>
  <p>Pick a point-of-use system, buy through the checkout that issues your <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>, and keep your records &mdash; see <a href="how-to-buy-water-filter-with-hsa-fsa.html">how to buy with HSA/FSA</a>. Educational only, not medical advice.</p>
''',
 faq=[
  ("Can renters buy an HSA/FSA-eligible water filter?","Yes. Point-of-use systems like under-sink RO and countertop filters qualify with a Letter of Medical Necessity and need no permanent installation."),
  ("What's the best filter for a rental?","An under-sink reverse osmosis system is the most thorough no-install option, around $399. Countertop and faucet filters are even simpler."),
  ("Does it move with me?","Yes. Point-of-use systems are not built into the home, so you can remove them and take them to your next place."),
 ])

# ---------- #57 Softener AND filter ----------
article(
 "need-water-softener-and-filter-hsa-fsa.html",
 "Do You Need a Softener AND a Filter? Combo Guide",
 "Do you need both a water softener and a filter? Here is how to tell, what each does, and how an HSA/FSA-eligible combo covers both with one LMN.",
 "Softener and filter",
 "Do you need a softener AND a filter? An HSA/FSA combo guide",
 "Filters and softeners solve different problems, and many homes &mdash; especially on hard well water &mdash; benefit from both. Here is how to tell if you need both, and how an HSA/FSA-eligible combo covers them in one documented system.",
 f'''
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">Two jobs, one system</p>
    <p class="ruling"><b>A filter removes contaminants; a softener removes hardness.</b> If you have both problems, a combo handles them together &mdash; and the filtration half anchors the Letter of Medical Necessity.</p>
  </div>

  <h2>What each one does</h2>
  <p>The distinction is simple but important. A <strong>filter</strong> removes contaminants &mdash; chlorine, lead, sediment, and more &mdash; which is the health-relevant job. A <strong>softener</strong> removes hardness minerals (calcium and magnesium) to stop scale and improve the feel of the water, which is mostly a comfort and appliance-protection job. They are not interchangeable.</p>

  <h2>When you need both</h2>
  <p>You likely want both if your water is <em>both</em> hard <em>and</em> carries contaminants you want reduced &mdash; common on <a href="city-water-vs-well-water-filter-eligible.html">well water</a>, and in many hard-water city areas. Signs of hardness include scale on fixtures, spotty dishes, and poor soap lather; a <a href="are-water-test-kits-fsa-hsa-eligible.html">water test</a> confirms both hardness and contaminants so you treat the right things.</p>

  <h2>The combo solution</h2>
  <p>Rather than buying two separate systems, a <strong>filter + softener combo</strong> integrates both. It is tidier, often more cost-effective, and &mdash; importantly for eligibility &mdash; documents as a single system whose filtration component carries a genuine health rationale. See our <a href="reviews/springwell-filter-softener-combo-review.html">combo review</a> and the <a href="best-hsa-fsa-eligible-water-softeners.html">best eligible softeners</a>.</p>

  <h2>Salt-based vs salt-free</h2>
  <p>Within a combo you can choose salt-based softening (maximum scale removal) or salt-free conditioning (no added sodium, lower maintenance). If a low-sodium need is documented, salt-free is the better fit &mdash; see <a href="hard-water-health-skin-softening.html">hard water and your skin</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Both in one</span>
    <h3>SpringWell Filter + Softener Combo</h3>
    <p>Contaminant filtration and hardness control in one eligible system, via the TrueMed checkout with a Letter of Medical Necessity.</p>
    {aff("filter-softener-combo","Check price","btn")}
    &nbsp;{aff("salt-free-combo","See salt-free","btn ghost")}
  </div>

  <h2>Eligibility</h2>
  <p>A combo is easier to document than a standalone softener because the filtration half has the clear health rationale &mdash; the basis for the <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>. Educational only, not medical advice.</p>
''',
 faq=[
  ("Do I need both a water softener and a filter?","If your water is both hard and carries contaminants you want reduced, yes. A filter handles contaminants; a softener handles hardness. A combo does both in one system."),
  ("Is a filter + softener combo HSA/FSA eligible?","Yes, with a Letter of Medical Necessity. The combo is easier to document than a standalone softener because the filtration component carries the clear health rationale."),
  ("Salt-based or salt-free in a combo?","Salt-based gives maximum scale removal; salt-free adds no sodium and needs less maintenance. Choose salt-free if a low-sodium need is documented."),
 ])

# ======================================================================
#  CLUSTER H — Service comparison (Article #58)
# ======================================================================

# ---------- #58 TrueMed & LMN services ----------
article(
 "truemed-vs-flex-lmn-services-springwell.html",
 "TrueMed & LMN Services: How SpringWell's Checkout Works",
 "How do LMN services like TrueMed make a water filter HSA/FSA eligible? Here is how SpringWell's TrueMed checkout works and what these services do.",
 "TrueMed &amp; LMN services",
 "TrueMed and LMN services: how SpringWell's HSA/FSA checkout works",
 "A water filter only becomes HSA/FSA eligible with a Letter of Medical Necessity &mdash; and getting one used to mean a doctor's visit. Services like TrueMed streamline that step. Here is how the model works and how SpringWell's checkout uses it.",
 f'''
  {disc(0)}
  <div class="verdict" data-reveal>
    <span class="seal-check">{CHECK}</span>
    <p class="status">What they do</p>
    <p class="ruling"><b>LMN services connect you to a licensed provider who can issue the Letter of Medical Necessity.</b> SpringWell's checkout uses TrueMed to handle this at the point of purchase &mdash; no separate appointment.</p>
  </div>

  <h2>The problem these services solve</h2>
  <p>As we cover throughout this site, a water filter is not automatically eligible &mdash; it needs a <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a> from a licensed provider tying it to a health condition. Traditionally that meant scheduling an appointment and explaining the request. LMN services exist to make that step fast and online.</p>

  <h2>How the model works</h2>
  <ol class="steps">
    <li><h4>Complete a health survey</h4><p>You answer questions about your health and water concerns.</p></li>
    <li><h4>A licensed provider reviews it</h4><p>If appropriate, they issue a Letter of Medical Necessity for the filter.</p></li>
    <li><h4>Pay with your HSA/FSA</h4><p>You use your HSA/FSA card or get reimbursed, with the letter on file.</p></li>
  </ol>
  <p>The provider's independent judgment is central &mdash; the letter is issued only if your situation supports it. See <a href="how-truemed-works-for-water-filters.html">how TrueMed works for water filters</a> for the detailed walkthrough.</p>

  <h2>How SpringWell uses TrueMed</h2>
  <p>SpringWell integrates <strong>TrueMed</strong> directly into its checkout for eligible systems, so the survey-and-letter step happens as part of buying &mdash; you do not have to arrange anything separately. That convenience is a big part of why SpringWell is straightforward to buy with HSA/FSA dollars.</p>

  <h2>What to understand about LMN services generally</h2>
  <p>Several services in the market follow this same broad model of connecting customers to licensed providers for medical-necessity documentation. What matters for you is the substance, not the brand name: a real licensed provider must make the determination, the letter must reflect a genuine medical need, and you keep the documentation. Always be truthful in the survey &mdash; the letter is only valid if the need is real, which also protects you if a claim is ever <a href="will-my-fsa-hsa-water-filter-claim-be-denied.html">reviewed</a>.</p>

  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Built-in eligibility</span>
    <h3>SpringWell + TrueMed checkout</h3>
    <p>The Letter of Medical Necessity is handled at purchase &mdash; no separate appointment to arrange.</p>
    {aff("truemed-how-it-works","See how it works","btn")}
    &nbsp;{aff("truemed-eligible-category","Shop eligible systems","btn ghost")}
  </div>

  <h2>The bottom line</h2>
  <p>LMN services like TrueMed do not change the rules &mdash; they make the required step convenient. The filter still needs a genuine, provider-issued <a href="guides/letter-of-medical-necessity-water-filter.html">Letter of Medical Necessity</a>; the service just brings that to your checkout. This page is educational, not medical or tax advice.</p>
''',
 faq=[
  ("What is an LMN service like TrueMed?","It connects you to a licensed provider who can issue a Letter of Medical Necessity online, so an eligible product can be bought with HSA/FSA funds without a separate appointment."),
  ("How does SpringWell's TrueMed checkout work?","You complete a health survey at checkout, a licensed provider reviews it and issues the Letter of Medical Necessity if appropriate, and you pay with your HSA/FSA."),
  ("Do these services guarantee eligibility?","No. A licensed provider must determine that your situation supports the letter. Be truthful in the survey; the letter is only valid if the medical need is genuine."),
 ])

# ======================================================================
#  HTML SITEMAP PAGE (human-readable, categorized)
# ======================================================================
SITEMAP_CATS = [
 ("&#129517; Start here", [
   ("index.html","Home &mdash; Are water filters FSA/HSA eligible?"),
   ("best-fsa-hsa-eligible-water-filters.html","Best HSA/FSA-eligible systems (2026)"),
   ("fsa-hsa-eligible-water-filters-list.html","FSA/HSA-eligible filters: the full list"),
   ("how-to-buy-water-filter-with-hsa-fsa.html","How to buy with HSA/FSA"),
   ("how-much-save-water-filter-hsa-fsa.html","How much can you save?"),
 ]),
 ("&#9989; Eligibility basics", [
   ("are-water-filters-fsa-eligible.html","Are water filters FSA eligible?"),
   ("are-water-filters-hsa-eligible.html","Are water filters HSA eligible?"),
   ("whole-house-water-filtration-hsa-fsa-eligible.html","Whole-house filtration eligibility"),
   ("are-water-softeners-fsa-hsa-eligible.html","Are water softeners eligible?"),
   ("is-reverse-osmosis-fsa-hsa-eligible.html","Is reverse osmosis eligible?"),
   ("water-filter-replacement-cartridges-fsa-eligible.html","Replacement cartridges eligibility"),
   ("are-shower-filters-fsa-hsa-eligible.html","Are shower filters eligible?"),
   ("are-uv-water-purifiers-fsa-hsa-eligible.html","Are UV purifiers eligible?"),
   ("is-bottled-water-fsa-hsa-eligible.html","Is bottled water eligible?"),
   ("are-water-test-kits-fsa-hsa-eligible.html","Are water test kits eligible?"),
   ("is-distilled-purified-water-fsa-eligible.html","Is distilled / purified water eligible?"),
 ]),
 ("&#128203; The process &amp; paperwork", [
   ("guides/letter-of-medical-necessity-water-filter.html","Letter of Medical Necessity: how it works"),
   ("how-truemed-works-for-water-filters.html","How TrueMed works for water filters"),
   ("how-to-get-letter-of-medical-necessity.html","How to get a Letter of Medical Necessity"),
   ("how-to-get-reimbursed-water-filter-fsa-hsa.html","How to get reimbursed"),
   ("hsa-fsa-water-filter-reimbursement-checklist.html","Reimbursement documents checklist"),
   ("will-my-fsa-hsa-water-filter-claim-be-denied.html","Will my claim be denied?"),
   ("can-you-use-fsa-hsa-card-for-water-filter.html","Can you use your FSA/HSA card?"),
   ("do-you-need-prescription-fsa-eligible-water-filter.html","Do you need a prescription?"),
 ]),
 ("&#11088; Reviews &amp; best-of", [
   ("reviews/springwell-whole-house-water-filter-review.html","SpringWell Whole House review"),
   ("reviews/springwell-filter-softener-combo-review.html","SpringWell Filter + Softener Combo review"),
   ("springwell-well-water-filter-system-review.html","SpringWell Well Water Filter review"),
   ("best-hsa-fsa-eligible-water-softeners.html","Best eligible water softeners"),
   ("best-fsa-eligible-under-sink-ro-water-filters.html","Best under-sink &amp; RO filters"),
   ("cheapest-fsa-hsa-eligible-water-filters.html","Cheapest eligible options"),
   ("springwell-truemed-savings-coupons.html","SpringWell savings &amp; TrueMed"),
 ]),
 ("&#9878;&#65039; SpringWell vs competitors", [
   ("springwell-vs-clearly-filtered-fsa-eligible.html","SpringWell vs Clearly Filtered"),
   ("springwell-vs-aquasana-hsa-fsa.html","SpringWell vs Aquasana"),
   ("springwell-vs-culligan-fsa-hsa.html","SpringWell vs Culligan"),
   ("truemed-vs-flex-lmn-services-springwell.html","TrueMed &amp; LMN services explained"),
 ]),
 ("&#128179; Accounts &amp; who qualifies", [
   ("hsa-vs-fsa-water-filter.html","HSA vs FSA for a water filter"),
   ("can-you-use-hra-for-water-filter.html","Can you use an HRA?"),
   ("lpfsa-water-filtration-eligible.html","Can you use an LPFSA?"),
   ("fsa-eligible-water-filters-families-young-children.html","Families with young children"),
   ("hsa-fsa-water-filters-pregnancy.html","Pregnancy"),
   ("fsa-hsa-water-filtration-immunocompromised.html","Immunocompromised households"),
   ("self-employed-hsa-home-water-filtration.html","Self-employed + HSA"),
 ]),
 ("&#129514; Contaminants &amp; health", [
   ("lead-in-drinking-water-fsa-eligible-filtration.html","Lead in drinking water"),
   ("pfas-tap-water-filtration-hsa-fsa.html","PFAS &lsquo;forever chemicals&rsquo;"),
   ("nitrates-well-water-filtration.html","Nitrates in well water"),
   ("chlorine-chloramine-health-filtration.html","Chlorine &amp; chloramine"),
   ("hard-water-health-skin-softening.html","Hard water &amp; your skin"),
   ("bacteria-well-water-uv-filtration.html","Bacteria in well water"),
   ("microplastics-drinking-water-filters.html","Microplastics in drinking water"),
   ("iron-manganese-sulfur-well-water-treatment.html","Iron, manganese &amp; sulfur"),
   ("how-to-read-water-quality-report-ccr.html","How to read your water report (CCR)"),
 ]),
 ("&#128176; Money, tax &amp; timing", [
   ("fsa-deadline-water-filter-use-it-or-lose-it.html","FSA deadline: use it or lose it"),
   ("hsa-fsa-open-enrollment-water-filter.html","Open-enrollment planning"),
   ("end-of-year-hsa-fsa-spending-water-filter.html","End-of-year spending ideas"),
   ("water-filter-tax-deductible-medical-expense.html","Tax-deductible beyond FSA/HSA?"),
 ]),
 ("&#127968; Choosing the right system", [
   ("city-water-vs-well-water-filter-eligible.html","City water vs well water"),
   ("whole-house-vs-under-sink-water-filter-hsa-fsa.html","Whole-house vs under-sink"),
   ("water-filters-renters-hsa-fsa-no-installation.html","Water filters for renters"),
   ("need-water-softener-and-filter-hsa-fsa.html","Do you need a softener AND a filter?"),
 ]),
 ("&#127970; Company &amp; policies", [
   ("about.html","About Us"),
   ("contact.html","Contact Us"),
   ("editorial-policy.html","Editorial &amp; eligibility policy"),
   ("affiliate-disclosure.html","Affiliate disclosure"),
   ("disclaimer.html","Disclaimer"),
   ("terms-of-use.html","Terms of Use"),
   ("privacy-policy.html","Privacy policy"),
   ("cookie-policy.html","Cookie policy"),
   ("accessibility.html","Accessibility statement"),
 ]),
]
_smap_total = sum(len(v) for _, v in SITEMAP_CATS)
smap = head("Sitemap — FSA Eligible Water Filter",
  "Every page on FSA Eligible Water Filter in one place — eligibility guides, the LMN process, reviews, comparisons, contaminant guides, and company info.",
  "sitemap.html", depth=0)
smap += f"""
<div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> &rsaquo; Sitemap</div>
<article class="hero">
  <span class="eyebrow">{CHECK} Site map &middot; browse everything</span>
  <h1 class="prose">Sitemap</h1>
  <p class="lede prose">Everything on {NAME}, in one place &mdash; from the core eligibility question to the Letter of Medical Necessity process, system reviews, comparisons, and contaminant guides. Looking for the XML sitemap for search engines? That is at <a href="sitemap.xml">sitemap.xml</a>.</p>
</article>
<div class="prose">
  <div class="smap-stats">
    <div class="stat"><span class="num">{_smap_total}</span><span class="lbl">Pages &amp; guides</span></div>
    <div class="stat"><span class="num">{len(SITEMAP_CATS)}</span><span class="lbl">Topic categories</span></div>
    <div class="stat"><span class="num">100%</span><span class="lbl">Free to read</span></div>
    <div class="stat"><span class="num">1</span><span class="lbl">Honest, test-first mission</span></div>
  </div>
"""
for _cat, _items in SITEMAP_CATS:
    smap += f'  <div class="smap-cat">\n    <h2>{_cat}</h2>\n    <p class="cnt">{len(_items)} pages</p>\n    <ul>\n'
    for _slug, _label in _items:
        smap += f'      <li><a href="{_slug}">{_label}</a></li>\n'
    smap += '    </ul>\n  </div>\n'
smap += f"""
  <div class="cta-box" data-reveal>
    <span class="kicker">{CHECK} Not sure where to start?</span>
    <h3>Begin with the eligibility guide</h3>
    <p>The clearest starting point is whether a water filter is eligible at all &mdash; and the Letter of Medical Necessity that makes it so.</p>
    <p style="margin:.8rem 0 0"><a class="btn" href="index.html">Read the eligibility guide</a> &nbsp; <a class="btn ghost" href="best-fsa-hsa-eligible-water-filters.html">See the best systems</a></p>
  </div>
</div>
</div>
"""
smap += footer(0)
write("sitemap.html", smap)

# ======================================================================
#  SITEMAP (generated from everything written above)
# ======================================================================
def sm_url(p):
    return SITE + "/" if p == "index.html" else f"{SITE}/{p}"
prio = {"index.html":"1.0","best-fsa-hsa-eligible-water-filters.html":"0.9"}
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in URLS:
    pr = prio.get(p, "0.7" if (p.startswith(("reviews/","guides/")) or "-" in p) else "0.4")
    cf = "weekly" if pr in ("1.0","0.9") else "monthly"
    sm.append(f"  <url><loc>{sm_url(p)}</loc><changefreq>{cf}</changefreq><priority>{pr}</priority></url>")
sm.append("</urlset>")
with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
    f.write("\n".join(sm))
print(f"  sitemap.xml  ({len(URLS)} URLs)")

print("\nDone.")
