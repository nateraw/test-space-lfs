import streamlit as st
import re
from pathlib import Path

st.set_page_config(layout="wide")

REGEX_YAML_BLOCK = re.compile(r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r](.*)", re.DOTALL)

text = Path('README.md').read_text()
match = REGEX_YAML_BLOCK.search(text)
page_content = match.group(2)

st.markdown(page_content, unsafe_allow_html=True)
