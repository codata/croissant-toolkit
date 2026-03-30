import os
import sys
import json
import uuid
import argparse
from pathlib import Path

# Try to import rohub, but allow for failures if it's not installed
try:
    import rohub
except ImportError:
    rohub = None
    print("WARNING: 'rohub' library not found. Please install it with 'pip install rohub'.")

def login():
    """Authentication for RO-Hub using environment variables."""
    user = os.getenv("ROHUB_USER")
    password = os.getenv("ROHUB_PASSWORD")
    
    if not (user and password):
        # Fallback to local files as seen in the reference notebook if they exist
        user_file = Path("~/rohub_users/rohub-user").expanduser()
        pwd_file = Path("~/rohub_users/rohub-pwd").expanduser()
        
        if user_file.exists() and pwd_file.exists():
            user = user_file.read_text().strip()
            password = pwd_file.read_text().strip()
        else:
            print("ERROR: ROHUB_USER and ROHUB_PASSWORD environment variables are not set.")
            sys.exit(1)
            
    if rohub:
        try:
            rohub.login(username=user, password=password)
            print(f"Successfully logged into RO-Hub as {user}")
        except Exception as e:
            print(f"Authentication failed: {e}")
            sys.exit(1)
    else:
        print(f"MOCK: Authenticated as {user} (rohub library missing)")

def create_or_load_ro(ro_id=None, title=None, areas=None, description=None):
    """Creates a new RO or loads an existing one."""
    if rohub:
        if ro_id:
            print(f"Loading existing Research Object: {ro_id}")
            return rohub.ros_load(identifier=ro_id)
        else:
            print(f"Creating new Research Object: {title}")
            return rohub.ros_create(
                title=title or "Untitled RO",
                research_areas=areas or ["Research and development"],
                description=description or "Automatic deposit via Croissant Toolkit"
            )
    else:
        print(f"MOCK: Loaded/Created RO (ID: {ro_id or 'new-uuid'})")
        return None

def add_resources_from_crate(ro, crate_dir):
    """Uploads files from the RO-Crate directory as RO-Hub resources."""
    if not ro or not crate_dir:
        return

    crate_path = Path(crate_dir)
    metadata_file = crate_path / "ro-crate-metadata.json"
    if not metadata_file.exists():
        print(f"WARNING: RO-Crate metadata not found in {crate_dir}")
        return

    with open(metadata_file, "r") as f:
        crate_data = json.load(f)

    # Map files from @graph
    for entity in crate_data.get("@graph", []):
        if entity.get("@type") == "File":
            file_id = entity.get("@id")
            # Handle both relative paths and absolute paths
            file_path = crate_path / file_id if not Path(file_id).is_absolute() else Path(file_id)
            
            if file_path.exists() and file_path.is_file():
                print(f"Uploading resource to RO-Hub: {file_id}")
                title = entity.get("name", file_id)
                description = entity.get("description", "")
                
                # Determine resource type (Dataverse Landing Page -> Document, others -> File)
                res_type = "Document" if "landing_page.html" in file_id else "File"
                
                try:
                    ro.add_internal_resource(
                        res_type=res_type,
                        file_path=str(file_path),
                        title=title,
                        description=description
                    )
                except Exception as e:
                    print(f"Error uploading {file_id}: {e}")

def add_semantic_triples(ro, metadata_path=None):
    """
    Translates metadata (JSON/JSON-LD) into RO-Hub semantic annotations.
    """
    if not ro:
        print("Skipping triple addition (no RO or mock mode).")
        return

    # Create a new annotation set in RO-Hub
    new_annot = ro.add_annotations()
    annotation_id = new_annot['identifier']
    print(f"Created new annotation set: {annotation_id}")
    
    # Common Predicates
    RELATED_PRODUCT = "https://schema.org/isRelatedTo"
    HAS_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    PRODUCT = "https://schema.org/Product"
    NAME = "https://schema.org/name"

    # Base identifier for the RO - using full API link for URI validation
    ro_pid = ro.api_link

    # 1. Example: Connect RO to a MVP Product
    mvp_id = f"{ro_pid}/product/1"
    ro.add_triple(the_subject=ro_pid, the_predicate=RELATED_PRODUCT, the_object=mvp_id, 
                  annotation_id=annotation_id, object_class="URIRef")
    
    # 2. Example: Set product type
    ro.add_triple(the_subject=mvp_id, the_predicate=HAS_TYPE, the_object=PRODUCT, 
                  annotation_id=annotation_id, object_class="URIRef")

    # If we have a metadata file, we could parse it and add more granular triples
    if metadata_path and Path(metadata_path).exists():
        with open(metadata_path, 'r') as f:
            data = json.load(f)
            if 'name' in data:
                ro.add_triple(the_subject=mvp_id, the_predicate=NAME, the_object=data['name'], 
                              annotation_id=annotation_id)
            
            if 'keywords' in data:
                for kw in data['keywords']:
                     ro.add_triple(the_subject=mvp_id, the_predicate="https://schema.org/keywords", 
                                   the_object=kw, annotation_id=annotation_id)

    print("Successfully added semantic triples to RO-Hub.")

def main():
    parser = argparse.ArgumentParser(description="Deposit Research Objects to RO-Hub.")
    parser.add_argument("--id", help="Existing RO identifier (UUID). If omitted, a new RO will be created.")
    parser.add_argument("--title", help="Title for the new Research Object.")
    parser.add_argument("--description", help="Description for the Research Object.")
    parser.add_argument("--areas", help="Comma-separated research areas.")
    parser.add_argument("--metadata", help="Path to a JSON/JSON-LD file (e.g. Croissant) to extract annotations from.")
    
    args = parser.parse_args()
    
    # 1. Login
    login()
    
    # 2. Prepare research areas
    research_areas = [a.strip() for a in args.areas.split(",")] if args.areas else None
    
    # Extract title/description from metadata if not provided
    title = args.title
    description = args.description
    if not title and args.metadata:
        try:
            with open(args.metadata, "r") as f:
                crate_data = json.load(f)
                for entity in crate_data.get("@graph", []):
                    if entity.get("@id") == "./" or entity.get("@id") == ".":
                        title = entity.get("name")
                        if not description:
                            description = entity.get("description")
                        break
        except Exception:
            pass

    # 3. Create or load RO
    ro = create_or_load_ro(ro_id=args.id, title=title, areas=research_areas, description=description)
    
    # 4. Upload resources from RO-Crate if available
    if ro and args.metadata:
        crate_dir = Path(args.metadata).parent
        add_resources_from_crate(ro, crate_dir)

    # 5. Add semantic triples if an RO is available
    if ro:
        add_semantic_triples(ro, metadata_path=args.metadata)
    
    print("\n--- RO-Hub Deposit Task Completed ---")

if __name__ == "__main__":
    main()
