import os
import json
import requests
import argparse
from pathlib import Path
import sys

# Flexible path resolution for ODRL Expert
POSSIBLE_ODRL_PATHS = [
    Path.cwd() / ".gemini" / "skills" / "odrl-expert" / "scripts",
    Path(__file__).parent.parent.parent / "odrl-expert" / "scripts",
    Path.cwd() / "scripts" # If installed as standalone
]

for p in POSSIBLE_ODRL_PATHS:
    if p.exists():
        sys.path.append(str(p))
        break

try:
    from odrl_client import create_did, save_user_package
except ImportError:
    print("[RO-Crate Expert] WARNING: ODRL Expert not found. DID generation will be skipped.")
    create_did = None
    save_user_package = None

# Using the requested library: https://github.com/ResearchObject/ro-crate-py
try:
    from rocrate.rocrate import ROCrate
    from rocrate.model.person import Person
except ImportError:
    print("[RO-Crate Expert] ERROR: 'rocrate' library is not installed.")
    print("[RO-Crate Expert] TIP: Run 'pip install rocrate' to use this skill.")
    ROCrate = None

def get_dataverse_metadata(doi, exporter="schema.org"):
    """Fetches metadata from Dataverse."""
    if "persistentId=" in doi:
        doi = doi.split("persistentId=")[1]
    
    url = "https://demo.dataverse.org/api/datasets/export"
    params = {"exporter": exporter, "persistentId": doi}
    
    print(f"[RO-Crate Expert] Retrieving {exporter} metadata for {doi}...")
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[RO-Crate Expert] Dataverse API Error: {e}")
        return None

def download_file(url, dest_path):
    """Downloads a file from a URL."""
    try:
        print(f"[RO-Crate Expert] Downloading {url} -> {dest_path}...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"[RO-Crate Expert] Download Error: {e}")
        return False

def build_crate(metadata, output_path, ore_metadata=None, make_zip=False):
    """Constructs the RO-Crate and integrates ODRL DID."""
    if not ROCrate:
        return None
        
    crate = ROCrate()
    name = metadata.get("name", "Research Dataset")
    crate.name = name
    crate.description = metadata.get("description", "")
    
    # 1. Create Identity via ODRL
    did = None
    did_package = None
    if create_did:
        print(f"[RO-Crate Expert] Initializing Decentralized ID for '{name}'...")
        did_data = create_did(name=name, role="ResearchObject")
        if did_data:
            did = did_data.get("did")
            did_package = did_data
            print(f"[RO-Crate Expert] DID Created: {did}")
            
            # Attribute the crate to the DID
            crate.root_dataset.append_to("identifier", did)
            did_props = {
                "prov:wasAttributedTo": did,
                "dct:publisher": did,
                "url": f"https://odrl.dev.codata.org/api/did/resolve/{did}"
            }
            for k, v in did_props.items():
                crate.root_dataset[k] = v

    # 2. Map Creators
    creators = metadata.get("creator", [])
    if isinstance(creators, dict): creators = [creators]
    for c in creators:
        c_name = c.get("name")
        if c_name:
            crate.add(Person(crate, c_name, properties={"affiliation": c.get("affiliation", "")}))

    # 3. Handle OAI_ORE and File Downloads
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if ore_metadata:
        aggregates = ore_metadata.get("ore:describes", {}).get("ore:aggregates", [])
        if aggregates:
            data_dir = out_dir / "data"
            data_dir.mkdir(exist_ok=True)
            for file_info in aggregates:
                file_name = file_info.get("schema:name")
                download_url = file_info.get("schema:sameAs")
                if file_name and download_url:
                    dest = data_dir / file_name
                    if download_file(download_url, dest):
                        # Add file to RO-Crate
                        crate.add_file(dest, dest_path=f"data/{file_name}", properties={
                            "name": file_name,
                            "description": file_info.get("schema:description", ""),
                            "contentSize": file_info.get("dvcore:filesize"),
                            "encodingFormat": file_info.get("schema:fileFormat")
                        })

    # 4. Write Crate
    crate.write(out_dir)
    
    # 5. Save the "Digitally Signed File" (DID Package)
    if did_package and save_user_package:
        sig_file = out_dir / "did_signature.json"
        with open(sig_file, "w") as f:
            json.dump(did_package, f, indent=2)
        print(f"[RO-Crate Expert] Digitally signed DID Package saved to: {sig_file}")
        # Register the signature file in the crate
        crate.add_file(sig_file, dest_path="did_signature.json", properties={
            "name": "DID Signature",
            "description": "Digitally signed DID Package (OOYDID)"
        })

    # 6. Package as ZIP if requested
    if make_zip:
        # Sanitize DID for filename (replace colons with underscores)
        safe_did = did.replace(":", "_") if did else "unknown"
        zip_path = Path("data") / f"rocrate_{safe_did}.zip"
        print(f"[RO-Crate Expert] Packaging as ZIP: {zip_path}...")
        crate.write_zip(zip_path)
        print(f"[RO-Crate Expert] ZIP package created at: {zip_path}")

    print(f"[RO-Crate Expert] Package successfully created at: {out_dir}")
    return did

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RO-Crate Expert Integrator")
    parser.add_argument("doi", help="DOI or Dataverse URL")
    parser.add_argument("--output", default="./data/rocrate_output", help="Output directory")
    parser.add_argument("--zip", action="store_true", help="Create a ZIP package of the RO-Crate")
    
    args = parser.parse_args()
    
    # 1. Get Schema.org metadata
    data = get_dataverse_metadata(args.doi, exporter="schema.org")
    
    # 2. Get OAI_ORE metadata for file discovery
    ore_data = get_dataverse_metadata(args.doi, exporter="OAI_ORE")
    
    if data:
        build_crate(data, args.output, ore_metadata=ore_data, make_zip=args.zip)
