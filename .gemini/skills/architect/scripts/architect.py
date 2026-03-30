import os
import sys
import argparse
import google.generativeai as genai

# Configuration
MODEL_NAME = "gemini-1.5-flash" # Use a fast model for diagram generation

def get_model(api_key=None):
    """Configure and return the Gemini model."""
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

def generate_architecture(description, api_key=None):
    """Generate architecture diagram using Gemini."""
    model = get_model(api_key)
    
    prompt = f"""You are an Expert Principal Systems Architect. Your primary job is to design robust software architectures and visually represent them using Mermaid.js.

Analyze: Analyze the provided description to determine the necessary components (frontend, API gateways, microservices, databases, caching, message brokers).
Design: Choose the most scalable, secure, and appropriate architectural pattern.
Visualize: Generate a clear, well-structured mermaid code block (no markdown fences around the code block itself, just the raw code).
Explain: Always accompany your diagram with a brief "Architecture Decision Record" (ADR) explaining why you chose specific components and how data flows through the system.

Diagram Guidelines:
- Use clean formatting and clear node names.
- Group related components using subgraph.
- Use directional arrows (-->) with labels.
- Keep it legible.

User Request: {description}
"""
    
    try:
        response = model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Error generating architecture: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="The Visual Systems Architect: Generate diagrams from descriptions.")
    parser.add_argument("description", help="Description of the system or data flow.")
    parser.add_argument("--api-key", help="Gemini API key.")
    
    args = parser.parse_args()
    
    if not args.description:
        print("Error: Please provide a description of the system.")
        sys.exit(1)
        
    generate_architecture(args.description, args.api_key)

if __name__ == "__main__":
    main()
