# Email Skill

Send and reply to email from Claude Code using Newry's Microsoft Graph API integration.

## Prerequisites

Two environment variables must be set on the user's machine (one-time setup):
- `NEWRY_MAIL_SECRET` — the Azure app client secret (get from Sylvan securely)
- `NEWRY_MAIL_USER` — your Newry email address (e.g. `mszugye@newrycorp.com`)

## Python path

Resolve at runtime in PowerShell:
```powershell
$python = "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe"
```

## How to use

### Send a new email
```
python skills/email/send_email.py --to recipient@example.com --subject "Subject" --body "Body text"
```

### Reply to a thread (preserves conversation context)
```
python skills/email/send_email.py --reply-to-id <message-id> --body "Reply text"
```

The `message-id` comes from the Outlook MCP connector's `outlook_email_search` tool — it's the `id` field on any returned email.

## Workflow for replying

1. Use `outlook_email_search` to find the email (returns `id` and thread context)
2. Confirm reply text with the user
3. Call `send_email.py --reply-to-id <id> --body "..."`

## Important

- Always confirm the reply text with the user before sending — do not send without explicit approval
- The script saves sent emails to Sent Items automatically
- Thread replies maintain full conversation context in the recipient's mail client
