# Bulk Email Sender Script

A Python CLI tool to send personalized bulk emails with optional PDF attachments in controlled batches.

## 🚀 Features

- **Personalized Greetings**: Automatically prepends `Hi <name>,` and replaces `{name}` placeholders.
- **Domain-Based Batching**: Groups recipients by email domain (school/company) and sends up to 5 emails per domain in each batch.
- **Rate Limiting**: Waits 60 seconds between batches for the same domain to prevent throttling.
- **PDF Attachments**: Optionally attach a PDF file to every email.
- **CSV Input**: Load recipients from a CSV file (`name,email`).
- **Text Template**: Load message body from a text file, supporting `{name}` placeholders.

## ⚙️ Requirements

- Python 3.7+
- Standard libraries only: `smtplib`, `csv`, `time`, `os`, `email`

## 📥 Installation

1. Clone or download this script into your project folder.
2. Ensure you have Python 3.7+ installed.

## 🛠️ Usage

1. Open a terminal and navigate to the folder containing the script:
   ```bash
   cd path/to/folder
   ```
2. Run the script:
   ```bash
   python bulk_email_sender.py
   ```
3. Follow the prompts:
   - **Sender Email**: your Gmail (or SMTP‑supported) address
   - **Sender Password**: your email password or app‑specific password
   - **Email Subject**: subject line for all emails
   - **CSV File Path**: path to CSV with `name,email` rows
   - **Message File Path**: path to a `.txt` file containing your email body; use `{name}` to insert each recipient’s name
   - **PDF Attachment Path** (optional): path to a PDF file to attach; press Enter to skip

4. The script will display send status and adhere to the 60s delay per batch.

## ⚠️ Security & Limitations

- **Credentials**: Entering plain text passwords is insecure. Use environment variables or a secrets manager in production.
- **SMTP**: Default is Gmail SMTP (`smtp.gmail.com:587`). Modify `smtp_server`/`smtp_port` in code for other providers.
- **Batching**: Fixed to 5 emails per domain per batch; adjust in code if needed.

## 📄 License

MIT © Your Name

