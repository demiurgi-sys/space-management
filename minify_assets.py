import re
import os

base_dir = r"c:\Users\infop\OneDrive\Desktop\skill manager\art-of-space-management"

def minify_css(css):
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    css = css.replace('{ ', '{').replace(' {', '{').replace('} ', '}').replace(' }', '}').replace(': ', ':').replace('; ', ';').replace(', ', ',')
    return css.strip()

paths = {
    "styles": os.path.join(base_dir, "assets", "css", "styles.css"),
    "footer": os.path.join(base_dir, "assets", "css", "footer.css")
}

for name, path in paths.items():
    with open(path, "r", encoding="utf-8") as f:
        minified = minify_css(f.read())
    
    out_path = path.replace(".css", ".min.css")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(minified)
    print(f"Created {out_path}")
