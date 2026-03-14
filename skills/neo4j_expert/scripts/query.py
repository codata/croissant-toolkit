import os
import sys
import json
import google.generativeai as genai
from neo4j import GraphDatabase

class Neo4jQuery:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_cypher(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

def ask_gemini_for_cypher(question):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        return ""
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')

    schema = """
    Nodes:
    - Dataset {name, description, url}
    - Person {name}
    - Organization {name}
    - Place {name}
    - Keyword {name}
    - FileObject {name, contentUrl, encodingFormat}
    
    Relationships:
    - (a:Person/Organization)-[:CREATOR_OF]->(d:Dataset)
    - (d:Dataset)-[:SPATIAL_COVERAGE]->(p:Place)
    - (d:Dataset)-[:HAS_KEYWORD]->(k:Keyword)
    - (d:Dataset)-[:HAS_DISTRIBUTION]->(f:FileObject)
    """

    prompt = f"""
    Act as a Neo4j Cypher expert. Given the schema below, generate a Cypher query to answer the user's question.
    
    SCHEMA:
    {schema}
    
    QUESTION:
    {question}
    
    Return ONLY the Cypher query, no other text or explanation.
    """
    
    response = model.generate_content(prompt)
    query = response.text.strip()
    if "```cypher" in query:
        parts = query.split("```cypher")
        query = parts[1].split("```")[0].strip()
    elif "```" in query:
        parts = query.split("```")
        query = parts[1].split("```")[0].strip()
    return query

def summarize_result(question, results):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key not found."
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""
    Based on the following Neo4j query results, provide a concise answer to the user's question.
    
    QUESTION: {question}
    RESULTS: {json.dumps(results, indent=2)}
    
    Answer concisely:
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query.py <QUESTION>")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")

    if not password:
        print("Error: NEO4J_PASSWORD environment variable not set.")
        sys.exit(1)

    query_tool = Neo4jQuery(uri, user, password)
    
    try:
        print(f"[Neo4j Expert] Translating question to Cypher...")
        cypher = ask_gemini_for_cypher(question)
        if not cypher:
            print("[Neo4j Expert] Failed to generate Cypher query.")
            return

        print(f"[Neo4j Expert] Executing Query: {cypher}")
        results = query_tool.run_cypher(cypher)
        
        if not results:
            print("[Neo4j Expert] No matching records found.")
        else:
            summary = summarize_result(question, results)
            print(f"\n--- Result ---\n{summary}\n")
    except Exception as e:
        print(f"[Neo4j Expert] Query failed: {e}")
    finally:
        query_tool.close()

if __name__ == "__main__":
    main()
