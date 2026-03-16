import os
import sys
import json
import urllib.request
import urllib.parse
import mimetypes

def send_telegram_message(token, chat_id, text):
    """Sends a text message to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[Telegram Expert] Error sending message: {e}")
        return None

def send_telegram_document(token, chat_id, caption, file_path):
    """Sends a document to Telegram using multipart/form-data."""
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    
    if not os.path.exists(file_path):
        print(f"[Telegram Expert] File not found: {file_path}")
        return None

    boundary = '----TelegramBotBoundary'
    parts = []
    
    # Chat ID part
    parts.append(f'--{boundary}')
    parts.append(f'Content-Disposition: form-data; name="chat_id"')
    parts.append('')
    parts.append(str(chat_id))
    
    # Caption part
    parts.append(f'--{boundary}')
    parts.append(f'Content-Disposition: form-data; name="caption"')
    parts.append('')
    parts.append(caption)
    
    # Document part
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    parts.append(f'--{boundary}')
    parts.append(f'Content-Disposition: form-data; name="document"; filename="{filename}"')
    parts.append(f'Content-Type: {mime_type}')
    parts.append('')
    
    with open(file_path, 'rb') as f:
        file_content = f.read()

    body_parts = []
    for p in parts:
        if isinstance(p, str):
            body_parts.append(p.encode('utf-8'))
        else:
            body_parts.append(p)
            
    body = b'\r\n'.join(body_parts)
    body += b'\r\n' + file_content + b'\r\n--' + boundary.encode('utf-8') + b'--\r\n'

    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body))
    }
    
    try:
        req = urllib.request.Request(url, data=body, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[Telegram Expert] Error sending document: {e}")
        return None

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token:
        print("[Telegram Expert] Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: python3 send_telegram.py <MESSAGE> [FILE_PATH] [--chat_id ID]")
        sys.exit(1)

    message = sys.argv[1]
    file_path = None
    
    # Parse args
    args = sys.argv[2:]
    if "--chat_id" in args:
        idx = args.index("--chat_id")
        chat_id = args[idx + 1]
        args.pop(idx + 1)
        args.pop(idx)
    
    if args:
        file_path = args[0]

    if not chat_id:
        print("[Telegram Expert] Error: TELEGRAM_CHAT_ID environment variable not set and no --chat_id provided.")
        sys.exit(1)

    if file_path:
        print(f"[Telegram Expert] Sending message and file to {chat_id}...")
        result = send_telegram_document(token, chat_id, message, file_path)
    else:
        print(f"[Telegram Expert] Sending message to {chat_id}...")
        result = send_telegram_message(token, chat_id, message)

    if result and result.get("ok"):
        print("[Telegram Expert] Success!")
    else:
        print(f"[Telegram Expert] Failed: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
