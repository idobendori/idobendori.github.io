import re, glob

PAGES = [f for f in sorted(glob.glob('*.html')) if f != '_downloads.html']

def do(html, old, new, expected, label, fname):
    n = html.count(old)
    assert n == expected, f"{fname} :: {label}: expected {expected}, found {n}"
    return html.replace(old, new, expected) if expected else html

GBP_URL = "https://share.google/nJyE00OVPE9DVMMNT"

sameas_old = '"https://www.youtube.com/@junglebubble"\n  ]'
sameas_new = '"https://www.youtube.com/@junglebubble",\n    "' + GBP_URL + '"\n  ]'

footer_reviews_old = '<div>Youtube</div></a></div>'
footer_reviews_new = (
    '<div>Youtube</div></a>'
    f'<a href="{GBP_URL}" target="_blank" class="footer1_social-link w-inline-block"><div>ביקורות בגוגל</div></a>'
    '</div>'
)

footer_workshop_old = '<a href="diyterrarium.html" class="footer1_link">איך מכינים טרריום</a>'
footer_workshop_new = '<a href="workshop.html" class="footer1_link">סדנת טרריום</a>' + footer_workshop_old

nav_plain_old = '<a href="contact.html" class="button is-small is-nav w-button">יצירת קשר</a>'
nav_plain_new = '<a href="workshop.html" class="button is-small is-nav w-button">סדנאות</a>'

nav_current_old = '<a href="contact.html" aria-current="page" class="button is-small is-nav w-button w--current">יצירת קשר</a>'
nav_current_new_normalized = '<a href="workshop.html" class="button is-small is-nav w-button">סדנאות</a>'  # normalized to plain

results = []
for fname in PAGES:
    html = open(fname, encoding='utf-8').read()
    orig = html

    html = do(html, sameas_old, sameas_new, 1, "sameAs GBP link", fname)
    html = do(html, footer_reviews_old, footer_reviews_new, 1, "footer google reviews link", fname)
    html = do(html, footer_workshop_old, footer_workshop_new, 1, "footer workshop link", fname)

    has_plain = html.count(nav_plain_old)
    has_current = html.count(nav_current_old)
    assert has_plain + has_current == 1, f"{fname} :: nav button: expected exactly 1 total nav-button match, found plain={has_plain} current={has_current}"
    if has_plain:
        html = html.replace(nav_plain_old, nav_plain_new, 1)
    else:
        html = html.replace(nav_current_old, nav_current_new_normalized, 1)

    if html != orig:
        open(fname, 'w', encoding='utf-8').write(html)
        results.append(fname)

print("changed:", results)
print("count:", len(results))
