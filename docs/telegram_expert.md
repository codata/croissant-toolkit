# Telegram Expert

The Telegram Expert skill allows the toolkit to send results and notifications to Telegram channels or private users via a Telegram Bot.

## Core functionality
- **Instant Alerts**: Sends markdown-formatted messages.
- **File Sharing**: Uploads `.jsonld` files or other documents to a chat.
- **Bot Integration**: Uses the Telegram Bot API for reliable delivery.

## Configuration

To use this skill, the following environment variables must be set:

| Variable | Description |
| :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | The secret token from [@BotFather](https://t.me/botfather) |
| `TELEGRAM_CHAT_ID` | The ID of the target channel or user |

## Usage

### 1. Send text message
```bash
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py "Task completed successfully!"
```

### 2. Send with attachment
```bash
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py "New metadata file generated" "./data/croissant/example.jsonld"
```
