# 🥐 Croissant Toolkit


[![Event](https://img.shields.io/badge/Event-Gemini_3_Hackathon_Paris-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Hackathon_Prototype-FFC107?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge)](LICENSE)

> **Built with ❤️ at the Gemini 3 Hackathon in Paris** 🇫🇷

**Croissant Toolkit** is an intelligent suite of tools designed to work seamlessly with the [MLCommons Croissant](https://mlcommons.org/croissant) metadata format for machine learning datasets. Powered by the incredible capabilities of **Google Gemini 3**, this toolkit simplifies, validates, and enhances ML dataset preparation, discovery, and exploration.

---

## 🌟 Key Features

* 🧙 **Wizard Data Integrator**: A single command to rule them all. Orchestrates transcription, translation, and NLP to generate fully-enriched Croissant metadata.
* 🤖 **Intelligent Metadata Generation**: Automatically generate and enrich Croissant `.jsonld` metadata from raw dataset files using Gemini 3's advanced multimodal reasoning.
* 🥐 **Croissant Expert Logic**: Deep integration with the MLCommons Croissant specification for 100% compliant JSON-LD serialization.
* 🌐 **Automated Browser Navigation**: Seamlessly launch Google Chrome and perform Google searches directly from the toolkit.
* 🎥 **YouTube Video Discovery**: Search and extract structured video data (titles, descriptions, URLs).
* 📝 **Automated Transcription**: Fetch and store full text transcripts from YouTube videos.
* 🌍 **Intelligent Translation**: Automatically recognize source languages and translate video scripts or dataset documents precisely into English using Gemini 3.
* 🧠 **Multilingual NLP**: Detect people, organizations, dates, AI models, and currency. Preserves original non-English names in metadata.
* 📧 **Communication Officer**: Securely deliver generated datasets and reports to stakeholders via email.
* 💎 **Obsidian Expert**: Automatically transform Croissant metadata into rich Markdown notes.
* 🕸️ **Neo4j Expert**: Ingest Croissant datasets into a Neo4j Graph Database for relational discovery and semantic search.
* 🚶 **Walker Expert**: Extract and explore internal links from a page when deep research is required.
* 📸 **Photograph**: Automatically capture high-quality snapshots of web pages and record screen activity during process execution.
* 🔍 **Semantic Dataset Search**: Search through local and remote datasets using natural language queries.
* ✅ **Format Validation**: Ensure your metadata files are 100% compliant with the MLCommons Croissant specification.
* 💬 **Dataset Q&A**: Ask questions directly about your datasets, getting instant insights from descriptions, structures, and schemas.
* 🕵️ **Fact Checker**: High-fidelity AI analysis of sensitive claims, legal conflicts, and innovation impacts with visual passage highlighting and video evidence.
* 📊 **Claims Detection**: Automated extraction of verifiable factual statements with MD5-based unique IDs and Schema.org semantic mapping.

## 🧩 Skills & Tools

### 🧭 Navigator Skill
The `Navigator` skill acts as an intelligent bridge between the toolkit and the web. It allows the agent to:
1.  **Search**: Execute high-intent searches on Google.
2.  **Browse**: Open the specific search results in Google Chrome for the user.
3.  **Analyze**: Extract and structure metadata (titles, snippets, keywords) from the web to feed into the Croissant reasoning engine.

### 📺 Youtuber Skill
The `Youtuber` skill expands the toolkit's reach to video content. It allows the agent to:
1.  **Discovery**: Find relevant video tutorials, explanations, and demonstrations on YouTube.
2.  **Structured Extraction**: Parse YouTube's internal data to get clean titles, URLs, and video descriptions.
3.  **Multi-Modal Context**: Use video descriptions to provide richer context for dataset understanding.

### 📝 Transcriber Skill
The `Transcriber` skill converts video content into a machine-readable format. It:
1.  **Downloads**: Fetches accurate closed-caption data from YouTube.
2.  **Stores**: Organizes transcripts in `./data/transcripts/` for downstream processing.
3.  **Synthesizes**: Enables Gemini 3 to "understand" video content by reasoning over the full spoken text.

### 🧙 Wizard (Data Integrator) Skill
The `Wizard` is the master orchestrator of the toolkit. It provides a single entry point for complex data tasks:
1.  **Automation**: Chaining transcription, translation, and NLP enrichment.
2.  **Multilingual Support**: Captures entities in both English and their original language (e.g., Ukrainian, Russian, French) using JSON-LD tags.
3.  **Synthesis**: Combines factual measurements and AI-driven fact-checking into a single investigative report.
4.  **End-to-End**: Goes from a raw link to a finalized Croissant metadata file with automated verification and secure vaulting.

### 🌍 Translator Skill
The `Translator` skill ensures the toolkit is truly global. It:
1.  **Detection**: Automatically identifies the source language of any text or video script.
2.  **Precision**: Translates content precisely into English using Gemini 1.5 Flash.
3.  **Persistence**: Saves translated versions alongside originals for easy integration.

### 🧠 NLP Expert Skill
The `NLP Expert` skill extracts structured knowledge. It:
1.  **Recognition**: Identifies persons, organizations, locations, and dates.
2.  **Semantic Mapping**: Converts detected entities into Schema.org JSON-LD.
3.  **Contextual Enrichment**: Provides deeper understanding of dataset provenance and coverage.

### 🥐 Croissant Expert Skill
The `Croissant Expert` skill is the brains behind the metadata formatting. It:
1.  **Spec Compliance**: Reads and interprets the official MLCommons Croissant specification.
2.  **Serialization**: Transforms dataset high-level metadata into standardized JSON-LD.
3.  **Organization**: Automatically stores output files in `./data/croissant/`.
4.  **Extensible Design**: Support for `FileObject`, `FileSet`, and complex `RecordSet` mappings.

### 📧 Communication Officer Skill
The `Communication Officer` skill handles the delivery of results via email. It:
1.  **Secure Delivery**: Sends emails using SMTP with TLS.
2.  **Smart Attachments**: Automatically attaches generated Croissant JSON-LD files.

### 🤖 Telegram Expert Skill
The `Telegram Expert` skill provides instant messaging notifications. It:
1.  **Instant Alerts**: Sends status updates and summaries to a Telegram chat or channel.
2.  **File Delivery**: Uploads generated `.jsonld` files directly to Telegram.
3.  **Bot API**: Uses the standard Telegram Bot API for reliable communication.

### 🕸️ Neo4j Expert Skill
The `Neo4j Expert` translates Croissant files into a Knowledge Graph. It:
1.  **Ingestion**: Standardizes JSON-LD into Graph nodes (Dataset, Creator, Location).
2.  **Semantic Querying**: Allows natural language queries that are translated into Cypher via Gemini 3.

### 🚶 Walker Skill
The `Walker` skill performs deep web exploration. It:
1.  **Deep Crawl**: Extracts all internal links from a specified URL.
2.  **Autonomous Navigation**: Can be triggered to visit all discovered pages if initial information is insufficient.

### 🔒 ODRL Expert Skill
The `ODRL Expert` provides a decentralized security layer. It:
1.  **Identity**: Manages your master identity via DIDs (Decentralized Identifiers).
2.  **Rights Management**: Enforces ODRL policies to restrict or permit skill usage via the [CODATA OAC Profile](https://odrl.dev.codata.org/docs).
3.  **Skill Vault**: Encrypts skill source code using your private key to ensure physical security.
4.  **Branding**: Automatically applies CODATA/Croissant branding and provenance metadata to generated artifacts.

### 🕵️ Fact Checker Skill
The `Fact Checker` performing deep investigative analysis on a document or URL. It:
1.  **Sensitive Discovery**: Detects high-stakes claims related to terminations, legal conflicts, and corporate sensitive data.
2.  **Innovation Summary**: Synthesizes the cognitive impact and innovative potential of the analyzed content.
3.  **Visual Evidence**: Generates highlight-annotated video recordings of its reasoning process.

### 📊 Claims Detection (Data Expert) Skill
The `Claims Detection` skill transforms documents into structured factual datasets. It:
1.  **Granular Extraction**: Isolates core factual claims and their original context sentences.
2.  **Verifiable IDs**: Assigns unique MD5 hashes to every claim for reproducible identification.
3.  **Standardized Export**: Generates `data/claims.json` with full DID attribution and truth probability scoring.

## 🛠️ Tech Stack

* **[Gemini 3 API](https://ai.google.dev/)**: For LLM-driven metadata generation, reasoning, and semantic search.
* **[MLCommons Croissant](https://github.com/mlcommons/croissant)**: The standard format for ML dataset metadata.
* **Python 3.10+**: Core backend logic and tooling.
* **DuckDuckGo HTML Engine**: For robust, non-JS result scraping.
* **YouTube Data Parser**: Custom scraper for YouTube's initial metadata.
* **YouTube Transcript API**: For secure retrieval of video caption text.
* **AI Translation & NLP**: High-precision multi-lingual support and entity extraction via Gemini 3.

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)
* Google Chrome installed (for `Navigator` and `Youtuber` skills)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/codata/croissant-toolkit.git
   cd croissant-toolkit
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment**:
   ```bash
   # Required for AI Reasoning
   export GEMINI_API_KEY="your-api-key-here"

   # Optional: Config for Communication Officer (Email)
   export SMTP_USER="your-email@gmail.com"
   export SMTP_PASS="your-google-app-password"

   # Optional: Config for Telegram Expert
   export TELEGRAM_BOT_TOKEN="your-bot-token"
   export TELEGRAM_CHAT_ID="your-chat-or-channel-id"
   ```

### Quick Start

**Using the Navigator Skill:**
```bash
# Search for datasets and extract metadata to google_search_results.json
# Search and extract structured web data
python .gemini/skills/navigator/scripts/navigate.py "MLCommons Croissant"
```

**Using the Youtuber Skill:**
```bash
# Search and extract structured video data
python .gemini/skills/youtuber/scripts/search_youtube.py "NLP data engineering"
```

**Using the Transcriber Skill:**
```bash
# Fetch transcripts for a specific video
python .gemini/skills/transcriber/scripts/transcribe.py 6cWcZ2G53gE
```

**Using the Translator Skill:**
```bash
# Translate a specific transcript file
python .gemini/skills/translator/scripts/translate.py data/transcripts/VIDEO_ID.txt
```

**Using the NLP Expert Skill:**
```bash
# Extract named entities into JSON-LD from text or files
python .gemini/skills/nlp_expert/scripts/extract_entities.py "Sergei Bodrov was born in Moscow."
```

**Using the Croissant Expert Skill:**
```bash
# Serialize dataset metadata with Intelligent NLP enrichment
# (Detects creators, locations, and dates automatically)
python .gemini/skills/croissant_expert/scripts/serialize.py metadata.json --nlp
```

**Using the Wizard Skill (End-to-End):**
```bash
# Process a video, enrich metadata, email, and save to Obsidian
export SMTP_USER="your@email.com"
export SMTP_PASS="your-password"
export OBSIDIAN_VAULT_PATH="/path/to/my/vault"

python3 .gemini/skills/wizard/scripts/wizard.py "https://youtube.com/link" "My Dataset" "recipient@example.com"
```

**Using the Communication Officer Skill:**
```bash
# Send a file manually
python3 .gemini/skills/communication_officer/scripts/send_email.py "user@example.com" "Subject" "Body" "path/to/file.jsonld"
```

**Using the Telegram Expert Skill:**
```bash
# Send a notification manually
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py "Notification message"

# Send with an attachment
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py "Check this file" "./data/croissant/dataset.jsonld"
```

**Using the Obsidian Expert Skill:**
```bash
# Convert a Croissant file to a beautiful Obsidian note
python3 .gemini/skills/obsidian_expert/scripts/to_obsidian.py "./data/croissant/dataset.jsonld"
```

**Using the Neo4j Expert Skill:**
```bash
# Ingest into Neo4j
export NEO4J_PASSWORD="your-password"
python3 skills/neo4j_expert/scripts/ingest.py "./data/croissant/dataset.jsonld"

# Query via Natural Language
python3 skills/neo4j_expert/scripts/query.py "Which datasets were created in France?"
```

**Using the Walker Skill:**
```bash
# Extract and visit links for deep research
python3 skills/walker/scripts/walk.py "https://example.com" --limit 5 --navigate
```

**Using the Photograph Skill:**
```bash
# Take a standard screenshot
python3 .gemini/skills/photograph/scripts/take_screenshot.py "https://www.google.com"

# Take a full-page screenshot
python3 .gemini/skills/photograph/scripts/take_screenshot.py "https://mlcommons.org/croissant" --full_page

# Record the screen while running a process (e.g. searching YouTube)
python3 .gemini/skills/photograph/scripts/record_screen.py --command "python3 .gemini/skills/youtuber/scripts/youtube_search.py MLCommons"

# Take a YouTube snapshot (automatically waits for ads)
python3 .gemini/skills/youtuber/scripts/video_snapshot.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Metadata Generation:**
```bash
# Example: Generate a Croissant metadata file from a raw dataset directory
python main.py generate ./my-local-dataset
```

### 🔒 ODRL & Skill Vault
The toolkit uses the [CODATA ODRL Infrastructure](https://odrl.dev.codata.org/) for decentralized access control.

**Initialize your security wallet:**
```bash
python3 .gemini/skills/odrl_expert/scripts/odrl_client.py init
```

**Encrypt/Vault a skill:**
```bash
python3 .gemini/skills/odrl_expert/scripts/odrl_client.py vault-skill "fact-checker"
```

**Decrypt/Restore a skill:**
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py unvault-skill "fact-checker"
```

## 🧪 Testing
 
This toolkit includes a comprehensive suite of automated tests to ensure all skills are functioning correctly.
 
### 1. Running All Tests
You can execute the entire test suite using the `test-all` skill runner:
```bash
python3 .gemini/skills/test-all/scripts/test_all.py
```
This script will discover and execute all `test_*.py` files within the `.gemini/skills/` directory and provide a summary of the results.
 
### 2. Using `gemini-cli`
The **Gemini CLI** is the primary way to interact with the toolkit's intelligent agents. It allows you to run skills using natural language or direct commands.
 
**Install Gemini CLI:**
```bash
npm install -g @google/gemini-cli
```
 
**Execute tests via CLI:**
You can ask the agent to run tests for you:
```bash
gemini "Use the test-all skill to verify the system integrity"
```
Or target a specific skill:
```bash
gemini "Test the Navigator skill and ensure it returns results"
```
 
## 🌐 Chrome Extension — Croissant Converter

A Chrome extension that converts any web page into Croissant JSON-LD metadata, with a contextual chat powered by Gemini 3.

### Setup

**1. Start the backend API:**

```bash
cd api
pip install -r requirements.txt
export GEMINI_API_KEY="your-api-key-here"
python server.py
```

The API runs on `http://localhost:8000`.

**2. Load the extension in Chrome:**

1. Open `chrome://extensions/`
2. Enable **Developer mode** (toggle top-right)
3. Click **Load unpacked**
4. Select the `extension/` folder

**3. Use it:**

1. Navigate to any website
2. Click the croissant icon in the toolbar — the side panel opens
3. Click **Generate Croissant** — extracts the page content and generates a Croissant JSON-LD
4. Copy or download the JSON-LD
5. Use the **Chat** section to ask questions about the page based on the generated metadata

## 🧠 The Hackathon Vision

Managing ML dataset metadata is traditionally a tedious and manual process. While the Croissant format introduces a powerful and elegant standard, creating compliant metadata files from scratch remains a bottleneck for data scientists. 

For the **Gemini 3 Hackathon in Paris**, we recognized an opportunity to leverage **Gemini 3's** unmatched contextual understanding and long context window to completely automate this pipeline. Our goal is to bring joy back to data engineering, accelerate the open-data ecosystem, and make data more discoverable and interoperable for everyone.

## 📖 Documentation & Learning
 
* [**Project Structure & Individual Skills**](./README.md#project-structure): Detailed breakdown of every skill in the toolkit.
* [**📖 Skill Cookbook**](./cookbook/skill_combinations.md): Learn how to combine multiple skills into powerful, autonomous workflows.
* [**Testing Guide**](./README.md#-testing): How to run the automated integrity suite.

## 🏢 Project Structure

For detailed documentation on each skill, please refer to the [`docs/`](./docs/) directory:
- [Communication Officer](./docs/communication_officer.md)
- [Telegram Expert](./docs/telegram_expert.md)
- [Croissant Expert](./docs/croissant_expert.md)
- [NLP Expert](./docs/nlp_expert.md)
- [Navigator](./docs/navigator.md)
- [YouTuber](./docs/youtuber.md)
- [Photograph](./docs/photograph.md)
- [Fact Checker](./docs/fact_checker.md)
- [Claims Detection (Data Expert)](./docs/data_expert.md)

## 👥 Team

* **[Slava Tykhonov](https://github.com/4tikhonov)**
* **[Aymen El ouagouti](https://github.com/aymen-eloagouti)**
* **[Sacha Henneuveux](https://github.com/sachenneuveux)**
* **[Elio Bteich](https://github.com/elio-bteich)**

## 📄 License

This project is licensed under the MIT License.
 
