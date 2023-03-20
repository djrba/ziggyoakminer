#
# simple LLM tool for email listener that reads inbox, parse body of email and reply with ChatGPT Output.
# (c) OakMiner RBA 2023
#
# OpenAI API Key: OPENAI_API_KEY
# Run on terminal setx OPENAI_API_KEY <your key>

from email.mime.text import MIMEText
import imaplib
import email
import os
import smtplib
import openai
import time
from email.header import decode_header

email = "your email"
password ="your password"

def process_email(sender, subject, body):
    # Get API Key from environment variable or from file
        # Process the email content here
    openai.api_key = os.getenv("OPENAI_API_KEY")
    llm = LLM()
    out = llm.generate(body)
    send_email(sender,subject,out)
    # e.g., send the body to ChatGPT API, store results in the database, and send the response
    pass
# interval -  every 90 seconds
def email_listener(email_address, password, check_interval=90):
    while True:
        try:
            # Connect to the IMAP server and log in
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, password)

            # Select the mailbox you want to check
            mail.select("inbox")

            # Search for all emails marked as unseen
            _, message_numbers = mail.search(None, "UNSEEN")
            message_numbers = message_numbers[0].split()

            for num in message_numbers:
                # Fetch the email data
                _, msg_data = mail.fetch(num, "(RFC822)")

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Decode and process the email sender, subject, and body
                        sender = decode_header(msg["From"])[0][0]
                        subject = decode_header(msg["Subject"])[0][0]
                        body = ""

                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                        else:
                            body = msg.get_payload(decode=True).decode()

                        process_email(sender, subject, body)

                        # Mark the email as seen
                        mail.store(num, "+FLAGS", "\\Seen")

            # Log out and close the IMAP connection
            mail.logout()

        except Exception as e:
            print(f"Error: {e}")

        # Wait for the specified interval before checking for new emails again
        time.sleep(check_interval)

class LLM:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.0):
        self.model = model
        self.temperature = temperature
        
    def generate(self, text):
        c = openai.ChatCompletion.create(
          model=self.model,
          messages = [
            {"role": "user", "content": text},
        ],
        )
        return c.choices[0].message.content
   
   
def send_email(to, subject, body):
    from_email = email
    from_password = password

    # Create a MIMEText object with the email body
    msg = MIMEText(body)
    msg["Subject"] = "Ziggy Answer to your subject message "+subject
    msg["From"] = email
    msg["To"] = to

    # Connect to the SMTP server, log in, and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, from_password)
        server.send_message(msg) 
# Run the email listener       
# Start the email listener with your email credentials
email_listener(email, password)
