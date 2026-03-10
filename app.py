import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="TutorVest: Professores",
    page_icon="🎓",
    layout="wide",
)

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "index.html"
ICON_PATH = ROOT / "tutorvest.jpg"

if not HTML_PATH.exists():
    st.error("Não encontrei o arquivo index.html na raiz do repositório.")
    st.stop()

if not ICON_PATH.exists():
    st.error("Não encontrei o arquivo tutorvest.jpg na raiz do repositório.")
    st.stop()

html = HTML_PATH.read_text(encoding="utf-8")

# Lê o JPG e cria data URI
icon_b64 = base64.b64encode(ICON_PATH.read_bytes()).decode("utf-8")
icon_data_uri = f"data:image/jpeg;base64,{icon_b64}"

# 1) Se seu HTML ainda tiver o placeholder {{BASE64_ICON}}, substitui.
if "{{BASE64_ICON}}" in html:
    html = html.replace("{{BASE64_ICON}}", icon_b64)

# 2) Além disso, garante que os <img> do ícone recebam o src certo,
# mesmo se o JS não estiver setando corretamente.
# (coloca um script no final forçando src nos 2 IDs usados no mockup)
inject = f"""
<script>
  (function() {{
    const src = "{icon_data_uri}";
    const ids = ["appIcon", "appIconLogin"];
    ids.forEach(id => {{
      const el = document.getElementById(id);
      if (el) el.src = src;
    }});
  }})();
</script>
"""
html = html + inject

# Opcional: reduzir “margens Streamlit” pro app parecer fullscreen
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      .block-container {padding-top: 0.5rem; padding-bottom: 0.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(html, height=1100, scrolling=True)
