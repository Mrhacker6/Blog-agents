import gradio as gr
from crew import blog
import time


# -----------------------------
# Blog Generator Function
# -----------------------------
def generate_blog(channel, topic):

    if not channel or not topic:
        raise gr.Error("Please fill all the fields.")

    progress_text = "🔍 Research Agent is searching YouTube..."

    yield progress_text, "", None

    time.sleep(0.5)

    progress_text = "📺 Extracting video insights..."

    yield progress_text, "", None

    time.sleep(0.5)

    progress_text = "🧠 AI is understanding the content..."

    yield progress_text, "", None

    result = blog(channel, topic)

    filename = f"{topic}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    yield "✅ Blog Generated Successfully!", result, filename


# -----------------------------
# UI
# -----------------------------
with gr.Blocks(
    title="AI YouTube Blog Generator",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
# 🤖 AI YouTube Blog Generator

Generate high-quality blogs from **ANY YouTube Channel**
using **CrewAI Agents**
"""
    )

    with gr.Row():

        channel = gr.Textbox(
            label="📺 YouTube Channel URL",
            placeholder="https://www.youtube.com/..."
        )

        topic = gr.Textbox(
            label="📝 Blog Topic",
            placeholder="LangGraph..?"
        )

    generate_btn = gr.Button(
        "🚀 Generate Blog",
        variant="primary"
    )

    status = gr.Markdown()

    output = gr.Markdown(label="Generated Blog")

    download = gr.File(label="Download Markdown")

    generate_btn.click(
        fn=generate_blog,
        inputs=[channel, topic],
        outputs=[status, output, download]
    )

    gr.Markdown("---")

    gr.Markdown("## 🤖 CrewAI Dashboard")

    gr.Markdown("""
### 👨‍💻 Active Agents

- 🔍 Research Agent
- ✍ Blog Writer

---

### ⚙ Configuration

- LLM : gemini-2.5-flash
- Execution : Sequential
- Memory : Disabled
- Cache : Disabled

---

### 📈 Features

- ✅ Dynamic YouTube Channel
- ✅ AI Research
- ✅ Blog Generation
- ✅ Markdown Export
""")


demo.launch()