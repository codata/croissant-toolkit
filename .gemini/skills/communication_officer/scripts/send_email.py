import os
import sys
import smtplib
from email.message import EmailMessage

def send_email(recipient, subject, body, attachment_path=None):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print("\n[Communication Officer] Error: Email credentials not found.")
        print("Please configure your environment for slava@codata.org:")
        print("export SMTP_USER='slava@codata.org'")
        print("export SMTP_PASS='your-google-app-password'")
        return False

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"Email successfully sent to {recipient}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 send_email.py <RECIPIENT> <SUBJECT> <BODY> [ATTACHMENT_PATH]")
        sys.exit(1)

    recipient = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None

    send_email(recipient, subject, body, attachment)

if __name__ == "__main__":
    main()
