import os
import sys
import json
import requests
import argparse
from pathlib import Path

# Add parent directory for ODRL imports if needed
lib_path = Path(__file__).parent.parent.parent / "odrl-expert" / "scripts"
sys.path.insert(0, str(lib_path))

try:
    from odrl_client import resolve_did, ODRLWallet
except ImportError:
    pass

class GithubOrchestrator:
    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def list_repo_skills(self, repo_url):
        """Extract owner and repo from URL and list .gemini/skills/ content."""
        # Simple parser for github.com/owner/repo
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
           print(f"Error: Invalid GitHub URL: {repo_url}")
           return None
        
        owner, repo = parts[-2], parts[-1]
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/.gemini/skills"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return [item['name'] for item in response.json() if item['type'] == 'dir']
        except Exception as e:
            print(f"[Github Orchestrator] Error listing skills from {repo_url}: {e}")
            return None

    def list_repo_vault(self, repo_url):
        """List encrypted skills in the vault of the remote repository."""
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/.gemini/vault"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return [item['name'].replace('.zip', '') for item in response.json() if item['name'].endswith('.zip')]
        except Exception as e:
            # Vault might not exist or be empty
            return []

    def verify_sovereignty(self, repo_url):
        """
        Check if the remote repository has a sovereign DID identity.
        Extracts the Master Identity from AGENTS.md.
        """
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/AGENTS.md"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            content_data = response.json()
            if 'content' in content_data:
                import base64
                content = base64.b64decode(content_data['content']).decode('utf-8')
                for line in content.split('\n'):
                    if "Master Identity" in line and "did:oyd:" in line:
                         # Extract did:oyd...
                         did = line.split('`')[-2] if '`' in line else line.split(' ')[-1]
                         return did
            return True # Found file but no DID extracted
        except:
            return False

def main():
    parser = argparse.ArgumentParser(description="Github Orchestrator: Secure skill & workflow management.")
    parser.add_argument("repo", help="The GitHub repository URL (e.g. https://github.com/codata/croissant-toolkit).")
    parser.add_argument("--sync", action="store_true", help="Sync remote skills to local environment (Placeholder).")
    parser.add_argument("--status", action="store_true", help="Show the security and skill status of the remote repo.")
    
    args = parser.parse_args()
    
    orchestrator = GithubOrchestrator()
    
    if args.status:
        print(f"\n--- GitHub Repository Security Audit: {args.repo} ---")
        did = orchestrator.verify_sovereignty(args.repo)
        
        if did and isinstance(did, str):
            print(f"Sovereign Identity (DID): ✅ {did}")
        else:
            print(f"Sovereign Identity (AGENTS.md): {'✅ FOUND (Incomplete)' if did else '❌ MISSING'}")
        
        skills = orchestrator.list_repo_skills(args.repo)
        if skills:
            print(f"Open Skills ({len(skills)}): {', '.join(skills)}")
        
        vaulted = orchestrator.list_repo_vault(args.repo)
        if vaulted:
            print(f"Restricted Skills (Vaulted) ({len(vaulted)}): {', '.join(vaulted)}")
        print("------------------------------------------------------\n")
        
        if not did:
            print("[Warning] This repository does not follow the ODRL Sovereignty protocol (missing AGENTS.md or DID).")
            print("Usage is permitted, but automated provenance tracking may be limited.")

if __name__ == "__main__":
    main()
