import asyncio
import re
from pathlib import Path

import streamlit as st

from crew import blog

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def sanitize_filename(topic: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*]', "", topic)
    safe = re.sub(r"\s+", " ", safe).strip().rstrip(".")
    if not safe:
        safe = "generated_blog"
    return f"{safe}.md"


def run_blog(channel_url: str, topic: str) -> str:
    """Run the async crew.blog() coroutine from within Streamlit's sync context."""
    return asyncio.run(blog(channel_url, topic))


st.set_page_config(
    page_title="AI YouTube Blog Generator",
    page_icon="📝",
    layout="centered",
)

st.title("📝 AI YouTube Blog Generator")
st.caption("Turn any YouTube channel's content into a polished, SEO-friendly blog post using CrewAI + Gemini.")

if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.filename = None

with st.form("blog_form"):
    channel_url = st.text_input(
        "YouTube Channel URL",
        placeholder="https://www.youtube.com/@some-channel",
        help="The channel that will be searched for relevant videos.",
    )
    topic = st.text_input(
        "Topic",
        placeholder="e.g. Retrieval Augmented Generation (RAG)",
        help="What you want the blog post to be about.",
    )
    submitted = st.form_submit_button("Generate Blog", type="primary", use_container_width=True)

if submitted:
    if not channel_url.strip():
        st.error("Please enter a YouTube channel URL.")
    elif not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Researching the channel and writing your blog... this can take a few minutes."):
            try:
                result = run_blog(channel_url.strip(), topic.strip())
                filename = sanitize_filename(topic.strip())
                file_path = OUTPUT_DIR / filename
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(result)

                st.session_state.result = result
                st.session_state.filename = filename
                st.success("Blog generated successfully!")
            except Exception as e:
                st.session_state.result = None
                st.session_state.filename = None
                st.error(f"Something went wrong while generating the blog: {e}")

if st.session_state.result:
    st.divider()
    st.subheader("Generated Blog")
    st.markdown(st.session_state.result)

    st.download_button(
        label="⬇️ Download as Markdown",
        data=st.session_state.result,
        file_name=st.session_state.filename,
        mime="text/markdown",
        use_container_width=True,
    )