import os
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
    from odrl_client import ODRLWallet
except ImportError:
    print("[RO-Crate Expert] ERROR: ODRL Expert not found.")
    sys.exit(1)

def decrypt_crate_zip(zip_path, output_dir=None):
    """
    Decrypts an encrypted RO-Crate ZIP using the ODRL Master Private Key.
    """
    wallet = ODRLWallet()
    pk = wallet.get_private_key()
    if not pk:
        print("[RO-Crate Expert] ERROR: No ODRL Private Key found.")
        return None

    zip_file = Path(zip_path)
    if not zip_file.exists():
        print(f"[RO-Crate Expert] ERROR: ZIP file not found: {zip_path}")
        return None

    out_dir = Path(output_dir or zip_file.parent / f"decrypted_{zip_file.stem}")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[RO-Crate Expert] Decrypting {zip_path} into {out_dir}...")
    
    try:
        # -P password, -o overwrite, -d destination
        subprocess.run([
            "unzip", "-P", pk, "-o", str(zip_file), "-d", str(out_dir)
        ], check=True, capture_output=True)
        
        print(f"[RO-Crate Expert] Success! RO-Crate decrypted into: {out_dir}")
        return out_dir
    except Exception as e:
        print(f"[RO-Crate Expert] Decryption failed: {e}. Check if you are the DID owner.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RO-Crate Decryption Expert")
    parser.add_argument("zip_file", help="Path to the encrypted RO-Crate ZIP file")
    parser.add_argument("--output", help="Optional output directory for decrypted files")
    
    args = parser.parse_args()
    decrypt_crate_zip(args.zip_file, args.output)
