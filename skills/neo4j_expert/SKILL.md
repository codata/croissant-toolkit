---
name: neo4j_expert
description: Store and query Croissant datasets in a Neo4j Graph Database for relational discovery and semantic search.
---

# 🕸️ Neo4j Expert Skill

The Neo4j Expert skill transforms hierarchical Croissant JSON-LD files into a knowledge graph. This allows users to discover relationships between datasets, creators, locations, and keywords using powerful graph queries.

## Features
- **Knowledge Graph Ingestion**: Automatically maps Croissant structures to Dataset, Person, Place, and Keyword nodes.
- **Natural Language Querying**: Ask questions in plain English (e.g., "Who created datasets about Ukraine?") and the and get answers powered by Cypher + Gemini 3.
- **Relational Discovery**: Find datasets that share creators or locations.

## Configuration
Set your Neo4j credentials in the environment:
```bash
export NEO4J_URI="bolt://your-neo4j-instance:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-strong-password"
```

## Usage

### 1. Ingest a Croissant File
```bash
python3 skills/neo4j_expert/scripts/ingest.py "./data/croissant/my_dataset.jsonld"
```

### 2. Query the Knowledge Graph
```bash
python3 skills/neo4j_expert/scripts/query.py "Which datasets mention Kyiv?"
```

## Graph Schema
- **Nodes**: `Dataset`, `Person`, `Organization`, `Place`, `Keyword`, `FileObject`.
- **Relationships**: 
    - `(:Person/Organization)-[:CREATOR_OF]->(:Dataset)`
    - `(:Dataset)-[:SPATIAL_COVERAGE]->(:Place)`
    - `(:Dataset)-[:HAS_KEYWORD]->(:Keyword)`
    - `(:Dataset)-[:HAS_DISTRIBUTION]->(:FileObject)`
