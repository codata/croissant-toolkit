import os
import sys
import json
from neo4j import GraphDatabase

class Neo4jIngestor:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def ingest_croissant(self, json_data):
        with self.driver.session() as session:
            session.execute_write(self._create_graph, json_data)

    @staticmethod
    def _create_graph(tx, data):
        # 1. Create Dataset Node
        name = data.get("name")
        if isinstance(name, dict): name = name.get("@value")
        
        description = data.get("description")
        if isinstance(description, dict): description = description.get("@value")
        
        url = data.get("url")
        
        tx.run("""
            MERGE (d:Dataset {name: $name})
            SET d.description = $description, d.url = $url
            RETURN d
        """, name=name, description=description, url=url)

        # 2. Creators (Persons/Organizations)
        creators = data.get("creator", [])
        if not isinstance(creators, list): creators = [creators]
        
        for c in creators:
            ctype = c.get("@type", "sc:Person").replace("sc:", "")
            cname = c.get("name")
            
            # Handle list of names (multilingual)
            names = []
            if isinstance(cname, list):
                names = [n.get("@value") if isinstance(n, dict) else n for n in cname]
            elif isinstance(cname, dict):
                names = [cname.get("@value")]
            else:
                names = [cname]
                
            for n in names:
                if not n: continue
                tx.run(f"""
                    MERGE (a:{ctype} {{name: $name}})
                    WITH a
                    MATCH (d:Dataset {{name: $dataset_name}})
                    MERGE (a)-[:CREATOR_OF]->(d)
                """, name=n, dataset_name=name)

        # 3. Spatial Coverage (Places)
        spatial = data.get("spatialCoverage", [])
        if not isinstance(spatial, list): spatial = [spatial]
        
        for s in spatial:
            snames = []
            if isinstance(s, list):
                snames = [n.get("@value") if isinstance(n, dict) else n for n in s]
            elif isinstance(s, dict):
                snames = [s.get("@value")]
            else:
                snames = [s]
                
            for sn in snames:
                if not sn: continue
                tx.run("""
                    MERGE (p:Place {name: $name})
                    WITH p
                    MATCH (d:Dataset {name: $dataset_name})
                    MERGE (d)-[:SPATIAL_COVERAGE]->(p)
                """, name=sn, dataset_name=name)

        # 4. Keywords
        keywords = data.get("keywords", [])
        if not isinstance(keywords, list): keywords = [keywords]
        
        for k in keywords:
            kname = k.get("@value") if isinstance(k, dict) else k
            if not kname: continue
            tx.run("""
                MERGE (kw:Keyword {name: $name})
                WITH kw
                MATCH (d:Dataset {name: $dataset_name})
                MERGE (d)-[:HAS_KEYWORD]->(kw)
            """, name=kname, dataset_name=name)

        # 5. Distribution (Files)
        distribution = data.get("distribution", [])
        if not isinstance(distribution, list): distribution = [distribution]
        
        for f in distribution:
            fname = f.get("name")
            content_url = f.get("contentUrl")
            encoding = f.get("encodingFormat")
            
            tx.run("""
                MERGE (fo:FileObject {contentUrl: $content_url})
                SET fo.name = $name, fo.encodingFormat = $encoding
                WITH fo
                MATCH (d:Dataset {name: $dataset_name})
                MERGE (d)-[:HAS_DISTRIBUTION]->(fo)
            """, name=fname, content_url=content_url, encoding=encoding, dataset_name=name)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ingest.py <JSONLD_PATH>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")

    if not password:
        print("Error: NEO4J_PASSWORD environment variable not set.")
        sys.exit(1)

    if not os.path.exists(json_path):
        print(f"Error: File {json_path} not found.")
        sys.exit(1)

    with open(json_path, 'r') as f:
        data = json.load(f)

    ingestor = Neo4jIngestor(uri, user, password)
    try:
        print(f"[Neo4j Expert] Ingesting {json_path}...")
        ingestor.ingest_croissant(data)
        print("[Neo4j Expert] Ingestion successful.")
    except Exception as e:
        print(f"[Neo4j Expert] Ingestion failed: {e}")
    finally:
        ingestor.close()

if __name__ == "__main__":
    main()
