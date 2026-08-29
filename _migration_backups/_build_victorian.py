# -*- coding: utf-8 -*-
import re, io

path = "terrariumplants.html"
html = io.open(path, encoding="utf-8").read()

# 1) Add Google Fonts link for the new typefaces, right after the existing gstatic preconnect
old_head_anchor = '<link href="https://fonts.gstatic.com" rel="preconnect"/>'
assert html.count(old_head_anchor) == 1, "head anchor not found or not unique"
font_link = ('<link href="https://fonts.gstatic.com" rel="preconnect"/>'
    '<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:ital,wght@0,400;0,700;1,400'
    '&family=Frank+Ruhl+Libre:wght@300;400;500;700&family=Inconsolata:wght@400;700&display=swap" rel="stylesheet"/>')
html = html.replace(old_head_anchor, font_link, 1)

PLANTS = [
    ("פיטוניה גידי כסף", "images/6162a9c6a82f7e6d9e9c43cd_IDO_9713.JPG"),
    ("פפרומיה פרוסטרטה", "images/6162ab822ebb56e7df460665_IDO_9707.jpg"),
    ("דקל חמודריאה", "images/6162b34ab9a5d8b5a4958ace_Chamaedorea_elegans_Mart.jpeg"),
    ("סינגוניום", "images/6162b29e91c4945c035f5780_close-up-beautiful-arrowhead-plant-syngonium-podop-NS9DN73.jpg"),
    ("שרכים", "images/6162d82f8223cb73d2a8d58d_Edited-111.jpg"),
    ("נרוגוליה קרולינאה", "images/6162d7efa25838815fdb5e5e_IMG_8490.JPG"),
    ("קרפטנטוס", "images/6162d2c45c67da73620aba74_3746262021_f576b69861_c.jpg"),
    ("פפרומיה טטרגונה", "images/6162d2c4cbdf1d548fcb5ed7_efb26bd9422ca8932bac06a1bd6cb333.jpeg"),
]
ROMAN = ["I","II","III","IV","V","VI","VII","VIII"]

def render_cards():
    out = []
    for (name, img), no in zip(PLANTS, ROMAN):
        out.append(
            '<figure class="jbv-card">'
            f'<div class="jbv-card-no">{no}</div>'
            f'<img src="{img}" alt="{name}"/>'
            f'<figcaption>{name}</figcaption>'
            '</figure>'
        )
    return "".join(out)

CARDS_HTML = render_cards()

BODY_P_INNER = ('בעמוד זה תוכלו למצוא את שמות הצמחים המתאימים לטרריום.<br/><br/>'
    'מומלץ לבחור בשתילים של <strong>פִיטֹונְיָה גִידֵי הַכֶסֶף</strong>. '
    'צמח זה נמצא במרבית המשתלות, הוא עמיד מאוד למחלות, הוא יפה וקיים במגוון צבעים.<br/><br/>'
    'שתילים מּומלצים נוספים הם <strong>קִיסֹוס, הִיּפֹואֶסְטֶס או סִינְגֹונְיּום</strong>;<br/>‍<br/>'
    'למטה תוכלו למצוא רשימה מלאה עם תמונות של  צמחים נוספים. <br/><br/>'
    '<em>*אינני מוכר את הצמחים, ניתן להשיגם במרבית המשתלות.</em>')

NEW_MIDDLE = f'''<style>
.jbv-mobile-only{{display:block}}
.jbv-desktop-only{{display:none}}
@media (min-width:768px){{
  .jbv-mobile-only{{display:none}}
  .jbv-desktop-only{{display:block}}
}}
.jbv-section{{font-family:'Frank Ruhl Libre',Georgia,serif}}
.jbv-eyebrow{{font-family:'Inconsolata',monospace;font-size:11px;letter-spacing:.3em;color:#a8bd94}}
.jbv-rule{{height:2px;background:#a8bd94;width:84px;margin:20px 0}}

.jbv-hero-mobile{{background:#24352a;color:#eee9d9;position:relative;overflow:hidden;padding:34px 22px 44px}}
.jbv-hero-sketch-mobile{{position:absolute;left:-60px;top:-10px;height:430px;opacity:.4;pointer-events:none}}
.jbv-hero-inner-mobile{{position:relative}}
.jbv-h1-mobile{{margin:12px 0 0;font-family:'Bona Nova',serif;font-weight:700;font-size:38px;line-height:1.15;color:#f7f4ea;text-shadow:0 2px 14px rgba(26,37,29,.75)}}
.jbv-body-mobile{{margin:0;font-size:16px;line-height:1.85;color:#ded8c6}}
.jbv-body-mobile strong{{color:#fff;font-family:'Bona Nova',serif;font-size:18px}}
.jbv-body-mobile em{{color:#a8bd94;font-size:14px;font-style:italic}}
.jbv-cta-col{{display:flex;flex-direction:column;gap:14px;margin-top:28px;font-size:16px}}
.jbv-btn-primary{{background:#e9e3d1;color:#24352a;padding:13px 0;text-align:center;display:block}}
.jbv-links-row{{display:flex;gap:22px;flex-wrap:wrap}}
.jbv-link-underline{{border-bottom:1px solid #a8bd94;padding-bottom:3px;color:#eee9d9}}

.jbv-listwrap{{padding:32px 22px 8px;background:#f7f4ea}}
.jbv-list-header-mobile{{display:flex;align-items:flex-end;justify-content:center;gap:2px;border-bottom:2px solid #24352a;padding-bottom:10px;color:#1f2a20}}
.jbv-basket-img{{height:120px;mix-blend-mode:multiply}}
.jbv-list-title-mobile{{text-align:center;flex:none;padding:0 6px}}
.jbv-eyebrow-dark{{font-family:'Inconsolata',monospace;font-size:10px;letter-spacing:.22em;color:#8d8871}}
.jbv-h2-mobile{{margin:6px 0 0;font-family:'Bona Nova',serif;font-weight:700;font-size:25px;line-height:1.08;color:#1f2a20}}

.jbv-hero-desktop{{background:#24352a;color:#eee9d9;position:relative;overflow:hidden;padding:60px 6vw 70px}}
.jbv-hero-sketch-desktop{{position:absolute;left:-40px;bottom:-30px;height:480px;opacity:.5;pointer-events:none}}
.jbv-hero-inner-desktop{{position:relative;max-width:640px}}
.jbv-h1-desktop{{margin:16px 0 0;font-family:'Bona Nova',serif;font-weight:700;font-size:58px;line-height:1.1;color:#f7f4ea}}
.jbv-rule-desktop{{height:2px;background:#a8bd94;width:110px;margin:24px 0}}
.jbv-body-desktop{{margin:0;font-size:18px;line-height:1.9;color:#ded8c6}}
.jbv-body-desktop strong{{color:#fff;font-family:'Bona Nova',serif;font-size:20px}}
.jbv-body-desktop em{{color:#a8bd94;font-size:15px;font-style:italic}}
.jbv-cta-row-desktop{{display:flex;flex-wrap:wrap;align-items:center;gap:24px;margin-top:32px;font-size:16px}}
.jbv-btn-primary-desktop{{background:#e9e3d1;color:#24352a;padding:12px 26px}}
.jbv-link-underline-desktop{{border-bottom:1px solid #a8bd94;padding-bottom:3px;color:#eee9d9}}

.jbv-listwrap-desktop{{padding:56px 6vw 20px;background:#f7f4ea;color:#1f2a20}}
.jbv-list-header-desktop{{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;border-bottom:2px solid #24352a;padding-bottom:14px}}
.jbv-h2-desktop{{margin:0;font-family:'Bona Nova',serif;font-weight:700;font-size:32px;color:#1f2a20}}
.jbv-sedum-img{{height:110px;mix-blend-mode:multiply}}

.jbv-grid{{display:grid;grid-template-columns:repeat(2,1fr);color:#1f2a20}}
@media (min-width:768px){{ .jbv-grid{{grid-template-columns:repeat(4,1fr)}} }}
.jbv-card{{margin:0;padding:16px 14px;border-bottom:1px solid #cfc9b4;border-left:1px solid #cfc9b4}}
.jbv-card-no{{font-family:'Inconsolata',monospace;font-size:10.5px;letter-spacing:.2em;color:#8d8871}}
.jbv-card img{{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;margin-top:9px;filter:saturate(.78) contrast(1.03)}}
.jbv-card figcaption{{margin-top:9px;font-family:'Bona Nova',serif;font-size:17px;line-height:1.3}}
@media (min-width:768px){{
  .jbv-card{{padding:22px 20px}}
  .jbv-card figcaption{{font-size:19px}}
}}
</style>

<section class="jbv-mobile-only jbv-section jbv-hero-mobile" dir="rtl">
  <img src="images/victorian-davallia-lineart.png" alt="" class="jbv-hero-sketch-mobile"/>
  <div class="jbv-hero-inner-mobile">
    <div class="jbv-eyebrow">מידע ומדריכים · צמחים</div>
    <h1 class="jbv-h1-mobile">צמחים מתאימים לטרריום</h1>
    <div class="jbv-rule"></div>
    <p class="jbv-body-mobile">{BODY_P_INNER}</p>
    <div class="jbv-cta-col">
      <a href="contact.html" class="jbv-btn-primary">יצירת קשר</a>
      <div class="jbv-links-row">
        <a href="aboutterrariums.html" class="jbv-link-underline">מה זה טרריום</a>
        <a href="diyterrarium.html" class="jbv-link-underline">מדריך הכנת טרריום</a>
      </div>
    </div>
  </div>
</section>
<section class="jbv-mobile-only jbv-section jbv-listwrap" dir="rtl">
  <div class="jbv-list-header-mobile">
    <img src="images/victorian-basket.png" alt="" class="jbv-basket-img"/>
    <div class="jbv-list-title-mobile">
      <div class="jbv-eyebrow-dark">VIII SPECIMENS</div>
      <h2 class="jbv-h2-mobile">רשימת<br/>הצמחים</h2>
    </div>
    <img src="images/victorian-basket.png" alt="" class="jbv-basket-img"/>
  </div>
  <div class="jbv-grid">{CARDS_HTML}</div>
</section>

<section class="jbv-desktop-only jbv-section jbv-hero-desktop" dir="rtl">
  <img src="images/victorian-davallia-lineart.png" alt="" class="jbv-hero-sketch-desktop"/>
  <div class="jbv-hero-inner-desktop">
    <div class="jbv-eyebrow">מידע ומדריכים · צמחים</div>
    <h1 class="jbv-h1-desktop">צמחים מתאימים<br/>לטרריום</h1>
    <div class="jbv-rule-desktop"></div>
    <p class="jbv-body-desktop">{BODY_P_INNER}</p>
    <div class="jbv-cta-row-desktop">
      <a href="contact.html" class="jbv-btn-primary-desktop">יצירת קשר</a>
      <a href="aboutterrariums.html" class="jbv-link-underline-desktop">מה זה טרריום</a>
      <a href="diyterrarium.html" class="jbv-link-underline-desktop">מדריך הכנת טרריום</a>
    </div>
  </div>
</section>
<section class="jbv-desktop-only jbv-section jbv-listwrap-desktop" dir="rtl">
  <div class="jbv-list-header-desktop">
    <h2 class="jbv-h2-desktop">רשימת הצמחים</h2>
    <img src="images/victorian-sedum.png" alt="" class="jbv-sedum-img"/>
  </div>
  <div class="jbv-grid">{CARDS_HTML}</div>
</section>
'''

start_anchor = '<div class="section-7">'
end_anchor = '<figure class="footer1_component">'
assert html.count(start_anchor) == 1, "start anchor issue"
assert html.count(end_anchor) == 1, "end anchor issue"
start_idx = html.index(start_anchor)
end_idx = html.index(end_anchor)
assert start_idx < end_idx

html = html[:start_idx] + NEW_MIDDLE + html[end_idx:]

io.open(path, "w", encoding="utf-8").write(html)
print("OK, new length:", len(html))
