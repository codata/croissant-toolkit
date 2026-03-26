import os
import sys
import json
import argparse
import requests
import re
from datetime import datetime

def fetch_cdif_inventory(term):
    model = "gpt-oss:latest"
    base_url = "https://cdif-4-xas.dev.codata.org/ollama"
    encoded_term = requests.utils.quote(term)
    url = f"{base_url}?term={encoded_term}&model={model}"
    
    try:
        print(f"[CDIF Maker] Requesting inventory for '{term}'...")
        response = requests.get(url, timeout=60)
        
        if response.status_code != 200:
            print(f"[CDIF Maker] API Error {response.status_code}: {response.text}")
            return None
        
        data = response.json()
        return data
        
    except Exception as e:
        print(f"[CDIF Maker] Connection Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="CDIF Maker: Variable Inventory Generator via Specialized AI Service")
    parser.add_argument("term", help="The measurement term to resolve (e.g., 'soil temperature 10 cm')")
    parser.add_argument("--json", action="store_true", help="Output pure JSON to stdout")
    args = parser.parse_args()
    
    term = args.term
    data = fetch_cdif_inventory(term)
    
    if not data:
        print(f"[CDIF Maker] Error: Could not generate CDIF inventory for '{term}'.")
        return
    
    # Sanitize term for filename
    safe_term = re.sub(r'[^a-zA-Z0-9]', '_', term).lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_dir = "data/cdif"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"inventory_{safe_term}_{timestamp}.json")
    
    with open(report_path, "w") as f:
        json.dump(data, f, indent=4)
    
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("\n--- CDIF VARIABLE INVENTORY ---")
        print(f"Name: {data.get('name')}")
        ollama = data.get('ollama', {})
        print(f"Variable: {ollama.get('variable_name')}")
        print(f"Definition: {ollama.get('definition')}")
        
        units = ollama.get('units', {})
        if isinstance(units, dict):
            print(f"Units: {units.get('symbol')} ({units.get('description')})")
        else:
            print(f"Units: {units}")
        
        print(f"\n[CDIF Maker] Success! Inventory saved to: {os.path.abspath(report_path)}")

if __name__ == "__main__":
    main()
