# 🥐 Croissant Toolkit

[![Event](https://img.shields.io/badge/Event-Gemini_3_Hackathon_Paris-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Hackathon_Prototype-FFC107?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge)](LICENSE)

> **Built with ❤️ at the Gemini 3 Hackathon in Paris** 🇫🇷

**Croissant Toolkit** is an intelligent suite of tools designed to work seamlessly with the [MLCommons Croissant](https://mlcommons.org/croissant) metadata format for machine learning datasets. Powered by the incredible capabilities of **Google Gemini 3**, this toolkit simplifies, validates, and enhances ML dataset preparation, discovery, and exploration.

---

## 🌟 Key Features

* 🤖 **Intelligent Metadata Generation**: Automatically generate and enrich Croissant `.jsonld` metadata from raw dataset files using Gemini 3's advanced multimodal reasoning.
* 🌐 **Automated Browser Navigation**: Seamlessly launch Google Chrome and perform Google searches directly from the toolkit.
* 🎥 **YouTube Video Discovery**: Search and extract structured video data (titles, descriptions, URLs) for dataset tutorials and deep-dives.
* 📊 **Deep Result Extraction**: Automatically scrape search results, including page titles, snippets, and intelligent keyword extraction (powered by DuckDuckGo HTML for high reliability).
* 🔍 **Semantic Dataset Search**: Search through local and remote datasets using natural language queries.
* ✅ **Format Validation**: Ensure your metadata files are 100% compliant with the MLCommons Croissant specification.
* 💬 **Dataset Q&A**: Ask questions directly about your datasets, getting instant insights from descriptions, structures, and schemas.

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

## 🛠️ Tech Stack

* **[Gemini 3 API](https://ai.google.dev/)**: For LLM-driven metadata generation, reasoning, and semantic search.
* **[MLCommons Croissant](https://github.com/mlcommons/croissant)**: The standard format for ML dataset metadata.
* **Python 3.10+**: Core backend logic and tooling.
* **DuckDuckGo HTML Engine**: For robust, non-JS result scraping.
* **YouTube Data Parser**: Custom scraper for YouTube's initial dataset.

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)
* Google Chrome installed (for `Navigator` and `Youtuber` skills)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/4tikhonov/croissant-toolkit.git
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

4. **Configure your environment:**
   ```bash
   export GEMINI_API_KEY="AIzaSyBi7BVb50H7sj6oq--PzHqx43EGaM1VkKE"
   ```

### Quick Start

**Using the Navigator Skill:**
```bash
# Search for datasets and extract metadata to google_search_results.json
python skills/navigator/scripts/navigate.py "MNIST dataset croissant format"
```

**Using the Youtuber Skill:**
```bash
# Search for YouTube videos about Croissant and extract to youtube_search_results.json
python skills/youtuber/scripts/youtube_search.py "MLCommons Croissant format"
```

**Metadata Generation:**
```bash
# Example: Generate a Croissant metadata file from a raw dataset directory
python main.py generate ./my-local-dataset
```

## 🧠 The Hackathon Vision

Managing ML dataset metadata is traditionally a tedious and manual process. While the Croissant format introduces a powerful and elegant standard, creating compliant metadata files from scratch remains a bottleneck for data scientists. 

For the **Gemini 3 Hackathon in Paris**, we recognized an opportunity to leverage **Gemini 3's** unmatched contextual understanding and long context window to completely automate this pipeline. Our goal is to bring joy back to data engineering, accelerate the open-data ecosystem, and make data more discoverable and interoperable for everyone.

## 👥 Team

* **Vyacheslav Tykhonov**
* *(Add other team members here!)*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
