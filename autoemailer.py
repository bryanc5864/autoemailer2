import smtplib
import csv
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_bulk_emails(sender_email, sender_password, subject, recipients, message_body,
                     smtp_server="smtp.gmail.com", smtp_port=587, pdf_attachment=None):
    """
    Sends a personalized email to each recipient in the recipients list.
    Recipients is expected to be a list of tuples: (name, email_address).

    The emails are grouped by school (determined by the email domain, i.e. the part after '@')
    and sent in batches of up to 5 emails per school. After sending a batch from a given school,
    the script waits 60 seconds before sending the next batch from that school.

    Each email will start with the greeting "Hi <name>," (followed by a blank line) then the rest
    of the message. Any occurrence of the placeholder {name} in the message_body is also replaced.

    pdf_attachment: If provided, should be a tuple (filename, data) where 'data' is the binary
    content of the PDF file. This PDF will be attached to each email.
    """
    if not recipients:
        print("No recipients provided.")
        return

    # Group recipients by school domain.
    groups = {}
    for name, email_address in recipients:
        if "@" in email_address:
            domain = email_address.split("@")[1].lower().strip()
        else:
            domain = ""
        groups.setdefault(domain, []).append((name, email_address))
    
    # Set up a secure SMTP connection.
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Process groups in a round-robin fashion until all groups are empty.
    while any(groups[domain] for domain in groups):
        for domain in list(groups.keys()):
            if groups[domain]:
                # Take up to 5 recipients for this school (domain)
                batch = groups[domain][:5]
                for name, email_address in batch:
                    # Create the greeting line.
                    greeting_line = f"Hi {name},\n\n"
                    # Replace the {name} placeholder in the message_body and prepend the greeting.
                    personalized_body = greeting_line + message_body.replace("{name}", name)
                    
                    # Create the email message.
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = email_address
                    msg["Subject"] = subject
                    # Attach the plain text message.
                    msg.attach(MIMEText(personalized_body, "plain"))
                    
                    # If a PDF attachment is provided, attach it.
                    if pdf_attachment is not None:
                        pdf_filename, pdf_data = pdf_attachment
                        attachment = MIMEApplication(pdf_data, _subtype="pdf")
                        attachment.add_header("Content-Disposition", "attachment", filename=pdf_filename)
                        msg.attach(attachment)
                    
                    try:
                        server.sendmail(sender_email, email_address, msg.as_string())
                        print(f"Email sent to {name} ({email_address}) from domain '{domain}'")
                    except Exception as e:
                        print(f"Error sending email to {email_address}: {e}")
                
                # Remove the sent recipients from this school's group.
                groups[domain] = groups[domain][len(batch):]
                print(f"Sent a batch of {len(batch)} emails for domain '{domain}'. Waiting 60 seconds before the next batch for this domain...")
                time.sleep(60)  # Wait 60 seconds before processing the next batch for this domain.

    server.quit()

if __name__ == "__main__":
    # Get sender details from user input.
    sender_email = input("Enter your sender email address: ").strip()
    sender_password = input("Enter your sender email password: ").strip()
    subject = input("Enter the email subject: ").strip()
    
    # Get CSV file path for recipients.
    csv_file_path = input("Enter the CSV file path (with recipients in the format: name, email): ").strip()

    # Read recipients from the CSV file.
    recipients = []
    try:
        with open(csv_file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    email = row[1].strip()
                    recipients.append((name, email))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

    # Get email message file path from user input.
    message_file_path = input("Enter the text file path containing the email message (use {name} as placeholder if needed): ").strip()
    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            message_body = f.read()
    except Exception as e:
        print(f"Error reading email message file: {e}")
        exit(1)
    
    # Prompt user for a PDF file attachment.
    pdf_file_path = input("Enter the PDF file path for attachment (or leave blank if none): ").strip()
    pdf_attachment = None
    if pdf_file_path:
        try:
            with open(pdf_file_path, "rb") as f:
                pdf_data = f.read()
            pdf_filename = os.path.basename(pdf_file_path)
            pdf_attachment = (pdf_filename, pdf_data)
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            exit(1)

    send_bulk_emails(
        sender_email=sender_email,
        sender_password=sender_password,
        subject=subject,
        recipients=recipients,
        message_body=message_body,
        pdf_attachment=pdf_attachment
    )
