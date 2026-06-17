import streamlit as st
import base64
from pathlib import Path

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from PIL import Image
import time
"""

st.set_page_config(
    page_title="Tamil Poetry Studio Royal",
    layout="wide"
)

# ==========================================
# Helpers
# ==========================================

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_asset_files(folder):
    folder = Path(folder)

    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)

    files = sorted([
        f.name
        for f in folder.iterdir()
        if f.suffix.lower() in [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        ]
    ])

    return files

def pretty_name(filename):
    return (
        filename
        .replace("_", " ")
        .replace(".png", "")
        .replace(".jpg", "")
        .replace(".jpeg", "")
        .replace(".webp", "")
        .title()
    )

# ==========================================
# Theme Config
# ==========================================

THEMES = {

    "Royal": {
        "title": "#6b4a22",
        "poem": "#3d2b15",
        "author": "#6b4a22",
        "watermark": "#7a5126"
    },

    "Black Gold": {
        "title": "#d4af37",
        "poem": "#f5e6a8",
        "author": "#d4af37",
        "watermark": "#c9a227"
    },

    "Temple": {
        "title": "#5d4037",
        "poem": "#3e2723",
        "author": "#5d4037",
        "watermark": "#795548"
    },

    "Sangam": {
        "title": "#704214",
        "poem": "#4b2e19",
        "author": "#704214",
        "watermark": "#8b5a2b"
    }
}

# ==========================================
# Discover Assets Automatically
# ==========================================

border_files = get_asset_files(
    "assets/borders"
)

quill_files = get_asset_files(
    "assets/quills"
)

background_files = get_asset_files(
    "assets/backgrounds"
)

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("🎨 Design Studio")

theme = st.sidebar.selectbox(
    "Theme",
    list(THEMES.keys())
)

border_choice = st.sidebar.selectbox(
    "Border",
    border_files,
    format_func=pretty_name
)

quill_choice = st.sidebar.selectbox(
    "Quill",
    quill_files,
    format_func=pretty_name
)

bg_choice = st.sidebar.selectbox(
    "Background",
    background_files,
    format_func=pretty_name
)

quill_position = st.sidebar.selectbox(
    "Quill Position",
    [
        "Top Center",
        "Top Left",
        "Top Right"
    ]
)

# ==========================================
# Inputs
# ==========================================

st.title("📜 Tamil Poetry Studio Royal")

title = st.text_input(
    "தலைப்பு"
)

poem = st.text_area(
    "கவிதை",
    height=250
)

author = st.text_input(
    "ஆசிரியர்",
    "சமரன்"
)

watermark = st.text_input(
    "Watermark",
    "சமரன் கவிதைகள்"
)

# ==========================================

# Smart Font Fit

# ==========================================

lines = poem.splitlines()

line_count = max(len(lines), 1)

longest_line = max(
[len(line) for line in lines],
default=1
)

char_count = len(poem)

# Start large

font_px = 48

# Reduce based on total content

estimated_height = (
line_count * font_px * 1.8
)

while estimated_height > 420 and font_px > 18:


 font_px -= 2

 estimated_height = (
    line_count * font_px * 1.8
)


# Additional reduction for long lines

if longest_line > 40:
 font_px -= 2

if longest_line > 55:
 font_px -= 2

font_px = max(font_px, 18)

poem_font_size = "48px"


# ==========================================
# Theme
# ==========================================

theme_cfg = THEMES[theme]

# ==========================================
# Asset Paths
# ==========================================

border_path = (
    Path("assets/borders")
    / border_choice
)

quill_path = (
    Path("assets/quills")
    / quill_choice
)

bg_path = (
    Path("assets/backgrounds")
    / bg_choice
)

border_b64 = image_to_base64(border_path)
quill_b64 = image_to_base64(quill_path)
bg_b64 = image_to_base64(bg_path)

# ==========================================
# Quill Position
# ==========================================

quill_positions = {

    "Top Center":
        "top:40px;left:50%;transform:translateX(-50%);",

    "Top Left":
        "top:40px;left:80px;",

    "Top Right":
        "top:40px;right:80px;"
}

# ==========================================
# HTML
# ==========================================

html = f"""
<!DOCTYPE html>
<html lang="ta">

<head>

<meta charset="UTF-8">

<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&display=swap" rel="stylesheet">

<style>

body {{
    margin:0;
}}

.container {{
    position:relative;
    width:1080px;
    height:1080px;
    font-family:'Noto Serif Tamil', serif;
}}

.background {{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
}}

.border {{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
}}

.header {{
    position:absolute;
    top:40px;
    width:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    z-index:20;
}}

.quill {{
    width:220px;
    display:block;
    margin:0;
}}

.title {{
    margin-top:2px;
    text-align:center;
    color:{theme_cfg["title"]};
    font-size:64px;
    font-weight:700;
    line-height:1.1;
}}

.content {{
    position:absolute;
    top:330px;
    left:8%;
    width:84%;
    height:500px;
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
    z-index:20;
}}

.poem {{
    width:100%;
    text-align:center;
    color:{theme_cfg["poem"]};
    font-size:48px;
    line-height:1.6;
    word-break:break-word;
}}


.author {{

    position:absolute; 
    bottom:110px; 
    width:100%; 
    text-align:center; 
    color:{theme_cfg["author"]}; 
    font-size:34px; 
    z-index:20;
}}

.watermark {{
    position:absolute;
    bottom:15px;
    right:35px;
    color:{theme_cfg["watermark"]};
    font-size:24px;
    font-weight:700;
    opacity:.75;
    text-shadow:
        1px 1px 2px rgba(255,255,255,.5);
}}

</style>

</head>

<body>

<div class="container">

<img class="background"
src="data:image/jpeg;base64,{bg_b64}">

<img class="border"
src="data:image/jpeg;base64,{border_b64}">

<div class="header">

    <img
        class="quill"
        src="data:image/png;base64,{quill_b64}"
    >

    <div class="title">
        {title}
    </div>

</div>

<div class="content">

<div class="poem">
{poem.replace(chr(10), "<br>")}
</div>

</div>

<div class="author">
❦══════❖══════❦<br>
{author}<br>
❦══════❖══════❦
</div>

<div class="watermark">
✦ {watermark} ✦
</div>

</div>

<script>

window.onload = function() {{

    const poem =
        document.querySelector('.poem');

    const content =
        document.querySelector('.content');

    let size = 48;

    poem.style.fontSize =
        size + "px";

    while (
        poem.scrollHeight >
        content.clientHeight &&
        size > 16
    ) {{

        size--;

        poem.style.fontSize =
            size + "px";
    }}
}}

</script>

</body>
</html>
"""


st.components.v1.html(
    html,
    height=1100,
    scrolling=False
)

# ==========================================

# PNG Export (Temporary Test)

# ==========================================

st.info(
"PNG Export will be migrated from Selenium to browser-side capture."
)


