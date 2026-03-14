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
To use this skill with your Google account (**slava@codata.org**), you must set your credentials. 

> [!IMPORTANT]
> Google requires an **App Password** for SMTP. Regular passwords will not work.
> 1. Go to your [Google Account Security](https://myaccount.google.com/security).
> 2. Enable 2-Step Verification.
> 3. Search for "App Passwords" and generate one for "Mail".

```bash
export SMTP_USER="slava@codata.org"
export SMTP_PASS="your-16-character-app-password"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

You can also add these to your `~/.zshrc` or `~/.bash_profile` to make them permanent.

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
