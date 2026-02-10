import os
import re

base_dir = r"c:\Users\infop\OneDrive\Desktop\skill manager\art-of-space-management"
html_path = os.path.join(base_dir, "index.html")
styles_path = os.path.join(base_dir, "assets", "css", "styles.css")

with open(styles_path, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Fix non-composited animations
# imageShimmer fix (left -> transform)
css = css.replace(
    'animation: imageShimmer 3s infinite;',
    'animation: imageShimmer 3s infinite; will-change: transform;'
)
css = re.sub(
    r'@keyframes imageShimmer \{.*?\}',
    '@keyframes imageShimmer { 0% { transform: translateX(0) skewX(-25deg); } 20% { transform: translateX(600%) skewX(-25deg); } 100% { transform: translateX(600%) skewX(-25deg); } }',
    css, flags=re.DOTALL
)

# textShimmer fix (will-change)
css = css.replace(
    'animation: textShimmer 3s linear infinite;',
    'animation: textShimmer 3s linear infinite; will-change: background-position;'
)

# shine fix (will-change)
css = css.replace(
    'animation: shine 3s linear infinite;',
    'animation: shine 3s linear infinite; will-change: background-position;'
)

# 2. Add will-change to pulse
css = css.replace(
    'animation: pulse 2s infinite;',
    'animation: pulse 2s infinite; will-change: transform, box-shadow;'
)

# 3. Extract Critical CSS (Reset + Root + Hero)
# Roughly lines 1-500
critical_parts = []
# Root
match = re.search(r':root\s*\{.*?\}', css, re.DOTALL)
if match: critical_parts.append(match.group(0))
# Reset
match = re.search(r'/\* Reset & Base \*/(.*?)/\* Hero Section \*/', css, re.DOTALL)
# Actually just take up to Hero
critical_parts.append(css[:css.find('/* Pre-Training Section */')])

critical_css_raw = "\n".join(critical_parts)

def minify_css(content):
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'\s+', ' ', content)
    return content.replace('{ ', '{').replace(' {', '{').replace('} ', '}').replace(' }', '}').replace(': ', ':').replace('; ', ';').replace(', ', ',').strip()

critical_css_min = minify_css(critical_css_raw)
full_styles_min = minify_css(css)

# Save minified full styles
with open(os.path.join(base_dir, "assets", "css", "styles.min.css"), "w", encoding="utf-8") as f:
    f.write(full_styles_min)

# 4. Update index.html
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inline Critical CSS & Load Full CSS Async
css_links = (
    f'<style id="critical-css">{critical_css_min}</style>\n'
    '    <link rel="preload" as="style" href="assets/css/styles.min.css" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
    '    <noscript><link rel="stylesheet" href="assets/css/styles.min.css"></noscript>\n'
    '    <link rel="preload" as="style" href="assets/css/footer.min.css" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
    '    <noscript><link rel="stylesheet" href="assets/css/footer.min.css"></noscript>'
)

# Replace old CSS links
html = re.sub(r'<link rel="stylesheet" href="assets/css/styles\.min\.css">.*?<link rel="stylesheet" href="assets/css/footer\.min\.css">', css_links, html, flags=re.DOTALL)

# 5. Fix JS (Layout Thrashing)
# Find offsetWidth/Height and cache them
html = html.replace(
    'const cardWidth = grid.querySelector(\'.pre-training__card\').offsetWidth + 20;',
    'const firstCard = grid.querySelector(\'.pre-training__card\'); const cardWidth = firstCard ? (firstCard.offsetWidth + 20) : 320;'
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Surgical Optimization Applied!")
