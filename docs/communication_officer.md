# Communication Officer

The Communication Officer skill handles the delivery of generated Croissant metadata and project summaries via email.

## Core functionality
- **SMTP Integration**: Securely sends emails using TLS/SSL.
- **Attachments**: Automatically attaches generated files to the outgoing email.
- **Reporting**: Provides a standardized way to share results with stakeholders.

## Configuration

To use this skill (specifically via Gmail), you must use an **App Password**.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SMTP_USER` | Your email address (e.g., slava@codata.org) | - |
| `SMTP_PASS` | Your 16-character App Password | - |
| `SMTP_SERVER` | SMTP host address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |

## Usage

### 1. Send result with attachment
```bash
python3 .gemini/skills/communication_officer/scripts/send_email.py \
    "stakeholder@example.com" \
    "New Croissant Dataset" \
    "The generation is complete." \
    "./data/croissant/my_dataset.jsonld"
```
