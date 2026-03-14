import os
import sys
import json
from datetime import datetime

def format_as_markdown(json_data):
    """Converts Croissant JSON-LD to Obsidian Markdown."""
    name = json_data.get("name", "Untitled Dataset")
    if isinstance(name, dict):
        name = name.get("@value", name)
    
    description = json_data.get("description", "")
    if isinstance(description, dict):
        description = description.get("@value", description)
    
    url = json_data.get("url", "")
    creators = json_data.get("creator", [])
    keywords = json_data.get("keywords", [])
    
    # Extract names from creators
    creator_names = []
    for c in creators:
        cname = c.get("name", "")
        if isinstance(cname, list):
            cname = ", ".join([n.get("@value") if isinstance(n, dict) else str(n) for n in cname])
        elif isinstance(cname, dict):
            cname = cname.get("@value")
        creator_names.append(str(cname))
    
    # Extract keyword values
    keyword_list = []
    for k in keywords:
        if isinstance(k, dict):
            keyword_list.append(k.get("@value"))
        else:
            keyword_list.append(str(k))

    md = f"---\n"
    md += f"type: dataset/croissant\n"
    md += f"name: \"{name}\"\n"
    md += f"source_url: {url}\n"
    if creator_names:
        md += f"creators: [{', '.join([f'\"{c}\"' for c in creator_names])}]\n"
    md += f"date_created: {datetime.now().strftime('%Y-%m-%d')}\n"
    md += f"tags: [croissant, dataset, nlp]\n"
    md += f"---\n\n"
    
    md += f"# {name}\n\n"
    md += f"## 📝 Description\n{description}\n\n"
    
    if keyword_list:
        md += f"## 🏷️ Keywords\n"
        md += ", ".join([f"#{k.replace(' ', '_')}" for k in keyword_list if k]) + "\n\n"
    
    md += f"## 🔗 Resources\n"
    md += f"- [Source URL]({url})\n"
    dist = json_data.get("distribution", [])
    for d in dist:
        c_url = d.get("contentUrl", "")
        d_name = d.get("name", "Data file")
        md += f"- [{d_name}]({c_url})\n"
    
    md += f"\n---\n## 🛠️ Raw Metadata (JSON-LD)\n"
    md += f"```json\n{json.dumps(json_data, indent=2, ensure_ascii=False)}\n```\n"
    
    return md

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 to_obsidian.py <CROISSANT_JSONLD_PATH> [OUTPUT_DIR]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/obsidian"
    
    if not os.path.exists(json_path):
        print(f"Error: File {json_path} not found.")
        sys.exit(1)

    with open(json_path, 'r') as f:
        json_data = json.load(f)

    md_content = format_as_markdown(json_data)
    
    name = json_data.get("name", "dataset")
    if isinstance(name, dict):
        name = name.get("@value", "dataset")
    
    safe_name = "".join([c if c.isalnum() else "_" for c in name])
    output_path = os.path.join(output_dir, f"{safe_name}.md")
    
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(md_content)

    print(f"\n[Obsidian Expert] Note created: {output_path}")
    
    # If OBSIDIAN_VAULT_PATH is set, also copy it there
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if vault_path and os.path.isdir(vault_path):
        vault_note_path = os.path.join(vault_path, f"{safe_name}.md")
        with open(vault_note_path, 'w') as f:
            f.write(md_content)
        print(f"[Obsidian Expert] Copied to vault: {vault_note_path}")
        
    # Try to open in Obsidian using URI scheme if on macOS
    if sys.platform == "darwin":
        import urllib.parse
        abs_path = os.path.abspath(output_path)
        # If it was copied to a vault, open that one instead
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
        if vault_path and os.path.isdir(vault_path):
            abs_path = os.path.abspath(os.path.join(vault_path, f"{safe_name}.md"))
            
        encoded_path = urllib.parse.quote(abs_path)
        obsidian_uri = f"obsidian://open?path={encoded_path}"
        print(f"[Obsidian Expert] Attempting to open in Obsidian: {obsidian_uri}")
        os.system(f"open '{obsidian_uri}'")

if __name__ == "__main__":
    main()
