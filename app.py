import base64
from pathlib import Path

import streamlit as st

TOPICS_PER_ROW = 4
BACKGROUND_IMAGE = Path(__file__).parent / "assets" / "background.webp"
# 0 = photo at full brightness, 1 = completely black. Higher = easier to read.
BACKGROUND_DARKNESS = 0.65


@st.cache_data
def _image_as_base64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def set_background(image_path, darkness):
    # The image is embedded in the CSS as base64, so no static file server is
    # needed. A dark gradient is layered on top of it to keep text readable.
    encoded = _image_as_base64(str(image_path))
    st.markdown(f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0, 0, 0, {darkness}), rgba(0, 0, 0, {darkness})),
                url("data:image/webp;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        .stApp h1, .stApp [data-testid="stMarkdownContainer"] p {{
            color: #ffffff;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
        }}
        /* Button labels are markdown paragraphs too, so the rule above would
           make them white. This more specific rule keeps them black. */
        .stApp .stButton button {{
            background-color: #ffffff;
        }}
        .stApp .stButton button [data-testid="stMarkdownContainer"] p {{
            color: #000000;
            text-shadow: none;
        }}
        </style>
    """, unsafe_allow_html=True)


set_background(BACKGROUND_IMAGE, BACKGROUND_DARKNESS)

st.title("News with AI")
st.write("Choose the topic you would like to see the news summary.")
topics = ["Science", "Finance", "Business", "Technology", "Health", "Sport",  "Politics", "Education"]

for i, topic in enumerate(topics):
    # Start a new row of columns every TOPICS_PER_ROW topics
    if i % TOPICS_PER_ROW == 0:
        columns = st.columns(TOPICS_PER_ROW)
    with columns[i % TOPICS_PER_ROW]:
        if st.button(topic, width="stretch"):
            st.switch_page(f"pages/{topic}.py")
