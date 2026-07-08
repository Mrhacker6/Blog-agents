from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from crew import blog
from pathlib import Path
import re
from urllib.parse import quote

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="AI YouTube Blog Generator API",
    description="CrewAI-powered API for generating blogs from YouTube channels",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------
class BlogRequest(BaseModel):
    channel: str
    topic: str


def sanitize_filename(topic: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*]', "", topic)
    safe = re.sub(r"\s+", " ", safe).strip().rstrip(".")
    if not safe:
        safe = "generated_blog"
    return f"{safe}.md"


def resolve_output_file(filename: str) -> Path:
    safe_name = Path(filename).name
    file_path = (OUTPUT_DIR / safe_name).resolve()

    try:
        file_path.relative_to(OUTPUT_DIR.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="File not found.") from exc

    return file_path


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.get("/api")
async def api_status():
    return {
        "status": "running",
        "message": "AI YouTube Blog Generator API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# -----------------------------
# Generate Blog Endpoint
# -----------------------------
@app.post("/generate")
async def generate_blog(request: BlogRequest):

    if not request.channel.strip():
        raise HTTPException(
            status_code=400,
            detail="Channel URL cannot be empty."
        )

    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Topic cannot be empty."
        )

    try:
        result = await blog(
            request.channel,
            request.topic
        )

        filename = sanitize_filename(request.topic)
        file_path = OUTPUT_DIR / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result)

        return {
            "success": True,
            "topic": request.topic,
            "channel": request.channel,
            "blog": result,
            "download_file": filename,
            "download_url": f"/download/{quote(filename)}"
        }

    except HTTPException:
        raise

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Download Markdown
# -----------------------------
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = resolve_output_file(filename)

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="text/markdown"
    )


app.mount("/static", StaticFiles(directory="static"), name="static")
