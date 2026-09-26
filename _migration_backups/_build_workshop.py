# -*- coding: utf-8 -*-
import io, re

path = "workshop.html"
html = io.open(path, encoding="utf-8").read()

# 1) Add Google Fonts link for the new typefaces (Frank Ruhl Libre; Bona Nova & Inconsolata already load via WebFont.load)
old_head_anchor = '<link href="https://fonts.gstatic.com" rel="preconnect"/>'
assert html.count(old_head_anchor) == 1, "head anchor not found or not unique"
font_link = ('<link href="https://fonts.gstatic.com" rel="preconnect"/>'
    '<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:ital,wght@0,400;0,700;1,400'
    '&family=Frank+Ruhl+Libre:wght@300;400;500;700&family=Inconsolata:wght@400;700&display=swap" rel="stylesheet"/>')
html = html.replace(old_head_anchor, font_link, 1)

CSS = '''<style>
.jbv-mobile-only{display:block}
.jbv-desktop-only{display:none}
@media (min-width:768px){
  .jbv-mobile-only{display:none}
  .jbv-desktop-only{display:block}
}
.jbv2-wrap{font-family:'Frank Ruhl Libre',Georgia,serif;background:#f3ece0;color:#1f2a20}
.jbv2-eyebrow{font-family:'Inconsolata',monospace;letter-spacing:.3em;color:#6d6353}
.jbv2-frame{border:1px solid #24352a;position:relative}
.jbv2-frame::before,.jbv2-frame::after,.jbv2-frame .jbv2-dot{position:absolute;width:9px;height:9px;background:#24352a}
.jbv2-h1{margin:0;font-family:'Bona Nova',serif;font-weight:700;line-height:1.1}
.jbv2-h2{margin:0;font-family:'Bona Nova',serif;font-weight:700}
.jbv2-rule{display:flex;align-items:center;gap:14px}
.jbv2-rule span{height:1px;background:#24352a;flex:1}
.jbv2-rule i{width:7px;height:7px;background:#24352a;transform:rotate(45deg);display:block}
.jbv2-body{font-size:18px;line-height:1.9}
.jbv2-facts{display:grid;grid-template-columns:repeat(3,1fr)}
.jbv2-facts>div{padding:14px 12px}
.jbv2-facts>div+div{border-right:1px solid #cdc3ae}
.jbv2-facts-label{font-family:'Inconsolata',monospace;font-size:10px;letter-spacing:.2em;color:#8b8171}
.jbv2-facts-val{font-family:'Bona Nova',serif;font-size:20px;margin-top:4px}
.jbv2-strip{background:#e9e3d1;border-bottom:1px solid #cfc9b4;display:grid;grid-template-columns:repeat(3,1fr)}
.jbv2-strip>div{padding:22px 30px}
.jbv2-strip>div+div{border-right:1px solid #cfc9b4}
.jbv2-strip-label{font-family:'Inconsolata',monospace;font-size:10.5px;letter-spacing:.22em;color:#6f7a63}
.jbv2-strip-val{font-family:'Bona Nova',serif;font-size:22px;margin-top:6px}
.jbv2-cta{display:inline-block;border:1px solid #23201a;padding:12px 26px;font-size:16px;background:#23201a;color:#f3ece0}
.jbv2-vessel-fig{margin:0;border:1px solid #24352a;padding:9px;background:#fbf8ef}
.jbv2-vessel-fig img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.jbv2-vessel-cap{margin-top:10px;padding-top:9px;border-top:1px solid #cfc9b4;display:flex;justify-content:space-between;align-items:baseline}
.jbv2-vessel-name{font-family:'Bona Nova',serif;font-size:22px}
.jbv2-vessel-note{font-family:'Inconsolata',monospace;font-size:12px;color:#6f7a63}
.jbv2-photo{background:#eee9d9;display:block;width:100%;height:100%;object-fit:cover}
.jbv2-map iframe{border:0;width:100%;height:100%;display:block}
.jbv2-placeholder{border:1px dashed #8fa37c;background:#eee9d9;display:flex;align-items:center;justify-content:center;font-family:'Inconsolata',monospace;font-size:11px;letter-spacing:.16em;color:#6f7a63;text-align:center;padding:10px}
.jbv2-play{width:58px;height:58px;border:1px solid #24352a;border-radius:50%;display:flex;align-items:center;justify-content:center}
.jbv2-play i{width:0;height:0;border-top:10px solid transparent;border-bottom:10px solid transparent;border-left:16px solid #24352a;margin-left:4px;display:block}
.jbv2-order{padding:56px 44px 60px;position:relative;overflow:hidden}
.jbv2-order-deco{position:absolute;left:-30px;bottom:0;height:300px;mix-blend-mode:multiply;opacity:.45}
.jbv2-order-inner{position:relative;max-width:660px;margin:0 auto}
.jbv2-form{background:#fbf8ef;border:1px solid #24352a;padding:28px;display:flex;flex-direction:column;gap:18px}
.jbv2-form-row{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.jbv2-field{display:flex;flex-direction:column;gap:7px}
.jbv2-field label{font-size:15px}
.jbv2-field input,.jbv2-field select,.jbv2-field textarea{border:1px solid #b9b3a0;background:#fff;padding:11px 12px;font-size:16px;font-family:'Frank Ruhl Libre',Georgia,serif}
.jbv2-field textarea{min-height:110px}
.jbv2-submit{background:#24352a;color:#e9e3d1;border:none;padding:14px;font-size:17px;font-family:'Frank Ruhl Libre',Georgia,serif;cursor:pointer}
.jbv2-msg-success,.jbv2-msg-error{display:none;text-align:center;font-size:17px;margin-top:16px}
.jbv2-msg-error{color:#a33}

/* ---- desktop-only sizing ---- */
.jbv2-desktop .jbv2-eyebrow{font-size:11.5px}
.jbv2-desktop .jbv2-h1{font-size:56px}
.jbv2-desktop .jbv2-body{margin:24px 0 0}
.jbv2-desktop .jbv2-facts{margin-top:30px;border-top:1px solid #cdc3ae;border-bottom:1px solid #cdc3ae}
.jbv2-desktop .jbv2-hero-grid{display:grid;grid-template-columns:1.15fr .85fr}
.jbv2-desktop .jbv2-hero-photo-col{position:relative;border-right:1px solid #24352a;overflow:hidden;min-height:520px}
.jbv2-desktop .jbv2-hero-photo-col img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.jbv2-desktop .jbv2-hero-photo-col .jbv2-hero-grad{position:absolute;inset:0;background:linear-gradient(to top,rgba(35,32,26,.55),rgba(35,32,26,0) 55%)}
.jbv2-desktop .jbv2-hero-photo-col .jbv2-hero-cap{position:absolute;bottom:16px;right:18px;left:18px;font-family:'Inconsolata',monospace;font-size:11px;letter-spacing:.22em;color:#f3ece0}
.jbv2-desktop .jbv2-hero-text{padding:44px 40px 40px}
.jbv2-desktop .jbv2-rule{margin:24px 0}
.jbv2-desktop .jbv2-vessels-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:32px}
.jbv2-desktop .jbv2-studio-grid{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid #cfc9b4}
.jbv2-desktop .jbv2-studio-text{padding:56px 44px}
.jbv2-desktop .jbv2-studio-photo{min-height:420px;border-right:1px solid #cfc9b4}
.jbv2-desktop .jbv2-map{margin-top:12px;height:190px}
.jbv2-desktop .jbv2-gallery-grid{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:190px 190px;gap:14px}
.jbv2-desktop .jbv2-gallery-grid>.jbv2-video{grid-row:span 2;flex-direction:column;gap:14px}

/* ---- mobile-only sizing ---- */
.jbv2-mobile .jbv2-eyebrow{font-size:10.5px;text-align:center}
.jbv2-mobile .jbv2-h1{font-size:36px;text-align:center}
.jbv2-mobile .jbv2-body{margin-top:20px}
.jbv2-mobile .jbv2-rule{margin:18px auto 0;max-width:220px}
.jbv2-mobile .jbv2-facts{margin-top:22px;border-top:1px solid #cdc3ae;border-bottom:1px solid #cdc3ae;grid-template-columns:1fr}
.jbv2-mobile .jbv2-facts>div{display:flex;justify-content:space-between;align-items:baseline;padding:11px 0}
.jbv2-mobile .jbv2-facts>div+div{border-right:none;border-top:1px solid #cdc3ae}
.jbv2-mobile .jbv2-hero-photo{margin:20px 0 0}
.jbv2-mobile .jbv2-hero-photo img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.jbv2-mobile .jbv2-hero-cap{margin-top:8px;text-align:center;font-family:'Inconsolata',monospace;font-size:10.5px;letter-spacing:.22em;color:#6d6353}
.jbv2-mobile .jbv2-cta-wrap{margin-top:22px;text-align:center}
.jbv2-mobile .jbv2-cta{display:block}
.jbv2-mobile .jbv2-vessels-grid{display:flex;flex-direction:column;gap:16px}
.jbv2-mobile .jbv2-vessel-fig img{aspect-ratio:16/10}
.jbv2-mobile .jbv2-studio-photo{height:210px}
.jbv2-mobile .jbv2-map{margin-top:10px;height:160px}
.jbv2-mobile .jbv2-gallery-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.jbv2-mobile .jbv2-gallery-grid>.jbv2-video{grid-column:span 2;aspect-ratio:16/10;flex-direction:column;gap:10px}
.jbv2-mobile .jbv2-gallery-grid>.jbv2-photo-slot{aspect-ratio:1/1}
</style>'''

MAPS_IFRAME = '<iframe src="https://maps.google.com/maps?q=32.0943134,34.7917161&z=15&output=embed" loading="lazy" title="מיקום הסדנה"></iframe>'

def order_form(suffix, extra_class=""):
    s = suffix
    return f'''<div id="workshop-order{s}" class="jbv2-order {extra_class}">
  <img src="images/victorian-sedum.png" alt="" class="jbv2-order-deco"/>
  <div class="jbv2-order-inner">
    <h2 class="jbv2-h2" style="font-size:36px;text-align:center">הזמנת סדנה פרטית</h2>
    <p style="margin:12px 0 30px;font-size:18px;text-align:center;color:#3f4c3f">השאירו פרטים ואחזור אליכם לקבוע תאריך שעה ומחיר</p>
    <form id="wf-form-Workshop-Order{s}" name="wf-form-Workshop-Order" method="POST" action="https://formspree.io/f/meaqqora" class="jbv2-form">
      <div class="jbv2-form-row">
        <div class="jbv2-field"><label for="name{s}">שם</label><input id="name{s}" name="name" type="text" maxlength="256" required="required"/></div>
        <div class="jbv2-field"><label for="phone{s}">טלפון</label><input id="phone{s}" name="phone" type="tel" maxlength="256" required="required"/></div>
      </div>
      <div class="jbv2-field"><label for="email{s}">אימייל</label><input id="email{s}" name="email" type="email" maxlength="256" required="required"/></div>
      <div class="jbv2-form-row">
        <div class="jbv2-field"><label for="participants{s}">עבור כמה אנשים (גם אם משוער)</label><input id="participants{s}" name="participants" type="number" required="required"/></div>
        <div class="jbv2-field"><label for="terrarium_type{s}">איזה כלים תרצו להכין</label>
          <select id="terrarium_type{s}" name="terrarium_type" required="required">
            <option value="Lab 500 ml">כלי מעבדה קטן 500 מ״ל</option>
            <option value="Lab 2000 ml">כלי מעבדה גדול 2000 מ״ל</option>
            <option value="Demijean 10/15">דמיג׳אן 10 / 15 ליטר</option>
          </select>
        </div>
      </div>
      <div class="jbv2-field"><label for="message{s}">משהו נוסף לומר?</label><textarea id="message{s}" name="message" maxlength="5000" placeholder="הקלידו את הודעתכם..."></textarea></div>
      <input type="hidden" name="_subject" value="הזמנת סדנה - Jungle Bubble"/>
      <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off"/>
      <input type="submit" value="שליחה" class="jbv2-submit"/>
    </form>
    <div class="jbv2-msg-success">הפניה נשלחה, תודה!<br/>אצור עמכם קשר בהקדם</div>
    <div class="jbv2-msg-error">חלה שגיאה. אנא נסו שוב...</div>
  </div>
</div>'''

GALLERY_DESKTOP = '''<div class="jbv2-gallery-grid">
  <div class="jbv2-placeholder jbv2-video" style="display:flex"><div class="jbv2-play"><i></i></div><span>סרטון</span></div>
  <div class="jbv2-placeholder jbv2-photo-slot">תמונה 1</div>
  <div class="jbv2-placeholder jbv2-photo-slot">תמונה 2</div>
  <div class="jbv2-placeholder jbv2-photo-slot">תמונה 3</div>
  <div class="jbv2-placeholder jbv2-photo-slot">תמונה 4</div>
</div>'''

GALLERY_MOBILE = '''<div class="jbv2-gallery-grid">
  <div class="jbv2-placeholder jbv2-video" style="display:flex"><div class="jbv2-play"><i></i></div><span>סרטון</span></div>
  <div class="jbv2-placeholder jbv2-photo-slot">תמונה 1</div>
  <div class="jbv2-placeholder jbv2-photo-slot">תמונה 2</div>
</div>'''

FACTS = ['משך','משתתפים','כלול'], ['כשעתיים וחצי','2 עד 12','כל החומרים']

def facts_block():
    labels, vals = FACTS
    rows = "".join(f'<div><div class="jbv2-facts-label">{l}</div><div class="jbv2-facts-val">{v}</div></div>' for l, v in zip(labels, vals))
    return f'<div class="jbv2-facts">{rows}</div>'

def strip_block():
    labels = ['משך הסדנה', 'גודל קבוצה', 'כלול במחיר']
    vals = ['כשעתיים וחצי', '2 עד 12 משתתפים', 'כל החומרים והכלים']
    rows = "".join(f'<div><div class="jbv2-strip-label">{l}</div><div class="jbv2-strip-val">{v}</div></div>' for l, v in zip(labels, vals))
    return f'<div class="jbv2-strip">{rows}</div>'

def vessels_block():
    return f'''<div class="jbv2-vessels-grid">
  <figure class="jbv2-vessel-fig">
    <img src="images/img_9856.jpg" alt="כלי מעבדה קטן"/>
    <figcaption class="jbv2-vessel-cap"><span class="jbv2-vessel-name">כלי מעבדה קטן</span><span class="jbv2-vessel-note">נפח עד 500 מ״ל</span></figcaption>
  </figure>
  <figure class="jbv2-vessel-fig">
    <img src="images/tabs-10.jpg" alt="דמיג׳אן"/>
    <figcaption class="jbv2-vessel-cap"><span class="jbv2-vessel-name">דמיג׳אן</span><span class="jbv2-vessel-note">10 / 15 ליטר</span></figcaption>
  </figure>
</div>'''

PARAGRAPH = 'בואו להכין טרריום אישי בסביבה נעימה ורגועה.יחד נלמד רקע תיאורטי ומשם נגלוש ישר לעבודה מעשית: לעצב ולהכין טרריומים. ההדרכה בסדנה בליווי צמוד וכוללת את כל החומרים הנדרשים לעבודה.'
VESSELS_PARAGRAPH = 'בסדנא הפרטית מתאפשר להכין טרריומים בכל כלי שניתן לאטום. הכלי המקובל להכנת טרריומים גדולים הוא הדמיג׳אן (הכלי בצורת טיפה). ניתן גם להכין בגדלים קטנים יותר בכלי מעבדה שונים'
STUDIO_PARAGRAPH = 'הסדנא ממוקמת בחצר ירוקה, מבודדת ושקטה במדרחוב קטן בצפון הישן של תל אביב. בסדנא תמצאו את כל החומרים והכלים הנדרשים לעבודה.'

DESKTOP = f'''<section class="jbv-desktop-only jbv2-wrap jbv2-desktop" dir="rtl">
  <div style="padding:44px 44px 0">
    <div class="jbv2-frame" style="padding:7px">
      <div class="jbv2-frame jbv2-hero-grid">
        <span class="jbv2-dot" style="top:-5px;right:-5px"></span><span class="jbv2-dot" style="top:-5px;left:-5px"></span>
        <span class="jbv2-dot" style="bottom:-5px;right:-5px"></span><span class="jbv2-dot" style="bottom:-5px;left:-5px"></span>
        <div class="jbv2-hero-text">
          <div class="jbv2-eyebrow">WORKSHOPS · סדנאות</div>
          <h1 class="jbv2-h1">סדנאות טרריום פרטיות לזוגות וקבוצות</h1>
          <div class="jbv2-rule"><span></span><i></i><span></span></div>
          <p class="jbv2-body">{PARAGRAPH}</p>
          {facts_block()}
          <div style="margin-top:28px"><a href="#workshop-order-desktop" class="jbv2-cta">להזמנת סדנה</a></div>
        </div>
        <div class="jbv2-hero-photo-col">
          <img src="images/img_5866.jpg" alt="הסדנה בעבודה"/>
          <div class="jbv2-hero-grad"></div>
          <div class="jbv2-hero-cap">PL. I — הסדנה בעבודה</div>
        </div>
      </div>
    </div>
  </div>

  <div style="height:44px"></div>

  {strip_block()}

  <div style="padding:56px 44px 60px">
    <div style="max-width:620px">
      <h2 class="jbv2-h2" style="font-size:34px">אילו טרריומים ניתן להכין בסדנא</h2>
      <p class="jbv2-body" style="margin-top:14px">{VESSELS_PARAGRAPH}</p>
    </div>
    {vessels_block()}
  </div>

  <div class="jbv2-studio-grid">
    <div class="jbv2-studio-text">
      <h2 class="jbv2-h2" style="font-size:34px">הסדנא בה נעבוד</h2>
      <p class="jbv2-body" style="margin-top:14px">{STUDIO_PARAGRAPH}</p>
      <div style="margin-top:30px;font-size:16px">מיקום הסדנא:</div>
      <div class="jbv2-map">{MAPS_IFRAME}</div>
    </div>
    <div class="jbv2-studio-photo"><img class="jbv2-photo" src="images/67a8ac79b7b7e3d82b75b055_IMG_9803.JPG" alt="החצר בה מתקיימת הסדנה"/></div>
  </div>

  <div style="padding:56px 44px;border-top:1px solid #cfc9b4">
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:26px">
      <h2 class="jbv2-h2" style="font-size:34px;white-space:nowrap">תמונות וסרטים מהסדנה</h2>
      <div style="height:1px;background:#a89d86;flex:1"></div>
    </div>
    {GALLERY_DESKTOP}
  </div>

  {order_form('-desktop')}
</section>'''

MOBILE = f'''<section class="jbv-mobile-only jbv2-wrap jbv2-mobile" dir="rtl">
  <div style="padding:22px 18px 0">
    <div class="jbv2-frame" style="padding:5px">
      <div class="jbv2-frame" style="padding:24px 18px 26px">
        <span class="jbv2-dot" style="top:-4px;right:-4px"></span><span class="jbv2-dot" style="top:-4px;left:-4px"></span>
        <span class="jbv2-dot" style="bottom:-4px;right:-4px"></span><span class="jbv2-dot" style="bottom:-4px;left:-4px"></span>
        <div class="jbv2-eyebrow">WORKSHOPS · סדנאות</div>
        <h1 class="jbv2-h1">סדנאות טרריום פרטיות לזוגות וקבוצות</h1>
        <div class="jbv2-rule"><span></span><i></i><span></span></div>
        <figure class="jbv2-hero-photo" style="margin:20px 0 0">
          <img src="images/img_5866.jpg" alt="הסדנה בעבודה"/>
          <figcaption class="jbv2-hero-cap">PL. I — הסדנה בעבודה</figcaption>
        </figure>
        <p class="jbv2-body" style="font-size:17px">{PARAGRAPH}</p>
        {facts_block()}
        <div class="jbv2-cta-wrap"><a href="#workshop-order-mobile" class="jbv2-cta">להזמנת סדנה</a></div>
      </div>
    </div>
  </div>

  <div style="height:22px"></div>

  {strip_block()}

  <div style="padding:30px 22px 34px">
    <h2 class="jbv2-h2" style="font-size:26px">אילו טרריומים ניתן להכין בסדנא</h2>
    <p class="jbv2-body" style="font-size:17px;margin:12px 0 20px">{VESSELS_PARAGRAPH}</p>
    {vessels_block()}
  </div>

  <div style="border-top:1px solid #cfc9b4">
    <div class="jbv2-studio-photo"><img class="jbv2-photo" src="images/67a8ac79b7b7e3d82b75b055_IMG_9803.JPG" alt="החצר בה מתקיימת הסדנה"/></div>
    <div style="padding:28px 22px 34px">
      <h2 class="jbv2-h2" style="font-size:26px">הסדנא בה נעבוד</h2>
      <p class="jbv2-body" style="font-size:17px;margin-top:12px">{STUDIO_PARAGRAPH}</p>
      <div style="margin-top:20px;font-size:16px">מיקום הסדנא:</div>
      <div class="jbv2-map">{MAPS_IFRAME}</div>
    </div>
  </div>

  <div style="padding:32px 20px;border-top:1px solid #cfc9b4">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px">
      <h2 class="jbv2-h2" style="font-size:24px;white-space:nowrap">תמונות וסרטים</h2>
      <div style="height:1px;background:#a89d86;flex:1"></div>
    </div>
    {GALLERY_MOBILE}
  </div>

  {order_form('-mobile')}
</section>'''

NEW_MIDDLE = CSS + "\n" + DESKTOP + "\n" + MOBILE

start_anchor = '<section id="workshops" class="section_layout">'
end_anchor = '<figure class="footer1_component">'
assert html.count(start_anchor) == 1, "start anchor issue: %d" % html.count(start_anchor)
assert html.count(end_anchor) == 1, "end anchor issue"
start_idx = html.index(start_anchor)
end_idx = html.index(end_anchor)
assert start_idx < end_idx

html = html[:start_idx] + NEW_MIDDLE + html[end_idx:]

# Rewrite the submit-handling script to support multiple forms sharing name="wf-form-Workshop-Order"
old_script_marker = "(function () {\n  var form = document.getElementById('wf-form-Workshop-Order');"
old_script_start = html.find("(function () {\n  var form = document.getElementById")
assert old_script_start != -1, "old script not found"
old_script_end = html.find("})();\n</script></body></html>")
assert old_script_end != -1, "old script end not found"
old_script_end_full = old_script_end + len("})();\n</script>")

new_script = '''(function () {
  var forms = document.querySelectorAll('form[name="wf-form-Workshop-Order"]');
  forms.forEach(function (form) {
    var wrap = form.closest('.jbv2-order-inner') || form.parentElement;
    var doneMsg = wrap.querySelector('.jbv2-msg-success');
    var failMsg = wrap.querySelector('.jbv2-msg-error');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (failMsg) failMsg.style.display = 'none';
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (response) {
        if (response.ok) {
          form.style.display = 'none';
          if (doneMsg) doneMsg.style.display = 'block';
        } else {
          response.json().then(function (data) {
            console.error('Formspree error:', data);
            if (failMsg) failMsg.style.display = 'block';
          });
        }
      }).catch(function (err) {
        console.error('Formspree error:', err);
        if (failMsg) failMsg.style.display = 'block';
      });
    });
  });
})();
</script>'''

html = html[:old_script_start] + new_script + html[old_script_end_full:]

io.open(path, "w", encoding="utf-8").write(html)
print("OK, new length:", len(html))
