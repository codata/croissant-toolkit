import os
import re
import json
import logging
import subprocess
import tempfile
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(BASE_DIR, "..", "skills")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "..", "data", "transcripts")
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("croissant-api")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
))

file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "api.log"),
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def run_skill(script_path: str, args: list[str], timeout: int = 120) -> str:
    """Run a skill script as a subprocess and return its stdout.

    Args:
        script_path: Path to the Python script.
        args: CLI arguments to pass.
        timeout: Max execution time in seconds.

    Returns:
        The stdout output from the script.

    Raises:
        RuntimeError: If the script exits with a non-zero code.
    """
    cmd = ["python3", script_path, *args]
    logger.debug("[run_skill] Running: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=os.path.join(BASE_DIR, ".."),
    )
    if result.stderr:
        logger.debug("[run_skill] stderr: %s", result.stderr.strip())
    if result.returncode != 0:
        logger.error("[run_skill] Script failed (rc=%d): %s", result.returncode, result.stderr.strip())
        raise RuntimeError(f"Skill script failed: {result.stderr.strip()}")
    return result.stdout


YOUTUBE_PATTERN = re.compile(
    r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([0-9A-Za-z_-]{11})'
)


def get_video_id(url: str) -> str | None:
    """Extract a YouTube video ID from a URL."""
    match = YOUTUBE_PATTERN.search(url)
    return match.group(1) if match else None


app = FastAPI(title="Croissant Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_NAME = "gemini-3-pro-preview"


def get_model():
    """Configure and return the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


def log_skill_call(skill: str, input_summary: str, output_summary: str, duration_ms: float):
    """Log a skill invocation with input/output and timing."""
    separator = "=" * 80
    logger.debug(
        "\n%s\n"
        "SKILL CALL — %s\n"
        "timestamp: %s\n"
        "duration: %.0fms\n"
        "%s\n"
        "INPUT:\n%s\n"
        "%s\n"
        "OUTPUT:\n%s\n"
        "%s",
        separator, skill,
        datetime.now(timezone.utc).isoformat(), duration_ms,
        "-" * 40, input_summary, "-" * 40, output_summary, separator,
    )


def log_gemini_call(skill: str, prompt: str, response_text: str, duration_ms: float):
    """Log a Gemini API call with prompt, response and timing."""
    separator = "=" * 80
    logger.debug(
        "\n%s\n"
        "GEMINI CALL — skill: %s\n"
        "model: %s\n"
        "timestamp: %s\n"
        "duration: %.0fms\n"
        "%s\n"
        "PROMPT:\n%s\n"
        "%s\n"
        "RESPONSE:\n%s\n"
        "%s",
        separator, skill, MODEL_NAME,
        datetime.now(timezone.utc).isoformat(), duration_ms,
        "-" * 40, prompt, "-" * 40, response_text, separator,
    )


class PageContent(BaseModel):
    """Content extracted from a web page."""
    url: str
    title: str
    description: str
    keywords: list[str] = []
    headings: list[str] = []
    links: list[str] = []
    images: list[dict] = []
    body_text: str = ""
    lang: str = "en"


class ChatRequest(BaseModel):
    """Chat request with Croissant context."""
    message: str
    croissant: dict
    history: list[dict] = []


def clean_json_response(text: str) -> str:
    """Strip markdown fences from a JSON response."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every incoming HTTP request."""
    start = datetime.now(timezone.utc)
    logger.info("[request] %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration = (datetime.now(timezone.utc) - start).total_seconds() * 1000
    logger.info("[response] %s %s | status=%d | %.0fms", request.method, request.url.path, response.status_code, duration)
    return response


@app.post("/generate-croissant")
async def generate_croissant(content: PageContent):
    """Generate a Croissant JSON-LD using the toolkit skills pipeline.

    Pipeline:
    1. Translator skill — detect language and translate if needed
    2. NLP Expert skill — extract named entities (Gemini call)
    3. Croissant Expert skill — serialize into Croissant JSON-LD with NLP enrichment
    """
    pipeline_start = datetime.now(timezone.utc)
    skills_used = []

    logger.info("[generate-croissant] Starting pipeline | url=%s title=%s lang=%s",
                content.url, content.title, content.lang)
    logger.debug("[generate-croissant] Full input | headings=%s links_count=%d images_count=%d body_len=%d",
                 content.headings[:10], len(content.links), len(content.images), len(content.body_text))

    text_for_nlp = f"{content.title}. {content.description}. {' '.join(content.headings)}. {content.body_text[:3000]}"
    translator_script = os.path.join(SKILLS_DIR, "translator", "scripts", "translate.py")
    nlp_script = os.path.join(SKILLS_DIR, "nlp_expert", "scripts", "extract_entities.py")
    transcriber_script = os.path.join(SKILLS_DIR, "transcriber", "scripts", "transcribe.py")
    serializer_script = os.path.join(SKILLS_DIR, "croissant_expert", "scripts", "serialize.py")

    # Step 1: Translator skill — detect language, translate if not English
    translated_text = text_for_nlp
    detected_lang = content.lang

    try:
        start = datetime.now(timezone.utc)
        logger.info("[skill:translator] Running translate subprocess | text_len=%d", len(text_for_nlp))
        stdout = run_skill(translator_script, [text_for_nlp[:3000]])
        duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000

        for line in stdout.splitlines():
            if line.startswith("[Language Recognition]:"):
                detected_lang = line.split(":", 1)[1].strip()
            elif line.startswith("[English Translation]:"):
                translated_text = line.split(":", 1)[1].strip()

        if not translated_text.startswith("[English Translation]"):
            lines = stdout.splitlines()
            translation_start = None
            for i, line in enumerate(lines):
                if "[English Translation]" in line:
                    translation_start = i + 1
                    break
            if translation_start is not None:
                translation_lines = []
                for line in lines[translation_start:]:
                    if line.strip().startswith("--"):
                        break
                    translation_lines.append(line)
                if translation_lines:
                    translated_text = "\n".join(translation_lines).strip()

        skills_used.append("translator")
        log_skill_call(
            "translator",
            f"text_len={len(text_for_nlp)} first_100_chars={text_for_nlp[:100]}",
            f"detected_lang={detected_lang} translated_len={len(translated_text)}",
            duration_ms,
        )
        logger.info("[skill:translator] Done | detected_lang=%s duration=%.0fms", detected_lang, duration_ms)
    except Exception as e:
        logger.error("[skill:translator] Error: %s", e, exc_info=True)

    # Step 2: NLP Expert skill — extract entities
    entities = None
    try:
        start = datetime.now(timezone.utc)
        logger.info("[skill:nlp_expert] Running extract_entities subprocess | text_len=%d", len(translated_text))
        stdout = run_skill(nlp_script, [translated_text[:3000]])
        duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000

        json_start = stdout.find("{")
        json_end = stdout.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            entities = json.loads(stdout[json_start:json_end])

        if entities:
            entity_count = len(entities.get("itemListElement", []))
            skills_used.append("nlp_expert")
            log_skill_call(
                "nlp_expert (extract_entities)",
                f"text_len={len(translated_text)} first_100_chars={translated_text[:100]}",
                f"entity_count={entity_count} entities={json.dumps(entities, ensure_ascii=False)[:500]}",
                duration_ms,
            )
            logger.info("[skill:nlp_expert] Done | entities=%d duration=%.0fms", entity_count, duration_ms)
        else:
            logger.warning("[skill:nlp_expert] No entities parsed from output")
    except Exception as e:
        logger.error("[skill:nlp_expert] Error: %s", e, exc_info=True)

    # Step 3: Build metadata dict (BEFORE transcriber so it can append to it)
    full_description = content.description or translated_text[:500]

    metadata = {
        "name": content.title or "Untitled Dataset",
        "description": full_description,
        "url": content.url,
        "license": "CC-BY-4.0",
        "keywords": content.keywords if content.keywords else [],
        "creator": [],
        "publisher": [],
        "spatialCoverage": [],
        "temporalCoverage": [],
        "distribution": [
            {
                "type": "FileObject",
                "name": "web_page",
                "contentUrl": content.url,
                "encodingFormat": "text/html",
            }
        ],
        "recordSet": [
            {
                "name": "page_content",
                "field": [
                    {
                        "name": "body_text",
                        "dataType": "sc:Text",
                        "source_file": "web_page",
                        "extract_property": "content",
                    }
                ],
            }
        ],
        "apply_nlp": True,
        "nlp_text": translated_text[:3000],
    }

    if content.images:
        for i, img in enumerate(content.images[:5]):
            metadata["distribution"].append({
                "type": "FileObject",
                "name": f"image_{i}",
                "contentUrl": img.get("src", ""),
                "encodingFormat": "image/jpeg",
            })
        metadata["recordSet"].append({
            "name": "images",
            "field": [
                {"name": "image_url", "dataType": "sc:URL", "source_file": "image_0"},
                {"name": "alt_text", "dataType": "sc:Text"},
            ],
        })

    if content.headings:
        metadata["recordSet"].append({
            "name": "headings",
            "field": [
                {"name": "heading_text", "dataType": "sc:Text", "source_file": "web_page"},
            ],
        })

    if content.links:
        metadata["recordSet"].append({
            "name": "links",
            "field": [
                {"name": "link_url", "dataType": "sc:URL", "source_file": "web_page"},
            ],
        })

    # Step 4: Transcriber skill — detect YouTube links and transcribe videos
    video_ids = list(set(YOUTUBE_PATTERN.findall(" ".join(content.links))))
    transcripts_text = ""

    if video_ids:
        logger.info("[skill:transcriber] Found %d YouTube video(s): %s", len(video_ids), video_ids)
        for vid in video_ids[:3]:
            try:
                start = datetime.now(timezone.utc)
                logger.info("[skill:transcriber] Transcribing video %s", vid)
                run_skill(transcriber_script, [vid])
                duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000

                transcript_path = os.path.join(TRANSCRIPTS_DIR, f"{vid}.txt")
                if os.path.exists(transcript_path):
                    with open(transcript_path, "r", encoding="utf-8") as f:
                        transcript = f.read()
                    transcripts_text += f"\n[Video {vid}]: {transcript[:2000]}"

                    metadata["distribution"].append({
                        "type": "FileObject",
                        "name": f"video_transcript_{vid}",
                        "contentUrl": f"https://youtube.com/watch?v={vid}",
                        "encodingFormat": "text/plain",
                    })

                    log_skill_call(
                        f"transcriber (video: {vid})",
                        f"video_id={vid}",
                        f"transcript_len={len(transcript)}",
                        duration_ms,
                    )
                    logger.info("[skill:transcriber] Done | video=%s duration=%.0fms transcript_len=%d", vid, duration_ms, len(transcript))
                else:
                    logger.warning("[skill:transcriber] No transcript file for video %s", vid)
            except Exception as e:
                logger.error("[skill:transcriber] Error for video %s: %s", vid, e, exc_info=True)

        if transcripts_text:
            skills_used.append("transcriber")
            text_for_nlp += transcripts_text
            translated_text += transcripts_text

            metadata["recordSet"].append({
                "name": "video_transcripts",
                "field": [
                    {"name": "video_id", "dataType": "sc:Text"},
                    {"name": "transcript_text", "dataType": "sc:Text"},
                ],
            })

    # Also check if the page URL itself is a YouTube video
    page_video_id = get_video_id(content.url)
    if page_video_id and page_video_id not in video_ids:
        try:
            start = datetime.now(timezone.utc)
            logger.info("[skill:transcriber] Page is a YouTube video: %s", page_video_id)
            run_skill(transcriber_script, [page_video_id])
            duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000

            transcript_path = os.path.join(TRANSCRIPTS_DIR, f"{page_video_id}.txt")
            if os.path.exists(transcript_path):
                with open(transcript_path, "r", encoding="utf-8") as f:
                    transcript = f.read()
                transcripts_text += f"\n[Video {page_video_id}]: {transcript[:3000]}"
                text_for_nlp += transcripts_text
                translated_text += transcripts_text
                skills_used.append("transcriber")

                metadata["distribution"].append({
                    "type": "FileObject",
                    "name": f"video_transcript_{page_video_id}",
                    "contentUrl": content.url,
                    "encodingFormat": "text/plain",
                })

                log_skill_call(
                    f"transcriber (page video: {page_video_id})",
                    f"video_id={page_video_id}",
                    f"transcript_len={len(transcript)}",
                    duration_ms,
                )
        except Exception as e:
            logger.error("[skill:transcriber] Error for page video %s: %s", page_video_id, e, exc_info=True)

    # Step 5: Gemini structured extraction — extract all key data from the page
    structured_summary = ""
    try:
        model = get_model()
        all_content = content.body_text[:5000]
        if transcripts_text:
            all_content += f"\n\nVideo Transcripts:{transcripts_text[:3000]}"

        extraction_prompt = f"""Extract ALL key information from this web page content into a structured summary.
Include everything: prices/prizes, schedules, rules, requirements, locations, dates, contacts, lists, any factual data.
If video transcripts are included, extract key information from them too.
Be exhaustive. Output a clean text summary organized by topic.

Page content:
{all_content}"""

        start = datetime.now(timezone.utc)
        logger.info("[skill:gemini_extractor] Calling Gemini for structured extraction")
        extraction_response = model.generate_content(extraction_prompt)
        duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        structured_summary = extraction_response.text.strip()
        skills_used.append("gemini_extractor")

        log_gemini_call("gemini_extractor", extraction_prompt, structured_summary, duration_ms)
        logger.info("[skill:gemini_extractor] Done | summary_len=%d duration=%.0fms", len(structured_summary), duration_ms)
    except Exception as e:
        logger.error("[skill:gemini_extractor] Error: %s", e, exc_info=True)

    # Enrich description with structured summary
    if structured_summary:
        metadata["description"] = f"{metadata['description']}\n\n--- Extracted Structured Data ---\n{structured_summary}"

    # Step 6: Croissant Expert skill — serialize into Croissant JSON-LD
    try:
        start = datetime.now(timezone.utc)
        logger.info("[skill:croissant_expert] Running serialize subprocess | apply_nlp=True")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, dir=tempfile.gettempdir()
        ) as tmp:
            json.dump(metadata, tmp, ensure_ascii=False)
            tmp_input = tmp.name

        output_file = os.path.join(tempfile.gettempdir(), "croissant_output.json")
        run_skill(serializer_script, [tmp_input, output_file, "--nlp"])

        with open(output_file, "r", encoding="utf-8") as f:
            croissant_data = json.load(f)

        os.unlink(tmp_input)
        os.unlink(output_file)

        duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        skills_used.append("croissant_expert")

        log_skill_call(
            "croissant_expert (serialize)",
            f"metadata_keys={list(metadata.keys())} nlp_text_len={len(metadata.get('nlp_text', ''))}",
            f"croissant_keys={list(croissant_data.keys())} dist_count={len(croissant_data.get('distribution', []))} rs_count={len(croissant_data.get('recordSet', []))}",
            duration_ms,
        )
        logger.info("[skill:croissant_expert] Done | duration=%.0fms", duration_ms)
    except Exception as e:
        logger.error("[skill:croissant_expert] Error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Croissant serialization failed: {e}")

    total_duration = (datetime.now(timezone.utc) - pipeline_start).total_seconds() * 1000
    logger.info(
        "[generate-croissant] Pipeline complete | skills_used=%s total_duration=%.0fms url=%s",
        skills_used, total_duration, content.url,
    )

    return {
        "croissant": croissant_data,
        "skills_used": skills_used,
        "duration_ms": round(total_duration),
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """Answer questions about a website based on its Croissant JSON-LD."""
    model = get_model()

    logger.info("[chat] Received | message=%s history_len=%d", request.message[:200], len(request.history))

    history_text = ""
    for msg in request.history[-10:]:
        role = msg.get("role", "user")
        history_text += f"\n{role}: {msg.get('content', '')}"

    prompt = f"""You are a helpful assistant that answers questions about a website based on its Croissant JSON-LD metadata.

Here is the Croissant JSON-LD describing the website:
{json.dumps(request.croissant, indent=2)}

Conversation history:{history_text}

User question: {request.message}

Answer the question based on the information available in the Croissant JSON-LD.
If the answer cannot be determined from the metadata, say so clearly.
Be concise and helpful."""

    try:
        start = datetime.now(timezone.utc)
        logger.info("[chat] Calling Gemini | model=%s", MODEL_NAME)
        response = model.generate_content(prompt)
        duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        answer = response.text.strip()

        log_gemini_call("chat", prompt, answer, duration_ms)

        logger.info("[chat] Success | duration=%.0fms response_len=%d", duration_ms, len(answer))
        return {"response": answer}
    except Exception as e:
        logger.error("[chat] Error | %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info("Starting Croissant Converter API | model=%s log_dir=%s", MODEL_NAME, LOG_DIR)
    logger.info("Skills called via subprocess: translator, nlp_expert, transcriber, gemini_extractor, croissant_expert")
    uvicorn.run(app, host="0.0.0.0", port=8000)
