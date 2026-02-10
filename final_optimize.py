import os
import re

base_dir = r"c:\Users\infop\OneDrive\Desktop\skill manager\art-of-space-management"
input_path = os.path.join(base_dir, "index.html.bak")
output_path = os.path.join(base_dir, "index.html")

with open(input_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fonts Optimization (Non-blocking)
fonts_optimized = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap">\n'
    '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" media="print" onload="this.media=\'all\'">\n'
    '    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap"></noscript>'
)
html = re.sub(r'<link rel="preconnect".*?>\s*<link rel="preconnect".*?>\s*<link href="https://fonts\.googleapis\.com.*?rel="stylesheet">', fonts_optimized, html, flags=re.DOTALL)

# 2. Minified Styles
html = html.replace('<link rel="stylesheet" href="assets/css/styles.css">', '<link rel="stylesheet" href="assets/css/styles.min.css">')
html = html.replace('<link rel="stylesheet" href="assets/css/footer.css">', '<link rel="stylesheet" href="assets/css/footer.min.css">')

# 3. Favicon
favicon_svg = (
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
    'viewBox=\'0 0 100 100\'%3E%3Crect width=\'100\' height=\'100\' rx=\'20\' fill=\'%23a30000\'/%3E'
    '%3Ctext x=\'50%25\' y=\'50%25\' dominant-baseline=\'central\' text-anchor=\'middle\' '
    'font-family=\'Arial, sans-serif\' font-weight=\'bold\' font-size=\'40\' fill=\'white\'%3EGSD%3C/text%3E%3C/svg%3E">'
)
if "</title>" in html:
    html = html.replace("</title>", "</title>\n    " + favicon_svg)

# 4. Image Dimensions & Cleanup (Fixing PageSpeed warnings)
# Footer Logo
html = html.replace('<img src="assets/images/logo.webp" alt="Grinevich School Logo" class="footer__logo">', 
                    '<img src="assets/images/logo.webp" alt="Grinevich School Logo" class="footer__logo" width="170" height="170">')

# Sales Avatar
html = html.replace('<img src="assets/images/sales_avatar.webp" alt="Група Нескорені" class="sales__avatar">',
                    '<img src="assets/images/sales_avatar.webp" alt="Група Нескорені" class="sales__avatar" width="300" height="300">')

# 5. Telegram Link
html = html.replace('href="https://t.me/olena_grinevich"', 'href="https://t.me/+SCC6z8LsTtWEe8NF"')

# 6. Floating CTA (Restored)
if '</body>' in html:
    cta_html = '\n    <a href="#pricing" class="floating-cta">Забронювати місце</a>\n</body>'
    html = html.replace('</body>', cta_html)

# 7. Metadata (OG tags were missing in the .bak but present in my thought process)
og_tags = (
    '    <meta property="og:title" content="Курс Дизайну Інтер\'єру | Grinevich School">\n'
    '    <meta property="og:description" content="Стань професійним дизайнером за 7 місяців. Навчання з нуля до профі.">\n'
    '    <meta property="og:url" content="https://school-design.space/">\n'
    '    <meta property="og:type" content="website">\n'
    '    <meta property="og:image" content="assets/images/logo.webp">' # Temporary until real OG image exists
)
if '<meta name="description"' in html:
    html = re.sub(r'<meta name="description".*?>', f'<meta name="description" content="Курс дизайну інтер\'єру — стань професійним дизайнером за 7 місяців">\n{og_tags}', html)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Final Vanilla Optimization Complete!")
