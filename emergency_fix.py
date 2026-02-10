import os
import re

base_dir = r"c:\Users\infop\OneDrive\Desktop\skill manager\art-of-space-management"
html_path = os.path.join(base_dir, "index.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix Blocking Fonts (CRITICAL LCP FIX)
# Find the blocking link
blocking_font_pattern = r'<link\s+href="https://fonts\.googleapis\.com/css2\?family=Montserrat:[^"]+"\s+rel="stylesheet">'
# Replacement (Async pattern)
async_font_replacement = (
    '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap">\n'
    '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" media="print" onload="this.media=\'all\'">\n'
    '    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap"></noscript>'
)

html = re.sub(blocking_font_pattern, async_font_replacement, html, flags=re.DOTALL)

# 2. Disable heavy animations on mobile (Performance Fix)
# Inject a style block right after the critical css
mobile_optimization_css = (
    '\n    <style>\n'
    '        @media (max-width: 768px) {\n'
    '            /* Disable heavy animations on mobile to save GPU/Battery and speed up rendering */\n'
    '            .hero__title, .hero__cta--primary, .sales__title, .sales__cta .btn--large, .floating-cta, .btn--premium {\n'
    '                animation: none !important;\n'
    '                will-change: auto !important;\n'
    '            }\n'
    '            /* Static gradients for visual consistency without animation */\n'
    '            .hero__cta--primary, .btn--premium, .floating-cta {\n'
    '                background: linear-gradient(110deg, #d94444 0%, #a30000 100%) !important;\n'
    '            }\n'
    '        }\n'
    '    </style>'
)

if '</style>' in html:
    # Append after the first style block (critical css)
    html = html.replace('</style>', '</style>' + mobile_optimization_css, 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Emergency Fix Applied: Fonts Async + Mobile Animations Disabled")
