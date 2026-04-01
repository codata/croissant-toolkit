import os
import sys
import json
import subprocess
from pathlib import Path

# Toolkit structure
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent # Root of the toolkit repo
VAULT_DIR = PROJECT_ROOT / ".gemini" / "vault"
SKILLS_DIR = PROJECT_ROOT / ".gemini" / "skills"
AUTH_FILE = Path.home() / ".odrl" / "authorize.did"

def get_auth_private_key():
    """Retrieve the private key from the authorize.did file (supports JSON or raw string)."""
    if not AUTH_FILE.exists():
        print(f"[ODRL Login] Error: Authorization file not found at {AUTH_FILE}")
        return None
    
    content = AUTH_FILE.read_text().strip()
    if not content:
        print(f"[ODRL Login] Error: {AUTH_FILE} is empty.")
        return None

    # Scenario 1: File is a JSON DID document
    try:
        data = json.loads(content)
        pk = data.get("keys", {}).get("private_key")
        if pk:
            return pk
        # Fallback for other potential structures
        pk = data.get("private_key")
        if pk:
            return pk
    except json.JSONDecodeError:
        # Scenario 2: File is a raw string (the key itself)
        return content
    
    print("[ODRL Login] Error: Could not extract private key from authorize.did")
    return None

def unvault_all_skills(private_key):
    """Attempt to unvault all restricted skills using the provided key."""
    if not VAULT_DIR.exists():
        print(f"[ODRL Login] Vault directory not found: {VAULT_DIR}")
        return

    # Find all zip files in the vault
    vaulted_skills = list(VAULT_DIR.glob("*.zip"))
    if not vaulted_skills:
        print("[ODRL Login] No vaulted skills found in the vault.")
        return

    print(f"[ODRL Login] Authorizing access for {len(vaulted_skills)} skills...")
    
    for zip_path in vaulted_skills:
        skill_name = zip_path.stem
        print(f"  --> Unpackaging: {skill_name}")
        
        try:
            # -P password, -o overwrite, -d destination
            # Note: zip password is the private key multibase string
            subprocess.run([
                "unzip", "-P", private_key, "-o", str(zip_path), "-d", str(PROJECT_ROOT)
            ], check=True, capture_output=True)
            print(f"      ✅ [{skill_name}] Restored successfully.")
        except subprocess.CalledProcessError as e:
            print(f"      ❌ [{skill_name}] Authentication failed. Incorrect key for this skill.")
        except Exception as e:
            print(f"      ❌ [{skill_name}] Error: {e}")

def main():
    print("--- ODRL Secure Login Interface ---")
    pk = get_auth_private_key()
    if pk:
        unvault_all_skills(pk)
    print("--- Login process completed ---\n")

if __name__ == "__main__":
    main()
