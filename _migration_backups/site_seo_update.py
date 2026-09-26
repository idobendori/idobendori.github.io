import re, os

DESCRIPTIONS = {
    "10-liter.html": "טרריום מוכן בכלי דמיג׳אן 10 ליטר - הגודל הקטן בסדרה, מתאים לשידה או שולחן. הזמנה אישית מ-Jungle Bubble.",
    "34-liter.html": "טרריום מוכן בכלי דמיג׳אן 34 ליטר - גודל אמצעי, מתאים לקונסולה או לרצפה. הזמנה אישית מ-Jungle Bubble.",
    "54-liter.html": "טרריום מוכן בכלי דמיג׳אן 54 ליטר - הגודל הגדול בסדרה, מתאים לקונסולה או לרצפה. הזמנה אישית מ-Jungle Bubble.",
    "aboutterrariums.html": "מה זה טרריום? כל מה שצריך לדעת על עולם הצמחים בבקבוק וכיצד הוא שומר על עצמו.",
    "contact.html": "יצירת קשר עם Jungle Bubble - הזמנת טרריום אישי, שאלות על סדנאות וטרריומים מוכנים.",
    "diyterrarium.html": "מדריך שלב-אחר-שלב להכנת טרריום בעצמכם - בחירת כלי, אדמה, שתילה וטיפוח.",
    "index.html": "Jungle Bubble - טרריומים בהזמנה אישית וסדנאות טרריום פרטיות בתל אביב, השראה וידע לעולם הצמחים בבקבוק.",
    "soil.html": "איזו אדמה מתאימה לטרריום וכיצד להרכיב את שכבות האדמה הנכונות לצמחים בריאים.",
    "terrariumplants.html": "צמחים מומלצים לטרריום - אילו זנים הכי מתאימים לסביבה סגורה ולחה, וטיפים לבחירה.",
    "unique.html": "טרריומים בגדלים וצורות מיוחדים - כלים ייחודיים להזמנה אישית מ-Jungle Bubble.",
    "wide-opening-terrarium.html": "טרריום בכלי דמיג׳אן עם פתח רחב - עיצוב ייחודי וגישה נוחה לתחזוקה. הזמנה אישית.",
    "workshop.html": "סדנאות טרריום פרטיות לזוגות וקבוצות בתל אביב - כשעתיים וחצי, כולל כל החומרים והכלים הנדרשים.",
}

JSON_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Jungle Bubble",
  "url": "https://www.junglebubble.co.il/",
  "description": "טרריומים בהזמנה אישית וסדנאות טרריום בתל אביב",
  "image": "https://www.junglebubble.co.il/images/img_5866.jpg",
  "logo": "https://www.junglebubble.co.il/images/6578800814b99a352d7cc51d_Jungle%20Bubble%20logo%20full%20size%20RTL.svg",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 32.0943134,
    "longitude": 34.7917161
  },
  "areaServed": "תל אביב",
  "sameAs": [
    "https://www.instagram.com/junglebubble__o",
    "https://www.facebook.com/groups/567912794008233/",
    "https://www.youtube.com/@junglebubble"
  ]
}
</script>
'''

changed_files = []
for fname, desc in DESCRIPTIONS.items():
    if not os.path.exists(fname):
        print("MISSING FILE:", fname)
        continue
    html = open(fname, encoding="utf-8").read()
    orig = html

    # 1) lang + dir on <html> tag (only the first <html ...> tag, only if not already set)
    def add_lang_dir(m):
        tag = m.group(0)
        if 'lang=' in tag:
            return tag
        return tag[:-1] + ' lang="he" dir="rtl">'
    html, n1 = re.subn(r'<html[^>]*>', add_lang_dir, html, count=1)

    # 2) meta description right after <title>...</title>
    meta_tag = f'<meta name="description" content="{desc}"/>'
    html, n2 = re.subn(r'(<title>[^<]*</title>)', r'\1' + meta_tag, html, count=1)

    # 3) JSON-LD before </head>
    html, n3 = re.subn(r'</head>', JSON_LD + '</head>', html, count=1)

    if html != orig:
        open(fname, "w", encoding="utf-8").write(html)
        changed_files.append((fname, n1, n2, n3))

for row in changed_files:
    print(row)
print("total files changed:", len(changed_files))
