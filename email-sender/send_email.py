#!/usr/bin/env python3
import os
import ssl
import smtplib
import argparse
import logging
from email.message import EmailMessage
from dotenv import load_dotenv


def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename=os.path.join('logs', 'send.log'),
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')


def send_email(smtp_host, smtp_port, smtp_user, smtp_pass, sender, recipients, subject, body):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        port = int(smtp_port)
        if port in (587, 25):
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_host, port, timeout=30) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        else:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, port, context=context, timeout=30) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

        logging.info(f"Email sent to: {recipients}")
        print('Email sent successfully')
    except Exception as exc:
        logging.exception('Failed to send email')
        print('Failed to send email:', exc)
        raise


def main():
    parser = argparse.ArgumentParser(description='Send email via SMTP')
    parser.add_argument('--to', '-t', nargs='+', help='Recipient email(s)', required=False)
    parser.add_argument('--subject', '-s', default=os.environ.get('DEFAULT_SUBJECT', 'test'))
    parser.add_argument('--body', '-b', default=os.environ.get('DEFAULT_BODY', 'I am testing you.'))
    args = parser.parse_args()

    load_dotenv()
    setup_logging()

    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = os.environ.get('SMTP_PORT', '465')
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    sender = os.environ.get('SENDER_EMAIL') or smtp_user

    if not smtp_user or not smtp_pass:
        print('SMTP_USER and SMTP_PASS must be set in .env')
        return

    recipients = args.to or [os.environ.get('DEFAULT_RECIPIENT', 'galgalloroba.gr.gr.gr@gmail.com')]

    send_email(smtp_host, smtp_port, smtp_user, smtp_pass, sender, recipients, args.subject, args.body)


if __name__ == '__main__':
    main()
