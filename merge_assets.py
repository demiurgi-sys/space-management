import os
import re

base_dir = r"c:\Users\infop\OneDrive\Desktop\skill manager\art-of-space-management"
index_path = os.path.join(base_dir, "index.html")
styles_path = os.path.join(base_dir, "assets", "css", "styles.css")
footer_path = os.path.join(base_dir, "assets", "css", "footer.css")
output_path = os.path.join(base_dir, "index_optimized.html")

print(f"Reading {index_path}...")
with open(index_path, "r", encoding="utf-8") as f:
    html_content = f.read()

print(f"Reading {styles_path}...")
with open(styles_path, "r", encoding="utf-8") as f:
    css_styles = f.read()

print(f"Reading {footer_path}...")
with open(footer_path, "r", encoding="utf-8") as f:
    css_footer = f.read()

# 1. Favicon Injection
favicon_svg = (
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
    'viewBox=\'0 0 100 100\'%3E%3Crect width=\'100\' height=\'100\' rx=\'20\' fill=\'%23a30000\'/%3E'
    '%3Ctext x=\'50%25\' y=\'50%25\' dominant-baseline=\'central\' text-anchor=\'middle\' '
    'font-family=\'Arial, sans-serif\' font-weight=\'bold\' font-size=\'70\' fill=\'white\'%3EA%3C/text%3E%3C/svg%3E">'
)

if "</title>" in html_content:
    html_content = html_content.replace("</title>", "</title>\n    " + favicon_svg)
else:
    print("Warning: </title> tag not found, inserting favicon in head.")
    html_content = html_content.replace("<head>", "<head>\n    " + favicon_svg)

# 2. CSS Injection
# Remove existing link tags
html_content = re.sub(r'\s*<link rel="stylesheet" href="assets/css/styles\.css">', '', html_content)
html_content = re.sub(r'\s*<link rel="stylesheet" href="assets/css/footer\.css">', '', html_content)

# Prepare inline styles
inline_style = f"\n    <style>\n/* Main Styles */\n{css_styles}\n\n/* Footer Styles */\n{css_footer}\n    </style>"

# Insert before </head>
if "</head>" in html_content:
    html_content = html_content.replace("</head>", inline_style + "\n</head>")
else:
    print("Error: </head> tag not found!")

# 3. Write Output
print(f"Writing to {output_path}...")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Optimization Successfully Completed!")
