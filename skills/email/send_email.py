"""
Send email via Microsoft Graph API using Newry's Azure app registration.
Uses client credentials (app-only) flow — no user sign-in required.

Usage:
    New email:
        python send_email.py --to user@example.com --subject "Subject" --body "Body text"

    Thread reply (preserves conversation threading):
        python send_email.py --reply-to-id <message-id> --body "Reply text"
"""

import argparse
import os
import sys
import requests

TENANT_ID = "5c2a4223-665c-4da1-82eb-8ebd1014f30e"
CLIENT_ID = "eca4ed2b-6cf9-4c31-8b42-918bac852905"
GRAPH     = "https://graph.microsoft.com/v1.0"


def get_token(secret: str) -> str:
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    resp = requests.post(url, data={
        "grant_type":    "client_credentials",
        "client_id":     CLIENT_ID,
        "client_secret": secret,
        "scope":         "https://graph.microsoft.com/.default",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]


def send_new(token: str, sender: str, to: str, subject: str, body: str) -> None:
    url = f"{GRAPH}/users/{sender}/sendMail"
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to}}],
        },
        "saveToSentItems": True,
    }
    resp = requests.post(url, json=payload, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()


def reply_to_thread(token: str, sender: str, message_id: str, body: str) -> None:
    # Graph's /reply endpoint handles In-Reply-To, References, and conversationId automatically.
    url = f"{GRAPH}/users/{sender}/messages/{message_id}/reply"
    payload = {"comment": body}
    resp = requests.post(url, json=payload, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description="Send email via Graph API")
    parser.add_argument("--to",          help="Recipient address (new email)")
    parser.add_argument("--subject",     help="Subject (new email)")
    parser.add_argument("--body",        required=True, help="Message body")
    parser.add_argument("--reply-to-id", help="Message ID to reply to (thread reply)")
    args = parser.parse_args()

    if args.reply_to_id and (args.to or args.subject):
        print("ERROR: use --reply-to-id alone, or --to + --subject for a new email", file=sys.stderr)
        sys.exit(1)
    if not args.reply_to_id and not (args.to and args.subject):
        print("ERROR: new email requires --to and --subject", file=sys.stderr)
        sys.exit(1)

    secret = os.environ.get("NEWRY_MAIL_SECRET")
    if not secret:
        print("ERROR: NEWRY_MAIL_SECRET environment variable not set", file=sys.stderr)
        sys.exit(1)

    sender = os.environ.get("NEWRY_MAIL_USER")
    if not sender:
        print("ERROR: NEWRY_MAIL_USER environment variable not set", file=sys.stderr)
        sys.exit(1)

    print("Getting token...")
    token = get_token(secret)
    print("Sending...")

    if args.reply_to_id:
        reply_to_thread(token, sender, args.reply_to_id, args.body)
        print("Thread reply sent.")
    else:
        send_new(token, sender, args.to, args.subject, args.body)
        print(f"Sent to {args.to}")


if __name__ == "__main__":
    main()
