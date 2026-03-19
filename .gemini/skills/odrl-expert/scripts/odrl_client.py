import requests
import json
import argparse
import sys
import os
import subprocess
import shutil
from pathlib import Path

BASE_URL = "https://odrl.dev.codata.org/api"
WALLET_DIR = Path.home() / ".odrl"
WALLET_FILE = WALLET_DIR / "did.json"
VAULT_DIR = Path.cwd() / ".gemini" / "vault"
SKILLS_DIR = Path.cwd() / ".gemini" / "skills"

class ODRLWallet:
    def __init__(self):
        WALLET_DIR.mkdir(parents=True, exist_ok=True)
        VAULT_DIR.mkdir(parents=True, exist_ok=True)
        self.did_data = self._load_wallet()

    def _load_wallet(self):
        if WALLET_FILE.exists():
            with open(WALLET_FILE, "r") as f:
                return json.load(f)
        return None

    def save_did(self, data):
        with open(WALLET_FILE, "w") as f:
            json.dump(data, f, indent=2)
        self.did_data = data
        print(f"[ODRL Wallet] Saved DID and Keys to {WALLET_FILE}")

    def get_did(self):
        return self.did_data.get("did") if self.did_data else None

    def get_private_key(self):
        if not self.did_data: return None
        return self.did_data.get("keys", {}).get("private_key")

def resolve_did(did):
    url = f"{BASE_URL}/did/resolve/{did}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ODRL Expert] Error resolving DID: {e}")
        return None

def create_did(name="Default User", role="Skill Owner"):
    url = f"{BASE_URL}/did/create"
    payload = {
        "payload": {
            "name": name,
            "role": role,
            "created_at": str(os.urandom(4).hex()), # unique seed
            "agent": "Antigravity AI"
        }
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ODRL Expert] Error creating DID: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"  Response: {e.response.text}")
        return None

def create_policy(assigner, assignee, asset, permission="use"):
    url = f"{BASE_URL}/oac/policy"
    policy_json = {
        "@context": ["http://www.w3.org/ns/odrl.jsonld"],
        "type": "odrl:Agreement",
        "odrl:uid": f"did:oyd:policy-{os.urandom(8).hex()}",
        "odrl:profile": "oac:",
        "odrl:permission": [{
            "assigner": assigner,
            "assignee": assignee,
            "target": asset,
            "action": permission
        }]
    }
    try:
        response = requests.post(url, json=policy_json)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ODRL Expert] Error creating policy: {e}")
        return None

def vault_skill(skill_name):
    """
    Encrypts the skill into a ZIP archive using the Wallet's private key.
    """
    wallet = ODRLWallet()
    pk = wallet.get_private_key()
    if not pk:
        print("[ODRL Vault] No private key found in wallet to protect skill.")
        return

    src_dir = SKILLS_DIR / skill_name
    zip_path = VAULT_DIR / f"{skill_name}.zip"

    if not src_dir.exists():
        print(f"[ODRL Vault] Target skill directory does not exist: {src_dir}")
        return

    print(f"[ODRL Vault] Encrypting skill {skill_name} into {zip_path}...")
    
    # -r recursive, -P password, -e encrypts, -j junk paths (keep relative structure from target)
    try:
        subprocess.run([
            "zip", "-r", "-P", pk, str(zip_path), f".gemini/skills/{skill_name}"
        ], check=True, capture_output=True)
        print(f"[ODRL Vault] Skill {skill_name} successfully encrypted and moved to the Vault.")
        
        # Optionally remove the plain source
        shutil.rmtree(src_dir)
        print(f"[ODRL Vault] Source directory removed. Skill now exists ONLY in the archive.")
    except Exception as e:
        print(f"[ODRL Vault] Error zipping skill: {e}")

def unvault_skill(skill_name):
    """
    Decrypts the skill back to the skills directory using the Wallet's private key.
    """
    wallet = ODRLWallet()
    pk = wallet.get_private_key()
    if not pk:
        print("[ODRL Vault] No private key found to decrypt vault.")
        return

    zip_path = VAULT_DIR / f"{skill_name}.zip"

    if not zip_path.exists():
        print(f"[ODRL Vault] Skill does not exist in the Vault: {zip_path}")
        return

    print(f"[ODRL Vault] Decrypting skill {skill_name} from {zip_path}...")
    
    try:
        # -P password, -o overwrite, -d destination
        subprocess.run([
            "unzip", "-P", pk, "-o", str(zip_path), "-d", str(Path.cwd())
        ], check=True, capture_output=True)
        print(f"[ODRL Vault] Skill {skill_name} extracted successfully back to the workspace.")
        
        # Keep the zip as an archive or remove?
        # User said 'read it back', I'll leave it in vault for now.
    except Exception as e:
        print(f"[ODRL Vault] Decryption failed: {e}. Check if private key provided is correct.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ODRL Expert Client (with Skills Vault Support)")
    # Global flag for current monthly identity
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialize local wallet")
    subparsers.add_parser("resolve-did").add_argument("did")
    
    # Protect
    protect_parser = subparsers.add_parser("protect")
    protect_parser.add_argument("skill_name")
    
    # VAULT
    vault_parser = subparsers.add_parser("vault-skill")
    vault_parser.add_argument("skill_name")

    unvault_parser = subparsers.add_parser("unvault-skill")
    unvault_parser.add_argument("skill_name")

    args = parser.parse_args()
    
    if args.command == "init":
        ODRLWallet()
    elif args.command == "resolve-did":
        print(json.dumps(resolve_did(args.did), indent=2))
    elif args.command == "vault-skill":
        vault_skill(args.skill_name)
    elif args.command == "unvault-skill":
        unvault_skill(args.skill_name)
    else:
        parser.print_help()
