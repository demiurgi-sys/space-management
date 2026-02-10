import os
import re

base_dir = r"c:\Users\infop\OneDrive\Desktop\skill manager\art-of-space-management"
input_path = os.path.join(base_dir, "index.html.bak")
styles_path = os.path.join(base_dir, "assets", "css", "styles.css")
footer_path = os.path.join(base_dir, "assets", "css", "footer.css")
output_path = os.path.join(base_dir, "index.html") # Overwriting the slow one

def minify_css(css):
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    css = css.replace('{ ', '{').replace(' {', '{').replace('} ', '}').replace(' }', '}').replace(': ', ':').replace('; ', ';').replace(', ', ',')
    return css.strip()

print(f"Reading base structure from {input_path}...")
with open(input_path, "r", encoding="utf-8") as f:
    html = f.read()

print("Reading and minifying styles...")
with open(styles_path, "r", encoding="utf-8") as f:
    styles = minify_css(f.read())

with open(footer_path, "r", encoding="utf-8") as f:
    footer = minify_css(f.read())

# 1. Non-blocking Google Fonts
# Replace blocking link with a high-performance one
fonts_link = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap">\n'
    '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" media="print" onload="this.media=\'all\'">\n'
    '    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap"></noscript>'
)

# Replace old font link and preconnects
html = re.sub(r'<link rel="preconnect".*?>\s*<link rel="preconnect".*?>\s*<link href="https://fonts\.googleapis\.com.*?rel="stylesheet">', fonts_link, html, flags=re.DOTALL)

# 2. Favicon
favicon_svg = (
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
    'viewBox=\'0 0 100 100\'%3E%3Crect width=\'100\' height=\'100\' rx=\'20\' fill=\'%23a30000\'/%3E'
    '%3Ctext x=\'50%25\' y=\'50%25\' dominant-baseline=\'central\' text-anchor=\'middle\' '
    'font-family=\'Arial, sans-serif\' font-weight=\'bold\' font-size=\'40\' fill=\'white\'%3EGSD%3C/text%3E%3C/svg%3E">'
)
html = html.replace("</title>", "</title>\n    " + favicon_svg)

# 3. Inline Minified CSS
# Remove old stylesheet links if any
html = re.sub(r'<link rel="stylesheet" href="assets/css/.*?">', '', html)

combined_css = f"<style>{styles}{footer}</style>"
html = html.replace("</head>", combined_css + "\n</head>")

# 4. Final Polish: Update Telegram link (just in case)
html = html.replace('href="https://t.me/olena_grinevich"', 'href="https://t.me/+SCC6z8LsTtWEe8NF"')

print(f"Writing optimized HTML to {output_path}...")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Optimization 2.0 Complete!")
