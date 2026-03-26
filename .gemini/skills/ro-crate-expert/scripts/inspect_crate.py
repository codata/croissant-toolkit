import json
import argparse
import zipfile
import sys
from pathlib import Path

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
    from odrl_client import resolve_did
except ImportError:
    print("[RO-Crate Expert] ERROR: ODRL Expert not found. Cannot resolve DID.")
    resolve_did = None

def get_did_from_crate(zip_path):
    """Extracts the DID from the RO-Crate ZIP metadata."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            if 'ro-crate-metadata.json' not in z.namelist():
                print(f"[RO-Crate Expert] Error: 'ro-crate-metadata.json' not found in {zip_path}")
                return None
            
            with z.open('ro-crate-metadata.json') as f:
                metadata = json.load(f)
                
                # Search for the root dataset and its DID
                for entity in metadata.get("@graph", []):
                    if entity.get("@id") == "./" or entity.get("@id") == ".":
                        did = entity.get("prov:wasAttributedTo")
                        if did:
                            return did
                        
                        # Fallback to identifier list
                        identifiers = entity.get("identifier", [])
                        if isinstance(identifiers, str): identifiers = [identifiers]
                        for ident in identifiers:
                            if ident.startswith("did:oyd:"):
                                return ident
    except Exception as e:
        print(f"[RO-Crate Expert] Error reading ZIP: {e}")
    return None

def inspect_crate(zip_path):
    """Inspects the crate and resolves its DID for provenance."""
    print(f"[RO-Crate Expert] Inspecting package: {zip_path}")
    
    did = get_did_from_crate(zip_path)
    if not did:
        print("[RO-Crate Expert] No OOYDID found in crate metadata.")
        return
    
    print(f"[RO-Crate Expert] Found DID: {did}")
    
    if resolve_did:
        print(f"[RO-Crate Expert] Resolving provenance via ODRL Universal Resolver...")
        resolution = resolve_did(did)
        if resolution:
            print("\n" + "="*60)
            print("🚀 PROVENANCE & IDENTITY REPORT (OOYDID)")
            print("="*60)
            print(json.dumps(resolution, indent=2))
            print("="*60)
        else:
            print(f"[RO-Crate Expert] Failed to resolve DID {did}")
    else:
        print("[RO-Crate Expert] ODRL Resolver not available.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RO-Crate Provenance Inspector")
    parser.add_argument("zip_file", help="Path to the RO-Crate ZIP file")
    
    args = parser.parse_args()
    inspect_crate(args.zip_file)
