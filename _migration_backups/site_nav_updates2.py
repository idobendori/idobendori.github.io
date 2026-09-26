import re, glob

PAGES = [f for f in sorted(glob.glob('*.html')) if f != '_downloads.html']
GBP_URL = "https://share.google/nJyE00OVPE9DVMMNT"

def apply(html, old, new, label, fname):
    """Idempotent: apply old->new once; if old absent but new present, assume already done; else error."""
    n = html.count(old)
    if n == 1:
        return html.replace(old, new, 1), "applied"
    if n == 0 and new in html:
        return html, "already-done"
    raise AssertionError(f"{fname} :: {label}: unexpected state (old_count={n})")

sameas_old = '"https://www.youtube.com/@junglebubble"\n  ]'
sameas_new = '"https://www.youtube.com/@junglebubble",\n    "' + GBP_URL + '"\n  ]'

footer_reviews_old = '<div>Youtube</div></a></div>'
footer_reviews_new = (
    '<div>Youtube</div></a>'
    f'<a href="{GBP_URL}" target="_blank" class="footer1_social-link w-inline-block"><div>ביקורות בגוגל</div></a>'
    '</div>'
)

footer_workshop_old_plain = '<a href="diyterrarium.html" class="footer1_link">איך מכינים טרריום</a>'
footer_workshop_new_plain = '<a href="workshop.html" class="footer1_link">סדנת טרריום</a>' + footer_workshop_old_plain

footer_workshop_old_current = '<a href="diyterrarium.html" aria-current="page" class="footer1_link w--current">איך מכינים טרריום</a>'
footer_workshop_new_current = '<a href="workshop.html" class="footer1_link">סדנת טרריום</a>' + footer_workshop_old_current

nav_plain_old = '<a href="contact.html" class="button is-small is-nav w-button">יצירת קשר</a>'
nav_plain_new = '<a href="workshop.html" class="button is-small is-nav w-button">סדנאות</a>'

nav_current_old = '<a href="contact.html" aria-current="page" class="button is-small is-nav w-button w--current">יצירת קשר</a>'
nav_current_new_normalized = '<a href="workshop.html" class="button is-small is-nav w-button">סדנאות</a>'

nav_workshop_plain = '<a href="workshop.html" class="button is-small is-nav w-button">סדנאות</a>'
nav_workshop_current = '<a href="workshop.html" aria-current="page" class="button is-small is-nav w-button w--current">סדנאות</a>'

log = []
for fname in PAGES:
    html = open(fname, encoding='utf-8').read()
    orig = html
    steps = []

    html, s = apply(html, sameas_old, sameas_new, "sameAs", fname); steps.append(s)
    html, s = apply(html, footer_reviews_old, footer_reviews_new, "footer_reviews", fname); steps.append(s)

    # footer workshop link: plain or current variant, idempotent-safe
    if footer_workshop_old_plain in html or footer_workshop_new_plain in html:
        html, s = apply(html, footer_workshop_old_plain, footer_workshop_new_plain, "footer_workshop_plain", fname); steps.append(s)
    else:
        html, s = apply(html, footer_workshop_old_current, footer_workshop_new_current, "footer_workshop_current", fname); steps.append(s)

    # nav button
    if nav_plain_old in html:
        html = html.replace(nav_plain_old, nav_plain_new, 1); steps.append("applied-nav-plain")
    elif nav_current_old in html:
        html = html.replace(nav_current_old, nav_current_new_normalized, 1); steps.append("applied-nav-current-normalized")
    elif nav_plain_new in html or nav_workshop_plain in html or nav_workshop_current in html:
        steps.append("nav-already-done")
    else:
        raise AssertionError(f"{fname} :: nav button not found in any known state")

    if html != orig:
        open(fname, 'w', encoding='utf-8').write(html)
    log.append((fname, steps))

# now make workshop.html's own nav button the "current" one
wf = 'workshop.html'
html = open(wf, encoding='utf-8').read()
if nav_workshop_plain in html:
    html = html.replace(nav_workshop_plain, nav_workshop_current, 1)
    open(wf, 'w', encoding='utf-8').write(html)
    log.append((wf, ['nav-set-current']))
elif nav_workshop_current in html:
    log.append((wf, ['nav-current-already-set']))
else:
    raise AssertionError("workshop.html nav button not in expected state for current-page step")

for row in log:
    print(row)
