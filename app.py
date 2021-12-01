import streamlit as st
import re
from pathlib import Path


REGEX_YAML_BLOCK = re.compile(r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r](.*)", re.DOTALL)

text = Path('README.md').read_text()
match = REGEX_YAML_BLOCK.search(text)
page_content = match.group(2)

st.markdown(page_content)
# st.markdown(
#     """
#     <p align="center">
#         <a href="https://github.com/nateraw/huggingpics-explorer" alt="Repo"><img src="https://img.shields.io/github/stars/nateraw/huggingpics-explorer?style=social" /></a>
#     </p>
#     """,
#     unsafe_allow_html=True,
# )
# st.write('Some change!')