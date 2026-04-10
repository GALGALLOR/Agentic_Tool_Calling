#!/usr/bin/env python3
"""Send email using Gmail API with OAuth2 (installed app flow).

Usage:
  1. Create OAuth credentials in Google Cloud Console (OAuth client ID, Desktop app)
     and download the JSON to `credentials.json` in the project folder (or set
     `GOOGLE_CLIENT_SECRET` to the path).
  2. Run this script; it will open a browser to authorize and save tokens to `token.json`.

Example:
  python send_email_oauth.py --to galgalloroba.gr.gr.gr@gmail.com --subject "test" --body "I am testing you."
"""
import argparse
import base64
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service(client_secret_file: str, token_file: str, port: int = 5000):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            # run_local_server will use a redirect URI like http://localhost:{port}/
            creds = flow.run_local_server(port=port)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, body_text):
    message = EmailMessage()
    message.set_content(body_text)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


def send_message(service, user_id, message_body):
    message = service.users().messages().send(userId=user_id, body=message_body).execute()
    return message


def main():
    parser = argparse.ArgumentParser(description='Send email via Gmail API (OAuth2)')
    parser.add_argument('--to', '-t', required=True, help='Recipient email')
    parser.add_argument('--subject', '-s', default='test')
    parser.add_argument('--body', '-b', default='I am testing you.')
    parser.add_argument('--from', '-f', dest='from_addr', help='Sender email (optional)')
    parser.add_argument('--client-secret', default=os.environ.get('GOOGLE_CLIENT_SECRET', 'credentials.json'))
    parser.add_argument('--token', default=os.environ.get('GOOGLE_TOKEN_FILE', 'token.json'))
    parser.add_argument('--port', type=int, default=5000, help='Local port for OAuth redirect (must match Console redirect URI)')
    args = parser.parse_args()

    client_secret = args.client_secret
    token_file = args.token

    if not os.path.exists(client_secret):
        print(f'Client secret file not found: {client_secret}')
        print('Create OAuth credentials in Google Cloud Console and save the JSON as this path.')
        return

    service = get_gmail_service(client_secret, token_file, port=args.port)

    # If from_addr not provided, try to infer from credentials' email using 'me'
    sender = args.from_addr or 'me'
    message_body = create_message(sender, args.to, args.subject, args.body)
    result = send_message(service, 'me', message_body)
    print('Message sent. ID:', result.get('id'))


if __name__ == '__main__':
    main()
