import os
import json
import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uvicorn


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("croissant-api")

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


def get_model(api_key: str = None):
    """Configure and return the Gemini model."""
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable not set and not provided in request.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3-pro-preview")


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


@app.post("/generate-croissant")
async def generate_croissant(content: PageContent):
    """Generate a Croissant JSON-LD from extracted page content."""
    model = get_model(content.api_key)

    prompt = f"""You are a Croissant JSON-LD expert. Generate a valid Croissant JSON-LD metadata descriptor
for the following web page content. The output must conform to the MLCommons Croissant 1.0 specification.

Here is an example of the expected JSON-LD structure:
{json.dumps(CROISSANT_EXAMPLE, indent=2)}

Web page content:
- URL: {content.url}
- Title: {content.title}
- Description: {content.description}
- Language: {content.lang}
- Keywords: {', '.join(content.keywords)}
- Headings: {', '.join(content.headings[:20])}
- Links (sample): {', '.join(content.links[:10])}
- Images: {json.dumps(content.images[:10])}
- Body text (excerpt): {content.body_text[:3000]}

Generate a complete and valid Croissant JSON-LD. Include:
- Proper @context with Croissant namespace
- name, description, url, license
- distribution with relevant FileObjects
- recordSet with meaningful fields
- keywords, creator, publisher if inferable

Return ONLY the raw JSON-LD object, no markdown fences, no explanation."""

    try:
        logger.info("[generate-croissant] Calling Gemini | url=%s title=%s", content.url, content.title)
        response = model.generate_content(prompt)
        raw = clean_json_response(response.text)
        croissant_data = json.loads(raw)
        logger.info("[generate-croissant] Success | url=%s keys=%s", content.url, list(croissant_data.keys()))
        return {"croissant": croissant_data}
    except json.JSONDecodeError:
        logger.error("[generate-croissant] JSON parse error | raw_response=%s", response.text[:500])
        raise HTTPException(status_code=500, detail="Failed to parse Croissant JSON-LD from model response.")
    except Exception as e:
        logger.error("[generate-croissant] Error | %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: ChatRequest):
    """Answer questions about a website based on its Croissant JSON-LD."""
    model = get_model(request.api_key)

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
        logger.info("[chat] Calling Gemini | message=%s history_len=%d", request.message[:100], len(request.history))
        response = model.generate_content(prompt)
        answer = response.text.strip()
        logger.info("[chat] Success | response_len=%d", len(answer))
        return {"response": answer}
    except Exception as e:
        logger.error("[chat] Error | %s", e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
