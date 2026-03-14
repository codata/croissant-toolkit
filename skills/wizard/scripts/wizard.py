import os
import sys
import json
import subprocess
import re

def extract_video_id(url):
    """Extracts the YouTube video ID from a URL."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def run_skill(script_path, args):
    """Runs a skill script as a subprocess and returns output/exit code."""
    cmd = [sys.executable, script_path] + args
    str_cmd = [str(a) for a in cmd]
    print(f"\n[Wizard] Running: {' '.join(str_cmd)}")
    result = subprocess.run(str_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Wizard] Error running {script_path}: {result.stderr}")
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wizard.py <CONTENT_OR_URL> [DATASET_NAME] [RECIPIENT_EMAIL]")
        sys.exit(1)

    input_val = sys.argv[1]
    dataset_name = sys.argv[2] if len(sys.argv) > 2 else "Wizard Generated Dataset"
    recipient_email = sys.argv[3] if len(sys.argv) > 3 else None
    
    video_id = extract_video_id(input_val)
    content_text = ""
    source_file = None

    # Step 1: Data Acquisition
    if video_id:
        print(f"[Wizard] Detected YouTube Video ID: {video_id}")
        transcriber_script = "skills/transcriber/scripts/transcribe.py"
        run_skill(transcriber_script, [video_id])
        
        transcript_path = f"data/transcripts/{video_id}.txt"
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r') as f:
                content_text = f.read()
            source_file = transcript_path
        else:
            print("[Wizard] Failed to get transcript. Aborting.")
            sys.exit(1)
    elif os.path.isfile(input_val):
        print(f"[Wizard] Detected local file: {input_val}")
        with open(input_val, 'r') as f:
            content_text = f.read()
        source_file = input_val
    else:
        print("[Wizard] Treating input as raw text.")
        content_text = input_val

    # Step 2: Translation (if needed)
    translator_script = "skills/translator/scripts/translate.py"
    # We always run it through the translator to check language and get a clean English string
    print("[Wizard] Checking language and translating if required...")
    
    original_content_text = content_text # Store original for NLP
    
    # We pass the content_text directly to translate.py
    trans_result = run_skill(translator_script, [content_text])
    
    # Simple heuristic to extract the translation from the script's output
    # The translate.py script prints [English Translation]: followed by the text
    if "[English Translation]:" in trans_result.stdout:
        content_text = trans_result.stdout.split("[English Translation]:")[1].split("-" * 50)[0].strip()
        print("[Wizard] Translation/Refinement successful.")

    # Step 3: Croissant Generation (which now handles NLP internally)
    print(f"[Wizard] Generating Croissant metadata for: {dataset_name}")
    
    content_str = str(content_text)
    if len(content_str) > 1000:
        final_desc = content_str[:1000] + "..."
    else:
        final_desc = content_str

    # Create a temporary metadata file for the Croissant Expert
    temp_metadata = {
        "name": str(dataset_name),
        "description": final_desc,
        "url": str(input_val) if video_id else "https://example.com/dataset",
        # Pass both original and translated for multilingual NLP extraction
        "nlp_text": f"{original_content_text}\n\n{content_text}", 
        "distribution": []
    }
    
    distribution_list = []
    temp_metadata["distribution"] = distribution_list
    
    if source_file:
        distribution_list.append({
            "name": "source-content",
            "contentUrl": os.path.abspath(source_file),
            "encodingFormat": "text/plain"
        })

    temp_meta_path = "data/wizard/temp_metadata.json"
    with open(temp_meta_path, 'w') as f:
        json.dump(temp_metadata, f, indent=2)

    croissant_script = "skills/croissant_expert/scripts/serialize.py"
    output_filename = dataset_name.lower().replace(" ", "_") + ".jsonld"
    
    # Run the Croissant Expert with the --nlp flag to automatically fill creator/spatial/temporal
    run_skill(croissant_script, [temp_meta_path, output_filename, "--nlp"])

    print(f"\n[Wizard] Process Complete! Your Croissant file is ready in data/croissant/{output_filename}")

    # Step 4: Communication (Optional)
    if recipient_email:
        print(f"[Wizard] Sending result to {recipient_email}...")
        comm_script = "skills/communication_officer/scripts/send_email.py"
        full_output_path = os.path.abspath(f"data/croissant/{output_filename}")
        subject = f"Croissant Dataset: {dataset_name}"
        body = f"Hello,\n\nThe Croissant dataset '{dataset_name}' has been successfully generated and refined with NLP metadata.\n\nPlease find the JSON-LD file attached.\n\nBest regards,\nYour Croissant Wizard"
        
        run_skill(comm_script, [recipient_email, subject, body, full_output_path])

if __name__ == "__main__":
    main()
