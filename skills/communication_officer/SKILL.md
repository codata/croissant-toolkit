---
name: communication_officer
description: Send results and data files to stakeholders via email.
---

# 📨 Communication Officer Skill

The Communication Officer skill automates the delivery of generated Croissant files and summaries to selected recipients.

## Features
- **Secure Delivery**: Uses SMTP with TLS for secure email transmission.
- **Attachments**: Supports sending generated `.jsonld` files as attachments.
- **Flexible Configuration**: Configurable via environment variables.

## Environment Variables
To use this skill, you must configure your SMTP settings:
```bash
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"
export SMTP_SERVER="smtp.gmail.com" # Default
export SMTP_PORT="587"              # Default
```

## Usage
### 1. Send reaching text
```bash
python3 skills/communication_officer/scripts/send_email.py \
    "stakeholder@example.com" \
    "Croissant Dataset Ready" \
    "The translation and metadata extraction are complete."
```

### 2. Send with Attachment (Recommended)
```bash
python3 skills/communication_officer/scripts/send_email.py \
    "stakeholder@example.com" \
    "Project Update" \
    "Please find the latest Croissant JSON-LD file attached." \
    "./data/croissant/my_dataset.jsonld"
```
