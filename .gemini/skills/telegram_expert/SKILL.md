---
name: telegram_expert
description: Send results and notifications to Telegram channels or users.
---

# 🤖 Telegram Expert Skill

The Telegram Expert skill allows the toolkit to send messages and generated files directly to Telegram chats or channels.

## Features
- **Instant Notifications**: Send status updates and summaries.
- **File Sharing**: Upload generated `.jsonld` files directly to Telegram.
- **Bot Integration**: Uses the standard Telegram Bot API.

## Environment Variables
To use this skill, you need a Telegram Bot token and a target Chat ID.

1.  **Bot Token**: Create a bot via [@BotFather](https://t.me/botfather) on Telegram.
2.  **Chat ID**: Get your chat ID (you can use @userinfobot or send a message to your bot and check `https://api.telegram.org/bot<TOKEN>/getUpdates`).

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
export TELEGRAM_CHAT_ID="your-chat-or-channel-id"
```

## Usage
### 1. Send Message
```bash
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py \
    "Croissant Dataset Generation Complete!"
```

### 2. Send with File
```bash
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py \
    "New dataset ready for review." \
    "./data/croissant/my_dataset.jsonld"
```

### 3. Override Chat ID
```bash
python3 .gemini/skills/telegram_expert/scripts/send_telegram.py \
    "Message for a different channel" \
    --chat_id "-100123456789"
```
