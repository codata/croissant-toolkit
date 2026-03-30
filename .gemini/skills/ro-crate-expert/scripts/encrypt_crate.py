import os
import json
import argparse
import subprocess
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
    from odrl_client import ODRLWallet, resolve_did
except ImportError:
    print("[RO-Crate Expert] ERROR: ODRL Expert not found. Encryption requires ODRL Wallet.")
    sys.exit(1)

def encrypt_crate_zip(zip_path, output_path=None):
    """
    Encrypts an existing RO-Crate ZIP using the ODRL Master Private Key.
    Following TRIZ 'Merging' and 'Inversion' principles.
    """
    wallet = ODRLWallet()
    pk = wallet.get_private_key()
    if not pk:
        print("[RO-Crate Expert] ERROR: No ODRL Private Key found. Run 'python3 .gemini/skills/odrl-expert/scripts/odrl_client.py init' first.")
        return None

    zip_file = Path(zip_path)
    if not zip_file.exists():
        print(f"[RO-Crate Expert] ERROR: ZIP file not found: {zip_path}")
        return None

    out_path = Path(output_path or zip_file.with_name(f"encrypted_{zip_file.name}"))
    
    # We use the private key as a password for the ZIP
    # In a production system, we would derive a specific key, but for this expert skill
    # the private key acts as the 'Secret' known only to the DID owner.
    print(f"[RO-Crate Expert] Encrypting {zip_path} -> {out_path}...")
    
    try:
        # Create a new encrypted ZIP from the original
        # We unzip to a temp dir and re-zip with password to ensure full encryption
        temp_dir = Path("data/tmp_encrypt")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        subprocess.run(["unzip", "-o", str(zip_file), "-d", str(temp_dir)], check=True, capture_output=True)
        
        if out_path.exists():
            out_path.unlink()

        # -r recursive, -P password, -j junk paths (to keep relative to root)
        # We change directory to temp_dir to keep ZIP structure clean
        subprocess.run([
            "zip", "-r", "-P", pk, str(out_path.absolute()), "."
        ], cwd=str(temp_dir), check=True, capture_output=True)
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print(f"[RO-Crate Expert] Success! Encrypted RO-Crate created at: {out_path}")
        print(f"[RO-Crate Expert] PROVENANCE: This file is locked with DID {wallet.get_did()}")
        return out_path
    except Exception as e:
        print(f"[RO-Crate Expert] Encryption failed: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RO-Crate Encryption Expert")
    parser.add_argument("zip_file", help="Path to the RO-Crate ZIP file to encrypt")
    parser.add_argument("--output", help="Optional output path for the encrypted ZIP")
    
    args = parser.parse_args()
    encrypt_crate_zip(args.zip_file, args.output)
