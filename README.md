# 🥐 Croissant Toolkit

[![Event](https://img.shields.io/badge/Event-Gemini_3_Hackathon_Paris-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Hackathon_Prototype-FFC107?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge)](LICENSE)

> **Built with ❤️ at the Gemini 3 Hackathon in Paris** 🇫🇷

**Croissant Toolkit** is an intelligent suite of tools designed to work seamlessly with the [MLCommons Croissant](https://mlcommons.org/croissant) metadata format for machine learning datasets. Powered by the incredible capabilities of **Google Gemini 3**, this toolkit simplifies, validates, and enhances ML dataset preparation, discovery, and exploration.

---

## 🌟 Key Features

* 🤖 **Intelligent Metadata Generation**: Automatically generate and enrich Croissant `.jsonld` metadata from raw dataset files using Gemini 3's advanced multimodal reasoning.
* 🔍 **Semantic Dataset Search**: Search through local and remote datasets using natural language queries.
* ✅ **Format Validation**: Ensure your metadata files are 100% compliant with the MLCommons Croissant specification.
* 💬 **Dataset Q&A**: Ask questions directly about your datasets, getting instant insights from descriptions, structures, and schemas.

## 🛠️ Tech Stack

* **[Gemini 3 API](https://ai.google.dev/)**: For LLM-driven metadata generation, reasoning, and semantic search.
* **[MLCommons Croissant](https://github.com/mlcommons/croissant)**: The standard format for ML dataset metadata.
* **Python 3.10+**: Core backend logic and tooling.

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

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
   export GEMINI_API_KEY="your_api_key_here"
   ```

### Quick Start
*(Placeholder for CLI/Usage instructions once implemented)*
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
