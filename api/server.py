import os
import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uvicorn


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

app = FastAPI(title="Croissant Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CROISSANT_EXAMPLE = {
    "@context": {
        "@language": "en",
        "@vocab": "https://schema.org/",
        "cr": "http://mlcommons.org/croissant/",
        "sc": "https://schema.org/",
        "dct": "http://purl.org/dc/terms/",
        "conformsTo": "dct:conformsTo",
        "recordSet": "cr:recordSet",
        "field": "cr:field",
        "source": "cr:source",
        "fileObject": "cr:fileObject",
        "fileSet": "cr:fileSet",
        "dataType": {"@id": "cr:dataType", "@type": "@id"},
    },
    "@type": "sc:Dataset",
    "dct:conformsTo": "http://mlcommons.org/croissant/1.0",
}

MODEL_NAME = "gemini-3-pro-preview"


def get_model(api_key: str = None):
    """Configure and return the Gemini model."""
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable not set and not provided in request.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


def log_gemini_call(skill: str, prompt: str, response_text: str, duration_ms: float):
    """Log a complete Gemini API call with prompt, response and timing."""
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
    api_key: str = None


class ChatRequest(BaseModel):
    """Chat request with Croissant context."""
    message: str
    croissant: dict
    history: list[dict] = []
    api_key: str = None


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
    """Generate a Croissant JSON-LD from extracted page content."""
    model = get_model(content.api_key)

    logger.info("[generate-croissant] Received | url=%s title=%s lang=%s keywords=%s",
                content.url, content.title, content.lang, content.keywords)
    logger.debug("[generate-croissant] Full input | headings=%s links_count=%d images_count=%d body_len=%d",
                 content.headings[:10], len(content.links), len(content.images), len(content.body_text))

    example_croissant = {
        "@context": CROISSANT_EXAMPLE["@context"],
        "@type": "sc:Dataset",
        "name": "Eiffel Tower History Dataset",
        "description": "A comprehensive dataset containing the history of the Eiffel Tower.",
        "url": "https://en.wikipedia.org/wiki/Eiffel_Tower",
        "license": "CC-BY-4.0",
        "dct:conformsTo": "http://mlcommons.org/croissant/1.0",
        "keywords": ["Eiffel Tower", "Paris", "History", "Architecture"],
        "creator": {"@type": "sc:Organization", "name": "Wikipedia"},
        "distribution": [
            {"@type": "cr:FileObject", "@id": "main_text", "name": "main_text", "contentUrl": "eiffel_tower_history.txt", "encodingFormat": "text/plain"},
            {"@type": "cr:FileObject", "@id": "entities_file", "name": "entities_file", "contentUrl": "entities.jsonld", "encodingFormat": "application/ld+json"},
        ],
        "recordSet": [
            {
                "@type": "cr:RecordSet", "@id": "history_text", "name": "history_text",
                "description": "Raw historical text content.",
                "field": [
                    {"@type": "cr:Field", "@id": "history_text/content", "name": "content", "dataType": "sc:Text", "source": {"fileObject": {"@id": "#main_text"}, "extract": {"fileProperty": "text"}}},
                ],
            },
            {
                "@type": "cr:RecordSet", "@id": "entities", "name": "entities",
                "description": "Named entities extracted from the text.",
                "field": [
                    {"@type": "cr:Field", "@id": "entities/entity_list", "name": "entity_list", "dataType": "sc:ItemList", "source": {"fileObject": {"@id": "#entities_file"}, "extract": {"fileProperty": "itemListElement"}}},
                ],
            },
        ],
    }

    prompt = f"""You are a Croissant JSON-LD expert. Generate a DETAILED and COMPREHENSIVE Croissant JSON-LD metadata descriptor for the following web page content. The output must conform to the MLCommons Croissant 1.0 specification.

Here is a complete example of a well-structured Croissant JSON-LD:
{json.dumps(example_croissant, indent=2)}

Web page content to convert:
- URL: {content.url}
- Title: {content.title}
- Description: {content.description}
- Language: {content.lang}
- Keywords: {', '.join(content.keywords)}
- Headings: {', '.join(content.headings[:30])}
- Links (sample): {', '.join(content.links[:15])}
- Images: {json.dumps(content.images[:15])}
- Body text: {content.body_text[:5000]}

IMPORTANT INSTRUCTIONS:
1. Create MULTIPLE distribution entries (FileObjects) for different types of content found on the page (text, images, structured data, etc.)
2. Create MULTIPLE recordSets with MULTIPLE fields each. Break down the page content into logical data structures. For example:
   - A recordSet for the main textual content
   - A recordSet for structured data (schedules, lists, tables, etc.)
   - A recordSet for media (images with their alt text, links, etc.)
   - A recordSet for metadata (dates, locations, contacts, etc.)
3. Each field must have a proper @id (format: "recordSetName/fieldName"), name, description, dataType, and source
4. Include: name, description, url, license, keywords, creator, publisher, spatialCoverage, temporalCoverage when inferable
5. Be as exhaustive as possible — extract ALL structured information from the page

Return ONLY the raw JSON-LD object, no markdown fences, no explanation."""

    try:
        start = datetime.now(timezone.utc)
        logger.info("[generate-croissant] Calling Gemini | model=%s", MODEL_NAME)
        response = model.generate_content(prompt)
        duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000

        log_gemini_call("generate-croissant", prompt, response.text, duration_ms)

        raw = clean_json_response(response.text)
        croissant_data = json.loads(raw)
        logger.info("[generate-croissant] Success | url=%s duration=%.0fms keys=%s",
                     content.url, duration_ms, list(croissant_data.keys()))
        return {"croissant": croissant_data}
    except json.JSONDecodeError:
        logger.error("[generate-croissant] JSON parse error | raw_response=%s", response.text[:1000])
        raise HTTPException(status_code=500, detail="Failed to parse Croissant JSON-LD from model response.")
    except Exception as e:
        logger.error("[generate-croissant] Error | %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: ChatRequest):
    """Answer questions about a website based on its Croissant JSON-LD."""
    model = get_model(request.api_key)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
